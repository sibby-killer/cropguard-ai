@echo off
echo 🌱 CropGuard AI - Quick Start
echo ================================

echo 📝 Step 1: Starting Backend Server...
echo.
start "Backend Server" cmd /k "cd /d %~dp0 && python run_backend.py"

timeout /t 3 /nobreak

echo 🌐 Step 2: Opening Web Interface...
echo.

REM Try to open the local development file
if exist "%~dp0web\local-dev.html" (
    start "" "%~dp0web\local-dev.html"
    echo ✅ Opened local-dev.html
) else (
    REM Fallback to creating a simple test page
    echo Creating test page...
    mkdir web 2>nul
    echo ^<!DOCTYPE html^>^<html^>^<head^>^<title^>Test^</title^>^</head^>^<body^>^<h1^>Backend is running!^</h1^>^<p^>Test URL: ^<a href="http://localhost:8000/api/health"^>http://localhost:8000/api/health^</a^>^</p^>^</body^>^</html^> > web\test.html
    start "" "web\test.html"
)

echo.
echo 📋 What's Running:
echo    Backend API: http://localhost:8000
echo    Health Check: http://localhost:8000/api/health
echo    Disease Detection: http://localhost:8000/api/detect
echo.
echo 🧪 How to Test:
echo    1. Wait for backend server to load completely
echo    2. Use the web interface to upload JPEG images
echo    3. Try custom plant names like 'Mango' or 'Spinach'
echo    4. Click Analyze Disease
echo.
echo 🛑 To stop: Close the backend server window
echo ❓ Problems? Check if Python is installed and run: python --version
pause