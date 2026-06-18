#!/bin/bash
# Round 2: Solar/electronics distributors in NEW markets
# Turkey, Saudi Arabia, Brazil, Nigeria, Pakistan, Vietnam

echo "=== SOLAR DISTRIBUTORS — NEW MARKETS ==="
for domain in \
  "enerjisa.com.tr:Turkey energy retailer" \
  "solarenerji.com.tr:Turkey solar distributor" \
  "neosolar.com.br:Brazil solar retailer" \
  "minhacasasolar.com.br:Brazil solar marketplace" \
  "aldosolar.com.br:Brazil solar distributor" \
  "portal-energia.com:Brazil energy portal" \
  "desert-technologies.com:Saudi solar EPC" \
  "solarabic.com:Saudi solar directory" \
  "gennextechnologies.com:Nigeria solar installer" \
  "solarmart.com.ng:Nigeria solar retailer" \
  "solarpowernigeria.com:Nigeria solar" \
  "dlight.com:Global off-grid solar" \
  "bbbox.com:PayGo solar Africa" \
  "solarnow.ug:Uganda solar" \
  "m-kopa.com:PayGo solar Kenya" \
  "solargarden.com.au:Australia solar" \
  "evoenergy.co.uk:UK solar installer" \
  "solartogether.co.uk:UK solar group-buy" \
  "dienmayxanh.com:Vietnam electronics" \
  "fptshop.com.vn:Vietnam electronics" \
  "pakistansolar.com:Pakistan solar" \
  "renewableenergy.go.ke:Kenya renewable" \
  "solarkenya.co.ke:Kenya solar" \
  "sonnendach.co.za:SA solar"; do
  
  d="${domain%%:*}"
  desc="${domain#*:}"
  
  code=$(curl -sL --connect-timeout 4 --max-time 8 \
    -o /dev/null -w "%{http_code}" \
    -H "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64)" \
    "https://www.$d" 2>/dev/null)
  
  if [ "$code" = "200" ] || [ "$code" = "301" ] || [ "$code" = "302" ]; then
    echo "✓ $d [$code] - $desc"
  else
    echo "✗ $d [$code] - $desc"
  fi
done
