@echo off
REM ═══════════════════════════════════════════════════════════
REM  LVMH Client Analytics - Démarrage Complet
REM  Ce script démarre le backend ET le frontend
REM ═══════════════════════════════════════════════════════════

echo.
echo ╔═══════════════════════════════════════════════════════════╗
echo ║   LVMH Client Analytics - Démarrage Complet              ║
echo ╚═══════════════════════════════════════════════════════════╝
echo.

REM Vérifier les dépendances du backend
if not exist "node_modules\" (
    echo [ATTENTION] Dépendances backend manquantes !
    echo Installation en cours...
    call npm install
    echo [OK] Backend installé !
    echo.
)

REM Vérifier les dépendances du frontend
if not exist "client\node_modules\" (
    echo [ATTENTION] Dépendances frontend manquantes !
    echo Installation en cours...
    cd client
    call npm install
    cd ..
    echo [OK] Frontend installé !
    echo.
)

echo ┌───────────────────────────────────────────────────────────┐
echo │  Démarrage des serveurs :                                │
echo │  - Backend API : http://localhost:5001                   │
echo │  - Frontend React : http://localhost:3000                │
echo └───────────────────────────────────────────────────────────┘
echo.
echo [INFO] Démarrage du backend...
echo.

REM Démarrer le backend en arrière-plan
start "LVMH Backend (Port 5001)" cmd /k "npm run dev"

REM Attendre 3 secondes
timeout /t 3 /nobreak >nul

echo [INFO] Démarrage du frontend...
echo.

REM Démarrer le frontend
start "LVMH Frontend (Port 3000)" cmd /k "cd client && npm start"

echo.
echo ╔═══════════════════════════════════════════════════════════╗
echo ║  ✅ Les deux serveurs sont en cours de démarrage !        ║
echo ║                                                           ║
echo ║  Ouvrez votre navigateur sur :                           ║
echo ║  http://localhost:3000                                    ║
echo ╚═══════════════════════════════════════════════════════════╝
echo.
echo Appuyez sur une touche pour fermer cette fenêtre...
pause >nul
