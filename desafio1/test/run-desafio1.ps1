# Smoke test for Desafio 1: networked containers
# Run from PowerShell in the desafio1 folder

$networkName = "mynet_desafio1"

Write-Host "Building server and client images..."
cd ..\server; docker build -t desafio1-server .; cd ..\client; docker build -t desafio1-client .; cd ..\

# Create network if not exists
if (-not (docker network ls --filter name=^$networkName`$ --format "{{.Name}}")) {
    docker network create $networkName | Out-Null
    Write-Host "Created network $networkName"
} else {
    Write-Host "Network $networkName already exists"
}

# Run server and client
Write-Host "Starting server..."
docker run -d --name desafio1-server --network $networkName -p 8080:8080 desafio1-server | Out-Null
Start-Sleep -Seconds 2
Write-Host "Starting client..."
docker run -d --name desafio1-client --network $networkName desafio1-client | Out-Null

Write-Host "Waiting 6 seconds for a few requests..."
Start-Sleep -Seconds 6

Write-Host "Server response (curl):"
curl http://localhost:8080/

Write-Host "Client logs:"
docker logs --tail 20 desafio1-client

Write-Host "Cleaning up..."
docker rm -f desafio1-client desafio1-server | Out-Null
# Note: do not remove network automatically to let user inspect if needed
Write-Host "Desafio 1 smoke test completed."
