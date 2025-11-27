# Desafio 5 — API Gateway e Microsserviços

Esse é o desafio mais completo. A ideia era montar uma arquitetura com um API Gateway centralizando o acesso aos microsserviços de backend.

## Arquitetura

Montei três serviços:

**Users Service** (porta interna 8002)
- Gerencia dados de usuários
- Expõe `/users`
- Rodando só na rede interna

**Orders Service** (porta interna 8003)
- Gerencia pedidos
- Expõe `/orders`
- Também só na rede interna

**Gateway** (porta pública 8080)
- Ponto único de entrada
- Roteia `/users` pro Users Service
- Roteia `/orders` pro Orders Service
- Único serviço exposto externamente

## Por que usar um Gateway?

Na vida real, você não quer expor dezenas de microsserviços direto pro mundo. O Gateway centraliza tudo:

- **Ponto único de acesso** — o cliente só precisa saber um endereço
- **Segurança** — você pode adicionar autenticação só no gateway
- **Controle** — rate limiting, logs, monitoramento, tudo em um lugar
- **Flexibilidade** — se você mudar um serviço de backend, o cliente nem percebe

É tipo a recepção de um prédio — ao invés de dar o endereço de cada sala, você dá o endereço da recepção e ela te direciona.

## Como funciona na prática

Quando você faz uma requisição pra `http://localhost:8080/users`, o gateway:
1. Recebe a requisição
2. Faz um request interno pra `http://users:8002/users`
3. Pega a resposta
4. Devolve pro cliente

O cliente nem sabe que existe um Users Service separado. Pra ele, tudo vem do gateway.

## Como rodar

```powershell
cd .\desafio5
docker-compose up --build -d
```

### Testando

Você sempre bate no gateway (porta 8080):

```powershell
# Buscar usuários via gateway
Invoke-RestMethod -Uri http://localhost:8080/users -Method Get

# Buscar pedidos via gateway
Invoke-RestMethod -Uri http://localhost:8080/orders -Method Get
```

Note que você NÃO acessa as portas 8002 ou 8003 — elas nem estão expostas pro host. Tudo passa pelo gateway.

## Implementação do Gateway

O gateway que fiz é bem simples — ele só repassa as requisições (proxy). Mas dá pra ver onde você colocaria:

- Autenticação (verificar token antes de repassar)
- Rate limiting (limitar requests por usuário)
- Logs centralizados (registrar tudo que passa)
- Transformação de dados (agregar respostas de múltiplos serviços)

Mantive simples pra focar no conceito, mas a estrutura já tá lá.

## Rede e comunicação

Todos os serviços tão na mesma rede Docker interna. O gateway consegue acessar `users:8002` e `orders:8003` porque o Docker resolve esses nomes.

Mas só o gateway tem a porta exposta pro host (`8080:8080`). Os outros ficam internos — mais seguro assim.

## Derrubar tudo

```powershell
docker-compose down --rmi local
```

## O que aprendi

Esse desafio fechou o ciclo dos microsserviços pra mim. Entendi porque grandes aplicações usam gateways:

- Simplifica pro cliente (um endpoint só)
- Facilita adicionar segurança e controle
- Permite mudar os serviços de backend sem quebrar nada

Também ficou claro o conceito de serviços privados vs públicos. Os backends ficam escondidos atrás do gateway, que funciona como uma interface pública.

É tipo ter vários microondas na cozinha mas só uma janela de atendimento — o cliente pede na janela e você se vira lá dentro pra fazer o pedido.
