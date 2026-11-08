# PowerShell Script khởi chạy Enigma Admin Portal kết nối Supabase
Write-Host "========================================================" -ForegroundColor Cyan
Write-Host "   KHỞI CHẠY ENIGMA ADMIN PORTAL & SUPABASE BACKEND (8000)" -ForegroundColor Green
Write-Host "========================================================" -ForegroundColor Cyan
Write-Host ""
$adminUrl = "http://localhost:8000/admin-portal/"
Write-Host "1. Kết nối cơ sở dữ liệu Supabase PostgreSQL..." -ForegroundColor Yellow
Write-Host "2. Đang mở trình duyệt tại: $adminUrl" -ForegroundColor Green
Start-Process $adminUrl

Set-Location "$PSScriptRoot\backend"
if (Test-Path "venv\Scripts\python.exe") {
    & ".\venv\Scripts\python.exe" -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
} else {
    python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
}
