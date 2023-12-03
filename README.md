# JobFinder

Ce projet a pour but d'offrir à un utilisateur la possibilité de chercher des métiers à partir d'une situation désirée basée sur des critères de salaire ou de localisation du métier en question. Notre base de données utilisée est la suivante :

Lien dataset : https://www.kaggle.com/datasets/willianoliveiragibin/data-jobs-salaries

## Utilisation

Pour lancer notre projet, voilà les démarches à suivre :

1) Télécharger le repo en local

2) Dans un terminal, se placer à la racine du projet

3) Exécuter les commandes suivantes :

```
docker compose build
docker compose up
```
4) Une fois les conteneurs créés dans Docker, on l'ouvre et on accès à l'API. On peut alors utiliser l'application normalement.

## Construction du projet

### Packages

Ce projet a été réalisé en utilisant les frameworks FastAPI, Minio, et SQLAlchemy. Ces outils nous ont permis de faire un backend complet.

### Arborescence du projet

L'arborescence de ce projet se base sur la séparation de toutes les parties de notre application dans des dossiers distincts. Ainsi, notre fichier main.py appellent simplement les routes permettant de naviguer à travers notre application.

## Objectifs :

- Créer une interface utilisateur
- Créer page d'accueil avec les différents paramètres de jobs
- Proposer les critères salaire, pays, remote ratio (à compléter)
- Proposer un job selon les critères choisis
- Proposer des courbes selon les critères choisis
- Webscrapper les offres de métier sur le web (optionnel)

## Mise en place

## Base de données

## Sécurité (optionnel)

Créé par Y.Lakhdari, V.Gerard, Y.Tissot.
