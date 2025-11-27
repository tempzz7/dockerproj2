# Desafio 3 — Orquestrando com Docker Compose

Aqui o objetivo era juntar tudo: múltiplos serviços rodando juntos, conversando entre si, gerenciados por um arquivo Compose.

## Arquitetura

Montei uma aplicação web com três componentes:

- **web** — API Flask que serve os endpoints
- **db** — PostgreSQL pra guardar dados de usuários
- **cache** — Redis pra cache rápido

A API Flask conversa com os dois, tanto o banco quanto o cache. É tipo uma mini-aplicação real.

## Por que esses serviços?

Quis usar um exemplo que fizesse sentido. Uma aplicação web normalmente tem:
- Um servidor (Flask)
- Um banco pra dados permanentes (Postgres)
- Um cache pra agilizar respostas (Redis)

O Compose simplifica demais isso. Ao invés de subir três containers na mão, configurar rede, etc., você descreve tudo num `docker-compose.yml` e sobe com um comando só.

## O que a API faz

Implementei alguns endpoints básicos:

- `GET /` — só pra ver se tá vivo
- `GET /users` — lista usuários do banco
- `POST /users` — adiciona um usuário novo
- `POST /cache` — salva algo no Redis
- `GET /cache/<chave>` — busca do cache

A tabela no Postgres é criada automaticamente quando a aplicação sobe pela primeira vez.

## Como rodar

### Jeito rápido (com script)

```powershell
cd .\desafio3
.\test\run-desafio3.ps1
```

### Jeito manual

```powershell
cd .\desafio3
docker-compose up --build -d
```

Depois testa os endpoints:

```powershell
# Adicionar um usuário
Invoke-RestMethod -Uri http://localhost:5000/users -Method Post `
  -Body (@{ name = 'Bob' } | ConvertTo-Json) `
  -ContentType 'application/json'

# Listar usuários
Invoke-RestMethod -Uri http://localhost:5000/users -Method Get

# Colocar algo no cache
Invoke-RestMethod -Uri http://localhost:5000/cache -Method Post `
  -Body (@{ key='greet'; value='ola' } | ConvertTo-Json) `
  -ContentType 'application/json'

# Buscar do cache
Invoke-RestMethod -Uri http://localhost:5000/cache/greet -Method Get
```

## Derrubar tudo

```powershell
docker-compose down -v
```

O `-v` remove os volumes também, limpando os dados do banco.

## Detalhes técnicos

### depends_on

Usei `depends_on` no Compose pra garantir que o banco e o cache sobem antes da web. Não é perfeito (não garante que tão prontos, só que iniciaram), mas pro propósito didático funciona.

Pra produção você usaria healthchecks ou scripts tipo wait-for-it, mas quis manter simples.

### Rede interna

O Compose cria uma rede automaticamente. Os serviços se enxergam pelos nomes definidos no YAML (`db`, `cache`, `web`). Por isso no código Flask eu conecto em `db:5432` e `cache:6379`.

### Variáveis de ambiente

As credenciais do banco tão no docker-compose.yml como variáveis de ambiente. Não é o ideal pra produção (você usaria secrets), mas facilita pra testar.

## O que aprendi

O Compose muda o jogo. Sem ele, você fica maluco criando rede, linkando containers, passando variáveis... Com ele, você descreve a arquitetura inteira num arquivo e o Docker cuida do resto.

Também ficou claro como os serviços dependem uns dos outros — a web precisa que o banco e o cache estejam disponíveis. O `depends_on` ajuda nisso, mas entender as limitações dele também é importante.
