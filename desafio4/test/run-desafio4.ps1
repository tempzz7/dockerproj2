Write-Host "Teste smoke do Desafio 4: dois microsserviços independentes"
Write-Host "Execute no PowerShell dentro da pasta desafio4"

Write-Host "Iniciando serviços via docker-compose..."
docker-compose up --build -d

Start-Sleep -Seconds 4

Write-Host "GET /users do serviço A"
Invoke-RestMethod -Uri http://localhost:8000/users -Method Get

Write-Host "GET /combined do serviço B"
Invoke-RestMethod -Uri http://localhost:8001/combined -Method Get

Write-Host "Finalizando serviços..."
docker-compose down --rmi local

Write-Host "Teste smoke do Desafio 4 concluído."
