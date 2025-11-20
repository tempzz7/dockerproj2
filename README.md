# Desafios Docker & Microsserviços

Este repositório contém implementações completas e didáticas de 5 desafios práticos sobre **Docker** e **arquitetura de microsserviços**. Cada desafio foi desenvolvido com foco em clareza, boas práticas e aprendizado hands-on.

## 📚 Visão Geral dos Desafios

### Desafios Docker (1-3)

| Desafio | Tema | Conceitos Principais |
|---------|------|---------------------|
| **1** | Containers em Rede | Redes Docker customizadas, comunicação entre containers, DNS interno |
| **2** | Volumes e Persistência | Volumes nomeados, persistência de dados, ciclo de vida de containers |
| **3** | Docker Compose | Orquestração multi-container, depends_on, variáveis de ambiente |

### Desafios Microsserviços (4-5)

| Desafio | Tema | Conceitos Principais |
|---------|------|---------------------|
| **4** | Microsserviços Independentes | Comunicação HTTP entre serviços, isolamento, escalabilidade |
| **5** | API Gateway | Gateway pattern, agregação de dados, roteamento centralizado |

## 🚀 Início Rápido

### Pré-requisitos

- Docker (versão 20.10 ou superior)
- Docker Compose (versão 1.29 ou superior)
- curl ou navegador web para testar as APIs

### Estrutura do Repositório

```
dockerproj2/
├── desafio1/          # Containers em Rede
│   ├── server/        # Servidor Flask
│   ├── client/        # Cliente curl em loop
│   └── README.md
├── desafio2/          # Volumes e Persistência
│   └── README.md      # PostgreSQL com volume persistente
├── desafio3/          # Docker Compose
│   ├── web/           # Aplicação Flask
│   ├── docker-compose.yml
│   └── README.md
├── desafio4/          # Microsserviços Independentes
│   ├── service_a/     # API de usuários
│   ├── service_b/     # Agregador
│   ├── docker-compose.yml
│   └── README.md
├── desafio5/          # API Gateway
│   ├── gateway/       # Gateway
│   ├── users/         # Microsserviço usuários
│   ├── orders/        # Microsserviço pedidos
│   ├── docker-compose.yml
│   └── README.md
└── README.md          # Este arquivo
```

## 📝 Detalhamento dos Desafios

### Desafio 1: Containers em Rede

**Objetivo**: Demonstrar comunicação entre containers usando rede Docker customizada.

**Tecnologias**: Python/Flask, Alpine Linux, curl

**O que você aprenderá**:
- Criar redes Docker customizadas
- Comunicação entre containers via DNS interno
- Logs e debugging de containers

**Como executar**:
```bash
cd desafio1
docker network create mynet_desafio1
cd server && docker build -t desafio1-server .
cd ../client && docker build -t desafio1-client .
cd ..

docker run -d --name desafio1-server --network mynet_desafio1 -p 8080:8080 desafio1-server
docker run -d --name desafio1-client --network mynet_desafio1 desafio1-client

docker logs -f desafio1-client
```

[Documentação completa](desafio1/README.md)

---

### Desafio 2: Volumes e Persistência

**Objetivo**: Demonstrar persistência de dados usando volumes Docker.

**Tecnologias**: PostgreSQL 15

**O que você aprenderá**:
- Criar e gerenciar volumes Docker
- Persistir dados de banco de dados
- Ciclo de vida de containers vs volumes

**Como executar**:
```bash
cd desafio2
docker volume create db_desafio2_data

docker run -d --name desafio2-postgres \
  -e POSTGRES_USER=usuario_demo \
  -e POSTGRES_PASSWORD=senha_segura \
  -e POSTGRES_DB=banco_desafio2 \
  -v db_desafio2_data:/var/lib/postgresql/data \
  -p 5432:5432 \
  postgres:15

docker exec -it desafio2-postgres psql -U usuario_demo -d banco_desafio2 \
  -c "CREATE TABLE pessoas (id SERIAL PRIMARY KEY, nome TEXT, idade INT);"

docker exec -it desafio2-postgres psql -U usuario_demo -d banco_desafio2 \
  -c "INSERT INTO pessoas (nome, idade) VALUES ('Maria Silva', 28), ('João Santos', 35);"

docker rm -f desafio2-postgres

docker run -d --name desafio2-postgres \
  -e POSTGRES_USER=usuario_demo \
  -e POSTGRES_PASSWORD=senha_segura \
  -e POSTGRES_DB=banco_desafio2 \
  -v db_desafio2_data:/var/lib/postgresql/data \
  -p 5432:5432 \
  postgres:15

docker exec -it desafio2-postgres psql -U usuario_demo -d banco_desafio2 \
  -c "SELECT * FROM pessoas;"
```

