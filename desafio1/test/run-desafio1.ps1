# Smoke test for Desafio 1: networked containers
# Run from PowerShell in the desafio1 folder

$networkName = "mynet_desafio1"

Write-Host "Construindo imagens do servidor e do cliente..."
cd ..\server; docker build -t desafio1-server .; cd ..\client; docker build -t desafio1-client .; cd ..\


if (-not (docker network ls --filter name=^$networkName`$ --format "{{.Name}}")) {
    docker network create $networkName | Out-Null
    Write-Host "Rede $networkName criada"
} else {
    Write-Host "Rede $networkName já existe"
}


Write-Host "Iniciando servidor..."
docker run -d --name desafio1-server --network $networkName -p 8080:8080 desafio1-server | Out-Null
Start-Sleep -Seconds 2
Write-Host "Iniciando cliente..."
docker run -d --name desafio1-client --network $networkName desafio1-client | Out-Null

Write-Host "Aguardando 6 segundos para algumas requisições..."
Start-Sleep -Seconds 6

Write-Host "Resposta do servidor (curl):"
curl http://localhost:8080/

Write-Host "Logs do cliente:"
docker logs --tail 20 desafio1-client

Write-Host "Limpando..."
docker rm -f desafio1-client desafio1-server | Out-Null
Write-Host "Teste smoke do Desafio 1 concluído."
