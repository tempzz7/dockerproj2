docker network create mynet_desafio1
docker run -d --name desafio1-server --network mynet_desafio1 -p 8080:8080 desafio1-server
docker run -d --name desafio1-client --network mynet_desafio1 desafio1-client
docker logs -f desafio1-client
docker logs -f desafio1-server
docker rm -f desafio1-client desafio1-server; docker network rm mynet_desafio1

# Desafio 1 — Containers em Rede

Objetivo: Demonstrar comunicação entre dois containers conectados por uma rede Docker personalizada.

Visão geral e escolhas técnicas:
- O servidor é um app Flask simples que responde em JSON com hora e IP do cliente.
- O cliente é um container Alpine que executa um script em loop usando `curl` para consultar o servidor.
- Usei uma rede Docker nomeada `mynet_desafio1` para demonstrar resolução de nomes entre containers.

Passo a passo (PowerShell):

1) Criar a rede:

```powershell
docker network create mynet_desafio1
```

2) Construir as imagens:

```powershell
Set-Location .\desafio1\server
docker build -t desafio1-server .
Set-Location ..\client
docker build -t desafio1-client .
Set-Location ..\..
```

3) Executar os containers conectados à rede:

```powershell
# iniciar servidor
docker run -d --name desafio1-server --network mynet_desafio1 -p 8080:8080 desafio1-server

# iniciar cliente (ele resolve 'server' pelo nome do container)
docker run -d --name desafio1-client --network mynet_desafio1 desafio1-client
```

4) Observar logs e comunicação:

```powershell
docker logs -f desafio1-client
# em outra janela
docker logs -f desafio1-server
```

Explicação do fluxo:
- O cliente faz requisições a cada 5 segundos e imprime a resposta JSON do servidor. Isso demonstra: criação de rede customizada, resolução de nomes (hostname `server`), e comunicação HTTP entre containers.

Limpeza rápida:

```powershell
docker rm -f desafio1-client desafio1-server
docker network rm mynet_desafio1
```

Observação sobre originalidade: o exemplo é intencionalmente simples, com foco em demonstrar explicitamente como a rede docker conecta containers e como inspecionar logs para comprovar a comunicação.

