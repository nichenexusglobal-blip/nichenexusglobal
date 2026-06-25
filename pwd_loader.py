#!/usr/bin/env python3
"""Load NICHE_EMAIL_PASSWORD from .env file or base64 fallback."""
import base64, os

_ENCODED = "NGNkN3ZRNEdWNTlBVHh4dA=="

def get_pwd():
    pwd = os.environ.get("NICHE_EMAIL_PASSWORD", "")
    if pwd:
        return pwd
    
    # Try .env files
    for path in [
        os.path.expanduser("~/nichenexusglobal/.env"),
        "C:/nichenexusglobal/.env",
        "D:/nichenexusglobal/.env"
    ]:
        if os.path.exists(path):
            with open(path) as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    if line.startswith("NICHE_EMAIL_PASSWORD"):
                        parts = line.split("=", 1)
                        if len(parts) == 2:
                            val = parts[1].strip("'\"")
                            if len(val) > 3:
                                return val
    
    # Fallback to base64 decode
    return base64.b64decode(_ENCODED).decode()
