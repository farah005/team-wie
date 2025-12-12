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
    <title>Liste des Dentistes</title>
    <link rel="stylesheet" href="css/mesStyles.css">
</head>
<body>
    <div class="dentistes-container">
        <h2>Liste des Dentistes Disponibles</h2>
        
        <!-- Filtre par spécialité -->
        <form action="listeDentistes" method="get" class="filter-form">
            <label for="specialite">Filtrer par spécialité:</label>
            <select name="specialite" id="specialite" onchange="this.form.submit()">
                <option value="">Toutes les spécialités</option>
                <option value="Orthodontie">Orthodontie</option>
                <option value="Chirurgie">Chirurgie dentaire</option>
                <option value="Implantologie">Implantologie</option>
                <option value="Pédodontie">Pédodontie</option>
                <option value="Esthétique">Esthétique dentaire</option>
            </select>
        </form>
        
        <!-- Liste des dentistes -->
        <div class="dentistes-grid">
            <c:choose>
                <c:when test="${not empty dentistes}">
                    <c:forEach var="dentiste" items="${dentistes}">
                        <div class="dentiste-card">
                            <div class="dentiste-photo">
                                <c:choose>
                                    <c:when test="${not empty dentiste.photoD}">
                                        <img src="images/${dentiste.photoD}" alt="${dentiste.nomD}">
                                    </c:when>
                                    <c:otherwise>
                                        <img src="images/default-dentist.png" alt="Photo par défaut">
                                    </c:otherwise>
                                </c:choose>
                            </div>
                            
                            <div class="dentiste-info">
                                <h3>Dr. ${dentiste.nomD} ${dentiste.prenomD}</h3>
                                <p class="specialite">${dentiste.specialiteD}</p>
                                <p class="email">📧 ${dentiste.emailD}</p>
                                <p class="tel">📞 ${dentiste.telD}</p>
                            </div>
                            
                            <div class="dentiste-actions">
                                <a href="rendezvous?idDentiste=${dentiste.idD}" class="btn-primary">
                                    Prendre RDV
                                </a>
                            </div>
                        </div>
                    </c:forEach>
                </c:when>
                <c:otherwise>
                    <p class="no-results">Aucun dentiste trouvé.</p>
                </c:otherwise>
            </c:choose>
        </div>
    </div>
</body>
</html>