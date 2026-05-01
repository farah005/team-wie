<%@ page language="java" contentType="text/html; charset=UTF-8" pageEncoding="UTF-8"%>
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Services Médicaux</title>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;700;800&display=swap" rel="stylesheet">
    <link rel="stylesheet" type="text/css" href="<%= request.getContextPath() %>/css/mesStyles.css">
</head>
<body>
    <div class="form-container">
        <h2>Gestion des Services Médicaux</h2>
        
        <% if (request.getAttribute("erreur") != null) { %>
            <div class="error-message">
                <%= request.getAttribute("erreur") %>
            </div>
        <% } %>
        
        <% if (request.getAttribute("message") != null) { %>
            <div class="success-message">
                <%= request.getAttribute("message") %>
            </div>
        <% } %>
        
        <!-- Section de recherche -->
        <div class="search-section">
            <h3>Rechercher un service</h3>
            <form action="<%= request.getContextPath() %>/service" method="post" class="search-form">
                <input type="hidden" name="action" value="search">
                
                <div class="form-group">
                    <label for="typeRecherche">Type de service :</label>
                    <input type="text" id="typeRecherche" name="typeRecherche" 
                           placeholder="Ex: Consultation, Chirurgie...">
                </div>
                
                <button type="submit" class="btn-primary">Rechercher</button>
                <a href="<%= request.getContextPath() %>/service?action=list" class="btn-secondary">
                    Voir tous les services
                </a>
            </form>
        </div>
        
        <hr>
        
        <!-- Formulaire d'ajout de service -->
        <div class="add-service-section">
            <h3>Ajouter un nouveau service</h3>
            <form action="<%= request.getContextPath() %>/service" method="post">
                <input type="hidden" name="action" value="create">
                
                <div class="form-row">
                    <div class="form-group">
                        <label for="nom">Nom du service * :</label>
                        <input type="text" id="nom" name="nom" required maxlength="100">
                    </div>
                    
                    <div class="form-group">
                        <label for="type">Type de service * :</label>
                        <input type="text" id="type" name="type" required maxlength="100" 
                               placeholder="Ex: Consultation, Chirurgie, Orthodontie">
                    </div>
                </div>
                
                <div class="form-group">
                    <label for="description">Description :</label>
                    <textarea id="description" name="description" rows="4" 
                              placeholder="Décrivez le service médical..."></textarea>
                </div>
                
                <div class="form-group">
                    <label for="tarif">Tarif (TND) :</label>
                    <input type="number" id="tarif" name="tarif" step="0.01" min="0" 
                           placeholder="0.00">
                </div>
                
                <div class="form-actions">
                    <button type="submit" class="btn-primary">Enregistrer le service</button>
                    <button type="reset" class="btn-secondary">Réinitialiser</button>
                </div>
            </form>
        </div>
        
        <!-- Liste des services (si disponible) -->
        <% if (request.getAttribute("services") != null) { %>
            <div class="services-list">
                <h3>Services trouvés</h3>
                <!-- Affichage dynamique des services -->
                <div class="services-grid">
                    <!-- Les services seront affichés ici -->
                </div>
            </div>
        <% } %>
    </div>
</body>
</html>