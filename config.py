"""
Configuration de l'application Flask pour l'analyse de la couverture terrestre.
"""
import os

class Config:
    """Configuration de base"""
    # Clé secrète pour les sessions et la protection CSRF
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'une-cle-secrete-difficile-a-deviner'
    
    # Paramètres de l'application
    APP_NAME = "Analyse de la couverture terrestre"
    
    # Chemin vers le dossier de credentials GEE
    GEE_CREDENTIALS_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'credentials')
    
    # Paramètres de la carte par défaut
    DEFAULT_MAP_CENTER = [43.0731, -89.4012]  # Madison, Wisconsin
    DEFAULT_MAP_ZOOM = 10
    DEFAULT_BBOX = [-89.7088, 42.9006, -89.0647, 43.2167]  # Madison area
    
    # Paramètres d'analyse par défaut
    DEFAULT_START_DATE = "2017-01-01"
    DEFAULT_END_DATE = "2021-12-31"
    DEFAULT_RETURN_TYPE = "class"
    
    # Palettes de couleurs pour Dynamic World
    DW_PALETTE = [
        "#419BDF",  # Water
        "#397D49",  # Trees
        "#88B053",  # Grass
        "#7A87C6",  # Flooded vegetation
        "#E49635",  # Crops
        "#DFC35A",  # Shrub & scrub
        "#C4281B",  # Built area
        "#A59B8F",  # Bare
        "#B39FE1",  # Snow & ice
    ]
    
    # Classes de Dynamic World
    DW_CLASSES = {
        0: {"name": "Eau", "color": "#419BDF"},
        1: {"name": "Arbres", "color": "#397D49"},
        2: {"name": "Herbe", "color": "#88B053"},
        3: {"name": "Végétation inondée", "color": "#7A87C6"},
        4: {"name": "Cultures", "color": "#E49635"},
        5: {"name": "Arbustes", "color": "#DFC35A"},
        6: {"name": "Zone bâtie", "color": "#C4281B"},
        7: {"name": "Sol nu", "color": "#A59B8F"},
        8: {"name": "Neige et glace", "color": "#B39FE1"}
    }

class DevelopmentConfig(Config):
    """Configuration pour le développement"""
    DEBUG = True
    # Autres paramètres spécifiques au développement

class ProductionConfig(Config):
    """Configuration pour la production"""
    DEBUG = False
    # Sécurisation supplémentaire
    SESSION_COOKIE_SECURE = True
    REMEMBER_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_HTTPONLY = True
    
    # Autres paramètres spécifiques à la production

# Configuration par défaut
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
