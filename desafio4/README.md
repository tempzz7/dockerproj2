# Desafio 4 — Microsserviços Independentes

## Descrição da Solução

Este desafio implementa uma arquitetura de **microsserviços**, onde dois serviços independentes se comunicam via HTTP. Cada serviço tem sua própria responsabilidade e pode ser desenvolvido, testado e escalado independentemente.

### Conceito de Microsserviços

Microsserviços são pequenas aplicações independentes que:
- Executam em processos separados
- Se comunicam através de APIs (geralmente HTTP/REST)
- Podem ser escritos em linguagens diferentes
- Podem ser implantados e escalados independentemente
- Têm bancos de dados próprios (quando necessário)

## Arquitetura e Decisões Técnicas

### Visão Geral da Arquitetura

```
         ┌────────────────┐
         │    Cliente     │
         └───────┬────────┘
                 │ HTTP
        ┌────────┴─────────┐
        │                  │
    ┌───▼────┐      ┌─────▼──────┐
    │Service │      │  Service   │
    │   A    │◄─────┤     B      │
    │        │ HTTP │            │
    │Porta   │      │ Porta 8001 │
    │ 8000   │      └────────────┘
    └────────┘

    [Fornece]      [Consome e Agrega]
```

### Microsserviço A - Gerenciamento de Usuários

**Responsabilidade**: Armazenar e fornecer informações básicas de usuários

**Tecnologia**: Flask (Python 3.11)

**Porta**: 8000

**Endpoints:**
- `GET /` - Informações sobre o serviço
- `GET /usuarios` - Lista todos os usuários cadastrados

**Dados fornecidos:**
```json
[
  {
    "id": 1,
    "nome": "Alice Martins",
    "ativo_desde": "2023-01-15"
  }
]
```

**Por que esse design?**

Este serviço representa um microserviço típico de "domínio de usuário". Em uma aplicação real, ele teria:
- Banco de dados próprio
- Lógica de negócio relacionada a usuários
- Autenticação e autorização
- Operações CRUD completas

### Microsserviço B - Agregador de Informações

**Responsabilidade**: Consumir dados do Serviço A e gerar informações agregadas/enriquecidas

**Tecnologia**: Flask (Python 3.11)

**Porta**: 8001

**Endpoints:**
- `GET /` - Informações sobre o serviço
- `GET /relatorio` - Relatório completo com cálculos adicionais
- `GET /resumo` - Resumo simplificado dos usuários

**O que ele faz:**

Consome a API do Serviço A e adiciona valor aos dados:
- Calcula quantos anos cada usuário está ativo
- Gera descrições textuais amigáveis
- Agrega informações de múltiplas fontes (neste exemplo, apenas uma)

**Por que esse design?**

Este padrão é comum em arquiteturas de microsserviços:
- **Backend for Frontend (BFF)**: Agrega dados de múltiplos serviços
- **API Gateway simplificado**: Fornece endpoints customizados para diferentes clientes
- **Camada de agregação**: Reduz o número de chamadas que o cliente precisa fazer

## Funcionamento

### Fluxo de Comunicação

**Cenário 1: Cliente consulta Serviço A diretamente**

```
Cliente → GET /usuarios → Serviço A → Retorna lista de usuários
```

**Cenário 2: Cliente consulta Serviço B (que chama Serviço A)**

```
Cliente → GET /relatorio → Serviço B
                              ↓
                  GET /usuarios → Serviço A
                              ↓
            Processa e enriquece dados
                              ↓
            Retorna relatório completo → Cliente
```

### Exemplo de Enriquecimento de Dados

**Serviço A retorna:**
```json
{"id": 1, "nome": "Alice Martins", "ativo_desde": "2023-01-15"}
```

**Serviço B processa e retorna:**
```json
{
  "id": 1,
  "nome": "Alice Martins",
  "data_cadastro": "2023-01-15",
  "anos_ativo": 2,
  "descricao": "Alice Martins está ativo desde 2023-01-15 (2 anos)"
}
```

## Instruções de Execução

### Passo 1: Subir os microsserviços

```bash
cd desafio4
docker-compose up --build -d
```

Isso cria:
- Container `service_a` (porta 8000)
- Container `service_b` (porta 8001)
- Rede interna para comunicação entre eles

### Passo 2: Verificar se estão rodando

```bash
docker-compose ps
```

### Passo 3: Testar o Serviço A isoladamente

**Informações do serviço:**
```bash
curl http://localhost:8000/
```

