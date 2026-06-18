#!/usr/bin/env python3
"""Send Mascom Kenya reply via WhatsApp with Pecron F1000LFP specs"""
import subprocess, json

# Pecron F1000LFP spec sheet text
specs = """Here is the F1000LFP spec for you to compare - 
960Wh LiFePO4 (3500 cycles), 1500W pure sine wave
UK socket, CE/FCC, app control
AC charge 0-80% in 50min, solar input 600W
Weight 10.85kg
FOB Shenzhen USD 202.5
Landed Mombasa roughly KSH 42,000 all in (freight, duty, VAT included)

vs your EcoFlow DELTA 2 at KSH 64,000 - same capacity range, way cheaper.
vs your RIVER 3 at KSH 33,000 - 4x the capacity for just KSH 9,000 more.

Questions on specs? Happy to share the full datasheet."""

payload = json.dumps({
    "chatId": "254708852521@s.whatsapp.net",
    "message": specs
})

result = subprocess.run(
    ['curl', '-s', '--max-time', '10', '-X', 'POST',
     'http://127.0.0.1:3000/send',
     '-H', 'Content-Type: application/json',
     '--data-binary', payload],
    capture_output=True, text=True)

print(f"Exit: {result.returncode}")
print(f"Output: {result.stdout}")
if result.stderr:
    print(f"Error: {result.stderr[:200]}")
