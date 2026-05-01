<%@ page language="java" contentType="text/html; charset=UTF-8" pageEncoding="UTF-8"%>
<%@ taglib uri="http://java.sun.com/jsp/jstl/core" prefix="c" %>
<%@ taglib uri="http://java.sun.com/jsp/jstl/fmt" prefix="fmt" %>
<%@ taglib uri="http://java.sun.com/jsp/jstl/functions" prefix="fn" %>
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <title>Liste des Services Médicaux</title>
    <link rel="stylesheet" type="text/css" href="${pageContext.request.contextPath}/css/mesStyles.css">
    <style>
        .table-container { margin: 20px; font-family: Arial, sans-serif; }
        table { width: 100%; border-collapse: collapse; margin-top: 20px; background: white; }
        th, td { border: 1px solid #ddd; padding: 12px; text-align: left; }
        th { background-color: #f4f7f6; color: #333; }
        tr:nth-child(even) { background-color: #f9f9f9; }
        tr:hover { background-color: #f1f1f1; }
        .badge { padding: 5px 10px; border-radius: 4px; font-size: 0.85em; background: #e0f2f1; color: #00796b; }
        .btn-edit { color: #2196F3; text-decoration: none; margin-right: 10px; font-weight: bold; }
        .btn-delete { color: #f44336; background: none; border: none; cursor: pointer; font-weight: bold; padding: 0; font-size: 1em; }
        .header-actions { display: flex; justify-content: space-between; align-items: center; }
    </style>
</head>
<body>

    <div class="table-container">
        <div class="header-actions">
            <h2>Répertoire des Services Médicaux</h2>
            <c:if test="${fn:toLowerCase(sessionScope.userType) == 'aide-soignant' || fn:toLowerCase(sessionScope.userType) == 'dentiste'}">
                <a href="${pageContext.request.contextPath}/service" class="btn-primary" style="text-decoration: none; padding: 10px 20px; background: #4CAF50; color: white; border-radius: 5px;">
                    + Ajouter un nouveau service
                </a>
            </c:if>
        </div>

        <c:if test="${not empty message}">
            <div class="success-message" style="color: green; padding: 10px; background: #e8f5e9; border: 1px solid #c8e6c9; margin: 10px 0;">
                ${message}
            </div>
        </c:if>

        <table>
            <thead>
                <tr>
                    <th>ID</th>
                    <th>Nom du Service</th>
                    <th>Catégorie / Type</th>
                    <th>Tarif</th>
                    <th>Description</th>
                    <th>Actions</th>
                </tr>
            </thead>
            <tbody>
                <c:forEach var="s" items="${services}">
                    <tr>
                        <td><strong>#${s.numSM}</strong></td>
                        <td>${s.nomSM}</td>
                        <td><span class="badge">${s.typeSM}</span></td>
                        <td>
                            <fmt:formatNumber value="${s.tarifSM}" type="currency" currencySymbol="TND" />
                        </td>
                        <td>
                            <small>${not empty s.descriptionSM ? s.descriptionSM : '---'}</small>
                        </td>
                        <td>
                            <c:if test="${fn:toLowerCase(sessionScope.userType) == 'aide-soignant' || fn:toLowerCase(sessionScope.userType) == 'dentiste'}">
                                <a href="${pageContext.request.contextPath}/service?action=edit&id=${s.numSM}" class="btn-edit">
                                    ✎ Modifier
                                </a>

                                <form action="${pageContext.request.contextPath}/service" method="post" style="display:inline;" onsubmit="return confirmerSuppression();">
                                    <input type="hidden" name="action" value="delete">
                                    <input type="hidden" name="id" value="${s.numSM}">
                                    <button type="submit" class="btn-delete">🗑 Supprimer</button>
                                </form>
                            </c:if>
                        </td>
                    </tr>
                </c:forEach>
                
                <c:if test="${empty services}">
                    <tr>
                        <td colspan="6" style="text-align: center; padding: 20px;">
                            Aucun service trouvé dans la base de données.
                        </td>
                    </tr>
                </c:if>
            </tbody>
        </table>
    </div>

    <script>
        function confirmerSuppression() {
            return confirm("Êtes-vous sûr de vouloir supprimer ce service ? Cette action est irréversible.");
        }
    </script>

</body>
