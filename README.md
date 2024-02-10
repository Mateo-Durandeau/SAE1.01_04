Voici une version révisée et améliorée de votre fichier `README.md`, avec une structure et une formulation plus professionnelles :

# Gestion de Données Geod'air - SAE 1.01_04
**Auteur :** Durandeau Matéo  
**Formation :** BUT Informatique

## Présentation du projet

Ce projet s'inscrit dans le cadre de la SAE 1.01_04, axée sur la manipulation et la gestion de données environnementales. Il traite spécifiquement des données de Geod'air, une base de données consacrée à la mesure de composants polluants dans l'air, répartis dans différentes zones géographiques. Le système de données est organisé selon une hiérarchie ASCAA, qui comprend des zones (zas) et des sites de mesure.

Les outils développés pour ce projet permettent de télécharger automatiquement les données disponibles sur un serveur HTTP et de les intégrer dans une base de données locale. L'objectif est de faciliter l'affichage dynamique de ces informations via une interface web, en utilisant le micro-framework Flask pour la gestion et la présentation des données.

## Mise en place

### Prérequis
- Python 3.12
- Flask
- SQLite

### Installation

1. Clonez le dépôt GitHub ou le download 

### Configuration

Avant de lancer l'application, assurez-vous de configurer correctement la connexion à votre base de données SQLite en ajustant les variables appropriées dans le fichier `config.py`.

## Utilisation

### Téléchargement des données

Pour télécharger les données et les insérer dans votre base de données, exécutez le script `automatisation_http_to_bdd.py` dans le repertoire Creation-BDD. Vous pouvez personnaliser le processus en suivant les instructions fournies dans les commentaires du script.

### Lancement de l'application web

Pour démarrer le serveur Flask et accéder à l'interface web :

```bash
python app.py
```

Veillez à ce que le nom de votre base de données soit correctement renseigné dans les variables du script.

### Tests

Des scripts de test sont disponibles pour vérifier l'intégrité des données, les performances des requêtes, et l'efficacité de l'ajout de nouvelles données. Consultez le dossier `tests` pour plus de détails.

