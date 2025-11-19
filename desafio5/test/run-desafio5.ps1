# Teste smoke do Desafio 5: API Gateway + users + orders
Write-Host "Execute no PowerShell dentro da pasta desafio5"

Write-Host "Iniciando stack do compose..."
docker-compose up --build -d

Start-Sleep -Seconds 5

Write-Host "Índice do Gateway"
Invoke-RestMethod -Uri http://localhost:8080/ -Method Get

Write-Host "Gateway -> /users"
Invoke-RestMethod -Uri http://localhost:8080/users -Method Get

Write-Host "Gateway -> /orders"
Invoke-RestMethod -Uri http://localhost:8080/orders -Method Get

Write-Host "Derrubando stack..."
docker-compose down --rmi local

Write-Host "Teste smoke do Desafio 5 concluído."
