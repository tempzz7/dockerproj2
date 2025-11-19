docker volume create db_desafio2_data
docker run -d --name desafio2-postgres `
docker exec -i desafio2-postgres psql -U demo_user -d desafio2db -c "CREATE TABLE IF NOT EXISTS people (id SERIAL PRIMARY KEY, name TEXT);"
docker exec -i desafio2-postgres psql -U demo_user -d desafio2db -c "INSERT INTO people (name) VALUES ('Alice');"
docker exec -i desafio2-postgres psql -U demo_user -d desafio2db -c "SELECT * FROM people;"
docker rm -f desafio2-postgres
docker run -d --name desafio2-postgres `
docker exec -i desafio2-postgres psql -U demo_user -d desafio2db -c "SELECT * FROM people;"
docker rm -f desafio2-postgres; docker volume rm db_desafio2_data

# Desafio 2 — Volumes e Persistência

Objetivo: Demonstrar persistência de dados usando volumes Docker com PostgreSQL.

Descrição e decisões técnicas:
- Usei uma imagem oficial `postgres:15` e um volume nomeado `db_desafio2_data` para armazenar os dados do banco em `/var/lib/postgresql/data`.
- O foco é provar que dados criados em um container persistem mesmo após removê-lo, desde que o volume seja reutilizado.

Passo-a-passo (PowerShell):

1) Criar volume e iniciar Postgres:

```powershell
docker volume create db_desafio2_data

docker run -d --name desafio2-postgres \
  -e POSTGRES_PASSWORD=example \
  -e POSTGRES_USER=demo_user \
  -e POSTGRES_DB=desafio2db \
  -v db_desafio2_data:/var/lib/postgresql/data \
  -p 5432:5432 \
  postgres:15
```

2) Criar tabela e inserir dados (executar comandos SQL dentro do container):

```powershell
docker exec -i desafio2-postgres psql -U demo_user -d desafio2db -c "CREATE TABLE IF NOT EXISTS pessoas (id SERIAL PRIMARY KEY, nome TEXT);"
docker exec -i desafio2-postgres psql -U demo_user -d desafio2db -c "INSERT INTO pessoas (nome) VALUES ('Alice');"
docker exec -i desafio2-postgres psql -U demo_user -d desafio2db -c "SELECT * FROM pessoas;"
```

3) Remover o container (o volume permanece):

```powershell
docker rm -f desafio2-postgres
```

4) Recriar o container ligando ao mesmo volume e verificar persistência:

```powershell
docker run -d --name desafio2-postgres \
  -e POSTGRES_PASSWORD=example \
  -e POSTGRES_USER=demo_user \
  -e POSTGRES_DB=desafio2db \
  -v db_desafio2_data:/var/lib/postgresql/data \
  -p 5432:5432 \
  postgres:15

docker exec -i desafio2-postgres psql -U demo_user -d desafio2db -c "SELECT * FROM pessoas;"
```

Observações e recomendações:
- O volume `db_desafio2_data` retém os arquivos do banco físico. Mesmo se o container for destruído, o volume mantém os dados.
- Para limpeza final (remova o volume se quiser apagar os dados):

```powershell
docker rm -f desafio2-postgres
docker volume rm db_desafio2_data
```
