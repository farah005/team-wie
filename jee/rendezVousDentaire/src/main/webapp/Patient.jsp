<%@ page language="java" contentType="text/html; charset=UTF-8" pageEncoding="UTF-8"%>
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Inscription Patient</title>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;700;800&display=swap" rel="stylesheet">
    <link rel="stylesheet" type="text/css" href="<%= request.getContextPath() %>/css/mesStyles.css">
</head>
<body>
    <div class="form-container">
        <h2>Inscription Patient</h2>
        <p>Créez votre dossier médical pour prendre rendez-vous facilement</p>
        
        <% if (request.getAttribute("erreur") != null) { %>
            <div class="error-message">
                <%= request.getAttribute("erreur") %>
            </div>
        <% } %>
        
        <form action="<%= request.getContextPath() %>/patient" method="post" enctype="multipart/form-data">
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
                    <label for="dateNaissance">Date de naissance :</label>
                    <input type="date" id="dateNaissance" name="dateNaissance">
                </div>
            </div>
            
            <div class="form-row">
                <div class="form-group">
                    <label for="sexe">Sexe :</label>
                    <select id="sexe" name="sexe">
                        <option value="">Sélectionner</option>
                        <option value="M">Masculin</option>
                        <option value="F">Féminin</option>
                    </select>
                </div>
                
                <div class="form-group">
                    <label for="groupeSanguin">Groupe sanguin :</label>
                    <select id="groupeSanguin" name="groupeSanguin">
                        <option value="">Sélectionner</option>
                        <option value="A">A</option>
                        <option value="B">B</option>
                        <option value="O">O</option>
                        <option value="AB">AB</option>
                    </select>
                </div>
            </div>
            
            <div class="form-group">
                <label for="recouvrement">Recouvrement social :</label>
                <input type="text" id="recouvrement" name="recouvrement" maxlength="100">
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