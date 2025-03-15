@echo off
REM Windows batch file to start the SidebarDashboard server

REM Get the directory where this script is located
set SCRIPT_DIR=%~dp0

REM Open browser to the server URL
start http://localhost:7531

REM Start the server
python "%SCRIPT_DIR%http_server_nocache.py"

pause
