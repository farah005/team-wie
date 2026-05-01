<%@ page language="java" contentType="text/html; charset=UTF-8" pageEncoding="UTF-8"%>
<%@ taglib uri="http://java.sun.com/jsp/jstl/core" prefix="c" %>
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <title>Détail Publication — Cabinet Sourire</title>
    <link rel="stylesheet" type="text/css" href="${pageContext.request.contextPath}/css/mesStyles.css">
</head>
<body>
    <div class="container">
        <div class="header-box">
            <h2>Publication publiée</h2>
        </div>

        <c:if test="${not empty dernierTitre}">
            <div style="background: #f8fafc; border: 1px solid #cbd5e1; border-radius: 12px; padding: 20px; margin-top: 20px;">
                <h3 style="color: #0f172a; margin-top: 0;">Votre publication a été enregistrée</h3>
                <p><strong>Titre :</strong> ${dernierTitre}</p>
                <p><strong>Type :</strong> ${dernierType}</p>
                <p><strong>Description :</strong> ${derniereDesc}</p>
                <p><strong>Fichier :</strong>
                    <a href="${pageContext.request.contextPath}/uploads/${dernierFichier}" target="_blank">${dernierFichier} (Ouvrir)</a>
                </p>
            </div>
        </c:if>

        <div style="margin-top: 20px;">
            <a href="${pageContext.request.contextPath}/publication">Publier une autre</a> |
            <a href="${pageContext.request.contextPath}/publication?action=list">Voir la liste</a>
        </div>
    </div>
</body>
</html>
