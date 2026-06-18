curl -s http://localhost:3000/qr 2>&1
echo "---"
curl -s http://localhost:3000/health 2>&1
echo "---"
curl -s http://localhost:3000/api/qr 2>&1
