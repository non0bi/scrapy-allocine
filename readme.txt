#Allociné Data Explorer

Une application de visualisation de données cinématographiques moderne et interactive, construite avec Dash, MongoDB et Scrapy,
le tout orchestré par Docker.

#Aperçu
Ce projet permet d'explorer les films scrapés depuis Allociné à travers une interface fluide et esthétique. 
L'application synchronise en temps réel un tableau de données complet avec une galerie d'affiches dynamique,
tout en proposant des analyses statistiques sur les genres et les notes.


#Stack Technique 

-Frontend : Dash (Python framework)
-Composants UI : Dash Bootstrap Components
-Base de données : MongoDB
-Traitement de données : Pandas
-Visualisation : Plotly ExpressCollecte de données : Scrapy
-Orchestration : Docker & Docker-Compose

#Installation et Lancement

Prérequis: 

Docker Desktop installé et fonctionnel.

Déploiement rapide : 
-Cloner le répertoire.

-lancer le fichier : launcher.bat

#Fonctionnalités
-Tableau Dynamique : Tri, filtrage et pagination.
-Galerie Synchronisée : Les affiches affichées correspondent exactement aux lignes visibles dans le tableau.
-Statistiques Globales : Calcul en temps réel du nombre total de films et de la note moyenne globale affichés dans des cartes dédiées.
-Visualisations Interactives :Top 10 des genres les plus représentés.
-Répartition des films par note spectateurs.

#Structure du Projet dash_app/ # Application Dash pour la visualisation
│   ├── app.py           # Code principal de l'application Dash
│   ├── requirements.txt # Dépendances Python
│   └── Dockerfile       # Configuration Docker pour Dash
├── scrapy_app/          # Moteur de collecte de données (Scrapy)
├── docker-compose.yml   # Orchestration des services
└── README.md            # Documentation du projet

#Auteurs

-Grégoire Bouet
-Bernard Noah 
