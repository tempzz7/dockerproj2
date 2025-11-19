# Top-level runner to execute all smoke tests in sequence
# Run from repo root: .\test\run_all_tests.ps1

$errors = @()

function RunTest($path) {
    Write-Host "\n=== Running tests in $path ==="
    Push-Location $path
    try {
        if (Test-Path .\test\run-*.ps1) {
            $script = Get-ChildItem .\test\run-*.ps1 | Select-Object -First 1
            Write-Host "Executing $($script.FullName)"
            & $script.FullName
        } else {
            Write-Host "No run script found in $path/test"
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
    Write-Host "Some tests failed in: $($errors -join ', ')" -ForegroundColor Red
    exit 1
} else {
    Write-Host "All smoke tests completed successfully." -ForegroundColor Green
}
