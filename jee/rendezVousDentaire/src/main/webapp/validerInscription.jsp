<%@ page language="java" contentType="text/html; charset=UTF-8" pageEncoding="UTF-8"%>
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Inscription Réussie</title>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;700;800&display=swap" rel="stylesheet">
    <link rel="stylesheet" type="text/css" href="<%= request.getContextPath() %>/css/mesStyles.css">
</head>
<body>
    <div class="success-container">
        <div class="success-icon">✓</div>
        <h2>Inscription réussie !</h2>
        <p class="success-message">
            Votre dossier médical a été créé avec succès.<br>
            Consultez la liste des dentistes disponibles et prenez rendez-vous dès maintenant.
        </p>
        
        <div class="success-actions">
            <a href="<%= request.getContextPath() %>/dentiste?action=list" class="btn-primary">
                Voir les dentistes disponibles
            </a>
            <a href="<%= request.getContextPath() %>/rendezvous" class="btn-secondary">
                Prendre un rendez-vous
            </a>
            <a href="<%= request.getContextPath() %>/connexion" class="btn-link">
                Se connecter
            </a>
        </div>
    </div>
</body>
</html>