**Lista de usuários:**
```bash
curl http://localhost:8000/usuarios
```

Resposta esperada:
```json
[
  {"id": 1, "nome": "Alice Martins", "ativo_desde": "2023-01-15"},
  {"id": 2, "nome": "Bruno Costa", "ativo_desde": "2024-03-02"},
  {"id": 3, "nome": "Carla Souza", "ativo_desde": "2023-08-20"}
]
```

### Passo 4: Testar o Serviço B (que consome o Serviço A)

**Informações do serviço:**
```bash
curl http://localhost:8001/
```

**Relatório completo:**
```bash
curl http://localhost:8001/relatorio
```

Resposta esperada:
```json
{
  "total_usuarios": 3,
  "usuarios": [
    {
      "id": 1,
      "nome": "Alice Martins",
      "data_cadastro": "2023-01-15",
      "anos_ativo": 2,
      "descricao": "Alice Martins está ativo desde 2023-01-15 (2 anos)"
    }
  ]
}
```

**Resumo:**
```bash
curl http://localhost:8001/resumo
```

### Passo 5: Visualizar logs

Logs de ambos os serviços:
```bash
docker-compose logs -f
```

Você verá as requisições sendo feitas:
- Serviço B recebe requisição do cliente
- Serviço B faz requisição para Serviço A
- Serviço A retorna dados
- Serviço B processa e retorna ao cliente

### Passo 6: Testar comunicação interna

Entre no container do Serviço B e faça chamadas diretas:

```bash
docker-compose exec service_b bash
```

Dentro do container:
```bash
curl http://service_a:8000/usuarios
```

Isso demonstra a resolução de nomes DNS automática do Docker.

### Passo 7: Limpeza

```bash
docker-compose down --rmi local
```

## Estrutura de Arquivos

```
desafio4/
├── README.md
├── docker-compose.yml
├── service_a/
│   ├── Dockerfile
│   ├── app.py
│   └── requirements.txt
└── service_b/
    ├── Dockerfile
    ├── app.py
    └── requirements.txt
```

## Isolamento e Independência

Cada microsserviço é completamente isolado:

**Dockerfiles separados:**
- Cada serviço tem seu próprio Dockerfile
- Podem usar versões diferentes de Python ou até linguagens diferentes
- Dependências gerenciadas independentemente

**Imagens independentes:**
```bash
docker images | grep desafio4
```

Você verá:
- `desafio4-service_a`
- `desafio4-service_b`

**Portas diferentes:**
- Serviço A: 8000
- Serviço B: 8001

**Facilita escalabilidade:**
```bash
docker-compose up -d --scale service_a=3
```

## Comunicação HTTP Entre Microsserviços

### Por que HTTP?

- **Universal**: Funciona em qualquer linguagem
- **Stateless**: Sem dependência de estado compartilhado
- **Debugável**: Fácil testar com curl, Postman, etc.
- **Firewall-friendly**: Porta 80/443 geralmente liberadas

### Alternativas em produção

- **gRPC**: Comunicação binária mais rápida
- **Message Queue**: RabbitMQ, Kafka para comunicação assíncrona
- **Service Mesh**: Istio, Linkerd para gerenciamento avançado

## Tratamento de Erros

O Serviço B trata falhas de comunicação:

```python
try:
    resposta = requests.get(url, timeout=5)
    resposta.raise_for_status()
except requests.exceptions.RequestException as erro:
    return jsonify({'erro': 'Serviço indisponível'}), 502
```

Teste derrubando o Serviço A:
```bash
docker-compose stop service_a
curl http://localhost:8001/relatorio
```

Você receberá um erro HTTP 502 com mensagem explicativa.

## Vantagens dessa Arquitetura

✅ **Desenvolvimento independente**: Times diferentes podem trabalhar em cada serviço

✅ **Tecnologias diferentes**: Cada serviço pode usar a melhor tecnologia para seu problema

✅ **Escalabilidade granular**: Escalar apenas o serviço que precisa

✅ **Resiliência**: Falha em um serviço não derruba todo o sistema

✅ **Deploy independente**: Atualizar um serviço sem mexer nos outros

## Desvantagens e Desafios

❌ **Complexidade operacional**: Mais containers para gerenciar

❌ **Latência de rede**: Chamadas HTTP entre serviços adicionam latência

❌ **Debugging mais difícil**: Rastrear requisições por múltiplos serviços

❌ **Consistência de dados**: Transações distribuídas são complexas

Este desafio demonstra os fundamentos de comunicação entre microsserviços!
