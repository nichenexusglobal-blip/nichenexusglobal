#!/bin/bash
# Brake pad distributor domain guessing - 5 markets
# Markets: UAE, South Africa, Kenya, Mexico, Philippines

total=0
alive=0
emails_found=0
tmpfile="/c/Users/Administrator/nichenexusglobal/.nail_tmp.html"

echo "=== BRAKE PAD NAIL SCAN - DOMAIN GUESSING ==="
echo ""

scan_domain() {
  local domain="$1"
  local desc="$2"
  total=$((total + 1))
  
  http_code=$(curl -sL --connect-timeout 4 --max-time 8 \
    -o "$tmpfile" \
    -w "%{http_code}" \
    -H "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36" \
    "https://www.$domain" 2>/dev/null)
  
  if [ "$http_code" = "200" ] || [ "$http_code" = "301" ] || [ "$http_code" = "302" ]; then
    alive=$((alive + 1))
    emails=$(grep -oiP '[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}' "$tmpfile" 2>/dev/null | \
      grep -vi '@2x\|@3x\|\.png\|\.jpg\|\.webp\|\.svg\|\.js\|\.css\|@example\|@domain\|noreply\|donotreply' | \
      sort -u)
    
    if [ -n "$emails" ]; then
      emails_found=$((emails_found + 1))
      echo "✓ ALIVE: $domain [$http_code] - $desc"
      echo "  EMAILS: $emails"
    else
      contact_emails=$(curl -sL --connect-timeout 4 --max-time 8 \
        -H "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36" \
        "https://www.$domain/contact" 2>/dev/null | \
        grep -oiP '[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}' | \
        grep -vi '@2x\|@3x\|\.png\|\.jpg\|\.webp\|\.svg\|@example\|@domain\|noreply' | \
        sort -u)
      
      if [ -n "$contact_emails" ]; then
        emails_found=$((emails_found + 1))
        echo "✓ ALIVE: $domain [$http_code] - $desc"
        echo "  EMAILS (/contact): $contact_emails"
      else
        echo "⚠ ALIVE: $domain [$http_code] - $desc (no public email)"
      fi
    fi
  else
    echo "✗ DEAD:  $domain [$http_code] - $desc"
  fi
  rm -f "$tmpfile"
}

# UAE
scan_domain "partsouq.com" "Partsouq UAE"
scan_domain "autopro.ae" "Autopro UAE"
scan_domain "dubaiautoparts.com" "Dubai Auto Parts"

# South Africa
scan_domain "autozone.co.za" "AutoZone SA"
scan_domain "midas.co.za" "Midas SA"
scan_domain "masterparts.com" "Masterparts SA"
scan_domain "alertengineparts.com" "Alert Engine Parts SA"
scan_domain "goldwagen.com" "Goldwagen SA"

# Kenya
scan_domain "toyotakenya.com" "Toyota Kenya"
scan_domain "autoparts.co.ke" "Auto Parts Kenya"

# Mexico
scan_domain "autozone.com.mx" "AutoZone Mexico"
scan_domain "sumitec.com.mx" "Sumitec Mexico"

# Philippines
scan_domain "autosupply.com.ph" "Auto Supply PH"

echo ""
echo "=== SUMMARY ==="
echo "Total: $total | Alive: $alive | With email: $emails_found"
