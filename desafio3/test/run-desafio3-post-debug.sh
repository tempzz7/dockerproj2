#!/bin/bash
set -euo pipefail
cd /mnt/d/Desktop/dockerproj2/desafio3
# garantir que esteja em execução
docker compose up --build -d
sleep 6
# criar json usando printf para evitar problemas de citação no shell
printf '%s' '{"name":"DebugUser"}' > /tmp/user_debug.json
echo '==> POSTando /users (debug)'
curl -v -X POST -H "Content-Type: application/json" -d @/tmp/user_debug.json http://localhost:5000/users || true

echo '--- logs do web (tail 200) ---'
docker logs --tail 200 desafio3-web-1 || true
