<%@ page language="java" contentType="text/html; charset=UTF-8" pageEncoding="UTF-8"%>
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <title>Connexion — Sourire & Co</title>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;700&display=swap" rel="stylesheet">
    
    <style>
        /* 1. Reset et Fixation de l'écran */
        html, body {
            height: 100%;
            margin: 0;
            padding: 0;
            background-color: #F9F7F2; /* Fond beige */
            font-family: 'Plus Jakarta Sans', sans-serif;
        }

        /* 2. Le moteur de centrage (Flexbox) */
        body {
            display: flex;
            align-items: center;      /* Centre verticalement */
            justify-content: center;    /* Centre horizontalement */
        }

        /* 3. La boîte blanche centrale */
        .connexion-container {
            background: #ffffff;
            width: 90%;
            max-width: 800px;
            padding: 50px;
            border-radius: 25px;
            box-shadow: 0 20px 60px rgba(74, 63, 53, 0.1);
            text-align: center;
        }

        h2 { color: #4A3F35; margin-bottom: 10px; font-size: 2rem; }
        p { color: #6B5B4B; margin-bottom: 40px; }

        /* 4. Les deux colonnes de choix */
        .user-type-selection {
            display: flex;
            gap: 25px;
        }

        .user-card {
            flex: 1;
            padding: 30px;
            border: 1px solid #F0EDE9;
            border-radius: 18px;
            background: #FDFBF9;
            transition: transform 0.3s ease;
        }

        .user-card:hover { transform: translateY(-5px); }

        /* 5. Style des Boutons */
        .btn-primary, .btn-secondary {
            display: block;
            width: 100%;
            padding: 14px 0;
            margin: 12px 0;
            border-radius: 50px;
            text-decoration: none;
            font-weight: 700;
            font-size: 13px;
            text-transform: uppercase;
            border: none;
            cursor: pointer;
        }

        .btn-primary { background: #4A3F35; color: white; }
        .btn-secondary { background: white; color: #4A3F35; border: 1px solid #4A3F35; }

        /* 6. Formulaire de login caché */
        .login-form {
            display: none;
            max-width: 400px;
            margin: 30px auto 0;
            text-align: left;
        }
        
        .form-group { margin-bottom: 20px; }
        .form-group label { display: block; margin-bottom: 8px; font-weight: 600; font-size: 14px; }
        .form-group input { 
            width: 100%; 
            padding: 12px; 
            border: 1px solid #E5E1DA; 
            border-radius: 10px; 
            box-sizing: border-box;
        }
    </style>
</head>
<body>

    <div class="connexion-container">
        <h2>Bienvenue sur notre plateforme</h2>
        <p>Veuillez sélectionner votre type de compte pour vous connecter</p>
        
        <% if (request.getAttribute("erreur") != null) { %>
            <div style="color: #d9534f; background: #fdf2f2; padding: 10px; border-radius: 8px; margin-bottom: 20px;">
                <%= request.getAttribute("erreur") %>
            </div>
        <% } %>
        
        <div class="user-type-selection" id="selectionZone">
            <div class="user-card">
                <h3>Patient</h3>
                <p>Prendre rendez-vous</p>
                <a href="<%= request.getContextPath() %>/patient" class="btn-primary">S'inscrire</a>
                <button onclick="showLoginForm('patient')" class="btn-secondary">Se connecter</button>
            </div>
            
            <div class="user-card">
                <h3>Aide-soignant</h3>
                <p>Gérer les rendez-vous</p>
                <a href="<%= request.getContextPath() %>/dentiste" class="btn-primary">S'inscrire</a>
                <button onclick="showLoginForm('dentiste')" class="btn-secondary">Se connecter</button>
            </div>
        </div>
        
        <div id="loginForm" class="login-form">
            <h3 style="text-align: center; margin-bottom: 25px;">Connexion</h3>
            <form action="<%= request.getContextPath() %>/connexion" method="post">
                <input type="hidden" name="userType" id="userType" value="">
                
                <div class="form-group">
                    <label>Email professionnel ou personnel</label>
                    <input type="email" name="email" required placeholder="exemple@mail.com">
                </div>
                
                <div class="form-group">
                    <label>Mot de passe</label>
                    <input type="password" name="password" required>
                </div>
                
                <div style="margin-top: 30px;">
                    <button type="submit" class="btn-primary">Valider la connexion</button>
                    <button type="button" onclick="hideLoginForm()" class="btn-secondary">Retour</button>
                </div>
            </form>
        </div>
    </div>

    <script>
        function showLoginForm(type) {
            document.getElementById('userType').value = type;
            document.getElementById('loginForm').style.display = 'block';
            document.getElementById('selectionZone').style.display = 'flex';
            document.getElementById('selectionZone').style.display = 'none';
        }
        
        function hideLoginForm() {
            document.getElementById('loginForm').style.display = 'none';
            document.getElementById('selectionZone').style.display = 'flex';
        }
    </script>
</body>
</html>