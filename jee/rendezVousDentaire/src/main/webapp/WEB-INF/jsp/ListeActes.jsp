<%@ page language="java" contentType="text/html; charset=UTF-8" pageEncoding="UTF-8"%>
<%@ taglib uri="http://java.sun.com/jsp/jstl/core" prefix="c" %>
<%@ taglib uri="http://java.sun.com/jsp/jstl/fmt" prefix="fmt" %>
<%@ taglib uri="http://java.sun.com/jsp/jstl/functions" prefix="fn" %>
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <title>Historique des Actes Médicaux</title>
    <link rel="stylesheet" type="text/css" href="${pageContext.request.contextPath}/css/mesStyles.css">
    <style>
        .container { padding: 20px; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
        .table-acte { width: 100%; border-collapse: collapse; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }
        .table-acte th { background-color: #2c3e50; color: white; padding: 12px; text-align: left; }
        .table-acte td { padding: 12px; border-bottom: 1px solid #eee; }
        .info-patient { font-weight: bold; color: #2980b9; }
        .info-service { font-style: italic; color: #7f8c8d; }
        .price { font-weight: bold; color: #27ae60; }
        .action-links a { color: #e74c3c; text-decoration: none; font-size: 0.9em; }
        .btn-add { display: inline-block; background: #3498db; color: white; padding: 10px 15px; 
                   text-decoration: none; border-radius: 4px; margin-bottom: 20px; }
    </style>
</head>
<body>

<div class="container">
    <h2>Historique des Actes Médicaux</h2>

    <div style="margin-bottom: 20px;">
        <c:if test="${fn:toLowerCase(sessionScope.userType) == 'aide-soignant' || fn:toLowerCase(sessionScope.userType) == 'dentiste'}">
            <a href="${pageContext.request.contextPath}/actemedical" class="btn-add">
                + Enregistrer un nouvel acte
            </a>
        </c:if>
    </div>

    <c:if test="${not empty message}">
        <div style="background: #d4edda; color: #155724; padding: 10px; border-radius: 4px; margin-bottom: 15px;">
            ${message}
        </div>
    </c:if>

    <table class="table-acte">
        <thead>
            <tr>
                <th>Date RV</th>
                <th>Patient</th>
                <th>Service / Acte</th>
                <th>Dentiste</th>
                <th>Tarif</th>
                <th>Actions</th>
            </tr>
        </thead>
        <tbody>
            <c:forEach var="acte" items="${actes}">
                <tr>
                    <td>
                        <fmt:formatDate value="${acte.rendezvous.dateRv}" pattern="dd/MM/yyyy HH:mm" />
                    </td>
                    <td>
                        <div class="info-patient">${acte.patient.nomP} ${acte.patient.prenomP}</div>
                        <small>ID: ${acte.rendezvous.idRv}</small>
                    </td>
                    <td>
                        <strong>${acte.serviceMedical.nomSM}</strong><br/>
                        <span class="info-service">${acte.descriptionAM}</span>
                    </td>
                    <td>Dr. ${acte.dentiste.nomD}</td>
                    <td class="price">
                        <fmt:formatNumber value="${acte.tarifAM}" type="currency" currencySymbol="TND" />
                    </td>
                    <td class="action-links">
                        <c:if test="${sessionScope.userType == 'aide-soignant' || sessionScope.userType == 'dentiste'}">
                            <form action="${pageContext.request.contextPath}/actemedical" method="post" 
                                  onsubmit="return confirm('Supprimer cet acte ?');">
                                <input type="hidden" name="action" value="delete">
                                <input type="hidden" name="id" value="${acte.idAM}">
                                <button type="submit" style="background:none; border:none; color:red; cursor:pointer;">
                                    Supprimer
                                </button>
                            </form>
                        </c:if>
                    </td>
                </tr>
            </c:forEach>

            <c:if test="${empty actes}">
                <tr>
                    <td colspan="6" style="text-align:center; padding: 30px; color: #95a5a6;">
                        Aucun acte médical enregistré.
                    </td>
                </tr>
            </c:if>
        </tbody>
    </table>
</div>

</body>
</html>