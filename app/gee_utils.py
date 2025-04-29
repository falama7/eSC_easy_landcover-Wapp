"""
Fonctions utilitaires pour interagir avec Google Earth Engine.
"""
import os
import ee
import json
import logging
import geemap.foliumap as geemap
import folium
from datetime import datetime

# Configuration du logging
logger = logging.getLogger(__name__)

def initialize_gee(credentials_path):
    """
    Initialise Google Earth Engine avec les credentials stockés
    dans le dossier spécifié.
    
    Args:
        credentials_path (str): Chemin vers le dossier contenant les credentials
        
    Returns:
        bool: True si l'initialisation a réussi, False sinon
    """
    try:
        # Vérifie si le dossier credentials existe
        if not os.path.exists(credentials_path):
            os.makedirs(credentials_path)
            logger.warning(f"Le dossier credentials {credentials_path} a été créé")
            return False
            
        # Chemin vers le fichier de credentials
        credentials_file = os.path.join(credentials_path, "gee-credentials.json")
        
        # Vérifie si le fichier de credentials existe
        if not os.path.isfile(credentials_file):
            logger.error(f"Fichier de credentials non trouvé: {credentials_file}")
            return False
            
        # Charge les credentials
        try:
            with open(credentials_file) as f:
                credentials = json.load(f)
                
            # Initialise Earth Engine avec les credentials
            credentials = ee.ServiceAccountCredentials(
                email=credentials.get('client_email'),
                key_data=json.dumps(credentials)
            )
            ee.Initialize(credentials)
            
            logger.info("Google Earth Engine initialisé avec succès")
            return True
            
        except json.JSONDecodeError:
            logger.error(f"Format de fichier de credentials invalide: {credentials_file}")
            return False
            
    except Exception as e:
        logger.error(f"Erreur lors de l'initialisation de GEE: {str(e)}")
        return False

def create_map(center=None, zoom=10):
    """
    Crée une carte Folium avec un fond de carte hybride.
    
    Args:
        center (list, optional): Coordonnées du centre [lat, lng]
        zoom (int, optional): Niveau de zoom
        
    Returns:
        folium.Map: La carte Folium créée
    """
    if center is None:
        center = [43.0731, -89.4012]  # Madison, Wisconsin
    
    m = folium.Map(
        location=center,
        zoom_start=zoom,
        control_scale=True
    )
    
    # Ajoute un fond de carte
    folium.TileLayer(
        tiles='https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}',
        attr='Google',
        name='Google Satellite',
        overlay=False,
        control=True
    ).add_to(m)
    
    # Ajoute un contrôle de couches
    folium.LayerControl().add_to(m)
    
    return m

def bbox_to_ee_geometry(bbox):
    """
    Convertit une bbox [xmin, ymin, xmax, ymax] en géométrie Earth Engine
    
    Args:
        bbox (list): Bounding box [xmin, ymin, xmax, ymax]
        
    Returns:
        ee.Geometry: Géométrie Earth Engine
    """
    return ee.Geometry.BBox(bbox[0], bbox[1], bbox[2], bbox[3])

def get_dynamic_world_timeseries(region, start_date, end_date, return_type="class"):
    """
    Récupère une série temporelle d'images Dynamic World
    
    Args:
        region (ee.Geometry): Région d'intérêt
        start_date (str): Date de début (YYYY-MM-DD)
        end_date (str): Date de fin (YYYY-MM-DD)
        return_type (str): Type de retour ("class", "hillshade", "visualize", "probability")
        
    Returns:
        ee.ImageCollection: Collection d'images Dynamic World
    """
    try:
        return geemap.dynamic_world_timeseries(
            region=region,
            start_date=start_date,
            end_date=end_date,
            return_type=return_type
        )
    except Exception as e:
        logger.error(f"Erreur lors de la récupération des données Dynamic World: {str(e)}")
        raise

def add_dw_image_to_map(m, image, vis_params=None, layer_name="Dynamic World"):
    """
    Ajoute une image Dynamic World à une carte Folium
    
    Args:
        m (folium.Map): Carte Folium
        image (ee.Image): Image Earth Engine
        vis_params (dict, optional): Paramètres de visualisation
        layer_name (str, optional): Nom de la couche
        
    Returns:
        folium.Map: Carte Folium avec l'image ajoutée
    """
    if vis_params is None:
        vis_params = {
            "min": 0,
            "max": 8,
            "palette": [
                "#419BDF",  # Water
                "#397D49",  # Trees
                "#88B053",  # Grass
                "#7A87C6",  # Flooded vegetation
                "#E49635",  # Crops
                "#DFC35A",  # Shrub & scrub
                "#C4281B",  # Built area
                "#A59B8F",  # Bare
                "#B39FE1",  # Snow & ice
            ],
        }
    
    try:
        m.addLayer(image, vis_params, layer_name)
        return m
    except Exception as e:
        logger.error(f"Erreur lors de l'ajout de l'image à la carte: {str(e)}")
        raise

def add_dw_legend_to_map(m):
    """
    Ajoute une légende Dynamic World à une carte Folium
    
    Args:
        m (folium.Map): Carte Folium
        
    Returns:
        folium.Map: Carte Folium avec la légende ajoutée
    """
    try:
        m.add_legend(title="Dynamic World Land Cover", builtin_legend="Dynamic_World")
        return m
    except Exception as e:
        logger.error(f"Erreur lors de l'ajout de la légende à la carte: {str(e)}")
        raise

