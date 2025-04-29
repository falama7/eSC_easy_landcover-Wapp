/**
 * Scripts pour la gestion des cartes et des visualisations
 */

document.addEventListener('DOMContentLoaded', function() {
    // Variables globales
    let map = null;
    let mapLayers = {};
    let layerControl = null;
    let tsInspector = null;
    
    /**
     * Initialise une carte Leaflet
     * @param {string} containerId - ID du conteneur de la carte
     * @param {Array} center - Coordonnées du centre [lat, lng]
     * @param {number} zoom - Niveau de zoom
     * @returns {L.Map} - Instance de la carte Leaflet
     */
    function initMap(containerId, center = [43.0731, -89.4012], zoom = 10) {
        // Crée la carte si elle n'existe pas
        if (!map) {
            map = L.map(containerId, {
                center: center,
                zoom: zoom,
                zoomControl: true,
                scrollWheelZoom: true
            });
            
            // Ajoute le fond de carte hybride (satellite + labels)
            L.tileLayer('https://{s}.google.com/vt/lyrs=y&x={x}&y={y}&z={z}', {
                maxZoom: 20,
                subdomains: ['mt0', 'mt1', 'mt2', 'mt3'],
                attribution: 'Google'
            }).addTo(map);
            
            // Ajoute le fond de carte OSM comme option alternative
            L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
                maxZoom: 19,
                attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
            });
            
            // Crée le contrôle de couches
            layerControl = L.control.layers({}, {}, { collapsed: false }).addTo(map);
            
            // Ajoute une échelle
            L.control.scale({ imperial: false }).addTo(map);
        }
        
        return map;
    }
    
    /**
     * Centre la carte sur une région (bbox)
     * @param {Array} bbox - Bounding box [xmin, ymin, xmax, ymax]
     */
    function centerMapOnBbox(bbox) {
        if (!map) return;
        
        // Convertit la bbox en bounds Leaflet
        const bounds = L.latLngBounds(
            L.latLng(bbox[1], bbox[0]),  // sw
            L.latLng(bbox[3], bbox[2])   // ne
        );
        
        // Centre la carte sur les bounds
        map.fitBounds(bounds);
    }
    
    /**
     * Dessine un rectangle représentant la région d'analyse
     * @param {Array} bbox - Bounding box [xmin, ymin, xmax, ymax]
     * @param {Object} options - Options de style
     */
    function drawRegionRectangle(bbox, options = {}) {
        if (!map) return;
        
        // Options par défaut
        const defaultOptions = {
            color: '#3388ff',
            weight: 3,
            opacity: 0.8,
            fill: true,
            fillColor: '#3388ff',
            fillOpacity: 0.1
        };
        
        // Fusionne les options par défaut avec les options fournies
        const mergedOptions = { ...defaultOptions, ...options };
        
        // Supprime le rectangle précédent s'il existe
        if (mapLayers.regionRectangle) {
            map.removeLayer(mapLayers.regionRectangle);
        }
        
        // Convertit la bbox en bounds Leaflet
        const bounds = L.latLngBounds(
            L.latLng(bbox[1], bbox[0]),  // sw
            L.latLng(bbox[3], bbox[2])   // ne
        );
        
        // Crée le rectangle
        mapLayers.regionRectangle = L.rectangle(bounds, mergedOptions).addTo(map);
        
        // Ajoute un popup avec les coordonnées
        mapLayers.regionRectangle.bindPopup(`
            <strong>Région d'analyse</strong><br>
            Min Long: ${bbox[0].toFixed(4)}<br>
            Min Lat: ${bbox[1].toFixed(4)}<br>
            Max Long: ${bbox[2].toFixed(4)}<br>
            Max Lat: ${bbox[3].toFixed(4)}
        `);
        
        // Ajoute au contrôle de couches
        layerControl.addOverlay(mapLayers.regionRectangle, "Région d'analyse");
        
        return mapLayers.regionRectangle;
    }
    
    /**
     * Ajoute un GeoJSON à la carte
     * @param {Object} geojson - Données GeoJSON
     * @param {Object} options - Options de style et de popup
     * @param {string} name - Nom de la couche
     */
    function addGeoJSON(geojson, options = {}, name = "GeoJSON") {
        if (!map) return;
        
        // Options par défaut
        const defaultOptions = {
            style: {
                color: '#ff7800',
                weight: 2,
                opacity: 0.8,
                fillOpacity: 0.3
            },
            onEachFeature: function(feature, layer) {
                // Popup par défaut avec les propriétés
                if (feature.properties) {
                    let popupContent = "<table class='table table-sm'>";
                    for (let prop in feature.properties) {
                        popupContent += `<tr><th>${prop}</th><td>${feature.properties[prop]}</td></tr>`;
                    }
                    popupContent += "</table>";
                    layer.bindPopup(popupContent);
                }
            }
        };
        
        // Fusionne les options par défaut avec les options fournies
        const mergedOptions = { ...defaultOptions, ...options };
        
        // Crée la couche GeoJSON
        const layer = L.geoJSON(geojson, mergedOptions).addTo(map);
        
        // Ajoute au contrôle de couches
        layerControl.addOverlay(layer, name);
        
        // Stocke la couche
        mapLayers[name] = layer;
        
        return layer;
    }
    
    /**
     * Ajoute une légende Dynamic World à la carte
     */
    function addDynamicWorldLegend() {
        if (!map) return;
        
        // Supprime la légende précédente si elle existe
        if (mapLayers.dwLegend) {
            map.removeControl(mapLayers.dwLegend);
        }
        
        // Crée la légende
        const legend = L.control({ position: 'bottomright' });
        
        legend.onAdd = function() {
            const div = L.DomUtil.create('div', 'info legend');
            div.innerHTML = `
                <div class="card">
                    <div class="card-header bg-dark text-white py-1 px-2">
                        <small><strong>Dynamic World</strong></small>
                    </div>
                    <div class="card-body p-2">
                        <div class="legend-item"><div class="color-box" style="background-color: #419BDF;"></div> Eau</div>
                        <div class="legend-item"><div class="color-box" style="background-color: #397D49;"></div> Arbres</div>
                        <div class="legend-item"><div class="color-box" style="background-color: #88B053;"></div> Herbe</div>
                        <div class="legend-item"><div class="color-box" style="background-color: #7A87C6;"></div> Végétation inondée</div>
                        <div class="legend-item"><div class="color-box" style="background-color: #E49635;"></div> Cultures</div>
                        <div class="legend-item"><div class="color-box" style="background-color: #DFC35A;"></div> Arbustes</div>
                        <div class="legend-item"><div class="color-box" style="background-color: #C4281B;"></div> Zone bâtie</div>
                        <div class="legend-item"><div class="color-box" style="background-color: #A59B8F;"></div> Sol nu</div>
                        <div class="legend-item"><div class="color-box" style="background-color: #B39FE1;"></div> Neige et glace</div>
                    </div>
                </div>
            `;
            return div;
        };
        
        legend.addTo(map);
        mapLayers.dwLegend = legend;
        
        return legend;
    }
    
    /**
     * Capture une vue de la carte au format PNG
     * @returns {string} - URL de l'image
     */
    function captureMapView() {
        if (!map) return null;
        
        // Crée un canvas pour la capture
        const canvas = document.createElement('canvas');
        const size = map.getSize();
        canvas.width = size.x;
        canvas.height = size.y;
        
        // Crée une image à partir de la carte
        html2canvas(map.getContainer(), {
            useCORS: true,
            allowTaint: true,
            canvas: canvas
        }).then(function(canvas) {
            return canvas.toDataURL('image/png');
        });
    }
    
    /**
     * Exporte les paramètres actuels de la carte (centre, zoom, couches) au format JSON
     * @returns {Object} - Paramètres de la carte
     */
    function exportMapState() {
        if (!map) return null;
        
        const center = map.getCenter();
        const zoom = map.getZoom();
        
        // Construit l'état de la carte
        const mapState = {
            center: [center.lat, center.lng],
            zoom: zoom,
            layers: {}
        };
        
        // Ajoute l'état des couches
        for (let layerName in mapLayers) {
            if (map.hasLayer(mapLayers[layerName])) {
                mapState.layers[layerName] = true;
            }
        }
        
        return mapState;
    }
    
    /**
     * Importe un état de carte précédemment exporté
     * @param {Object} mapState - État de la carte
     */
    function importMapState(mapState) {
        if (!map || !mapState) return;
        
        // Centre la carte
        if (mapState.center) {
            map.setView(mapState.center, mapState.zoom || 10);
        }
        
        // Gère les couches
        if (mapState.layers) {
            for (let layerName in mapState.layers) {
                if (mapLayers[layerName]) {
                    if (mapState.layers[layerName]) {
                        map.addLayer(mapLayers[layerName]);
                    } else {
                        map.removeLayer(mapLayers[layerName]);
                    }
                }
            }
        }
    }
    
    // Exporte les fonctions disponibles globalement
    window.mapUtils = {
        initMap,
        centerMapOnBbox,
        drawRegionRectangle,
        addGeoJSON,
        addDynamicWorldLegend,
        captureMapView,
        exportMapState,
        importMapState
    };
});
