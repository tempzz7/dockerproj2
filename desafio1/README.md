# Desafio 1 — Comunicação entre Containers

O objetivo aqui era fazer dois containers conversarem usando uma rede Docker customizada.

## Como funciona

Criei um setup bem direto:
- Um container roda um servidor Flask que responde requisições HTTP
- Outro container fica fazendo requisições pro servidor de tempos em tempos
- Os dois estão na mesma rede Docker, então conseguem se achar pelo nome

### Por que fiz assim

Escolhi Flask pro servidor porque é leve e fácil de entender — só responde com um JSON contendo a hora atual e o IP de quem fez a requisição. Nada muito elaborado.

O cliente é só um container Alpine com curl instalado, rodando um loop que faz requisições a cada 5 segundos. Dá pra ver claramente nos logs as mensagens indo e voltando.

A parte importante é a rede customizada (`mynet_desafio1`). Quando você coloca containers na mesma rede assim, o Docker cuida da resolução de nomes automaticamente — ou seja, o cliente consegue acessar o servidor só usando o nome `desafio1-server` ao invés de ter que descobrir o IP.

## Como rodar

### 1. Criar a rede

```powershell
docker network create mynet_desafio1
```

### 2. Buildar as imagens

```powershell
cd .\desafio1\server
docker build -t desafio1-server .
cd ..\client
docker build -t desafio1-client .
cd ..\..
```

### 3. Subir os containers

```powershell
# Servidor primeiro
docker run -d --name desafio1-server --network mynet_desafio1 -p 8080:8080 desafio1-server

# Depois o cliente
docker run -d --name desafio1-client --network mynet_desafio1 desafio1-client
```

### 4. Ver a comunicação acontecendo

Abre os logs dos containers pra ver as mensagens:

```powershell
docker logs -f desafio1-client
```

Ou do servidor:

```powershell
docker logs -f desafio1-server
```

Você vai ver o cliente fazendo requests e o servidor respondendo. É bem satisfatório de acompanhar.

## Limpando tudo depois

```powershell
docker rm -f desafio1-client desafio1-server
docker network rm mynet_desafio1
```

## O que aprendi fazendo isso

A parte mais legal foi entender na prática como a rede Docker funciona. Sem ela, os containers ficariam isolados ou você teria que ficar descobrindo IPs manualmente. Com a rede customizada, é só dar um nome pros containers e eles se encontram.

Também ficou claro como os logs são úteis pra debugar — dá pra ver exatamente o que tá passando entre os containers.
