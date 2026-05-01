<%@ page language="java" contentType="text/html; charset=UTF-8" pageEncoding="UTF-8"%>
<%@ taglib uri="http://java.sun.com/jsp/jstl/core" prefix="c" %>

<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <title>Connexion — Cabinet Sourire</title>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" type="text/css" href="${pageContext.request.contextPath}/css/mesStyles.css">
    <style>
        .login-container { max-width: 400px; margin: 80px auto; background: white; padding: 40px; border-radius: 15px; box-shadow: 0 10px 40px rgba(0,0,0,0.1); }
        .form-group { margin-bottom: 20px; display: flex; flex-direction: column; }
        label { font-weight: 600; color: #4A3F35; margin-bottom: 8px; }
        input, select { padding: 12px; border: 1px solid #E5E1DA; border-radius: 8px; font-size: 1rem; }
        .btn-login { background: #4A3F35; color: white; border: none; padding: 14px; border-radius: 8px; cursor: pointer; font-weight: 700; width: 100%; margin-top: 10px; transition: 0.3s; }
        .btn-login:hover { background: #352d26; }
        .info-msg { background: #E5F9F0; color: #2D8A5C; padding: 12px; border-radius: 8px; margin-bottom: 20px; text-align: center; border: 1px solid #CCF2E0; font-size: 0.9rem; }
    </style>
</head>
<body>
    <%-- Inclusion du Header commun --%>
    <%@ include file="header.jsp" %>

    <div class="login-container">
        <h2 style="text-align: center; color: #4A3F35; margin-top: 0;">Espace Patient</h2>
        
        <%-- Message de déconnexion réussie --%>
        <c:if test="${param.logout == 'true'}">
            <div class="info-msg">
                ✅ Vous avez été déconnecté.
            </div>
        </c:if>

        <%-- Message d'erreur de connexion --%>
        <c:if test="${not empty erreur}">
            <div class="error-message" style="background: #FDECEC; color: #C0392B; padding: 12px; border-radius: 8px; margin-bottom: 20px; border: 1px solid #FACCCC; text-align: center;">
                ${erreur}
            </div>
        </c:if>

        <form action="${pageContext.request.contextPath}/connexion" method="post">
            <div class="form-group">
                <label for="userType">Vous êtes :</label>
                <select name="userType" id="userType">
                    <option value="patient">Patient</option>
                    <option value="aide-soignant">Personnel Médical</option>
                    <option value="dentiste">Dentiste</option>
                </select>
            </div>

            <div class="form-group">
                <label for="email">Adresse Email</label>
                <input type="email" id="email" name="email" required placeholder="exemple@mail.com">
            </div>

            <div class="form-group">
                <label for="password">Mot de passe</label>
                <input type="password" id="password" name="password" required placeholder="••••••••">
            </div>

            <button type="submit" class="btn-login">Se connecter</button>
        </form>

        <div style="text-align: center; margin-top: 25px; font-size: 0.9rem; color: #6B5B4B;">
            Nouveau patient ? <a href="${pageContext.request.contextPath}/patient" style="color: #4A3F35; font-weight: 700; text-decoration: none;">Créer un compte</a>
        </div>
    </div>
</body>
</html>