/**
 * Script principal pour l'application d'analyse de la couverture terrestre
 */

document.addEventListener('DOMContentLoaded', function() {
    // Initialisation des tooltips Bootstrap
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // Initialisation des popovers Bootstrap
    const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });
    
    // Fonctions utilitaires
    
    /**
     * Formate une date au format "DD/MM/YYYY"
     * @param {string} dateString - Chaîne de date au format "YYYY-MM-DD"
     * @returns {string} Date formatée
     */
    function formatDate(dateString) {
        if (!dateString) return '';
        
        const date = new Date(dateString);
        const day = String(date.getDate()).padStart(2, '0');
        const month = String(date.getMonth() + 1).padStart(2, '0');
        const year = date.getFullYear();
        
        return `${day}/${month}/${year}`;
    }
    
    /**
     * Affiche un message de notification
     * @param {string} message - Message à afficher
     * @param {string} type - Type de message (success, danger, warning, info)
     * @param {number} duration - Durée d'affichage en ms (0 pour ne pas masquer)
     */
    function showNotification(message, type = 'info', duration = 5000) {
        // Crée un élément d'alerte
        const alertDiv = document.createElement('div');
        alertDiv.classList.add('alert', `alert-${type}`, 'alert-dismissible', 'fade', 'show');
        alertDiv.setAttribute('role', 'alert');
        
        // Ajout du contenu
        alertDiv.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Fermer"></button>
        `;
        
        // Recherche du conteneur pour les notifications
        const container = document.querySelector('main');
        if (container) {
            // Ajoute l'alerte au début du conteneur
            container.insertBefore(alertDiv, container.firstChild);
            
            // Masque l'alerte après la durée spécifiée
            if (duration > 0) {
                setTimeout(() => {
                    alertDiv.classList.remove('show');
                    setTimeout(() => {
                        alertDiv.remove();
                    }, 150);
                }, duration);
            }
        }
    }
    
    /**
     * Copie du texte dans le presse-papiers
     * @param {string} text - Texte à copier
     * @returns {Promise<boolean>} - Succès ou échec
     */
    async function copyToClipboard(text) {
        try {
            await navigator.clipboard.writeText(text);
            return true;
        } catch (err) {
            console.error('Erreur lors de la copie dans le presse-papiers:', err);
            return false;
        }
    }
    
    // Exposer les fonctions utilitaires globalement
    window.app = {
        formatDate,
        showNotification,
        copyToClipboard
    };
    
    // Gérer les erreurs AJAX
    window.addEventListener('error', function(e) {
        console.error('Erreur JavaScript:', e.error);
        showNotification('Une erreur JavaScript s\'est produite. Veuillez recharger la page.', 'danger');
    });
    
    // Gérer le clic sur les boutons de copie de code
    document.querySelectorAll('.btn-copy-code').forEach(button => {
        button.addEventListener('click', async function() {
            const codeElement = this.closest('.code-container').querySelector('pre');
            const code = codeElement.textContent;
            
            const success = await copyToClipboard(code);
            if (success) {
                // Changer temporairement le texte du bouton
                const originalText = this.innerHTML;
                this.innerHTML = '<i class="fas fa-check"></i> Copié!';
                
                setTimeout(() => {
                    this.innerHTML = originalText;
                }, 2000);
            } else {
                showNotification('Impossible de copier le code.', 'warning');
            }
        });
    });
});
