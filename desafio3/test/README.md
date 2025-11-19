# Testes do Desafio 3

Este script `run-desafio3.ps1` realiza um teste rápido das funcionalidades principais:
- Sobe a stack com `docker-compose up --build -d`
- Cria um usuário via `POST /users`
- Verifica endpoints de cache
- Faz `docker-compose down -v`

Use: executar do diretório `desafio3`:

```powershell
.\test\run-desafio3.ps1
```
