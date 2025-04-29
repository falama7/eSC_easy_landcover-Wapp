"""
Script de lancement de l'application Flask pour l'analyse de la couverture terrestre.
"""
import os
from app import create_app

# Création de l'application Flask
app = create_app(os.environ.get('FLASK_CONFIG', 'default'))

if __name__ == '__main__':
    # Lancement du serveur de développement
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
