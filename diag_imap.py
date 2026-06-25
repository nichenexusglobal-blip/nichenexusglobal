"""Diagnose IMAP — try all possible connection methods"""
import imaplib, socket, ssl

pwd = None
with open("C:/Users/leon/AppData/Local/hermes/profiles/nichenexusglobal/.env") as f:
    for line in f:
        if "EMAIL_PASSWORD" in line:
            pwd = line.split("=", 1)[1].strip()
            break

if not pwd:
    print("❌ No password found")
    exit(1)

# Method 1: standard SSL 993
print("1️⃣ imap.exmail.qq.com:993 SSL...")
try:
    mail = imaplib.IMAP4_SSL("imap.exmail.qq.com", 993, timeout=10)
    mail.login("pen@nichenexusglobal.com", pwd)
    print("  ✅ LOGIN OK")
    mail.logout()
except Exception as e:
    print(f"  ❌ {e}")

# Method 2: with STARTTLS on 143
print("\n2️⃣ imap.exmail.qq.com:143 STARTTLS...")
try:
    sock = socket.create_connection(("imap.exmail.qq.com", 143), timeout=10)
    mail = imaplib.IMAP4()
    mail.sock = sock
    mail.starttls()
    mail.login("pen@nichenexusglobal.com", pwd)
    print("  ✅ LOGIN OK")
    mail.logout()
except Exception as e:
    print(f"  ❌ {e}")

# Method 3: Try resolving IP first
print("\n3️⃣ DNS resolution...")
try:
    ips = socket.getaddrinfo("imap.exmail.qq.com", 993)
    for ip in ips[:3]:
        print(f"  IP: {ip[4][0]}")
except Exception as e:
    print(f"  ❌ {e}")

# Method 4: Try port 993 with SSL context (explicit)
print("\n4️⃣ imap.exmail.qq.com:993 with explicit SSL context...")
try:
    ctx = ssl.create_default_context()
    mail = imaplib.IMAP4_SSL("imap.exmail.qq.com", 993, timeout=10, ssl_context=ctx)
    mail.login("pen@nichenexusglobal.com", pwd)
    print("  ✅ LOGIN OK")
    mail.logout()
except Exception as e:
    print(f"  ❌ {e}")

print("\n=== Done ===")
