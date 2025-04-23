@echo off
echo =====================================
echo  Civil AI GUI Launcher (Windows)
echo =====================================

:: Check if Python is installed
python --version >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Python is not installed or not in PATH.
    echo Please install Python 3.10+ from https://www.python.org/downloads/
    pause
    exit /b
)

:: Ensure pip is available
python -m ensurepip >nul 2>&1

:: Install required packages
echo Installing Python dependencies...
pip install --upgrade pip >nul 2>&1
pip install -r requirements.txt

:: Launch the GUI
echo Launching Civil AI App...
python main.py

pause
