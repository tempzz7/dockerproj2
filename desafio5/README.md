# Desafio 5 — Microsserviços com API Gateway

## Descrição da Solução

Este desafio implementa o padrão **API Gateway**, uma das arquiteturas mais importantes em sistemas de microsserviços modernos. O gateway atua como ponto único de entrada para todos os clientes, centralizando o acesso e orquestrando chamadas para múltiplos microsserviços backend.

### O que é um API Gateway?

Um API Gateway é um servidor que atua como intermediário entre clientes e microsserviços. Ele:
- **Centraliza o acesso**: Clientes fazem requisições apenas ao gateway
- **Roteia requisições**: Direciona cada chamada ao microsserviço apropriado
- **Agrega dados**: Pode combinar respostas de múltiplos serviços
- **Aplica políticas**: Autenticação, rate limiting, logging, etc.

## Arquitetura e Decisões Técnicas

### Visão Geral da Arquitetura

```
                     ┌──────────────┐
                     │   Cliente    │
                     │ (Navegador,  │
                     │   App, etc)  │
                     └──────┬───────┘
                            │ HTTP
                            │ Porta 8080
                     ┌──────▼───────┐
                     │              │
                     │   Gateway    │
                     │              │
                     └──┬────────┬──┘
                        │        │
            ┌───────────┘        └──────────┐
            │ HTTP                           │ HTTP
            │ Porta 8002                     │ Porta 8003
     ┌──────▼──────┐                  ┌─────▼──────┐
     │   Serviço   │                  │  Serviço   │
     │   Usuários  │                  │  Pedidos   │
     │             │                  │            │
     └─────────────┘                  └────────────┘
```

### Componentes da Arquitetura

#### 1. API Gateway (Porta 8080)

**Responsabilidade**: Ponto único de entrada que roteia requisições

**Tecnologia**: Flask + Requests (Python)

**Função principal**: Atuar como proxy inteligente

**Endpoints expostos:**

- `GET /` - Informações do gateway e rotas disponíveis
- `GET /usuarios` - Proxy para serviço de usuários
- `GET /usuarios/<id>` - Detalhes de um usuário
- `GET /pedidos` - Proxy para serviço de pedidos
- `GET /pedidos/<id>` - Detalhes de um pedido
- `GET /pedidos/usuario/<id>` - Pedidos de um usuário
- `GET /relatorio/<id>` - **Agregação**: Combina dados de usuário e pedidos

**Por que esse design?**

- Clientes não precisam conhecer os endereços dos microsserviços internos
- Facilita mudanças na arquitetura interna sem afetar clientes
- Permite adicionar funcionalidades cross-cutting (auth, logging, etc.)

#### 2. Microsserviço de Usuários (Porta 8002)

**Responsabilidade**: Gerenciar informações de usuários

**Dados armazenados**: Nome, email, cidade

**Endpoints:**
- `GET /` - Info do serviço
- `GET /usuarios` - Lista todos
- `GET /usuarios/<id>` - Detalhes de um usuário

**Observação**: Este serviço NÃO é exposto diretamente ao cliente. Apenas o gateway pode acessá-lo.

#### 3. Microsserviço de Pedidos (Porta 8003)

**Responsabilidade**: Gerenciar pedidos de compra

**Dados armazenados**: Produto, valor, status, usuário relacionado

**Endpoints:**
- `GET /` - Info do serviço
- `GET /pedidos` - Lista todos (suporta filtro por usuário via query param)
- `GET /pedidos/<id>` - Detalhes de um pedido
- `GET /pedidos/usuario/<id>` - Pedidos de um usuário específico

**Observação**: Também não é exposto diretamente ao cliente.

## Funcionamento

### Fluxo 1: Requisição Simples (Proxy)

```
Cliente
   │
   │ GET http://localhost:8080/usuarios
   │
   ▼
Gateway
   │
   │ GET http://users:8002/usuarios
   │
   ▼
Serviço Usuários
   │
   │ Retorna JSON com lista de usuários
   │
   ▼
Gateway
   │
   │ Repassa resposta sem modificar
   │
   ▼
Cliente (recebe lista de usuários)
```

### Fluxo 2: Agregação de Dados

```
Cliente
   │
   │ GET http://localhost:8080/relatorio/1
   │
   ▼
Gateway
   │
   ├─► GET http://users:8002/usuarios/1
   │   └─► Recebe: {"id": 1, "nome": "Ana", ...}
   │
   ├─► GET http://orders:8003/pedidos/usuario/1
   │   └─► Recebe: {"pedidos": [...], "total_pedidos": 2}
   │
   │ Gateway processa e combina os dados:
   │ - Calcula valor total de todos os pedidos
   │ - Adiciona timestamp de geração
   │ - Monta resposta agregada
   │
   ▼
Cliente (recebe relatório completo)
```

### Exemplo de Resposta Agregada

**Cliente faz:** `GET /relatorio/1`

**Gateway retorna:**
```json
{
  "usuario": {
    "id": 1,
    "nome": "Ana Clara Santos",
    "email": "ana.santos@email.com",
    "cidade": "São Paulo"
  },
  "estatisticas_pedidos": {
    "total_pedidos": 2,
    "valor_total": 3950.00
  },
  "pedidos": [
    {
      "id": 101,
      "produto": "Notebook Dell",
      "valor": 3500.00,
      "status": "entregue"
    },
    {
      "id": 103,
      "produto": "Teclado Mecânico",
      "valor": 450.00,
      "status": "processando"
    }
  ],
  "gerado_em": "2025-11-20T16:30:45.123456"
}
```

Isso economiza várias chamadas do cliente!

## Instruções de Execução

### Passo 1: Subir toda a arquitetura

