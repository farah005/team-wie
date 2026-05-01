<%@ page language="java" contentType="text/html; charset=UTF-8" pageEncoding="UTF-8"%>
<%@ taglib uri="http://java.sun.com/jsp/jstl/core" prefix="c" %>

<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <title>Nos Praticiens — Cabinet Sourire</title>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" type="text/css" href="${pageContext.request.contextPath}/css/mesStyles.css">
    <style>
        .dentists-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
            gap: 25px;
            margin-top: 30px;
        }
        
        .dentist-card {
            background: white;
            border-radius: 15px;
            padding: 30px;
            text-align: center;
            transition: 0.3s ease;
            box-shadow: 0 10px 30px rgba(0,0,0,0.05);
            border: 1px solid rgba(74, 63, 53, 0.05);
        }
        
        .dentist-card:hover {
            transform: translateY(-8px);
            border-color: var(--accent-rose);
        }
        
        .photo-circle {
            width: 100px;
            height: 100px;
            margin: 0 auto 20px;
            background: var(--bg-nude);
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 40px;
            border: 2px solid var(--accent-rose);
        }

        .search-bar {
            width: 100%;
            max-width: 500px;
            margin: 0 auto 40px;
            display: flex;
            gap: 10px;
        }

        .badge-spec {
            display: inline-block;
            padding: 4px 12px;
            background: #F0F4FF;
            color: #4A69BD;
            border-radius: 50px;
            font-size: 0.75rem;
            font-weight: 700;
            margin-bottom: 10px;
        }
    </style>
</head>
<body>
    <%-- Inclusion du Header (Barre de navigation) --%>
    <%@ include file="header.jsp" %>

    <div class="form-container" style="max-width: 1100px;">
        <div style="text-align: center; margin-bottom: 40px;">
            <h2 style="font-family: 'Playfair Display', serif; font-size: 2.5rem;">Nos Praticiens</h2>
            <p style="color: #888;">Rencontrez notre équipe d'experts pour vos soins dentaires.</p>
        </div>

        <%-- Barre de recherche et filtres --%>
        <div class="search-bar">
            <input type="text" id="searchInput" placeholder="Rechercher par nom ou spécialité..." onkeyup="filterDentists()">
            <c:if test="${sessionScope.userType == 'aide-soignant'}">
                <a href="dentiste?action=addForm" class="btn-primary" style="width: auto; padding: 10px 20px; font-size: 0.8rem;">+ Ajouter</a>
            </c:if>
        </div>

        <%-- Grille des dentistes --%>
        <div class="dentists-grid" id="dentistsGrid">
            <c:forEach var="d" items="${dentistes}">
                <div class="dentist-card" data-name="${d.nomD.toLowerCase()} ${d.prenomD.toLowerCase()}" data-spec="${d.specialiteD.toLowerCase()}">
                    <div class="photo-circle">
                        <c:choose>
                            <c:when test="${not empty d.photoD}">
                                <img src="${pageContext.request.contextPath}/uploads/${d.photoD}" style="width:100%; height:100%; border-radius:50%; object-fit:cover;">
                            </c:when>
                            <c:otherwise>
                                ${d.sexeD == 'M' ? '👨‍⚕️' : '👩‍⚕️'}
                            </c:otherwise>
                        </c:choose>
                    </div>

                    <span class="badge-spec">${d.specialiteD}</span>
                    <h3 style="margin-bottom: 5px;">Dr. ${d.nomD} ${d.prenomD}</h3>
                    <p style="font-size: 0.85rem; color: #6B5B4B; margin-bottom: 20px;">
                        <i class="email-icon">📧</i> ${d.emailD}
                    </p>

                    <div style="display: flex; gap: 10px; justify-content: center;">
                        <a href="dentiste?action=view&id=${d.idD}" class="btn-secondary" style="padding: 8px 15px; font-size: 0.7rem; border: 1px solid #DDD; border-radius: 50px; text-decoration: none; color: #4A3F35;">Voir Profil</a>
                        <a href="rendezvous?idDentiste=${d.idD}" class="btn-primary" style="padding: 8px 15px; font-size: 0.7rem; width: auto;">Prendre RDV</a>
                    </div>
                    
                    <%-- Actions réservées à l'aide-soignant --%>
                    <c:if test="${sessionScope.userType == 'aide-soignant'}">
                        <div style="margin-top: 15px; border-top: 1px solid #EEE; padding-top: 10px;">
                            <a href="dentiste?action=delete&id=${d.idD}" style="color: #C0392B; text-decoration: none; margin-right: 12px;" 
                               onclick="return confirm('Confirmer la suppression du dentiste ?');">Supprimer</a>
                            <a href="dentiste?action=editForm&id=${d.idD}" style="color: #4A3F35; text-decoration: none;">Modifier</a>
                        </div>
                    </c:if>
                </div>
            </c:forEach>
        </div>

        <script>
            function filterDentists() {
                var input = document.getElementById('searchInput').value.toLowerCase();
                var grid = document.getElementById('dentistsGrid');
                var cards = grid.querySelectorAll('.dentist-card');
                cards.forEach(function(card){
                    var name = card.getAttribute('data-name') || '';
                    var spec = card.getAttribute('data-spec') || '';
                    if (name.indexOf(input) > -1 || spec.indexOf(input) > -1) {
                        card.style.display = '';
                    } else {
                        card.style.display = 'none';
                    }
                });
            }
        </script>

    </div>

</body>
</html>