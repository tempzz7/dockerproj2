docker-compose up --build -d

docker-compose down --rmi local

# Desafio 5 — Microsserviços com API Gateway

Objetivo: Implementar um gateway que centraliza o acesso a dois microsserviços (`users` e `orders`). O gateway expõe rotas públicas e encaminha internamente para os serviços correspondentes.

Serviços:
- `users` (porta interna 8002): fornece dados de usuários em `/users`.
- `orders` (porta interna 8003): fornece pedidos em `/orders`.
- `gateway` (porta 8080): expõe `/users` e `/orders` para clientes e faz a orquestração das chamadas.

Instruções (PowerShell):

```powershell
Set-Location .\desafio5
docker-compose up --build -d

# Testar via gateway
Invoke-RestMethod -Uri http://localhost:8080/users -Method Get
Invoke-RestMethod -Uri http://localhost:8080/orders -Method Get
```

Observações técnicas:
- O gateway encaminha as respostas dos serviços de backend sem transformar os dados (proxy simples). Em produções, poderíamos aplicar autenticação, rate-limiting e agregações.
- `depends_on` ajuda na ordem de inicialização, mas para produção usar healthchecks e retries apropriados.

Limpeza:

```powershell
docker-compose down --rmi local
```
