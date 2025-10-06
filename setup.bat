@echo off
REM ================================
REM Setup Python environment script
REM ================================

echo [1/3] Checking Python installation...
python --version >nul 2>&1
IF ERRORLEVEL 1 (
    echo Python not found! Please install Python 3.x first.
    pause
    exit /b 1
)

echo [2/3] Upgrading pip...
python -m pip install --upgrade pip

echo [3/3] Installing requirements from requirements.txt...
IF EXIST requirements.txt (
    pip install -r requirements.txt --break-system-packages
) ELSE (
    echo requirements.txt not found in current directory!
    pause
    exit /b 1
)

echo.
echo ================================
echo Environment setup completed!
echo ================================
pause
