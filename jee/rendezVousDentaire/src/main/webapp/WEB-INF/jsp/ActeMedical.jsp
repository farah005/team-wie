<%@ page language="java" contentType="text/html; charset=UTF-8" pageEncoding="UTF-8"%>
<%@ taglib uri="http://java.sun.com/jsp/jstl/core" prefix="c" %>
<%@ taglib uri="http://java.sun.com/jsp/jstl/functions" prefix="fn" %>
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <title>Enregistrer un acte médical</title>
    <link rel="stylesheet" type="text/css" href="${pageContext.request.contextPath}/css/mesStyles.css">
</head>
<body>
    <div class="form-container">
        <h2>Enregistrer un acte médical</h2>

        <c:if test="${not empty erreur}">
            <div style="color: red; margin-bottom: 12px;">${erreur}</div>
        </c:if>

        <c:if test="${fn:toLowerCase(sessionScope.userType) == 'aide-soignant' || fn:toLowerCase(sessionScope.userType) == 'dentiste'}">
            <form action="${pageContext.request.contextPath}/actemedical" method="post">
                <input type="hidden" name="action" value="create">

                <div class="form-group">
                    <label for="idRv">ID Rendez-vous *</label>
                    <input type="number" id="idRv" name="idRv" value="${param.idRv}" required>
                </div>

                <div class="form-group">
                    <label for="numSM">Service médical *</label>
                    <select id="numSM" name="numSM" required>
                        <c:forEach items="${services}" var="s">
                            <option value="${s.numSM}" ${param.numSM == s.numSM ? 'selected' : ''}>${s.nomSM} — ${s.typeSM}</option>
                        </c:forEach>
                    </select>
                </div>

                <div class="form-group">
                    <label for="description">Description</label>
                    <textarea id="description" name="description" rows="3">${param.description}</textarea>
                </div>

                <div class="form-group">
                    <label for="tarif">Tarif (TND)</label>
                    <input type="number" step="0.01" id="tarif" name="tarif" value="${param.tarif}">
                </div>

                <div class="form-actions">
                    <button type="submit" class="btn-primary">Enregistrer l'acte</button>
                    <a href="${pageContext.request.contextPath}/actemedical?action=list" class="btn-secondary">Retour</a>
                </div>
            </form>
        </c:if>

        <c:if test="${not (fn:toLowerCase(sessionScope.userType) == 'aide-soignant' || fn:toLowerCase(sessionScope.userType) == 'dentiste')}">
            <div style="color: #a00;">Accès refusé : vous n'avez pas les droits pour enregistrer un acte.</div>
        </c:if>
    </div>
</body>
</html>
