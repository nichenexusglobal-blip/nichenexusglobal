#!/usr/bin/env python3
"""Git: add all changes and push"""
import subprocess
r = subprocess.run(["git","add","-A"], cwd="C:/nichenexusglobal", capture_output=True)
r = subprocess.run(["git","commit","-m","clean: removed old temp files + bullets update"], cwd="C:/nichenexusglobal", capture_output=True)
r = subprocess.run(["git","push","origin","main"], cwd="C:/nichenexusglobal", capture_output=True, text=True, timeout=30)
print(f"{r.stdout[:200]}\n{r.stderr[:100]}")
