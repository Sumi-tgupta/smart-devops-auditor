import re
import os
from functools import cached_property
from typing import List, Optional, Any

from google.adk.models import Gemini
from google.genai import Client, types

def strip_json_fences(text: str) -> str:
    """
    Strips markdown code fences (like ```json ... ```) from a text response.
    Returns the raw cleaned text (e.g. JSON string).
    """
    text = text.strip()
    # Strip opening block: ```json or ```
    text = re.sub(r"^```(?:json)?\s*", "", text, flags=re.IGNORECASE)
    # Strip closing block: ```
    text = re.sub(r"\s*```$", "", text)
    return text.strip()

class KeyedGemini(Gemini):
    """
    A custom Gemini model implementation that binds an explicit API key
    to the underlying genai Client. Bypasses os.environ dependency.
    """
    def __init__(self, api_key: str, **kwargs):
        super().__init__(**kwargs)
        self._api_key = api_key

    @cached_property
    def api_client(self) -> Client:
        base_url, api_version = self._base_url_and_api_version
        kwargs_for_http_options = {
            'headers': self._tracking_headers(),
            'retry_options': self.retry_options,
            'base_url': base_url,
        }
        if api_version:
            kwargs_for_http_options['api_version'] = api_version

        kwargs = {
            'http_options': types.HttpOptions(**kwargs_for_http_options),
            'api_key': self._api_key,
        }
        if self.model.startswith('projects/'):
            kwargs['enterprise'] = True

        return Client(**kwargs)

def get_all_keys() -> List[str]:
    """Retrieves all defined Gemini API keys from the environment."""
    keys = []
    # Primary key
    p_key = os.getenv("GEMINI_API_KEY")
    if p_key:
        keys.append(p_key)
    # Additional keys
    for k in ["GEMINI_API_KEY_TWO", "GEMINI_API_KEY_THREE"]:
        val = os.getenv(k)
        if val and val not in keys:
            keys.append(val)
    if not keys:
        keys.append("")
    return keys

