<%@ page language="java" contentType="text/html; charset=UTF-8" pageEncoding="UTF-8"%>
<%@ taglib uri="http://java.sun.com/jsp/jstl/core" prefix="c" %>
<%@ taglib uri="http://java.sun.com/jsp/jstl/fmt" prefix="fmt" %>
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Rendez-vous</title>
    <link rel="stylesheet" href="css/mesStyles.css">
</head>
<body>
    <div class="rdv-container">
        <h2>Gestion des Rendez-vous</h2>
        
        <!-- Formulaire de prise de RDV -->
        <div class="rdv-form-section">
            <h3>Prendre un nouveau rendez-vous</h3>
            
            <% if (request.getAttribute("error") != null) { %>
                <div class="error-message">
                    <%= request.getAttribute("error") %>
                </div>
            <% } %>
            
            <form action="rendezvous" method="post" class="rdv-form">
                <div class="form-group">
                    <label for="idDentiste">Choisir un dentiste *</label>
                    <select name="idDentiste" id="idDentiste" required>
                        <option value="">Sélectionner un dentiste</option>
                        <c:forEach var="dentiste" items="${dentistes}">
                            <option value="${dentiste.idD}">
                                Dr. ${dentiste.nomD} ${dentiste.prenomD} - ${dentiste.specialiteD}
                            </option>
                        </c:forEach>
                    </select>
                </div>
                
                <div class="form-row">
                    <div class="form-group">
                        <label for="dateRdv">Date du rendez-vous *</label>
                        <input type="date" id="dateRdv" name="dateRdv" required>
                    </div>
                    
                    <div class="form-group">
                        <label for="heureRdv">Heure *</label>
                        <input type="time" id="heureRdv" name="heureRdv" required>
                    </div>
                </div>
                
                <div class="form-group">
                    <label for="details">Détails / Motif de la consultation</label>
                    <textarea id="details" name="details" rows="4"></textarea>
                </div>
                
                <button type="submit" class="btn-primary">Confirmer le rendez-vous</button>
            </form>
        </div>
        
        <!-- Liste des RDV existants -->
        <div class="rdv-list-section">
            <h3>Mes rendez-vous</h3>
            
            <c:choose>
                <c:when test="${not empty rendezvous}">
                    <table class="rdv-table">
                        <thead>
                            <tr>
                                <th>Date</th>
                                <th>Heure</th>
                                <th>Dentiste</th>
                                <th>Statut</th>
                                <th>Actions</th>
                            </tr>
                        </thead>
                        <tbody>
                            <c:forEach var="rdv" items="${rendezvous}">
                                <tr>
                                    <td>${rdv.dateRv}</td>
                                    <td>${rdv.heureRv}</td>
                                    <td>Dr. ${rdv.dentiste.nomD} ${rdv.dentiste.prenomD}</td>
                                    <td>
                                        <span class="statut-badge statut-${rdv.statutRv}">
                                            ${rdv.statutRv}
                                        </span>
                                    </td>
                                    <td class="actions">
                                        <a href="modifierRendezvous?id=${rdv.idRv}" class="btn-edit">
                                            Modifier
                                        </a>
                                        <a href="modifierRendezvous?id=${rdv.idRv}&action=annuler" 
                                           class="btn-cancel"
                                           onclick="return confirm('Êtes-vous sûr de vouloir annuler ce rendez-vous ?')">
                                            Annuler
                                        </a>
                                    </td>
                                </tr>
                            </c:forEach>
                        </tbody>
                    </table>
                </c:when>
                <c:otherwise>
                    <p class="no-results">Vous n'avez pas encore de rendez-vous.</p>
                </c:otherwise>
            </c:choose>
        </div>
    </div>
</body>
</html>