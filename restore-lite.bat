@echo off
chcp 65001 >nul 2>&1
title Restore Claude Desktop English (Lite)
cd /d "%~dp0"
taskkill /f /im claude.exe 2>nul
python pure_patch.py --restore
echo.
pause
