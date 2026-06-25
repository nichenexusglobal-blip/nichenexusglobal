#!/usr/bin/env python3
"""Debug: check what pwd_loader returns and what's in .env"""
import os, sys
sys.path.insert(0, '/c/nichenexusglobal')

# Check .env content raw bytes
with open('.env', 'rb') as f:
    raw = f.read()
print(f".env raw ({len(raw)} bytes): {raw[:80]}")

# Check what get_pwd returns
from pwd_loader import get_pwd
pwd = get_pwd()
print(f"get_pwd() returns: len={len(pwd)}, first char={pwd[:1] if pwd else 'EMPTY'}")
