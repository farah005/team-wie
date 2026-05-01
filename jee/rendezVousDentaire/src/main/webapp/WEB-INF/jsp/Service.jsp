<%@ page language="java" contentType="text/html; charset=UTF-8" pageEncoding="UTF-8"%>
<%@ taglib uri="http://java.sun.com/jsp/jstl/core" prefix="c" %>
<%@ taglib uri="http://java.sun.com/jsp/jstl/functions" prefix="fn" %>
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <title>Gestion Service Médical</title>
    <link rel="stylesheet" type="text/css" href="${pageContext.request.contextPath}/css/mesStyles.css">
</head>
<body>
    <div class="form-container">
        <%-- Titre dynamique et formulaire réservés aux aides-soignants et dentistes --%>
        <c:if test="${fn:toLowerCase(sessionScope.userType) == 'aide-soignant' || fn:toLowerCase(sessionScope.userType) == 'dentiste'}">
            <h2>${not empty serviceToEdit ? "Modifier le Service" : "Nouveau Service Médical"}</h2>
            
            <%-- Messages d'alerte --%>
            <c:if test="${not empty erreur}">
                <div class="error-message" style="color: red; padding: 10px; border: 1px solid red; margin-bottom: 10px;">
                    ${erreur}
                </div>
            </c:if>
            
            <form action="${pageContext.request.contextPath}/service" method="post">
                <%-- Détermine l'action pour la Servlet --%>
                <input type="hidden" name="action" value="${not empty serviceToEdit ? 'update' : 'create'}">
                
                <%-- ID caché nécessaire pour l'Update --%>
                <c:if test="${not empty serviceToEdit}">
                    <input type="hidden" name="id" value="${serviceToEdit.numSM}">
                </c:if>

                <div class="form-group">
                    <label for="nom">Nom du service * :</label>
                    <input type="text" id="nom" name="nom" 
                           value="${not empty serviceToEdit ? serviceToEdit.nomSM : ''}" 
                           required maxlength="100">
                </div>

                <div class="form-row">
                    <div class="form-group">
                        <label for="type">Type de service * :</label>
                        <input type="text" id="type" name="type" 
                               value="${not empty serviceToEdit ? serviceToEdit.typeSM : ''}" 
                               required placeholder="Ex: Chirurgie, Consultation">
                    </div>

                    <div class="form-group">
                        <label for="tarif">Tarif (TND) :</label>
                        <input type="number" id="tarif" name="tarif" step="0.01" 
                               value="${not empty serviceToEdit ? serviceToEdit.tarifSM : ''}">
                    </div>
                </div>

                <div class="form-group">
                    <label for="description">Description :</label>
                    <textarea id="description" name="description" rows="4">${not empty serviceToEdit ? serviceToEdit.descriptionSM : ''}</textarea>
                </div>

                <div class="form-actions">
                    <button type="submit" class="btn-primary">
                        ${not empty serviceToEdit ? "Enregistrer les modifications" : "Créer le service"}
                    </button>
                    <a href="${pageContext.request.contextPath}/service?action=list" class="btn-secondary" style="text-decoration: none;">
                        Annuler et retourner à la liste
                    </a>
                </div>
            </form>
        </c:if>

        <hr>

        <%-- Section de recherche améliorée --%>
        <div class="search-section">
            <h3>Rechercher un service existant</h3>
            <form action="${pageContext.request.contextPath}/service" method="post">
                <input type="hidden" name="action" value="search">
                <input type="text" name="nomRecherche" placeholder="Rechercher par nom (ex: endo)..." value="${param.nomRecherche}">
                <select name="typeRecherche">
                    <option value="">[Tous types]</option>
                    <c:forEach items="${types}" var="t">
                        <option value="${t}" ${param.typeRecherche == t ? 'selected' : ''}>${t}</option>
                    </c:forEach>
                </select>
                <button type="submit">Rechercher</button>
            </form>
        </div>
        
        <%-- Affichage des résultats de recherche s'ils existent --%>
        <c:if test="${not empty services}">
            <div class="results-table">
                <h3>Résultats de la recherche :</h3>
                <table border="1" width="100%">
                    <thead>
                        <tr>
                            <th>Nom</th>
                            <th>Type</th>
                            <th>Tarif</th>
                            <th>Actions</th>
                        </tr>
                    </thead>
                    <tbody>
                        <c:forEach var="s" items="${services}">
                            <tr>
                                <td>${s.nomSM}</td>
                                <td>${s.typeSM}</td>
                                <td>${s.tarifSM} TND</td>
                                <td>
                                    <c:if test="${fn:toLowerCase(sessionScope.userType) == 'aide-soignant' || fn:toLowerCase(sessionScope.userType) == 'dentiste'}">
                                        <a href="${pageContext.request.contextPath}/service?action=edit&id=${s.numSM}">Modifier</a>
                                    </c:if>
                                </td>
                            </tr>
                        </c:forEach>
                    </tbody>
                </table>
            </div>
        </c:if>
    </div>
</body>
</html>