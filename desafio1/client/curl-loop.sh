#!/bin/bash

ENDERECO_SERVIDOR="$1"
if [ -z "$ENDERECO_SERVIDOR" ]; then
  ENDERECO_SERVIDOR="http://desafio1-server:8080/"
fi

while true; do
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] Fazendo requisição para $ENDERECO_SERVIDOR"
  RESPOSTA=$(curl -sS "$ENDERECO_SERVIDOR")
  if [ $? -eq 0 ]; then
    echo "Resposta recebida: $RESPOSTA"
  else
    echo "Erro ao conectar no servidor"
  fi
  echo ""
  sleep 5
done
