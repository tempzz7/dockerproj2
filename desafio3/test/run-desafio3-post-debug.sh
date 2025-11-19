#!/bin/bash
set -euo pipefail
cd /mnt/d/Desktop/dockerproj2/desafio3
# ensure running
docker compose up --build -d
sleep 6
# create json using printf to avoid shell quoting issues
printf '%s' '{"name":"DebugUser"}' > /tmp/user_debug.json
echo '==> POSTing /users (debug)'
curl -v -X POST -H "Content-Type: application/json" -d @/tmp/user_debug.json http://localhost:5000/users || true

echo '--- web logs (tail 200) ---'
docker logs --tail 200 desafio3-web-1 || true
