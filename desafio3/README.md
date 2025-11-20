# Desafio 3 — Docker Compose Orquestrando Serviços

## Descrição da Solução

Este desafio demonstra o poder do **Docker Compose** para orquestrar múltiplos serviços que trabalham juntos. A aplicação é composta por três containers que se comunicam através de uma rede interna:

1. **Web** (Flask): API REST que coordena tudo
2. **Database** (PostgreSQL): Armazena dados relacionais
3. **Cache** (Redis): Armazena dados temporários em memória

Esta é uma arquitetura clássica de aplicações web modernas: camada de aplicação, persistência e cache.

## Arquitetura e Decisões Técnicas

### Visão Geral da Arquitetura

```
                    ┌─────────────┐
                    │   Cliente   │
                    └──────┬──────┘
                           │ HTTP
                    ┌──────▼──────┐
                    │     Web     │
                    │   (Flask)   │
                    │  Porta 5000 │
                    └──┬───────┬──┘
                       │       │
           ┌───────────┘       └────────────┐
           │ SQL                             │ Cache
    ┌──────▼──────┐                  ┌──────▼──────┐
    │  Database   │                  │    Cache    │
    │ (Postgres)  │                  │   (Redis)   │
    │  Porta 5432 │                  │  Porta 6379 │
    └─────────────┘                  └─────────────┘
         │
    ┌────▼────┐
    │ Volume  │ (persistência)
    └─────────┘
```

### Componentes Detalhados

#### 1. Serviço Web (Flask)

- **Linguagem**: Python 3.11
- **Framework**: Flask
- **Bibliotecas**: psycopg2 (PostgreSQL), redis
- **Porta exposta**: 5000
- **Função**: API REST que interage com banco e cache

**Endpoints disponíveis:**

- `GET /` - Status da aplicação
- `GET /usuarios` - Lista todas as pessoas do banco
- `POST /usuarios` - Cria nova pessoa (JSON: `{"nome": "Fulano"}`)
- `GET /cache/<chave>` - Consulta valor no Redis
- `POST /cache` - Grava valor no Redis (JSON: `{"chave": "x", "valor": "y"}`)

#### 2. Serviço Database (PostgreSQL 15)

- **Porta**: 5432 (interna, não exposta ao host)
- **Banco**: desafio3db
- **Usuário**: web_user
- **Volume**: db_data (persiste os dados)

#### 3. Serviço Cache (Redis 7)

- **Porta**: 6379 (interna)
- **Uso**: Armazenamento temporário de dados em memória
- **Performance**: Acesso extremamente rápido para dados frequentes

### Decisões Técnicas Importantes

**Por que usar `depends_on`?**

O Docker Compose inicia os serviços na ordem definida. O serviço `web` depende de `db` e `cache`, então eles são iniciados primeiro.

⚠️ **Importante**: `depends_on` apenas controla a ordem de início, não garante que o banco esteja pronto. Por isso, a aplicação Flask tem lógica de retry para esperar o banco ficar disponível.

**Por que usar uma rede interna?**

A rede `internal_net` isola os serviços. Apenas o container `web` expõe porta para o host. Os containers `db` e `cache` só são acessíveis internamente, aumentando a segurança.

**Por que usar volume nomeado?**

O volume `db_data` persiste os dados do PostgreSQL mesmo quando os containers são removidos, exatamente como demonstrado no Desafio 2.

## Funcionamento

### Fluxo de uma Requisição

1. Cliente faz requisição HTTP para `http://localhost:5000/usuarios`
2. Container `web` recebe a requisição
3. Flask executa função `listar_usuarios()`
4. Aplicação conecta ao PostgreSQL via hostname `db` (resolvido pelo DNS interno do Docker)
5. Executa query SQL e recebe resultados
6. Retorna JSON para o cliente

### Fluxo de Cache

1. Cliente envia `POST /cache` com `{"chave": "mensagem", "valor": "ola mundo"}`
2. Flask grava no Redis usando hostname `cache`
3. Redis armazena em memória
4. Cliente pode consultar com `GET /cache/mensagem`

