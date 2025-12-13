<%@ page language="java" contentType="text/html; charset=UTF-8" pageEncoding="UTF-8"%>
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Inscription Aide-soignant</title>
    <link rel="stylesheet" type="text/css" href="<%= request.getContextPath() %>/css/mesStyles.css">
</head>
<body>
    <div class="form-container">
        <h2>Inscription Aide-soignant / Dentiste</h2>
        <p>Créez votre profil professionnel</p>
        
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
        
        <form action="<%= request.getContextPath() %>/dentiste" method="post" enctype="multipart/form-data">
            <input type="hidden" name="action" value="create">
            
            <div class="form-row">
                <div class="form-group">
                    <label for="nom">Nom * :</label>
                    <input type="text" id="nom" name="nom" required maxlength="100">
                </div>
                
                <div class="form-group">
                    <label for="prenom">Prénom * :</label>
                    <input type="text" id="prenom" name="prenom" required maxlength="100">
                </div>
            </div>
            
            <div class="form-row">
                <div class="form-group">
                    <label for="email">Email * :</label>
                    <input type="email" id="email" name="email" required maxlength="100">
                </div>
                
                <div class="form-group">
                    <label for="telephone">Téléphone :</label>
                    <input type="tel" id="telephone" name="telephone" maxlength="8" pattern="[0-9]{8}">
                </div>
            </div>
            
            <div class="form-row">
                <div class="form-group">
                    <label for="specialite">Spécialité :</label>
                    <input type="text" id="specialite" name="specialite" maxlength="100" 
                           placeholder="Ex: Orthodontie, Chirurgie dentaire...">
                </div>
                
                <div class="form-group">
                    <label for="sexe">Sexe :</label>
                    <select id="sexe" name="sexe">
                        <option value="">Sélectionner</option>
                        <option value="M">Masculin</option>
                        <option value="F">Féminin</option>
                    </select>
                </div>
            </div>
            
            <div class="form-group">
                <label for="photo">Photo de profil :</label>
                <input type="file" id="photo" name="photo" accept="image/*">
            </div>
            
            <div class="form-row">
                <div class="form-group">
                    <label for="mdp">Mot de passe * :</label>
                    <input type="password" id="mdp" name="mdp" required maxlength="10">
                </div>
                
                <div class="form-group">
                    <label for="confirmMdp">Confirmer mot de passe * :</label>
                    <input type="password" id="confirmMdp" name="confirmMdp" required maxlength="10">
                </div>
            </div>
            
            <div class="form-actions">
                <button type="submit" class="btn-primary">Enregistrer</button>
                <button type="reset" class="btn-secondary">Réinitialiser</button>
            </div>
        </form>
        
        <p class="form-footer">
            Déjà inscrit ? <a href="<%= request.getContextPath() %>/connexion">Se connecter</a>
        </p>
    </div>
    
    <script>
        document.querySelector('form').addEventListener('submit', function(e) {
            var mdp = document.getElementById('mdp').value;
            var confirmMdp = document.getElementById('confirmMdp').value;
            
            if (mdp !== confirmMdp) {
                e.preventDefault();
                alert('Les mots de passe ne correspondent pas');
            }
        });
    </script>
</body>
</html>