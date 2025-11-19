# Smoke test for Desafio 5: API Gateway + users + orders
# Run from PowerShell in the desafio5 folder

Write-Host "Starting compose stack..."
docker-compose up --build -d

Start-Sleep -Seconds 5

Write-Host "Gateway index"
Invoke-RestMethod -Uri http://localhost:8080/ -Method Get

Write-Host "Gateway -> /users"
Invoke-RestMethod -Uri http://localhost:8080/users -Method Get

Write-Host "Gateway -> /orders"
Invoke-RestMethod -Uri http://localhost:8080/orders -Method Get

Write-Host "Bringing down stack..."
docker-compose down --rmi local

Write-Host "Desafio 5 smoke test completed."