## Instruções de Execução

### Passo 1: Subir a stack completa

```bash
cd desafio3
docker-compose up --build -d
```

**O que acontece:**
- Docker cria a rede `internal_net`
- Cria o volume `db_data`
- Inicia os containers na ordem: db → cache → web
- Compila a imagem do serviço web

### Passo 2: Verificar se tudo está rodando

```bash
docker-compose ps
```

Você deve ver 3 containers em estado "Up".

### Passo 3: Testar a API

**Verificar status:**
```bash
curl http://localhost:5000/
```

**Criar usuários:**
```bash
curl -X POST http://localhost:5000/usuarios \
  -H "Content-Type: application/json" \
  -d '{"nome": "Maria Silva"}'

curl -X POST http://localhost:5000/usuarios \
  -H "Content-Type: application/json" \
  -d '{"nome": "João Santos"}'
```

**Listar usuários:**
```bash
curl http://localhost:5000/usuarios
```

Resposta esperada:
```json
[
  {"id": 1, "nome": "Maria Silva"},
  {"id": 2, "nome": "João Santos"}
]
```

**Testar cache:**
```bash
curl -X POST http://localhost:5000/cache \
  -H "Content-Type: application/json" \
  -d '{"chave": "saudacao", "valor": "Olá Mundo!"}'

curl http://localhost:5000/cache/saudacao
```

### Passo 4: Visualizar logs

Logs de todos os serviços:
```bash
docker-compose logs -f
```

Logs apenas do serviço web:
```bash
docker-compose logs -f web
```

### Passo 5: Testar persistência

Derrube e suba novamente:
```bash
docker-compose down
docker-compose up -d
```

Liste os usuários novamente - eles ainda estarão lá porque o volume persiste os dados!

### Passo 6: Limpeza completa

Para remover tudo, incluindo volumes:
```bash
docker-compose down -v
```

## Testando a Comunicação Entre Serviços

Você pode entrar no container `web` e testar a conexão direta com os outros serviços:

```bash
docker-compose exec web bash
```

Dentro do container:
```bash
ping db
ping cache

apt-get update && apt-get install -y postgresql-client
psql -h db -U web_user -d desafio3db
```

Isso demonstra que os containers conseguem se comunicar usando os nomes dos serviços.

## Estrutura de Arquivos

```
desafio3/
├── README.md
├── docker-compose.yml
└── web/
    ├── Dockerfile
    ├── app.py
    └── requirements.txt
```

## Variáveis de Ambiente

O arquivo `docker-compose.yml` configura as variáveis de ambiente que conectam os serviços:

**Database:**
- `POSTGRES_USER=web_user`
- `POSTGRES_PASSWORD=example`
- `POSTGRES_DB=desafio3db`

**Web:**
- `DATABASE_HOST=db` (nome do serviço)
- `DATABASE_USER=web_user`
- `REDIS_HOST=cache` (nome do serviço)

Isso demonstra como o Compose facilita a configuração de aplicações multi-container.

## Boas Práticas Demonstradas

✅ **Separação de responsabilidades**: Cada serviço tem uma função específica

✅ **Configuração via variáveis de ambiente**: Flexibilidade para diferentes ambientes

✅ **Uso de depends_on**: Controle de ordem de inicialização

✅ **Rede interna isolada**: Segurança adicional

✅ **Volumes nomeados**: Persistência de dados

✅ **Retry logic**: Aplicação aguarda banco ficar disponível

## Possíveis Melhorias para Produção

Em um ambiente real, você adicionaria:

- **Healthchecks**: Garantir que serviços estão realmente prontos
- **Secrets management**: Não usar senhas em texto plano
- **Múltiplos ambientes**: docker-compose.prod.yml, docker-compose.dev.yml
- **Logging centralizado**: Enviar logs para serviço externo
- **Backup automatizado**: Scripts para backup do volume do banco

Este desafio demonstra os fundamentos de orquestração com Docker Compose!
