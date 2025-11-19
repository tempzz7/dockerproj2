docker-compose up --build -d

docker-compose down --rmi local

# Desafio 4 — Microsserviços Independentes

Objetivo: Construir dois microsserviços independentes que se comunicam por HTTP, demonstrando isolamento e chamada entre serviços.

Serviços:
- `service_a` (porta 8000): fornece uma lista de usuários com o campo `ativo_desde`.
- `service_b` (porta 8001): consome `service_a` e expõe `/combined` com frases descritivas em português.

Execução (PowerShell):

```powershell
Set-Location .\desafio4
docker-compose up --build -d

# Testes rápidos
Invoke-RestMethod -Uri http://localhost:8000/users -Method Get
Invoke-RestMethod -Uri http://localhost:8001/combined -Method Get
```

Notas:
- Cada serviço é isolado em seu próprio container com `Dockerfile` separado.
- A comunicação interna usa a rede criada pelo `docker-compose` e resolução de nomes pelos serviços (`service_a`).

Limpeza:

```powershell
docker-compose down --rmi local
```
