@echo off
title LVMH Client Pulse - Launcher

echo ===================================================
echo   LVMH CLIENT PULSE - DEMARRAGE AUTOMATIQUE
echo ===================================================
echo.
echo 1. Verification de l'installation...
if not exist "node_modules" (
    echo [INFO] Premier lancement detecte. Installation des dependances serveur...
    call npm install
)

if not exist "client\node_modules" (
    echo [INFO] Installation des dependances client...
    cd client
    call npm install
    cd ..
)

echo.
echo 2. Lancement du Cerveau (Backend)...
start "LVMH Backend (Port 5001)" npm start

echo.
echo 3. Lancement de l'Interface (Frontend)...
start "LVMH Frontend (Port 3000)" npm run client

echo.
echo ===================================================
echo   TOUT EST LANCE ! 🚀
echo ===================================================
echo.
echo - Backend : http://localhost:5001
echo - Frontend : http://localhost:3000
echo.
echo Ne fermez pas les fenetres noires qui se sont ouvertes.
echo.
pause
