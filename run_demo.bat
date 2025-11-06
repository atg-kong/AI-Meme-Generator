@echo off
REM AI Meme Generator - Demo Launcher Script (Windows)
REM Double-click this file to run the demo

title AI Meme Generator - Demo
color 0A

echo ========================================
echo   AI Meme Generator - Demo Launcher
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ from python.org
    echo.
    pause
    exit /b 1
)

REM Run the demo launcher
python demo_launcher.py

REM Keep window open
if errorlevel 1 (
    echo.
    echo Press any key to exit...
    pause >nul
)
