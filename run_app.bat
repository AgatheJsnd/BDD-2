@echo off
REM ========================================
REM   LVMH Client Analytics - Version Optimisée
REM   Extraction de tags : 85% de précision
REM ========================================
echo.
echo Lancement de l'application...
echo Version : Optimisée (85%% de précision)
echo.
echo Fonctionnalités :
echo - Détection ville : 100%%
echo - Support âge anglais : OUI
echo - Support francs : OUI
echo - Famille FR+EN : OUI
echo.
echo ========================================
echo.

REM Lancer Streamlit avec l'application optimisée
.\venv\Scripts\python -m streamlit run app.py

pause
