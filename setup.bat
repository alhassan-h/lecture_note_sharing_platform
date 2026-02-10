@echo off
REM Lecture Note Sharing Platform (LNSP) — Automated Setup Script (Windows)
REM This script sets up the development environment for both SQLite and MySQL.
REM Usage: setup.bat

setlocal enabledelayedexpansion
set "script_dir=%~dp0"
cd /d "%script_dir%"

echo.
echo ==========================================
echo LNSP Setup - Automated Environment Config
echo ==========================================
echo.

REM Step 1: Create .env from .env.example if it doesn't exist
echo 📋 Step 1: Creating .env file...
if exist .env (
    echo    ✓ .env already exists - skipping
) else (
    copy .env.example .env >nul 2>&1
    echo    ✓ .env created from .env.example
    echo    ⚠️  Please edit .env with your database credentials if using MySQL
)
echo.

REM Step 2: Create virtual environment
echo 🐍 Step 2: Creating Python virtual environment...
if exist venv (
    echo    ✓ venv already exists - skipping
) else (
    python -m venv venv
    if !errorlevel! neq 0 (
        echo    ✗ Failed to create venv. Ensure Python is installed.
        pause
        exit /b 1
    )
    echo    ✓ venv created
)
echo.

REM Step 3: Activate virtual environment
echo 🔌 Step 3: Activating virtual environment...
call venv\Scripts\activate.bat
if !errorlevel! neq 0 (
    echo    ✗ Failed to activate venv.
    pause
    exit /b 1
)
echo    ✓ venv activated
echo.

REM Step 4: Install dependencies
echo 📦 Step 4: Installing dependencies from requirements.txt...
python -m pip install --upgrade pip >nul 2>&1
pip install -r requirements.txt >nul 2>&1
if !errorlevel! neq 0 (
    echo    ✗ Failed to install dependencies.
    pause
    exit /b 1
)
echo    ✓ Dependencies installed
echo.

REM Step 5: Initialize database
echo 🗄️  Step 5: Initializing database...
python init_db.py
if !errorlevel! neq 0 (
    echo    ✗ Failed to initialize database.
    pause
    exit /b 1
)
echo    ✓ Database initialized
echo.

REM Step 6: Display next steps
echo ==========================================
echo ✅ Setup Complete!
echo ==========================================
echo.
echo Next steps:
echo   1. Activate venv (if not already active^):
echo      venv\Scripts\activate
echo.
echo   2. Run the app:
echo      python run.py
echo.
echo   3. Open browser and navigate to:
echo      http://localhost:5000
echo.
echo To switch databases, edit .env and change DB_CONNECTION:
echo   - DB_CONNECTION=sqlite  (default^)
echo   - DB_CONNECTION=mysql   (requires MySQL credentials in DATABASE_URL^)
echo.
echo ==========================================
echo.
pause