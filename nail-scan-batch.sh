#!/bin/bash
# Massive nail scan - domain guessing for brake pads + portable power
# 25+ domains across 8 markets

tmpf="/c/Users/Administrator/nichenexusglobal/.ns.html"
total=0 alive=0 found=0

check() {
  local domain="$1" desc="$2"
  total=$((total+1))
  
  local code
  code=$(curl -sL --connect-timeout 4 --max-time 8 \
    -o "$tmpf" -w "%{http_code}" \
    -H "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36" \
    "https://www.$domain" 2>/dev/null)
  
  if [ "$code" != "200" ] && [ "$code" != "301" ] && [ "$code" != "302" ]; then
    echo "✗ $domain [$code] $desc"
    return
  fi
  
  alive=$((alive+1))
  local emails
  emails=$(grep -oiP '[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}' "$tmpf" 2>/dev/null | \
    grep -vi '@2x\|@3x\|\.png\|\.jpg\|\.webp\|\.svg\|\.js\|\.css\|@example\|@domain\|noreply\|donotreply\|@w3\.org' | \
    sort -u | head -5)
  
  if [ -n "$emails" ]; then
    found=$((found+1))
    echo "✓ $domain [$code] $desc"
    echo "  → $emails"
  else
    # /contact
    local emails2
    emails2=$(curl -sL --connect-timeout 4 --max-time 8 \
      -H "User-Agent: Mozilla/5.0" \
      "https://www.$domain/contact" 2>/dev/null | \
      grep -oiP '[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}' | \
      grep -vi '@2x\|@3x\|\.png\|@example\|noreply\|donotreply\|@w3\.org' | \
      sort -u | head -5)
    
    if [ -n "$emails2" ]; then
      found=$((found+1))
      echo "✓ $domain [$code] $desc"
      echo "  /contact → $emails2"
    else
      echo "⚠ $domain [$code] alive, no email - $desc"
    fi
  fi
  rm -f "$tmpf"
}

echo "=== BATCH NAIL SCAN ==="
echo ""

echo "--- AUTO PARTS DISTRIBUTORS ---"
check "motus.co.za" "Motus - SA #1 automotive group"
check "boschcarservice.co.za" "Bosch Car Service SA"
check "autoworks.co.za" "AutoWorks SA"
check "samedayauto.co.za" "Same Day Auto SA"
check "autozone.co.za" "AutoZone SA (retail)"
check "alfuttaim.com" "Al-Futtaim UAE"
check "altayer-motors.com" "Al Tayer Motors UAE"
check "simbacolt.com" "Simba Colt Kenya"
check "cfao.com" "CFAO Group Africa"
check "autopartsnigeria.com" "Auto Parts Nigeria"
check "automedics.com.ng" "Automedics Nigeria"
check "kamsiparts.com" "Kamsi Parts Nigeria"

echo ""
echo "--- SOLAR / POWER STATION DISTRIBUTORS ---"
check "gennextechnologies.com" "Gennex Technologies Nigeria"
check "solarpowernigeria.com" "Solar Power Nigeria"
check "rubitecsolar.com" "Rubitec Solar Nigeria"
check "neosolar.com.br" "NeoSolar Brazil"
check "minhacasasolar.com.br" "Minha Casa Solar Brazil"
check "solarprime.com.br" "Solar Prime Brazil"
check "deserttechnologies.com" "Desert Technologies Saudi"
check "solarabic.com" "Solarabic Saudi"
check "loom-solar.com" "Loom Solar India"
check "solarmarts.com" "SolarMarts India"
check "solarclue.com" "SolarClue India"
check "solarland.com.bd" "SolarLand Bangladesh"
check "greensolar.com.bd" "Green Solar Bangladesh"
check "solar.ph" "Solar Philippines"
check "offgridbox.com" "OffGridBox (emerging markets)"
check "bbbox.com" "BBOXX (paygo solar Africa)"

echo ""
echo "=== SUMMARY: $total domains | $alive alive | $found with email ==="
