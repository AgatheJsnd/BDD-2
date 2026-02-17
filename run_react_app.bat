@echo off
echo ==========================================
echo   Lancement de LVMH Client Analytics (React)
echo ==========================================
echo.

echo 1. Demarrage du Cerveau (Backend Node.js)...
start "LVMH Backend" cmd /k "cd server && node index.js"

echo.
echo Attente du demarrage du serveur (5s)...
timeout /t 5 /nobreak >nul

echo.
echo 2. Demarrage de l'Interface (Frontend React)...
cd client
start "LVMH Frontend" cmd /k "npm start"

echo.
echo ==========================================
echo   Lancement termine !
echo   Backend : http://localhost:5001
echo   Frontend : http://localhost:3000
echo ==========================================
pause
