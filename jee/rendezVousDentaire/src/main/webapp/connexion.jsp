<%@ page language="java" contentType="text/html; charset=UTF-8" pageEncoding="UTF-8"%>
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>connexion</title>
    <link rel="stylesheet" type="text/css" href="<%= request.getContextPath() %>/css/mesStyles.css">
</head>
<body>
    <div class="connexion-container">
        <h2>Bienvenue sur notre plateforme</h2>
        <p>Veuillez sélectionner votre type de compte pour vous connecter</p>
        
        <% if (request.getAttribute("erreur") != null) { %>
            <div class="error-message">
                <%= request.getAttribute("erreur") %>
            </div>
        <% } %>
        
        <div class="user-type-selection">
            <div class="user-card">
                <h3>Je suis un Patient</h3>
                <p>Prendre rendez-vous avec un dentiste</p>
                <a href="<%= request.getContextPath() %>/patient" class="btn-primary">S'inscrire</a>
                <a href="#" onclick="showLoginForm('patient')" class="btn-secondary">Se connecter</a>
            </div>
            
            <div class="user-card">
                <h3>Je suis un Aide-soignant</h3>
                <p>Gérer les rendez-vous et consultations</p>
                <a href="<%= request.getContextPath() %>/dentiste" class="btn-primary">S'inscrire</a>
                <a href="#" onclick="showLoginForm('dentiste')" class="btn-secondary">Se connecter</a>
            </div>
        </div>
        
        <!-- Formulaire de connexion (caché par défaut) -->
        <div id="loginForm" class="login-form" style="display:none;">
            <h3>Connexion</h3>
            <form action="<%= request.getContextPath() %>/connexion" method="post">
                <input type="hidden" name="userType" id="userType" value="">
                
                <div class="form-group">
                    <label for="email">Email :</label>
                    <input type="email" id="email" name="email" required>
                </div>
                
                <div class="form-group">
                    <label for="password">Mot de passe :</label>
                    <input type="password" id="password" name="password" required>
                </div>
                
                <button type="submit" class="btn-primary">Se connecter</button>
                <button type="button" onclick="hideLoginForm()" class="btn-secondary">Annuler</button>
            </form>
        </div>
    </div>
    
    <script>
        function showLoginForm(type) {
            document.getElementById('userType').value = type;
            document.getElementById('loginForm').style.display = 'block';
            document.querySelector('.user-type-selection').style.display = 'none';
        }
        
        function hideLoginForm() {
            document.getElementById('loginForm').style.display = 'none';
            document.querySelector('.user-type-selection').style.display = 'flex';
        }
    </script>
</body>
</html>