[Documentação completa](desafio2/README.md)

---

### Desafio 3: Docker Compose Orquestrando Serviços

**Objetivo**: Orquestrar múltiplos serviços dependentes usando Docker Compose.

**Tecnologias**: Flask, PostgreSQL, Redis

**Arquitetura**:
- **Web**: API REST (porta 5000)
- **Database**: PostgreSQL (porta interna 5432)
- **Cache**: Redis (porta interna 6379)

**O que você aprenderá**:
- Escrever arquivos docker-compose.yml
- Configurar dependências entre serviços
- Gerenciar variáveis de ambiente
- Rede interna e volumes no Compose

**Como executar**:
```bash
cd desafio3
docker-compose up --build -d

curl http://localhost:5000/
curl -X POST http://localhost:5000/usuarios \
  -H "Content-Type: application/json" \
  -d '{"nome": "Maria Silva"}'
curl http://localhost:5000/usuarios

curl -X POST http://localhost:5000/cache \
  -H "Content-Type: application/json" \
  -d '{"chave": "teste", "valor": "funciona!"}'
curl http://localhost:5000/cache/teste

docker-compose down -v
```

[Documentação completa](desafio3/README.md)

---

### Desafio 4: Microsserviços Independentes

**Objetivo**: Criar microsserviços que se comunicam via HTTP.

**Tecnologias**: Flask (Python)

**Arquitetura**:
- **Service A** (porta 8000): Fornece lista de usuários
- **Service B** (porta 8001): Consome Service A e gera relatórios enriquecidos

**O que você aprenderá**:
- Arquitetura de microsserviços
- Comunicação HTTP entre serviços
- Isolamento e independência
- Dockerfiles separados por serviço

**Como executar**:
```bash
cd desafio4
docker-compose up --build -d

curl http://localhost:8000/usuarios
curl http://localhost:8001/relatorio
curl http://localhost:8001/resumo

docker-compose down --rmi local
```

[Documentação completa](desafio4/README.md)

---

### Desafio 5: Microsserviços com API Gateway

**Objetivo**: Implementar um API Gateway centralizando acesso a microsserviços.

**Tecnologias**: Flask (Python)

**Arquitetura**:
- **Gateway** (porta 8080): Ponto único de entrada
- **Users Service** (porta interna 8002): Gerencia usuários
- **Orders Service** (porta interna 8003): Gerencia pedidos

**O que você aprenderá**:
- Padrão API Gateway
- Roteamento centralizado
- Agregação de dados de múltiplos serviços
- Isolamento de backend (serviços não expostos diretamente)

**Como executar**:
```bash
cd desafio5
docker-compose up --build -d

curl http://localhost:8080/
curl http://localhost:8080/usuarios
curl http://localhost:8080/pedidos
curl http://localhost:8080/relatorio/1

docker-compose down --rmi local
```

**Diferencial**: O endpoint `/relatorio/<id>` demonstra agregação - o gateway consulta DOIS microsserviços e combina os resultados em uma única resposta!

[Documentação completa](desafio5/README.md)

---

## 🎯 Objetivos de Aprendizado

Ao completar estes desafios, você terá conhecimento prático sobre:

### Docker
- ✅ Criação e gerenciamento de containers
- ✅ Redes Docker customizadas
- ✅ Volumes e persistência de dados
- ✅ Dockerfiles e construção de imagens
- ✅ Docker Compose para orquestração
- ✅ Variáveis de ambiente
- ✅ Logs e debugging

### Microsserviços
- ✅ Arquitetura de microsserviços
- ✅ Comunicação HTTP/REST entre serviços
- ✅ API Gateway pattern
- ✅ Agregação de dados
- ✅ Service discovery via DNS
- ✅ Isolamento e independência de serviços
- ✅ Tratamento de erros em sistemas distribuídos

## 🛠️ Tecnologias Utilizadas

- **Docker** & **Docker Compose**
- **Python 3.11**
- **Flask** (framework web)
- **PostgreSQL 15** (banco relacional)
- **Redis 7** (cache em memória)
- **Alpine Linux** (imagens leves)
- **curl** (cliente HTTP)

## 📊 Comparação dos Desafios

