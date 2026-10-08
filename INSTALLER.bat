@echo off
cd /d "%~dp0"
call npm install
if errorlevel 1 goto end
echo Installation terminee. Lancez DEMARRER.bat
:end
pause
