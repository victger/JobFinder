# JobFinder

Ce projet a pour but d'offrir à un utilisateur la possibilité de chercher des métiers à partir d'une situation désirée basée sur des critères de salaire ou de localisation du métier en question. Notre base de données utilisée est la suivante :

Lien dataset : https://www.kaggle.com/datasets/willianoliveiragibin/data-jobs-salaries

## Utilisation

Pour lancer notre projet, voilà les démarches à suivre :

1. Télécharger le repo en local

2. Dans un terminal, se placer à la racine du projet

3. Exécuter les commandes suivantes :

```
docker compose build
docker compose up
```

4. Une fois les conteneurs créés dans Docker, on l'ouvre et on accès à l'API. On peut alors utiliser l'application normalement.

## Construction du projet

### Packages

Ce projet a été réalisé en utilisant les frameworks FastAPI, Minio, et SQLAlchemy. Ces outils nous ont permis de faire un backend complet.

### Arborescence du projet

L'arborescence de ce projet se base sur la séparation de toutes les parties de notre application dans des dossiers distincts. Ainsi, notre fichier main.py appellent simplement les routes permettant de naviguer à travers notre application.

## Fonctionnalités réalisées

Diverses fonctionnalités ont été réalisées dans le cadre du développement de ce projet :

- L'authentification dans la partie user. Elle se fait via la génération de tokens, du hachage, et de l'insertion dans notre base de données. Par la suite, diverses fonctions ont été élaborées pour assurer l'authentification sur l'application.
- L'utilisation de Minio dans la partie jobs. Minio permet de stocker des objets non structurés de manière sécurisée.
- Beaucoup de requêtes de données dans la partie salary.
- Les pratiques de développement logiciel visant à organiser le code de manière modulaire et à séparer les préoccupations dans toutes les parties du projet.

Évidemment, l'intégration de Docker au sein du projet permet également une portabilité de notre application et la facilité de son déploiement.

## Navigation sur le site

### Page d'accueil (non connecté)

Dans la page d'accueil, vous avez deux options. La première est de vous connecter si vous avez déjâ un compte. La seconde est de ciquer sur créer un compte. Cela vous redirigera vers une page pour créer un compte.

### Page d'accueil (connecté)

Une fois connecté, vous avez accès a deux pages. A partir de ce moment, la site reconnait l'utilisateurv ia la gestion de token.

### Jobs

La section jobs permet a l'utilisateur de telecharger les fiches metiers correspondant a chaque métier.

### Salary

La section salary permet de visualiser les jobs disponibles selon les critères de localisation et selon la description du job.

Créé par Y.Lakhdari, V.Gerard, Y.Tissot.
