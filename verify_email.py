#!/usr/bin/env python3
"""
Email Address Verification Tool
Verifies emails BEFORE sending by checking:
1. DNS MX records (domain accepts email)
2. SMTP RCPT TO verification (mailbox exists)
3. Known bounce blacklist (don't retry dead addresses)

Usage:
  python verify_email.py email@domain.com
  python verify_email.py --batch emails.txt
  python verify_email.py --check file_with_emails.txt
"""

import smtplib
import socket
import subprocess
import json
import sys
import os
import re
import time

# === CONFIG ===
BLACKLIST_FILE = os.path.join(os.path.dirname(__file__), 'email_blacklist.json')
RESULTS_FILE = os.path.join(os.path.dirname(__file__), 'email_verify_results.json')

# === LOAD BLACKLIST ===
def load_blacklist():
    if os.path.exists(BLACKLIST_FILE):
        with open(BLACKLIST_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_blacklist(bl):
    with open(BLACKLIST_FILE, 'w') as f:
        json.dump(bl, f, indent=2)

def load_results():
    if os.path.exists(RESULTS_FILE):
        with open(RESULTS_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_results(r):
    with open(RESULTS_FILE, 'w') as f:
        json.dump(r, f, indent=2)

# === MX LOOKUP ===
def get_mx_records(domain):
    """Get MX records using nslookup. Returns list of (priority, hostname)."""
    try:
        result = subprocess.run(
            ['nslookup', '-type=MX', domain],
            capture_output=True, text=True, timeout=10
        )
        records = []
        for line in result.stdout.split('\n'):
            if 'mail exchanger' in line.lower():
                # Format 1: "domain MX preference = 10, mail exchanger = mail.example.com" (Windows)
                # Format 2: "domain MX preference = 10 mail.example.com" (Linux)
                match = re.search(r'mail exchanger\s*=\s*(.+)', line, re.IGNORECASE)
                if match:
                    host = match.group(1).strip().rstrip('.')
                    records.append((0, host))
                else:
                    match = re.search(r'=\s*(\d+)\s+(.+)', line)
                    if match:
                        priority = int(match.group(1))
                        host = match.group(2).split(',')[0].strip().rstrip('.')
                        records.append((priority, host))
        records.sort()  # by priority
        return [r[1] for r in records]
    except Exception as e:
        print(f'MX lookup error for {domain}: {e}', file=sys.stderr)
        return []

# === SMTP VERIFICATION ===
def verify_smtp(email, mx_host, from_email='verify@nichenexusglobal.com', timeout=15):
    """
    Connect to MX server and verify email via RCPT TO.
    Returns: 'valid', 'invalid', 'catchall', or 'error:msg'
    
    IMPORTANT: Gmail/Google Workspace returns 250 for ALL addresses (catch-all).
    Microsoft 365/Outlook will return 550 for non-existent users.
    Many providers will block verification attempts.
    """
    try:
        server = smtplib.SMTP(mx_host, 25, timeout=timeout)
        server.ehlo('nichenexusglobal.com')
        
        # Some servers require STARTTLS
        if server.has_extn('STARTTLS'):
            try:
                server.starttls()
                server.ehlo('nichenexusglobal.com')
            except:
                server.quit()
                return 'error:tls_failed'
        
        # MAIL FROM
        code, msg = server.mail(from_email)
        if code != 250:
            server.quit()
            return f'error:mail_from_{code}'
        
        # RCPT TO - this is the key check
        code, msg = server.rcpt(email)
        server.quit()
        
        if code == 250:
            # Google Workspace returns 250 for everything (catch-all)
            # Check if this is a Google MX
            if 'google' in mx_host.lower() or 'googlemail' in mx_host.lower():
                return 'catchall_google'
            return 'valid'
        elif code == 550:
            return 'invalid'
        elif code == 551:
            return 'invalid'
        elif code == 552:
            return 'error:mailbox_full'
        elif code == 553:
            return 'invalid'
        else:
            return f'error:smtp_{code}'
            
    except smtplib.SMTPConnectError:
        return 'error:connect'
    except smtplib.SMTPServerDisconnected:
        return 'error:disconnected'
    except socket.timeout:
        return 'error:timeout'
    except Exception as e:
        return f'error:{str(e)[:80]}'

# === MAIN VERIFY FUNCTION ===
def verify_email(email):
    """Full verification pipeline. Returns (status, details)."""
    
    # 0. Basic syntax check
    if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
        return 'invalid_syntax', 'Email format is invalid'
    
    # 1. Check blacklist
    bl = load_blacklist()
    if email.lower() in bl:
        reason = bl[email.lower()]
        return 'blacklisted', f'Known dead: {reason}'
    
    # 2. Check cached results (< 7 days old)
    results = load_results()
    if email.lower() in results:
        cached = results[email.lower()]
        age = time.time() - cached.get('ts', 0)
        if age < 604800:  # 7 days
            return cached['status'], f'Cached: {cached.get("detail","")}'
    
    # 3. Extract domain and check MX
    domain = email.split('@')[1]
    mx_hosts = get_mx_records(domain)
    
    if not mx_hosts:
        return 'invalid_domain', f'No MX records for {domain}'
    
    # 4. SMTP verification (try first 2 MX servers)
    for mx in mx_hosts[:2]:
        status = verify_smtp(email, mx)
        
        # Cache result
        results[email.lower()] = {
            'status': status, 
            'detail': f'MX={mx}',
            'ts': time.time()
        }
        save_results(results)
        
        if status in ('valid', 'invalid', 'catchall_google'):
            return status, f'MX={mx} -> {status}'
        
        if not status.startswith('error:'):
            return status, f'MX={mx} -> {status}'
    
    return 'undetermined', f'Tried {len(mx_hosts)} MX, all failed or blocked'

# === BATCH VERIFICATION ===
def verify_batch(emails, delay=2):
    """Verify a list of emails with delay between each."""
    results = {}
    for i, email in enumerate(emails):
        email = email.strip()
        if not email:
            continue
        status, detail = verify_email(email)
        results[email] = {'status': status, 'detail': detail}
        print(f'[{i+1}/{len(emails)}] {status:20s} | {email:50s} | {detail}')
        if delay and i < len(emails) - 1:
            time.sleep(delay)
    return results

# === IMPORT KNOWN BOUNCES INTO BLACKLIST ===
def import_bounces(bounce_file):
    """Import bounce data into blacklist."""
    bl = load_blacklist()
    count = 0
    with open(bounce_file, 'r') as f:
        for line in f:
            line = line.strip()
            if '@' in line:
                parts = line.split('|')
                email = parts[0].strip()
                reason = parts[1].strip() if len(parts) > 1 else 'bounced'
                if email.lower() not in bl:
                    bl[email.lower()] = reason
                    count += 1
    save_blacklist(bl)
    print(f'Imported {count} new addresses into blacklist (total: {len(bl)})')

# === CLI ===
if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    
    cmd = sys.argv[1]
    
    if cmd == '--batch':
        # Read emails from file
        if len(sys.argv) < 3:
            print('Usage: python verify_email.py --batch emails.txt')
            sys.exit(1)
        with open(sys.argv[2], 'r') as f:
            emails = [line.strip() for line in f if line.strip() and '@' in line]
        print(f'Verifying {len(emails)} emails...')
        verify_batch(emails)
    
    elif cmd == '--import-bounces':
        if len(sys.argv) < 3:
            print('Usage: python verify_email.py --import-bounces bounces.txt')
            sys.exit(1)
        import_bounces(sys.argv[2])
    
    elif cmd == '--blacklist':
        bl = load_blacklist()
        for email, reason in sorted(bl.items()):
            print(f'{email:50s} | {reason}')
        print(f'\nTotal: {len(bl)}')
    
    elif cmd == '--check':
        # Check a file, output only valid/invalid lists
        if len(sys.argv) < 3:
            print('Usage: python verify_email.py --check file.txt')
            sys.exit(1)
        with open(sys.argv[2], 'r') as f:
            emails = [line.strip() for line in f if line.strip() and '@' in line]
        
        valid = []
        invalid = []
        undetermined = []
        
        for email in emails:
            status, detail = verify_email(email)
            if status == 'valid':
                valid.append(email)
            elif status in ('invalid', 'invalid_syntax', 'invalid_domain', 'blacklisted'):
                invalid.append((email, detail))
            else:
                undetermined.append((email, status, detail))
        
        print(f'\n=== VALID ({len(valid)}) ===')
        for e in valid:
            print(e)
        
        print(f'\n=== INVALID ({len(invalid)}) ===')
        for e, d in invalid:
            print(f'{e} — {d}')
        
        print(f'\n=== UNDETERMINED ({len(undetermined)}) ===')
        for e, s, d in undetermined:
            print(f'{e} — [{s}] {d}')
    
    else:
        # Single email verification
        email = cmd
        status, detail = verify_email(email)
        print(f'{status}: {detail}')
