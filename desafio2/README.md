# Desafio 2 — Persistência com Volumes

A ideia desse desafio era provar que volumes Docker realmente funcionam — que os dados sobrevivem mesmo quando você destroi o container.

## O que eu fiz

Usei PostgreSQL porque banco de dados é o caso clássico onde você precisa garantir que os dados não vão sumir. O setup é assim:

- Container rodando Postgres 15
- Um volume chamado `db_desafio2_data` montado no caminho onde o Postgres guarda seus arquivos
- Criei uma tabela, inseri dados, matei o container e subi de novo pra ver se os dados continuavam lá

## Por que volumes?

Sem volumes, tudo que você cria dentro de um container some quando ele morre. Com volumes, você tem um espaço no host que persiste independente do ciclo de vida do container.

A parte boa é que o volume fica separado — você pode destruir e recriar o container quantas vezes quiser, os dados ficam seguros no volume.

## Como testar

Tem um script PowerShell que automatiza o teste, mas vou explicar os passos pra ficar claro:

### 1. Criar o volume e subir o Postgres

```powershell
docker volume create db_desafio2_data

docker run -d --name desafio2-postgres `
  -e POSTGRES_PASSWORD=example `
  -e POSTGRES_USER=demo_user `
  -e POSTGRES_DB=desafio2db `
  -v db_desafio2_data:/var/lib/postgresql/data `
  -p 5432:5432 `
  postgres:15
```

### 2. Colocar dados no banco

```powershell
docker exec -i desafio2-postgres psql -U demo_user -d desafio2db -c "CREATE TABLE IF NOT EXISTS pessoas (id SERIAL PRIMARY KEY, nome TEXT);"
docker exec -i desafio2-postgres psql -U demo_user -d desafio2db -c "INSERT INTO pessoas (nome) VALUES ('Alice');"
docker exec -i desafio2-postgres psql -U demo_user -d desafio2db -c "SELECT * FROM pessoas;"
```

Aqui você vê a Alice aparecendo na consulta.

### 3. Destruir o container

```powershell
docker rm -f desafio2-postgres
```

Container morto. Mas o volume continua lá.

### 4. Subir de novo e verificar

```powershell
docker run -d --name desafio2-postgres `
  -e POSTGRES_PASSWORD=example `
  -e POSTGRES_USER=demo_user `
  -e POSTGRES_DB=desafio2db `
  -v db_desafio2_data:/var/lib/postgresql/data `
  -p 5432:5432 `
  postgres:15

docker exec -i desafio2-postgres psql -U demo_user -d desafio2db -c "SELECT * FROM pessoas;"
```

A Alice ainda tá lá. É isso que volumes fazem.

## Script automatizado

Se preferir não rodar comando por comando:

```powershell
cd .\desafio2
.\demo-persist.ps1
```

Esse script faz tudo automaticamente e vai mostrando o que tá acontecendo em cada etapa.

## Limpeza

Quando terminar de testar:

```powershell
docker rm -f desafio2-postgres
docker volume rm db_desafio2_data
```

## O que ficou claro

Antes de fazer isso, volumes eram meio abstratos pra mim. Depois de ver os dados persistindo mesmo destruindo o container, ficou bem mais concreto. É tipo ter um HD externo que você pode plugar em diferentes containers.

Também entendi melhor o caminho `/var/lib/postgresql/data` — é onde o Postgres joga todos os arquivos do banco. Apontar o volume pra esse caminho é o que garante a persistência.
