# eSC_easy_landcover-Wapp
# Application d'analyse temporelle de la couverture terrestre

![eSC_easy_landcover-Wapp](https://i.imgur.com/5DGOuTC.png)

Cette application web permet d'analyser l'évolution de la couverture terrestre au fil du temps en utilisant Google Earth Engine et le jeu de données Dynamic World. L'application est basée sur python en application web avec Streamlit et conteneurisée avec Docker.

## Fonctionnalités

- Analyse temporelle de la couverture terrestre sur n'importe quelle région du monde
- Visualisation des classes de couverture terrestre avec différentes options de rendu
- Interface utilisateur intuitive et réactive
- Authentification automatique à Google Earth Engine via un dossier de credentials
- Conteneurisation complète avec Docker

## Prérequis

- Docker et Docker Compose
- Compte Google Earth Engine avec des credentials de service

## Configuration des credentials Google Earth Engine

1. Créez un compte Google Earth Engine si vous n'en avez pas déjà un: [https://earthengine.google.com/](https://earthengine.google.com/)
2. Créez un projet dans la Google Cloud Console et activez l'API Earth Engine
3. Créez un compte de service et téléchargez les credentials au format JSON
4. Placez le fichier de credentials dans le dossier `credentials/` sous le nom `gee-credentials.json`

Des instructions détaillées sont disponibles dans le fichier `credentials/README.md`.

## Installation et démarrage

### Avec Docker Compose (recommandé)

1. Clonez ce dépôt
2. Placez vos credentials GEE dans le dossier `credentials/`
3. Exécutez la commande suivante:

```bash
docker-compose up -d
```

4. Accédez à l'application dans votre navigateur: [http://localhost:5000](http://localhost:5000)

### Sans Docker

1. Clonez ce dépôt
2. Créez un environnement virtuel Python:

```bash
python -m venv venv
source venv/bin/activate  # Sur Windows: venv\Scripts\activate
```

3. Installez les dépendances:

```bash
pip install -r requirements.txt
```

4. Placez vos credentials GEE dans le dossier `credentials/`
5. Lancez l'application:

```bash
# Mode développement
flask run --host=0.0.0.0 --port=5000

# Mode production
gunicorn --bind 0.0.0.0:5000 --workers 4 --timeout 120 run:app
```

6. Accédez à l'application dans votre navigateur: [http://localhost:5000](http://localhost:5000)

## Utilisation

1. Sélectionnez une région d'intérêt (prédéfinie ou personnalisée)
2. Définissez la période d'analyse
3. Choisissez le type de visualisation
4. Cliquez sur "Lancer l'analyse"
5. Explorez les résultats dans la carte interactive

## Structure du projet

```
landcover-app/
├── app/
│   ├── __init__.py           # Initialisation de l'application Flask
│   ├── routes.py             # Définition des routes et des API
│   ├── gee_utils.py          # Fonctions utilitaires pour Google Earth Engine
│   ├── static/               # Ressources statiques
│   │   ├── css/              # Styles CSS
│   │   ├── js/               # Scripts JavaScript
│   │   ├── img/              # Images et icônes
│   │   └── maps/             # Cartes générées dynamiquement
│   └── templates/            # Templates HTML
│       ├── base.html         # Template de base
│       ├── index.html        # Page principale
│       ├── about.html        # Page d'informations
│       └── errors/           # Pages d'erreur
├── credentials/              # Dossier pour stocker les credentials GEE
│   └── README.md             # Instructions pour les credentials
├── logs/                     # Logs de l'application
├── config.py                 # Configuration de l'application
├── run.py                    # Script pour lancer l'application
├── Dockerfile                # Configuration Docker
├── requirements.txt          # Dépendances Python
├── docker-compose.yml        # Configuration Docker Compose
└── README.md                 # Documentation
```

## Détails techniques

### Backend

- **Flask**: Framework web léger et flexible en Python
- **Google Earth Engine API**: Pour accéder aux données satellitaires
- **geemap**: Bibliothèque Python pour interagir avec Earth Engine
- **Folium**: Pour créer des cartes interactives

### Frontend

- **HTML5, CSS3, JavaScript**: Pour l'interface utilisateur
- **Bootstrap 5**: Framework CSS pour le design responsive
- **jQuery**: Pour les interactions JavaScript
- **CodeMirror**: Pour l'affichage des extraits de code
- **Leaflet**: Pour l'affichage des cartes interactives

### Déploiement

- **Docker**: Pour conteneuriser l'application
- **Gunicorn**: Serveur WSGI pour Python
- **Docker Compose**: Pour orchestrer les conteneurs

## Conversion du notebook original

Cette application est basée sur un notebook Jupyter montrant l'utilisation de Google Earth Engine et de Dynamic World pour analyser les changements de couverture terrestre. Toutes les cellules du notebook original sont accessibles dans l'interface utilisateur, permettant aux utilisateurs de comprendre le code sous-jacent.

## Licence

Ce projet est sous licence MIT. Voir le fichier LICENSE pour plus de détails.

## Crédits

- Google Earth Engine: [https://earthengine.google.com/](https://earthengine.google.com/)
#- Dynamic World: [https://dynamicworld.app](https://dynamicworld.app)
#- geemap: [https://geemap.org](https://geemap.org)

