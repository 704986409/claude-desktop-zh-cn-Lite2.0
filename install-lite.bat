@echo off
chcp 65001 >nul 2>&1
title Claude Desktop zh-CN Lite (JSON, no runtime inject)
cd /d "%~dp0"

echo ======================================
echo   Claude Desktop zh-CN Lite
echo   JSON + whitelist, no chunk inject
echo ======================================
echo.

echo [*] Stopping Claude Desktop...
taskkill /f /im claude.exe 2>nul
echo.

python pure_patch.py %*
if %errorlevel% neq 0 (
    echo PATCH FAILED. Try Run as Administrator.
    pause
    exit /b 1
)

python enhance_zh_cn.py --skip-hardcoded
if %errorlevel% neq 0 (
    echo ENHANCE copy failed.
    pause
    exit /b 1
)

echo.
echo Done. Restart Claude Desktop.
echo Full original installer: claude-zh-cn.bat
echo Restore: restore-lite.bat
pause
