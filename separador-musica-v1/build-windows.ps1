$ErrorActionPreference = 'Stop'
Set-Location $PSScriptRoot

if (-not (Get-Command py -ErrorAction SilentlyContinue)) {
    throw 'Python launcher (py) was not found. Install Python 3.11 or newer.'
}

py -3 -m venv .venv
& .\.venv\Scripts\python.exe -m pip install --upgrade pip
& .\.venv\Scripts\python.exe -m pip install -r requirements.txt
& .\.venv\Scripts\pyinstaller.exe --clean --noconfirm SeparadorMusica.spec

Write-Host ''
Write-Host 'BUILD TERMINADO' -ForegroundColor Green
Write-Host "EXE: $PSScriptRoot\dist\SeparadorMusica.exe"
