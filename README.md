# Docker & Microsserviços — Conjunto de Desafios

Este repositório contém as soluções propostas para os desafios solicitados.

Estrutura:
  
Smoke tests

Como usar (PowerShell):

Desafio 1 (script de build e smoke test):

```powershell
cd .\desafio1
# construir imagens
cd .\server; docker build -t desafio1-server .; Set-Location ..\client; docker build -t desafio1-client .; Set-Location ..\
# executar smoke test
.\test\run-desafio1.ps1
```

Desafio 2 (persistência - script guiado):

```powershell
cd .\desafio2
# executar demo de persistência
.\demo-persist.ps1
```

Desafio 3 (compose stack):

```powershell
cd .\desafio3
.\test\run-desafio3.ps1
```

Desafio 4 (microservices):

```powershell
cd .\desafio4
.\test\run-desafio4.ps1
```

Desafio 5 (API Gateway):

```powershell
cd .\desafio5
.\test\run-desafio5.ps1
```

Top-level runner (executa os smoke tests disponíveis):

```powershell
cd repo-root
.\test\run_all_tests.ps1
```

Observações finais:
# Docker & Microsserviços — Conjunto de Desafios

Este repositório contém implementações originais e didáticas para cada desafio proposto. Cada exemplo foi escrito com clareza para facilitar entendimento, execução e explicação posterior.

Estrutura do repositório:
- `desafio1/` — Containers em Rede (servidor Flask + cliente que faz requisições periódicas)
- `desafio2/` — Volumes e Persistência (Postgres com volume nomeado)
- `desafio3/` — Docker Compose (web Flask + Postgres + Redis)
- `desafio4/` — Microsserviços Independentes (service_a fornece usuários, service_b consome e enriquece)
- `desafio5/` — Microsserviços com API Gateway (users, orders e gateway de API)

Testes rápidos (smoke tests):
- Cada desafio contém um diretório `test` com scripts PowerShell para testes básicos de integração.
- O runner `test/run_all_tests.ps1` executa os testes dos desafios aplicáveis em sequência.

Como executar (PowerShell):

Desafio 1 — rede entre containers

```powershell
Set-Location .\desafio1
Set-Location .\server; docker build -t desafio1-server .; Set-Location ..\client; docker build -t desafio1-client .; Set-Location ..\..
.\test\run-desafio1.ps1
```

Desafio 2 — persistência com volumes (script guiado)

```powershell
Set-Location .\desafio2
.\demo-persist.ps1
```

Desafio 3 — composer stack (web + db + cache)

```powershell
Set-Location .\desafio3
.\test\run-desafio3.ps1
```

Desafio 4 — microsserviços independentes

```powershell
Set-Location .\desafio4
.\test\run-desafio4.ps1
```

Desafio 5 — API Gateway

```powershell
Set-Location .\desafio5
.\test\run-desafio5.ps1
```

Executar todos os testes disponíveis (top-level):

```powershell
Set-Location <raiz-do-repo>
.\test\run_all_tests.ps1
```
