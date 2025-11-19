# Script PowerShell para demonstrar persistência do Postgres usando volume
# Execute no PowerShell com privilégios adequados (usuário com permissão para Docker)

Write-Host "Criando volume 'db_desafio2_data'..."
docker volume create db_desafio2_data | Out-Null

Write-Host "Iniciando container Postgres..."
docker run -d --name desafio2-postgres -e POSTGRES_PASSWORD=example -e POSTGRES_USER=demo_user -e POSTGRES_DB=desafio2db -v db_desafio2_data:/var/lib/postgresql/data -p 5432:5432 postgres:15 | Out-Null

Start-Sleep -Seconds 5

Write-Host "Criando tabela e inserindo dados de exemplo..."
docker exec -i desafio2-postgres psql -U demo_user -d desafio2db -c "CREATE TABLE IF NOT EXISTS pessoas (id SERIAL PRIMARY KEY, nome TEXT);"
docker exec -i desafio2-postgres psql -U demo_user -d desafio2db -c "INSERT INTO pessoas (nome) VALUES ('Alice');"

Write-Host "Dados atuais:"
docker exec -i desafio2-postgres psql -U demo_user -d desafio2db -c "SELECT * FROM pessoas;"

Write-Host "Removendo container (o volume permanece intacto)..."
docker rm -f desafio2-postgres | Out-Null

Write-Host "Recriando container reutilizando o mesmo volume..."
docker run -d --name desafio2-postgres -e POSTGRES_PASSWORD=example -e POSTGRES_USER=demo_user -e POSTGRES_DB=desafio2db -v db_desafio2_data:/var/lib/postgresql/data -p 5432:5432 postgres:15 | Out-Null

Start-Sleep -Seconds 5

Write-Host "Verificando persistência dos dados:"
docker exec -i desafio2-postgres psql -U demo_user -d desafio2db -c "SELECT * FROM pessoas;"

Write-Host "Limpeza (opcional):"
Write-Host "  docker rm -f desafio2-postgres; docker volume rm db_desafio2_data"
