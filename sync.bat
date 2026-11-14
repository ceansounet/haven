@echo off
rem Synchronise le projet Haven avec GitHub (ceansounet/haven).
rem Double-clique dessus : enregistre tes changements, recupere ceux de GitHub, puis envoie le tout.
cd /d "%~dp0"

echo === Enregistrement des changements locaux ===
git add -A
git diff --cached --quiet || git commit -m "Sync %date% %time:~0,5%"

echo.
echo === Recuperation depuis GitHub ===
git pull --no-rebase --no-edit
if errorlevel 1 (
  echo.
  echo !! Conflit ou erreur pendant la recuperation. Rien n'a ete envoye.
  pause
  exit /b 1
)

echo.
echo === Envoi vers GitHub ===
git push
if errorlevel 1 (
  echo.
  echo !! L'envoi a echoue.
  pause
  exit /b 1
)

echo.
echo Synchronisation terminee.
timeout /t 3 >nul
