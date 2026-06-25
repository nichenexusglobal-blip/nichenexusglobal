"""Extract every rule I can find from memories"""
import json, re

# Read current rules from behavior_policy
print("=== EXISTING BEHAVIOR POLICY ===")
with open("C:/nichenexusglobal/behavior_policy.py") as f:
    print(f.read())

print("\n=== MEMORY.md RULES ===")
with open("C:/Users/leon/AppData/Local/hermes/profiles/nichenexusglobal/MEMORY.md") as f:
    content = f.read()
    # Extract bullets/numbers/lists
    for line in content.split("\n"):
        line = line.strip()
        if line.startswith("-") or line.startswith("*") or line.startswith("§") or re.match(r"^\d", line):
            print(line)

print("\n=== USER.md RULES ===")
with open("C:/Users/leon/AppData/Local/hermes/profiles/nichenexusglobal/USER.md") as f:
    content = f.read()
    for line in content.split("\n"):
        line = line.strip()
        if line.startswith("-") or line.startswith("*") or line.startswith("§"):
            print(line)