def get_time_series_map(region, start_date, end_date, return_type="class", center=None, zoom=10):
    """
    Crée une carte avec une série temporelle Dynamic World
    
    Args:
        region (ee.Geometry): Région d'intérêt
        start_date (str): Date de début (YYYY-MM-DD)
        end_date (str): Date de fin (YYYY-MM-DD)
        return_type (str): Type de retour ("class", "hillshade", "visualize", "probability")
        center (list, optional): Coordonnées du centre [lat, lng]
        zoom (int, optional): Niveau de zoom
        
    Returns:
        (folium.Map, dict): Carte Folium et informations sur les données
    """
    try:
        # Crée la carte avec geemap
        m = geemap.Map(center=center, zoom=zoom)
        m.add_basemap("HYBRID")
        
        # Centre la carte sur la région
        m.centerObject(region)
        
        # Récupère les images
        images = get_dynamic_world_timeseries(
            region=region,
            start_date=start_date,
            end_date=end_date,
            return_type=return_type
        )
        
        # Paramètres de visualisation
        vis_params = {
            "min": 0,
            "max": 8,
            "palette": [
                "#419BDF",  # Water
                "#397D49",  # Trees
                "#88B053",  # Grass
                "#7A87C6",  # Flooded vegetation
                "#E49635",  # Crops
                "#DFC35A",  # Shrub & scrub
                "#C4281B",  # Built area
                "#A59B8F",  # Bare
                "#B39FE1",  # Snow & ice
            ],
        }
        
        # Ajoute la première image
        if return_type != "probability":
            m.addLayer(images.first(), vis_params, "Première image")
            m.add_legend(title="Dynamic World Land Cover", builtin_legend="Dynamic_World")
        
        # Ajoute l'inspecteur temporel
        if return_type == "class" or return_type == "hillshade":
            m.ts_inspector(
                left_ts=images,
                right_ts=images,  # Utilisez la même collection d'images pour la droite
                left_names=['Classification'],  # Noms pour la légende de gauche
                right_names=['Classification'],  # Noms pour la légende de droite
                left_vis=vis_params if return_type == "class" else None,
                date_format="YYYY"
            )
        
        # Récupère des informations sur les données
        image_size = images.size().getInfo()
        first_date = images.first().date().format("YYYY-MM-dd").getInfo()
        last_date = images.sort("system:time_start", False).first().date().format("YYYY-MM-dd").getInfo()
        
        info = {
            "image_count": image_size,
            "first_date": first_date,
            "last_date": last_date,
            "region": region.getInfo(),
            "start_date": start_date,
            "end_date": end_date,
            "return_type": return_type
        }
        
        return m, info
        
    except Exception as e:
        logger.error(f"Erreur lors de la création de la carte avec série temporelle: {str(e)}")
        raise

def get_dw_class_description():
    """
    Retourne la description des classes Dynamic World
    
    Returns:
        dict: Dictionnaire avec les descriptions des classes
    """
    return {
        0: "Eau: Rivières, réservoirs, lacs, étangs, océans",
        1: "Arbres: Végétation arborée avec une hauteur supérieure à 5m",
        2: "Herbe: Prairies, pelouses, terres herbeuses",
        3: "Végétation inondée: Zones humides avec végétation émergente",
        4: "Cultures: Terres agricoles, terres cultivées",
        5: "Arbustes et buissons: Végétation ligneuse de moins de 5m de hauteur",
        6: "Zone bâtie: Bâtiments, routes, structures artificielles",
        7: "Sol nu: Sol nu, sable, roches",
        8: "Neige et glace: Zones couvertes de neige ou de glace"
    }

def get_cell_notebook_content():
    """
    Retourne le contenu des cellules du notebook original
    
    Returns:
        dict: Dictionnaire avec les cellules du notebook
    """
    cells = {
        "import": """
import ee
import geemap
        """,
        "create_map": """
Map = geemap.Map()
Map.add_basemap("HYBRID")
Map
        """,
        "set_region": """
# Set the region of interest by simply drawing a polygon on the map
region = Map.user_roi
if region is None:
    region = ee.Geometry.BBox(-89.7088, 42.9006, -89.0647, 43.2167)

Map.centerObject(region)
        """,
        "set_date": """
# Set the date range
start_date = "2017-01-01"
end_date = "2021-12-31"
        """,
        "get_images": """
images = geemap.dynamic_world_timeseries(
    region, start_date, end_date, return_type="class"
)
        """,
        "visualize": """
vis_params = {
    "min": 0,
    "max": 8,
    "palette": [
        "#419BDF",
        "#397D49",
        "#88B053",
        "#7A87C6",
        "#E49635",
        "#DFC35A",
        "#C4281B",
        "#A59B8F",
        "#B39FE1",
    ],
}
Map.addLayer(images.first(), vis_params, "First image")
Map.add_legend(title="Dynamic World Land Cover", builtin_legend="Dynamic_World")
Map
        """,
        "ts_inspector": """
Map.ts_inspector(images, left_vis=vis_params, date_format="YYYY")
        """,
        "hillshade": """
Map = geemap.Map()
Map.add_basemap("HYBRID")
Map.centerObject(region)

images = geemap.dynamic_world_timeseries(
    region, start_date, end_date, return_type="hillshade"
)
Map.ts_inspector(images, date_format="YYYY")
Map.add_legend(title="Dynamic World Land Cover", builtin_legend="Dynamic_World")

Map
        """
    }
    return cells
