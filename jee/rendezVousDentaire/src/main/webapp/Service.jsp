<%@ page language="java" contentType="text/html; charset=UTF-8" pageEncoding="UTF-8"%>
<%@ page language="java" contentType="text/html; charset=UTF-8" pageEncoding="UTF-8"%>
<%@ taglib uri="http://java.sun.com/jsp/jstl/core" prefix="c" %>
<%@ taglib uri="http://java.sun.com/jsp/jstl/fmt" prefix="fmt" %>
<!DOCTYPE html>
<html>
<%@ taglib uri="http://java.sun.com/jsp/jstl/core" prefix="c" %>
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Services Médicaux</title>
    <link rel="stylesheet" href="css/mesStyles.css">
</head>
<body>
    <div class="services-container">
        <h2>Nos Services Médicaux</h2>
        
        <!-- Grille des services -->
        <div class="services-grid">
            <c:forEach var="service" items="${services}">
                <div class="service-card">
                    <div class="service-icon">
                        🦷
                    </div>
                    <h3>${service.nomSM}</h3>
                    <p class="service-type">${service.typeSM}</p>
                    <p class="service-description">${service.descriptionSM}</p>
                    <p class="service-tarif">
                        <span class="prix">${service.tarifSM} DT</span>
                    </p>
                    <a href="rendezvous?service=${service.numSM}" class="btn-secondary">
                        Réserver
                    </a>
                </div>
            </c:forEach>
        </div>
    </div>
</body>
</html>