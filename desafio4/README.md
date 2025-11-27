# Desafio 4 — Microsserviços se Comunicando

A proposta aqui era simular uma arquitetura de microsserviços de verdade: serviços pequenos, focados, rodando separados mas conversando entre si.

## Como funciona

Criei dois serviços:

**Service A** (porta 8000)
- Retorna uma lista de usuários com informação de quando ficaram ativos
- É tipo um serviço de cadastro básico

**Service B** (porta 8001)
- Consome os dados do Service A
- Processa e retorna frases descritivas sobre cada usuário
- Seria tipo um serviço de apresentação ou relatório

O importante é que cada um roda no seu próprio container, totalmente isolado. O Service B faz requisições HTTP pro Service A pra buscar os dados.

## Por que assim?

Em microsserviços de verdade, você quebra a aplicação em pedaços menores. Cada pedaço tem uma responsabilidade:
- Service A cuida dos dados brutos dos usuários
- Service B cuida de apresentar esses dados de forma mais elaborada

Se amanhã eu quiser adicionar um Service C que também consome o Service A, é só criar. Os serviços não dependem uns dos outros além da comunicação HTTP.

## Como rodar

```powershell
cd .\desafio4
docker-compose up --build -d
```

### Testando os endpoints

Você pode acessar cada serviço separadamente:

```powershell
# Service A — dados brutos
Invoke-RestMethod -Uri http://localhost:8000/users -Method Get

# Service B — dados processados
Invoke-RestMethod -Uri http://localhost:8001/combined -Method Get
```

O interessante é ver que o Service B busca do Service A internamente. Se você olhar os logs, vê o Service B fazendo requests.

## Comunicação interna

Os serviços usam a rede Docker criada pelo Compose. Internamente, o Service B acessa o Service A usando o nome `service_a:8000`. Não precisa de IP, o Docker resolve automaticamente.

Se você tentar bater direto no Service A de dentro do Service B, funciona perfeitamente porque tão na mesma rede.

## Dockerfiles separados

Cada serviço tem seu próprio Dockerfile. Isso é importante — na vida real você pode querer:
- Versões diferentes de Python
- Dependências diferentes
- Até linguagens diferentes

Como tão totalmente isolados, cada um pode fazer o que quiser.

## Derrubar tudo

```powershell
docker-compose down --rmi local
```

O `--rmi local` remove as imagens também, limpando tudo.

## O que aprendi

Foi legal ver microsserviços funcionando de verdade, mesmo numa escala pequena. O conceito de serviços independentes que conversam por HTTP ficou muito mais claro.

Também entendi melhor o trade-off: você ganha flexibilidade e isolamento, mas perde um pouco de simplicidade. Tem que gerenciar a comunicação entre serviços, lidar com falhas de rede, etc.

Outra coisa que ficou evidente é como a rede Docker simplifica tudo. Sem ela, você ia ter que ficar descobrindo IPs, configurando rotas... Com ela, é só usar o nome do serviço e pronto.
