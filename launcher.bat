@echo off
title Lancement Projet Allocine
echo ===========================================
echo   Demarrage de Docker (Mongo, App, Scraper)
echo ===========================================

:: Lance tous les services en arriere-plan
docker-compose up -d

echo.
echo [+] Les services demarrent...
echo [+] Le scraper remplit la base de donnees.
echo [+] Ouverture du site dans 10 secondes...

:: Attente pour laisser le temps au site de charger
timeout /t 10 /nobreak > nul

:: Ouvre le navigateur
start http://localhost:8050

echo.
echo ===========================================
echo   C'est pret ! (Ne ferme pas Docker Desktop)
echo ===========================================
pause