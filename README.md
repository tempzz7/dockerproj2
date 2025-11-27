# Desafios de Docker & Microsserviços

Esse repositório tem as soluções que desenvolvi para os desafios propostos na disciplina. Cada um foi feito do zero, focando em deixar claro como as coisas funcionam.

## O que tem aqui

- **desafio1/** — Dois containers conversando via rede Docker
- **desafio2/** — Persistência de dados usando volumes
- **desafio3/** — Stack completa com Docker Compose (web + db + cache)
- **desafio4/** — Dois microsserviços se comunicando direto via HTTP
- **desafio5/** — Arquitetura com API Gateway gerenciando microsserviços

## Como rodar

Cada desafio tem seu próprio README explicando o que fiz e por quê. Também criei scripts de teste em PowerShell pra facilitar a execução.

### Desafio 1 — Comunicação em rede

```powershell
cd .\desafio1
cd .\server; docker build -t desafio1-server .; cd ..\client; docker build -t desafio1-client .; cd ..\
.\test\run-desafio1.ps1
```

### Desafio 2 — Volumes persistentes

```powershell
cd .\desafio2
.\demo-persist.ps1
```

Esse script vai guiando pelos passos de criar dados, remover o container e verificar que os dados continuam lá.

### Desafio 3 — Orquestrando com Compose

```powershell
cd .\desafio3
.\test\run-desafio3.ps1
```

### Desafio 4 — Microsserviços independentes

```powershell
cd .\desafio4
.\test\run-desafio4.ps1
```

### Desafio 5 — API Gateway

```powershell
cd .\desafio5
.\test\run-desafio5.ps1
```

### Rodar tudo de uma vez

Se quiser executar todos os testes automatizados:

```powershell
.\test\run_all_tests.ps1
```

## Sobre a implementação

Procurei manter tudo simples e direto. Não quis complicar com frameworks ou bibliotecas pesadas — o foco era entender como Docker funciona de verdade. Cada decisão técnica tá explicada no README de cada desafio, tipo por que escolhi Flask pro servidor, como configurei as redes, etc.

Os códigos são propositalmente enxutos pra facilitar na hora de explicar o que cada linha faz.