| Aspecto | Desafio 1 | Desafio 2 | Desafio 3 | Desafio 4 | Desafio 5 |
|---------|-----------|-----------|-----------|-----------|-----------|
| Containers | 2 | 1 | 3 | 2 | 3 |
| Compose | ❌ | ❌ | ✅ | ✅ | ✅ |
| Rede customizada | ✅ | ❌ | ✅ | ✅ | ✅ |
| Volumes | ❌ | ✅ | ✅ | ❌ | ❌ |
| Banco de dados | ❌ | ✅ | ✅ | ❌ | ❌ |
| Microsserviços | ❌ | ❌ | ❌ | ✅ | ✅ |
| Gateway | ❌ | ❌ | ❌ | ❌ | ✅ |

## 🎓 Boas Práticas Demonstradas

### Código
- ✅ Código 100% em português brasileiro
- ✅ Nomes de variáveis descritivos
- ✅ Separação de responsabilidades
- ✅ Tratamento de erros apropriado
- ✅ Timeout em requisições HTTP
- ✅ Retry logic para serviços dependentes

### Docker
- ✅ Imagens base oficiais
- ✅ .dockerignore para otimizar builds
- ✅ Multi-stage builds onde apropriado
- ✅ Exposição apenas das portas necessárias
- ✅ Uso de variáveis de ambiente
- ✅ Networks isoladas por aplicação
- ✅ Volumes nomeados para persistência

### Arquitetura
- ✅ Separação clara entre camadas
- ✅ Serviços desacoplados
- ✅ Comunicação via APIs REST
- ✅ Backend protegido (não exposto diretamente)
- ✅ Ponto único de entrada (Gateway)

## 🔍 Comandos Úteis

### Docker Básico
```bash
docker ps                    # Lista containers em execução
docker ps -a                 # Lista todos os containers
docker logs -f <container>   # Logs em tempo real
docker exec -it <container> bash  # Acessa container
docker rm -f <container>     # Remove container
docker images                # Lista imagens
docker rmi <image>          # Remove imagem
```

### Docker Networks
```bash
docker network ls            # Lista redes
docker network inspect <name>  # Detalhes da rede
docker network create <name>   # Cria rede
docker network rm <name>       # Remove rede
```

### Docker Volumes
```bash
docker volume ls             # Lista volumes
docker volume inspect <name> # Detalhes do volume
docker volume create <name>  # Cria volume
docker volume rm <name>      # Remove volume
```

### Docker Compose
```bash
docker-compose up -d         # Sobe serviços em background
docker-compose ps            # Status dos serviços
docker-compose logs -f       # Logs de todos os serviços
docker-compose down          # Para e remove containers
docker-compose down -v       # Remove também os volumes
```

## 📖 Material de Apoio

Cada desafio possui seu próprio README.md com:
- ✅ Descrição detalhada da solução
- ✅ Explicação da arquitetura
- ✅ Decisões técnicas justificadas
- ✅ Funcionamento passo a passo
- ✅ Instruções completas de execução
- ✅ Exemplos de comandos e saídas esperadas
- ✅ Estrutura de arquivos
- ✅ Conceitos importantes
- ✅ Vantagens e desvantagens

## 🚨 Resolução de Problemas

### Porta já em uso
```bash
docker ps  # Identifica container usando a porta
docker rm -f <container>  # Remove o container
```

### Problemas de rede
```bash
docker network prune  # Remove redes não utilizadas
docker network create <name>  # Recria a rede
```

### Container não inicia
```bash
docker logs <container>  # Verifica logs de erro
docker inspect <container>  # Detalhes do container
```

### Volumes com dados antigos
```bash
docker volume rm <volume>  # Remove volume
docker volume create <volume>  # Recria limpo
```

## 💡 Próximos Passos

Após dominar estes desafios, considere explorar:

- **Kubernetes**: Orquestração de containers em produção
- **Docker Swarm**: Clustering nativo do Docker
- **CI/CD**: Integração e deploy contínuo com Docker
- **Monitoring**: Prometheus, Grafana
- **Logging**: ELK Stack, Fluentd
- **Security**: Scanning de imagens, secrets management
- **Multi-stage builds**: Otimização de imagens
- **Health checks**: Monitoramento de saúde dos containers

## 📄 Licença

Este projeto foi desenvolvido para fins educacionais.

## ✍️ Autor

Desenvolvido com foco em aprendizado prático de Docker e microsserviços.

---

**Dica**: Comece pelo Desafio 1 e vá progredindo sequencialmente. Cada desafio introduz novos conceitos que se baseiam nos anteriores!
