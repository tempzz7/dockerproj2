docker-compose up --build -d
docker-compose down -v

# Desafio 3 — Docker Compose Orquestrando Serviços

Objetivo: Demonstrar orquestração com Docker Compose para uma aplicação simples composta por `web` (Flask), `db` (Postgres) e `cache` (Redis).

Decisões e detalhes técnicos:
- A aplicação `web` usa `psycopg2` para Postgres e `redis` para cache. Cria a tabela `pessoas` automaticamente no primeiro acesso.
- Uso de `depends_on` para ordenar a inicialização; para produção recomendamos healthchecks e wait-for-it, mas aqui simplificamos para foco didático.

Como subir a stack:

```powershell
Set-Location .\desafio3
.\test\run-desafio3.ps1
```

Endpoints principais:
- `GET /` : retorna status do serviço web.
- `GET /users` : lista pessoas armazenadas no Postgres.
- `POST /users` : cria uma nova pessoa (JSON: `{ "name": "Nome" }`).
- `POST /cache` : define uma chave no Redis (JSON: `{ "key": "k", "value": "v" }`).
- `GET /cache/<key>` : lê valor do Redis.

Exemplo rápido (PowerShell):

```powershell
Invoke-RestMethod -Uri http://localhost:5000/users -Method Post -Body (@{ name = 'Bob' } | ConvertTo-Json) -ContentType 'application/json'
Invoke-RestMethod -Uri http://localhost:5000/users -Method Get

Invoke-RestMethod -Uri http://localhost:5000/cache -Method Post -Body (@{ key='greet'; value='ola' } | ConvertTo-Json) -ContentType 'application/json'
Invoke-RestMethod -Uri http://localhost:5000/cache/greet -Method Get
```

Limpeza:

```powershell
docker-compose down -v
```