```bash
cd desafio5
docker-compose up --build -d
```

Isso cria:
- Container `gateway` (porta 8080)
- Container `users` (porta 8002, interna)
- Container `orders` (porta 8003, interna)
- Rede interna para comunicação

### Passo 2: Verificar status

```bash
docker-compose ps
```

Todos devem estar "Up".

### Passo 3: Consultar o gateway

**Rotas disponíveis:**
```bash
curl http://localhost:8080/
```

### Passo 4: Testar endpoints de usuários via gateway

**Listar todos os usuários:**
```bash
curl http://localhost:8080/usuarios
```

**Detalhes de um usuário:**
```bash
curl http://localhost:8080/usuarios/1
```

### Passo 5: Testar endpoints de pedidos via gateway

**Listar todos os pedidos:**
```bash
curl http://localhost:8080/pedidos
```

**Filtrar pedidos por usuário:**
```bash
curl "http://localhost:8080/pedidos?id_usuario=1"
```

**Detalhes de um pedido:**
```bash
curl http://localhost:8080/pedidos/101
```

**Pedidos de um usuário:**
```bash
curl http://localhost:8080/pedidos/usuario/1
```

### Passo 6: Testar agregação (funcionalidade do gateway!)

**Relatório completo de um usuário:**
```bash
curl http://localhost:8080/relatorio/1
```

Este endpoint chama DOIS serviços diferentes e agrega os resultados!

### Passo 7: Demonstrar isolamento

Tente acessar os microsserviços diretamente:

```bash
curl http://localhost:8002/usuarios
curl http://localhost:8003/pedidos
```

**Resultado**: Erro de conexão! As portas 8002 e 8003 não estão expostas ao host, apenas o gateway (8080) está.

Isso demonstra que o gateway é o **único ponto de acesso**.

### Passo 8: Visualizar logs

```bash
docker-compose logs -f gateway
```

Você verá todas as requisições passando pelo gateway.

### Passo 9: Limpeza

```bash
docker-compose down --rmi local
```

## Estrutura de Arquivos

```
desafio5/
├── README.md
├── docker-compose.yml
├── gateway/
│   ├── Dockerfile
│   ├── app.py
│   └── requirements.txt
├── users/
│   ├── Dockerfile
│   ├── app.py
│   └── requirements.txt
└── orders/
    ├── Dockerfile
    ├── app.py
    └── requirements.txt
```

## Padrões Implementados

### 1. API Gateway Pattern

O gateway centraliza o acesso e implementa:

- **Roteamento**: Direciona requisições aos serviços corretos
- **Agregação**: Endpoint `/relatorio/<id>` combina dados de múltiplos serviços
- **Tratamento de erros**: Retorna HTTP 503 quando serviços estão indisponíveis

### 2. Service Discovery (via Docker DNS)

```python
URL_SERVICO_USUARIOS = 'http://users:8002'
URL_SERVICO_PEDIDOS = 'http://orders:8003'
```

O Docker resolve automaticamente os nomes `users` e `orders` para os IPs internos dos containers.

### 3. Isolamento de Rede

```yaml
ports:
  - "8080:8080"  # Apenas gateway exposto
```

Microsserviços de backend não têm portas expostas ao host, aumentando a segurança.

## Vantagens do API Gateway

✅ **Ponto único de entrada**: Simplifica acesso para clientes

✅ **Desacoplamento**: Clientes não conhecem estrutura interna

✅ **Agregação**: Reduz número de chamadas do cliente

✅ **Segurança**: Backend protegido, apenas gateway exposto

✅ **Cross-cutting concerns**: Lugar ideal para auth, logging, rate limiting

✅ **Versionamento**: Suporta múltiplas versões de APIs

✅ **Transformação de dados**: Adapta respostas para diferentes clientes

## Recursos Implementados no Gateway

### Tratamento de Erros

```python
try:
    resposta = requests.get(url, timeout=5)
    return (resposta.content, resposta.status_code, resposta.headers.items())
except requests.exceptions.RequestException:
    return jsonify({'erro': 'Serviço indisponível'}), 503
```

### Agregação de Múltiplos Serviços

```python
resp_usuario = requests.get(f"{URL_USUARIOS}/usuarios/{id}")
resp_pedidos = requests.get(f"{URL_PEDIDOS}/pedidos/usuario/{id}")

relatorio_completo = {
    'usuario': resp_usuario.json(),
    'pedidos': resp_pedidos.json()
}
```

### Proxy Transparente

```python
return (resposta.content, resposta.status_code, resposta.headers.items())
```

Repassa a resposta completa do backend, incluindo headers e status code.

## Possíveis Melhorias para Produção

Em um ambiente real, você adicionaria:

- **Autenticação/Autorização**: JWT, OAuth2
- **Rate Limiting**: Limitar requisições por cliente
- **Caching**: Cache de respostas frequentes
- **Circuit Breaker**: Evitar sobrecarga quando serviços falham
- **Load Balancing**: Distribuir carga entre múltiplas instâncias
- **Service Discovery dinâmico**: Consul, Eureka
- **API Gateway dedicado**: Kong, Nginx, AWS API Gateway
- **Observability**: Tracing distribuído (Jaeger), métricas (Prometheus)
- **HTTPS**: Certificados SSL/TLS

## Comparação com Desafio 4

**Desafio 4**: Microsserviços se comunicam diretamente

**Desafio 5**: Comunicação através do gateway

Vantagens do gateway:
- Cliente não precisa conhecer múltiplos endpoints
- Mudanças internas não afetam clientes
- Centraliza políticas de segurança e monitoramento

Este desafio demonstra como o padrão API Gateway simplifica arquiteturas de microsserviços complexas!
