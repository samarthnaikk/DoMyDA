import re
from typing import Optional


def extract_base64(html: str) -> Optional[str]:
    """Try to find a base64 data block in the HTML and return the encoded string."""
    m = re.search(r"data:[^;]+;base64,([A-Za-z0-9+/=]+)", html)
    if m:
        return m.group(1)
    # fallback: look for long base64-like sequences
    m2 = re.search(r"([A-Za-z0-9+/=]{100,})", html)
    return m2.group(1) if m2 else None


def extract_submit_url(html: str) -> str:
    """Extract a submit URL from form action or JSON-like fields in HTML.

    Raises ValueError if not found.
    """
    m = re.search(r"action=[\"'](https?://[^\"']+)[\"']", html)
    if m:
        return m.group(1)
    m2 = re.search(r'"submit_url"\s*:\s*"(https?://[^"]+)"', html)
    if m2:
        return m2.group(1)
    raise ValueError("Submit URL not found on page")
