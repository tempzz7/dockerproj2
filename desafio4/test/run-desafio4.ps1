# Smoke test for Desafio 4: two independent microservices
# Run from PowerShell in the desafio4 folder

Write-Host "Starting services via docker-compose..."
docker-compose up --build -d

Start-Sleep -Seconds 4

Write-Host "GET /users from service A"
Invoke-RestMethod -Uri http://localhost:8000/users -Method Get

Write-Host "GET /combined from service B"
Invoke-RestMethod -Uri http://localhost:8001/combined -Method Get

Write-Host "Tearing down services..."
docker-compose down --rmi local

Write-Host "Desafio 4 smoke test completed."
