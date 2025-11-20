# Desafio 1 — Containers em Rede

## Descrição da Solução

Este desafio demonstra a comunicação entre containers Docker usando uma rede customizada. A implementação consiste em dois componentes principais:

**Servidor Web (Flask)**: Um servidor HTTP simples que responde com informações em JSON, incluindo o horário da requisição e o IP do cliente que fez a chamada.

**Cliente (Alpine + curl)**: Um container leve que executa requisições HTTP periódicas ao servidor, simulando um consumidor de API em tempo real.

## Arquitetura e Decisões Técnicas

A arquitetura escolhida foi intenciona lmente simples para focar no conceito principal: **comunicação entre containers via rede Docker**.

### Componentes:

1. **Rede Docker Customizada** (`mynet_desafio1`)
   - Permite que os containers se comuniquem usando seus nomes como hostnames
   - Isolamento da comunicação dos outros containers do sistema
   - Suporte nativo a resolução DNS interna do Docker

2. **Servidor Flask**
   - Linguagem: Python 3.11
   - Framework: Flask (leve e direto ao ponto)
   - Porta exposta: 8080
   - Retorna JSON com timestamp e IP do cliente

3. **Cliente Curl**
   - Base: Alpine Linux (imagem minimalista)
   - Script bash fazendo requisições em loop a cada 5 segundos
   - Exibe logs de todas as interações

### Por que essas escolhas?

- **Flask**: Framework minimalista, perfeito para APIs simples
- **Alpine**: Imagem base extremamente leve (~5MB), ideal para containers que executam tarefas simples
- **Rede customizada**: Demonstra como o Docker facilita a comunicação entre serviços sem configuração complexa

## Funcionamento

O fluxo de comunicação funciona assim:

1. Ambos os containers são conectados à mesma rede Docker (`mynet_desafio1`)
2. O servidor Flask inicia e fica escutando na porta 8080
3. O cliente faz requisições periódicas usando o hostname `desafio1-server` (nome do container do servidor)
4. O DNS interno do Docker resolve `desafio1-server` para o IP interno do container servidor
5. O servidor processa e responde com um JSON contendo o horário e IP do cliente
6. O cliente exibe a resposta nos logs

```
Cliente  ────[HTTP GET]────>  Servidor Flask
         <───[JSON response]──
```

## Instruções de Execução

### Passo 1: Criar a rede Docker

```bash
docker network create mynet_desafio1
```

### Passo 2: Construir as imagens

```bash
cd desafio1/server
docker build -t desafio1-server .

cd ../client
docker build -t desafio1-client .
cd ..
```

### Passo 3: Executar os containers

```bash
docker run -d \
  --name desafio1-server \
  --network mynet_desafio1 \
  -p 8080:8080 \
  desafio1-server

docker run -d \
  --name desafio1-client \
  --network mynet_desafio1 \
  desafio1-client
```

### Passo 4: Visualizar a comunicação

Acompanhe os logs do cliente (que faz as requisições):

```bash
docker logs -f desafio1-client
```

Em outro terminal, veja os logs do servidor:

```bash
docker logs -f desafio1-server
```

Você também pode testar diretamente do seu navegador ou terminal:

```bash
curl http://localhost:8080
```

### Passo 5: Limpeza

Para remover tudo:

```bash
docker rm -f desafio1-client desafio1-server
docker network rm mynet_desafio1
```

## Testando a Comunicação

Ao executar os containers, você verá saídas como:

**Cliente:**
```
[2025-11-20 15:30:01] Fazendo requisição para http://desafio1-server:8080/
Resposta recebida: {"horario":"2025-11-20T15:30:01.234Z","ip_cliente":"172.18.0.3","mensagem":"Servidor do Desafio 1 respondendo"}
```

**Servidor:**
```
172.18.0.2 - - [20/Nov/2025 15:30:01] "GET / HTTP/1.1" 200 -
```

Isso comprova que:
- O cliente consegue resolver o nome `desafio1-server`
- A comunicação HTTP está funcionando
- O servidor identifica o IP interno do cliente na rede Docker

## Estrutura de Arquivos

```
desafio1/
├── README.md
├── server/
│   ├── Dockerfile
│   ├── app.py
│   └── requirements.txt
└── client/
    ├── Dockerfile
    └── curl-loop.sh
```
