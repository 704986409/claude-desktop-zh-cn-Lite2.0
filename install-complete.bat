@echo off
chcp 65001 >nul 2>&1
title Claude Desktop zh-CN complete (JSON + hardcoded, no runtime inject)
cd /d "%~dp0"

echo ======================================
echo   JSON + whitelist + hardcoded UI
echo   (no font/session runtime inject)
echo ======================================
echo.

taskkill /f /im claude.exe 2>nul
python pure_patch.py %*
if %errorlevel% neq 0 goto :fail
python enhance_zh_cn.py
if %errorlevel% neq 0 goto :fail
echo.
echo Done. Restart Claude Desktop.
pause
exit /b 0

:fail
echo FAILED. Close Claude completely and retry as Administrator.
pause
exit /b 1
