#!/bin/bash
set -euo pipefail
cd /mnt/d/Desktop/dockerproj2/desafio3
# reiniciar stack
docker compose down -v >/dev/null 2>&1 || true
docker compose up --build -d
sleep 8
echo "==> GET / (índice)"
curl -sS http://localhost:5000/ || true

# criar user json (usar printf para evitar problemas de escape)
printf '%s' '{"name":"SmokeUser"}' > /tmp/user.json
echo "==> POST /users (criar usuário)"
curl -v -X POST -H "Content-Type: application/json" -d @/tmp/user.json http://localhost:5000/users || true

echo "==> GET /users (listar usuários)"
curl -sS http://localhost:5000/users || true

# cache (usar printf para evitar problemas de escape)
printf '%s' '{"key":"smoke","value":"ok"}' > /tmp/cache.json
echo "==> POST /cache (definir cache)"
curl -v -X POST -H "Content-Type: application/json" -d @/tmp/cache.json http://localhost:5000/cache || true

echo "==> GET /cache/smoke (obter cache)"
curl -sS http://localhost:5000/cache/smoke || true

# teardown
docker compose down -v || true

echo "Script WSL do Desafio3 finalizado"
