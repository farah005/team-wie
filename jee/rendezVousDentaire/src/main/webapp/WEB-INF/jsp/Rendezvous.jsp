<%@ page language="java" contentType="text/html; charset=UTF-8" pageEncoding="UTF-8"%>
<%@ taglib uri="http://java.sun.com/jsp/jstl/core" prefix="c" %>
<%@ taglib uri="http://java.sun.com/jsp/jstl/fmt" prefix="fmt" %>

<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <title>Agenda — Make sure to smile everyday</title>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" type="text/css" href="${pageContext.request.contextPath}/css/mesStyles.css">
    <style>
        /* Styles spécifiques à la page de gestion */
        .list-section { margin-top: 30px; background: white; padding: 25px; border-radius: 12px; box-shadow: 0 4px 20px rgba(0,0,0,0.05); }
        table { width: 100%; border-collapse: collapse; margin-top: 15px; }
        th { background-color: #F9F7F2; color: #4A3F35; padding: 12px; text-align: left; border-bottom: 2px solid #E5E1DA; }
        td { padding: 12px; border-bottom: 1px solid #F0EDE9; color: #6B5B4B; }
        
        .status-badge { padding: 4px 10px; border-radius: 20px; font-size: 0.75rem; font-weight: 600; }
        .en.attente { background: #FFF4E5; color: #B07D31; }
        .confirmé { background: #E5F9F0; color: #2D8A5C; }
        .annulé { background: #FDECEC; color: #C0392B; }
        
        .btn-confirm { background: #2D8A5C; color: white; border: none; padding: 6px 12px; border-radius: 4px; cursor: pointer; }
        .readonly-input { background-color: #F8F9FA; color: #888; border: 1px solid #DDD; }
    </style>
</head>
<body>
    <%-- Inclusion du Header (Barre de navigation et Déconnexion) --%>
    <%@ include file="header.jsp" %>

    <div class="form-container">
        <%-- Zone des Messages --%>
        <c:if test="${not empty erreur}">
            <div class="error-message"><strong>⚠️ Erreur :</strong> ${erreur}</div>
        </c:if>
        <c:if test="${not empty message}">
            <div class="success-message" style="background:#E5F9F0; color:#2D8A5C; padding:15px; border-radius:8px; margin-bottom:20px; border:1px solid #CCF2E0;">
                <strong>✅ Succès :</strong> ${message}
            </div>
        </c:if>

        <%-- Formulaire de Prise de RDV --%>
        <div class="appointment-section">
            <h3 style="color: #4A3F35; border-bottom: 2px solid #F9F7F2; padding-bottom: 10px;">Prendre un rendez-vous</h3>
            <form action="rendezvous" method="post" id="rvForm">
                <input type="hidden" name="action" value="create">
                
                <div class="form-row" style="display: flex; gap: 20px; margin-top: 15px;">
                    <div class="form-group" style="flex: 1;">
                        <label>ID Patient :</label>
                        <input type="number" name="idPatient" required 
                               value="${sessionScope.userType == 'patient' ? sessionScope.idConnecte : ''}"
                               ${sessionScope.userType == 'patient' ? 'readonly' : ''}
                               class="${sessionScope.userType == 'patient' ? 'readonly-input' : ''}">
                    </div>
                    
                    <div class="form-group" style="flex: 1;">
                        <label>Dentiste :</label>
                        <select name="idDentiste" required>
                            <option value="">-- Choisir un praticien --</option>
                            <c:forEach items="${lesDentistes}" var="d">
                                <option value="${d.idD}">Dr. ${d.nomD} (${d.specialite})</option>
                            </c:forEach>
                        </select>
                    </div>
                </div>
                
                <div class="form-row" style="display: flex; gap: 20px; margin-top: 15px;">
                    <div class="form-group" style="flex: 1;">
                        <label>Date :</label>
                        <input type="date" id="dateRv" name="dateRv" required>
                    </div>
                    <div class="form-group" style="flex: 1;">
                        <label>Heure (08:00 - 18:00) :</label>
                        <input type="time" id="heureRv" name="heureRv" required step="1800">
                    </div>
                </div>
                
                <button type="submit" class="btn-primary" style="margin-top: 20px;">Confirmer le rendez-vous</button>
            </form>
        </div>

        <%-- Liste des RDVs --%>
        <div class="list-section">
            <h3 style="color: #4A3F35;">${sessionScope.userType == 'aide-soignant' ? 'Tous les rendez-vous' : 'Mes consultations'}</h3>
            <table>
                <thead>
                    <tr>
                        <th>Date & Heure</th>
                        <c:if test="${sessionScope.userType == 'aide-soignant'}"><th>Patient</th></c:if>
                        <th>Dentiste</th>
                        <th>Statut</th>
                        <th>Actions</th>
                    </tr>
                </thead>
                <tbody>
                    <c:forEach items="${listeRdvs}" var="rdv">
                        <tr>
                            <td>
                                <strong><fmt:formatDate value="${rdv.dateRv}" pattern="dd/MM/yyyy" /></strong> 
                                à ${rdv.heureRv}
                            </td>
                            <c:if test="${sessionScope.userType == 'aide-soignant'}">
                                <td>${rdv.patient.nomP} ${rdv.patient.prenomP}</td>
                            </c:if>
                            <td>Dr. ${rdv.dentiste.nomD}</td>
                            <td>
                                <span class="status-badge ${rdv.statutRv.toLowerCase().replace(' ', '.')}">
                                    ${rdv.statutRv}
                                </span>
                            </td>
                            <td>
                                <c:if test="${sessionScope.userType == 'aide-soignant' && rdv.statutRv == 'En attente'}">
                                    <form action="rendezvous" method="post" style="display:inline;">
                                        <input type="hidden" name="action" value="updateStatut">
                                        <input type="hidden" name="id" value="${rdv.idRv}">
                                        <input type="hidden" name="statut" value="Confirmé">
                                        <button type="submit" class="btn-confirm">Valider</button>
                                    </form>
                                </c:if>
                                <a href="rendezvous?action=delete&id=${rdv.idRv}" style="color:red; margin-left:10px;" 
                                   onclick="return confirm('Annuler ce RDV ?')">Annuler</a>
                            </td>
                           <td>
                            
                        </tr>
                    </c:forEach>
                </tbody>
            </table>
        </div>
    </div>

    <script>
        // Sécurité Date : pas de passé
        document.getElementById('dateRv').min = new Date().toISOString().split('T')[0];
        
        // Sécurité Heure : entre 08h et 18h
        document.getElementById('rvForm').onsubmit = function(e) {
            const h = parseInt(document.getElementById('heureRv').value.split(':')[0]);
            if (h < 8 || h >= 18) {
                e.preventDefault();
                alert("Le cabinet est ouvert de 08:00 à 18:00 uniquement.");
            }
        };
    </script>
</body>
</html>
