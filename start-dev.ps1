# Basey Fare Guide - Start Development Servers
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Basey Fare Guide - Starting Servers" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

$projectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $projectRoot

Write-Host "[1/2] Starting Django Backend..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$projectRoot'; .\BFG-env\Scripts\Activate.ps1; python manage.py runserver"

Start-Sleep -Seconds 3

Write-Host "[2/2] Starting React Frontend..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$projectRoot\frontend'; npm start"

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "Servers are starting!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "Django Backend: " -NoNewline; Write-Host "http://localhost:8000" -ForegroundColor Blue
Write-Host "React Frontend: " -NoNewline; Write-Host "http://localhost:3000" -ForegroundColor Blue
Write-Host "Django Admin:   " -NoNewline; Write-Host "http://localhost:8000/admin" -ForegroundColor Blue
Write-Host ""
Write-Host "Press any key to exit this window..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
