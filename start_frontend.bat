@echo off
REM ═══════════════════════════════════════════════════════════
REM  LVMH Client Analytics - Démarrage Rapide
REM  Ce script démarre automatiquement le frontend React
REM ═══════════════════════════════════════════════════════════

echo.
echo ╔═══════════════════════════════════════════════════════════╗
echo ║   LVMH Client Analytics - Démarrage Frontend React        ║
echo ╚═══════════════════════════════════════════════════════════╝
echo.

REM Vérifier si node_modules existe dans client/
if not exist "client\node_modules\" (
    echo [ATTENTION] Les dépendances ne sont pas installées !
    echo Installation en cours...
    echo.
    cd client
    call npm install
    cd ..
    echo.
    echo [OK] Installation terminée !
    echo.
)

echo [INFO] Démarrage du serveur React sur le port 3000...
echo.
echo ┌───────────────────────────────────────────────────────────┐
echo │  Une fois démarré, ouvrez votre navigateur :             │
echo │  http://localhost:3000                                    │
echo └───────────────────────────────────────────────────────────┘
echo.

cd client
npm start
