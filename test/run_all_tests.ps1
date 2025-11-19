
$errors = @()

function RunTest($path) {
    Write-Host "\n=== Executando testes em $path ==="
    Push-Location $path
    try {
        if (Test-Path .\test\run-*.ps1) {
            $script = Get-ChildItem .\test\run-*.ps1 | Select-Object -First 1
            Write-Host "Executando $($script.FullName)"
            & $script.FullName
        } else {
            Write-Host "Nenhum script de execução encontrado em $path/test"
        }
    } catch {
        Write-Host ("Erro durante os testes em {0}: {1}" -f $path, $_.ToString()) -ForegroundColor Red
        $global:errors += $path
    } finally {
        Pop-Location
    }
}

$roots = @("desafio1", "desafio3", "desafio4", "desafio5")
foreach ($r in $roots) { RunTest($r) }

if ($errors.Count -gt 0) {
    Write-Host "Alguns testes falharam em: $($errors -join ', ')" -ForegroundColor Red
    exit 1
} else {
    Write-Host "Todos os testes de smoke foram concluídos com sucesso." -ForegroundColor Green
}
