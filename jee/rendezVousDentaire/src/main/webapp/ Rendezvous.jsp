<%@ page language="java" contentType="text/html; charset=UTF-8" pageEncoding="UTF-8"%>
<%@ taglib uri="http://java.sun.com/jsp/jstl/core" prefix="c" %>
<%@ taglib uri="http://java.sun.com/jsp/jstl/fmt" prefix="fmt" %>
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Prise de Rendez-vous</title>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;700;800&display=swap" rel="stylesheet">
    <link rel="stylesheet" type="text/css" href="<%= request.getContextPath() %>/css/mesStyles.css">
</head>
<body>
    <div class="form-container">
        <h2>Gestion des Rendez-vous</h2>
        
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
            <h3>Rechercher des rendez-vous</h3>
            <div class="search-options">
                <form action="<%= request.getContextPath() %>/rendezvous" method="get" class="inline-form">
                    <input type="hidden" name="action" value="byDate">
                    <label for="searchDate">Par date :</label>
                    <input type="date" id="searchDate" name="date">
                    <button type="submit" class="btn-small">Rechercher</button>
                </form>
                
                <form action="<%= request.getContextPath() %>/rendezvous" method="get" class="inline-form">
                    <input type="hidden" name="action" value="byStatut">
                    <label for="searchStatut">Par statut :</label>
                    <select id="searchStatut" name="statut">
                        <option value="">Tous</option>
                        <option value="En attente">En attente</option>
                        <option value="Confirmé">Confirmé</option>
                        <option value="Annulé">Annulé</option>
                        <option value="Terminé">Terminé</option>
                    </select>
                    <button type="submit" class="btn-small">Rechercher</button>
                </form>
                
                <a href="<%= request.getContextPath() %>/rendezvous?action=list" class="btn-secondary">
                    Voir tous mes rendez-vous
                </a>
            </div>
        </div>
        
        <hr>
        
        <!-- Formulaire de prise de rendez-vous -->
        <div class="appointment-section">
            <h3>Prendre un nouveau rendez-vous</h3>
            <form action="<%= request.getContextPath() %>/rendezvous" method="post">
                <input type="hidden" name="action" value="create">
                
                <div class="form-row">
                    <div class="form-group">
                        <label for="idPatient">ID Patient * :</label>
                        <input type="number" id="idPatient" name="idPatient" required 
                               placeholder="Votre identifiant patient">
                    </div>
                    
                    <div class="form-group">
                        <label for="idDentiste">Sélectionner un dentiste * :</label>
                        <select id="idDentiste" name="idDentiste" required>
                            <option value="">-- Choisir un dentiste --</option>
                            <!-- Les dentistes seront chargés dynamiquement ou depuis le serveur -->
                            <option value="1">Dr. Ahmed Ben Ali - Orthodontie</option>
                            <option value="2">Dr. Salma Karoui - Chirurgie dentaire</option>
                            <option value="3">Dr. Mohamed Trabelsi - Dentisterie générale</option>
                        </select>
                    </div>
                </div>
                
                <div class="form-row">
                    <div class="form-group">
                        <label for="dateRv">Date du rendez-vous * :</label>
                        <input type="date" id="dateRv" name="dateRv" required 
                               min="<%= new java.text.SimpleDateFormat("yyyy-MM-dd").format(new java.util.Date()) %>">
                    </div>
                    
                    <div class="form-group">
                        <label for="heureRv">Heure * :</label>
                        <input type="time" id="heureRv" name="heureRv" required 
                               min="08:00" max="18:00">
                        <small class="form-text">Horaires: 08h00 - 18h00</small>
                    </div>
                </div>
                
                <div class="form-group">
                    <label for="statut">Statut :</label>
                    <select id="statut" name="statut">
                        <option value="En attente">En attente</option>
                        <option value="Confirmé">Confirmé</option>
                        <option value="Annulé">Annulé</option>
                    </select>
                </div>
                
                <div class="form-group">
                    <label for="details">Détails / Motif de consultation :</label>
                    <textarea id="details" name="details" rows="4" 
                              placeholder="Décrivez la raison de votre consultation..."></textarea>
                </div>
                
                <div class="form-actions">
                    <button type="submit" class="btn-primary">📅 Confirmer le rendez-vous</button>
                    <button type="reset" class="btn-secondary">Réinitialiser</button>
                </div>
            </form>
        </div>
        
        <!-- Calendrier visuel (optionnel) -->
        <div class="calendar-section" style="margin-top: 30px;">
            <h3>📅 Disponibilités du mois</h3>
            <div class="calendar-placeholder">
                <p>Un calendrier interactif peut être intégré ici pour visualiser les créneaux disponibles.</p>
            </div>
        </div>
    </div>
    
    <script>
        // Validation de l'heure
        document.querySelector('form').addEventListener('submit', function(e) {
            var heure = document.getElementById('heureRv').value;
            if (heure) {
                var hours = parseInt(heure.split(':')[0]);
                if (hours < 8 || hours >= 18) {
                    e.preventDefault();
                    alert('Les rendez-vous sont disponibles uniquement entre 08h00 et 18h00');
                }
            }
        });
        
        // Désactiver les dates passées
        var today = new Date().toISOString().split('T')[0];
        document.getElementById('dateRv').setAttribute('min', today);
    </script>
</body>
</html>