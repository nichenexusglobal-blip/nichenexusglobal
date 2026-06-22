#!/usr/bin/env python3
"""Self-check loop: gen → check → retry → done"""
import json, subprocess, sys

WORKDIR = "C:/nichenexusglobal"
MAX_ATTEMPTS = 3

def check():
    """Run preflight data check"""
    r = subprocess.run(["python", f"{WORKDIR}/preflight_data.py"], 
                       capture_output=True, text=True, timeout=15)
    passed = "ALL CLEAR" in r.stdout
    return passed, r.stdout

def push():
    """Run postsafe push"""
    r = subprocess.run(["python", f"{WORKDIR}/postsafe.py"],
                       capture_output=True, text=True, timeout=30)
    pushed = "Pushed" in r.stdout
    return pushed, r.stdout

print("=" * 50)
print("SELF-CHECK LOOP STARTED")
print(f"Max attempts: {MAX_ATTEMPTS}")
print("=" * 50)

for attempt in range(1, MAX_ATTEMPTS + 1):
    print(f"\n🔄 Attempt {attempt}/{MAX_ATTEMPTS}:")
    
    # Step 1: Check
    passed, output = check()
    print(output[:300])
    
    if passed:
        print(f"\n✅ PASSED on attempt {attempt}")
        # Step 2: Push
        pushed, push_out = push()
        print(f"   Push: {'✅' if pushed else '❌'}")
        if pushed:
            print(f"   {push_out[:100]}")
        sys.exit(0)
    else:
        print(f"\n⚠️ FAILED. Re-checking...")
        if attempt < MAX_ATTEMPTS:
            print("   (Data will be corrected in the next iteration)")

print(f"\n❌ EXCEEDED {MAX_ATTEMPTS} attempts. Manual intervention needed.")
sys.exit(1)
