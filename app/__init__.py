"""
Initialisation de l'application Flask pour l'analyse de la couverture terrestre.
"""
import os
from flask import Flask
from config import config
import logging
from logging.handlers import RotatingFileHandler

def create_app(config_name=None):
    """
    Crée et configure l'application Flask
    
    Args:
        config_name (str): Nom de la configuration à utiliser (development, production)
        
    Returns:
        Flask: Application Flask configurée
    """
    # Détermine la configuration à utiliser
    if config_name is None:
        config_name = os.environ.get('FLASK_CONFIG', 'default')
    
    # Crée l'application Flask
    app = Flask(__name__)
    
    # Charge la configuration
    app.config.from_object(config[config_name])
    
    # Configure la journalisation
    if not app.debug:
        if not os.path.exists('logs'):
            os.mkdir('logs')
        file_handler = RotatingFileHandler('logs/landcover.log', maxBytes=10240, backupCount=10)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
        ))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)
        app.logger.setLevel(logging.INFO)
        app.logger.info('Application démarrée')
    
    # Initialise Google Earth Engine
    from app.gee_utils import initialize_gee
    credentials_path = app.config['GEE_CREDENTIALS_PATH']
    gee_initialized = initialize_gee(credentials_path)
    if not gee_initialized:
        app.logger.warning("Google Earth Engine n'a pas pu être initialisé")
    
    # Enregistre les routes
    from app import routes
    app.register_blueprint(routes.main_bp)
    
    return app
