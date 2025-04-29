"""
Définition des routes et API pour l'application Flask.
"""
import os
import json
import ee
from flask import Blueprint, render_template, request, jsonify, current_app
from datetime import datetime
from app.gee_utils import (
    bbox_to_ee_geometry,
    get_time_series_map,
    get_dw_class_description,
    get_cell_notebook_content
)

# Création du blueprint principal
main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """Page d'accueil"""
    current_year = datetime.now().year
    
    # Récupération des paramètres de configuration
    default_bbox = current_app.config['DEFAULT_BBOX']
    default_start_date = current_app.config['DEFAULT_START_DATE']
    default_end_date = current_app.config['DEFAULT_END_DATE']
    default_return_type = current_app.config['DEFAULT_RETURN_TYPE']
    dw_classes = current_app.config['DW_CLASSES']
    
    # Récupération du contenu des cellules du notebook
    notebook_cells = get_cell_notebook_content()
    
    return render_template(
        'index.html',
        title="Analyse de la couverture terrestre",
        default_bbox=default_bbox,
        current_year=current_year,
        default_start_date=default_start_date,
        default_end_date=default_end_date,
        default_return_type=default_return_type,
        dw_classes=dw_classes,
        notebook_cells=notebook_cells
    )

@main_bp.route('/about')
def about():
    """Page d'informations"""
    dw_class_descriptions = get_dw_class_description()
    return render_template(
        'about.html',
        title="À propos de l'application",
        dw_class_descriptions=dw_class_descriptions
    )

@main_bp.route('/api/analyze', methods=['POST'])
def analyze():
    """
    API pour analyser une région avec Dynamic World
    
    Request body:
    {
        "bbox": [xmin, ymin, xmax, ymax],
        "start_date": "YYYY-MM-DD",
        "end_date": "YYYY-MM-DD",
        "return_type": "class"|"hillshade"|"visualize"|"probability"
    }
    
    Returns:
        JSON avec l'URL de la carte et des informations sur les données
    """
    try:
        # Récupération des données de la requête
        data = request.get_json()
        
        # Validation des données
        if not data:
            return jsonify({"error": "Données manquantes"}), 400
            
        bbox = data.get('bbox', current_app.config['DEFAULT_BBOX'])
        start_date = data.get('start_date', current_app.config['DEFAULT_START_DATE'])
        end_date = data.get('end_date', current_app.config['DEFAULT_END_DATE'])
        return_type = data.get('return_type', current_app.config['DEFAULT_RETURN_TYPE'])
        
        # Conversion de la bbox en géométrie Earth Engine
        region = bbox_to_ee_geometry(bbox)
        
        # Calcul du centre de la carte
        center_x = (bbox[0] + bbox[2]) / 2
        center_y = (bbox[1] + bbox[3]) / 2
        center = [center_y, center_x]  # [lat, lng] pour Folium
        
        # Création de la carte
        m, info = get_time_series_map(
            region=region,
            start_date=start_date,
            end_date=end_date,
            return_type=return_type,
            center=center,
            zoom=10
        )
        
        # Génération d'un nom de fichier unique
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        map_filename = f"dw_map_{timestamp}.html"
        map_path = os.path.join(current_app.root_path, 'static', 'maps', map_filename)
        
        # Création du dossier maps s'il n'existe pas
        os.makedirs(os.path.dirname(map_path), exist_ok=True)
        
        # Sauvegarde de la carte
        m.save(map_path)
        
        # URL de la carte
        map_url = f"/static/maps/{map_filename}"
        
        # Préparation de la réponse
        response = {
            "success": True,
            "map_url": map_url,
            "info": info
        }
        
        return jsonify(response)
        
    except Exception as e:
        current_app.logger.error(f"Erreur lors de l'analyse: {str(e)}")
        return jsonify({"error": str(e)}), 500

@main_bp.route('/api/notebook')
def notebook():
    """
    Retourne le contenu des cellules du notebook
    
    Returns:
        JSON avec le contenu des cellules
    """
    cells = get_cell_notebook_content()
    return jsonify(cells)

@main_bp.errorhandler(404)
def page_not_found(e):
    """Gestionnaire d'erreur 404"""
    return render_template('errors/404.html'), 404

@main_bp.errorhandler(500)
def internal_server_error(e):
    """Gestionnaire d'erreur 500"""
    return render_template('errors/500.html'), 500
