@echo off
setlocal enabledelayedexpansion

REM ═══════════════════════════════════════════════════════════
REM  LVMH Client Analytics - Démarrage Réseau
REM  Permet l'accès depuis d'autres appareils (Tablette, Mobile)
REM ═══════════════════════════════════════════════════════════

echo.
echo ╔═══════════════════════════════════════════════════════════╗
echo ║   LVMH Client Analytics - ACCES RESEAU LOCAL             ║
echo ╚═══════════════════════════════════════════════════════════╝
echo.

REM Récupération de l'adresse IP locale
set IP=
for /f "tokens=2 delims=:" %%a in ('ipconfig ^| findstr /R /C:"Adresse IPv4"') do (
    set temp_ip=%%a
    set temp_ip=!temp_ip:^ =!
    REM On prend la première IP qui n'est pas 127.0.0.1 si possible
    if "!IP!"=="" set IP=!temp_ip!
)

if "%IP%"=="" (
    set IP=127.0.0.1
    echo [ERREUR] Impossible de trouver l'adresse IP locale.
) else (
    echo [OK] Adresse IP locale detectee : %IP%
)

echo.
echo ┌───────────────────────────────────────────────────────────┐
echo │  LIENS POUR VOS APPAREILS :                              │
echo │                                                           │
echo │  Frontend React : http://%IP%:3000                     │
echo │  Backend API :    http://%IP%:5001                     │
echo │  Streamlit App :  http://%IP%:8503                     │
echo │                                                           │
echo │  (Assurez-vous d'etre sur le MEME reseau Wi-Fi)           │
echo └───────────────────────────────────────────────────────────┘
echo.

echo [INFO] Mise a jour du proxy frontend pour l'IP %IP%...
REM Modification temporaire du proxy dans package.json pour le réseau
powershell -Command "(Get-Content client/package.json) -replace '\"proxy\": \".*\"', '\"proxy\": \"http://%IP%:5001\"' | Set-Content client/package.json"

echo [INFO] Demarrage du Backend sur %IP%:5001...
start "LVMH Backend" cmd /k "npm run dev"

echo [INFO] Attente du backend...
timeout /t 3 /nobreak >nul

echo [INFO] Demarrage du Frontend React sur 0.0.0.0 (Accessible via %IP%:3000)...
cd client
set HOST=0.0.0.0
start "LVMH Frontend" cmd /k "npm start"
cd ..

echo [INFO] Demarrage de Streamlit sur %IP%:8503...
start "LVMH Streamlit" cmd /k ".\.venv\Scripts\python -m streamlit run app.py --server.address 0.0.0.0 --server.port 8503"

echo.
echo ✅ TOUS LES SERVICES SONT EN COURS DE LANCEMENT !
echo.
echo IMPORTANT : Si le site s'affiche mais ne charge pas les donnees,
echo verifiez que votre pare-feu Windows autorise Node.js et React.
echo.
echo Utilisez ce lien sur votre mobile/tablette : http://%IP%:3000
echo.
pause
