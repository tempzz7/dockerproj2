#!/bin/bash
# Script simples em loop que consulta o servidor do Desafio 1
TARGET_URL="$1"
if [ -z "$TARGET_URL" ]; then
  TARGET_URL="http://server:8080/"
fi

while true; do
  echo "[cliente] consultando $TARGET_URL em $(date -u +%Y-%m-%dT%H:%M:%SZ)"
  if ! curl -sS "$TARGET_URL"; then
    echo "[cliente] falha na requisição"
  fi
  echo
  sleep 5
done
