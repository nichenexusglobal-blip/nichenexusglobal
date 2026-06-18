"""
纯 socket 验证邮箱方式，不依赖 nslookup/dnspython
直接通过系统 DNS 解析 + SMTP RCPT
"""
import socket, time

emails = [
    "rachel@lovebonito.com",
    "david@pomelofashion.com",
    "john.marco@sociolla.com",
    "danny@hipvan.com",
    "johannes@castlery.com",
]

fallbacks = {
    "lovebonito.com": ["press@lovebonito.com", "hello@lovebonito.com"],
    "pomelofashion.com": ["press@pomelofashion.com", "hello@pomelofashion.com"],
    "sociolla.com": ["partnership@sociolla.com", "info@sociolla.com"],
    "hipvan.com": ["partnerships@hipvan.com", "hello@hipvan.com"],
    "castlery.com": ["partners@castlery.com", "hello@castlery.com"],
}

def resolve_mx(domain):
    """通过系统 DNS 获取 MX 记录"""
    try:
        result = socket.getaddrinfo(domain, 25, socket.AF_INET, socket.SOCK_STREAM)
        # 这只是A记录，不是MX。但我们可以直接连接域名。
        addrs = list(set(r[4][0] for r in result))
        return addrs[:3]
    except:
        return []

def get_mx_via_text(domain):
    """尝试直接获取域名的邮件交换信息"""
    try:
        # 有些域名直接接受SMTP
        addrs = socket.getaddrinfo(f"aspmx.l.google.com", 25, socket.AF_INET, socket.SOCK_STREAM)
        if addrs:
            return [addrs[0][4][0]]
    except:
        pass
    return []

def smtp_verify(email_addr, mx_ip, port=25, timeout=10):
    """SMTP RCPT 验证"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        sock.connect((mx_ip, port))
        sock.settimeout(5)
        
        # 读 banner
        time.sleep(0.5)
        banner = b""
        try:
            while True:
                d = sock.recv(4096)
                if not d:
                    break
                banner += d
                if b"\n" in d:
                    break
        except socket.timeout:
            pass
        
        def cmd(c):
            sock.sendall((c + "\r\n").encode())
            time.sleep(0.3)
            resp = b""
            try:
                while True:
                    d = sock.recv(4096)
                    if not d:
                        break
                    resp += d
                    if b"\n" in d or len(resp) > 512:
                        break
            except socket.timeout:
                pass
            return resp.decode('utf-8', errors='replace').strip()
        
        cmd("EHLO nichenexusglobal.com")
        cmd(f"MAIL FROM:<verify@{email_addr.split('@')[1]}>")
        rcpt_resp = cmd(f"RCPT TO:<{email_addr}>")
        cmd("QUIT")
        sock.close()
        
        code = int(rcpt_resp[:3]) if rcpt_resp[:3].isdigit() else 0
        
        if code == 250:
            return ("EXISTS", rcpt_resp[:80])
        elif code == 550:
            return ("INVALID", rcpt_resp[:80])
        else:
            return ("UNKNOWN", f"Code {code}: {rcpt_resp[:80]}")
    
    except socket.timeout:
        return ("TIMEOUT", "Connection timed out")
    except ConnectionRefusedError:
        return ("REFUSED", "Connection refused")
    except socket.gaierror:
        return ("DNS_FAIL", "Cannot resolve hostname")
    except Exception as e:
        return ("ERROR", str(e)[:80])

print("=" * 60)
print("EMAIL VERIFICATION REPORT")
print("Method: Direct SMTP RCPT on port 25")
print("=" * 60)

for email in emails:
    domain = email.split('@')[1]
    
    # 先尝试解析MX域名
    mx_hosts = []
    for name in [f"aspmx.l.google.com", f"alt1.aspmx.l.google.com", f"alt2.aspmx.l.google.com"]:
        try:
            addrs = socket.getaddrinfo(name, 25, socket.AF_INET, socket.SOCK_STREAM)
            for a in addrs:
                mx_hosts.append(a[4][0])
        except:
            pass
        if mx_hosts:
            break
    
    if not mx_hosts:
        print(f"\n❌ {email} - Cannot resolve any mail server")
        continue
    
    # 先用Gmail验证（lovebonito/pomelo/sociolla/hipvan用Google Workspace）
    result, detail = smtp_verify(email, mx_hosts[0])
    
    if result == "EXISTS":
        print(f"\n✅ {email}")
    elif result == "INVALID":  
        print(f"\n❌ {email}")
    else:
        print(f"\n⚠️  {email}")
    
    print(f"   Mail server: {mx_hosts[0]}")
    print(f"   SMTP Result: {detail}")
    
    # Google Workspace 通常会返回250即使是假地址
    # 但如果是550就是明确不存在的地址
    # 如果超时，再试一个备用的
    if result == "TIMEOUT" and len(mx_hosts) > 1:
        result2, detail2 = smtp_verify(email, mx_hosts[1])
        print(f"   Retry on {mx_hosts[1]}: {result2} - {detail2}")
    
    # 如果主邮箱有问题，检查备用邮箱
    if result in ("INVALID", "UNKNOWN", "TIMEOUT", "REFUSED"):
        fbs = fallbacks.get(domain, [])
        if fbs:
            print(f"   --- Fallbacks ---")
            for fb in fbs:
                fr, fd = smtp_verify(fb, mx_hosts[0])
                fm = "✅" if fr == "EXISTS" else "❌" if fr == "INVALID" else "⚠️"
                print(f"   {fm} {fb}")
                print(f"      {fd}")

print("\n" + "=" * 60)
print("IMPORTANT: Google Workspace returns 250 for ALL @domain")
print("addresses by design, even non-existent ones. A 250 result")
print("does NOT guarantee the address is real.")
print("Outlook (castlery.com) also returns ambiguous results.")
print("=" * 60)
