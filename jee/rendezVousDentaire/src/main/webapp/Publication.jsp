<%@ page language="java" contentType="text/html; charset=UTF-8" pageEncoding="UTF-8"%>
<%@ taglib uri="http://java.sun.com/jsp/jstl/core" prefix="c" %>
<%@ taglib uri="http://java.sun.com/jsp/jstl/fmt" prefix="fmt" %>
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Publications et Statistiques</title>
    <link rel="stylesheet" href="css/mesStyles.css">
</head>
<body>
    <div class="publication-container">
        <h2>Tableau de Bord</h2>
        
        <!-- Menu de navigation -->
        <div class="pub-menu">
            <a href="publication?action=statistiques" class="tab ${action == 'statistiques' ? 'active' : ''}">
                📊 Statistiques
            </a>
            <a href="publication?action=patients" class="tab ${action == 'patients' ? 'active' : ''}">
                👥 Patients
            </a>
            <a href="publication?action=dentistes" class="tab ${action == 'dentistes' ? 'active' : ''}">
                👨‍⚕️ Dentistes
            </a>
            <a href="publication?action=rendezvous" class="tab ${action == 'rendezvous' ? 'active' : ''}">
                📅 Rendez-vous
            </a>
            <a href="publication?action=services" class="tab ${action == 'services' ? 'active' : ''}">
                🦷 Services
            </a>
        </div>
        
        <!-- Contenu selon l'action -->
        <div class="pub-content">
            <c:choose>
                <%-- STATISTIQUES --%>
                <c:when test="${action == 'statistiques' or empty action}">
                    <div class="stats-grid">
                        <div class="stat-card">
                            <div class="stat-icon">👥</div>
                            <div class="stat-number">${totalPatients}</div>
                            <div class="stat-label">Patients</div>
                        </div>
                        
                        <div class="stat-card">
                            <div class="stat-icon">👨‍⚕️</div>
                            <div class="stat-number">${totalDentistes}</div>
                            <div class="stat-label">Dentistes</div>
                        </div>
                        
                        <div class="stat-card">
                            <div class="stat-icon">📅</div>
                            <div class="stat-number">${totalRendezvous}</div>
                            <div class="stat-label">Rendez-vous</div>
                        </div>
                        
                        <div class="stat-card">
                            <div class="stat-icon">🦷</div>
                            <div class="stat-number">${totalServices}</div>
                            <div class="stat-label">Services</div>
                        </div>
                    </div>
                    
                    <div class="charts-section">
                        <div class="chart-box">
                            <h3>Rendez-vous par statut</h3>
                            <ul class="stat-list">
                                <li>En attente: <strong>${rdvEnAttente}</strong></li>
                                <li>Confirmés: <strong>${rdvConfirmes}</strong></li>
                                <li>Terminés: <strong>${rdvTermines}</strong></li>
                                <li>Annulés: <strong>${rdvAnnules}</strong></li>
                            </ul>
                        </div>
                        
                        <div class="chart-box">
                            <h3>Patients par sexe</h3>
                            <ul class="stat-list">
                                <li>Hommes: <strong>${patientsHommes}</strong></li>
                                <li>Femmes: <strong>${patientsFemmes}</strong></li>
                            </ul>
                        </div>
                        
                        <div class="chart-box">
                            <h3>Patients par groupe sanguin</h3>
                            <ul class="stat-list">
                                <li>Groupe A: <strong>${groupeA}</strong></li>
                                <li>Groupe B: <strong>${groupeB}</strong></li>
                                <li>Groupe O: <strong>${groupeO}</strong></li>
                                <li>Groupe AB: <strong>${groupeAB}</strong></li>
                            </ul>
                        </div>
                    </div>
                </c:when>
                
                <%-- LISTE DES PATIENTS --%>
                <c:when test="${action == 'patients'}">
                    <h3>Liste des Patients</h3>
                    <table class="data-table">
                        <thead>
                            <tr>
                                <th>ID</th>
                                <th>Nom</th>
                                <th>Prénom</th>
                                <th>Email</th>
                                <th>Sexe</th>
                                <th>Groupe Sanguin</th>
                            </tr>
                        </thead>
                        <tbody>
                            <c:forEach var="patient" items="${patients}">
                                <tr>
                                    <td>${patient.idP}</td>
                                    <td>${patient.nomP}</td>
                                    <td>${patient.prenomP}</td>
                                    <td>${patient.emailP}</td>
                                    <td>${patient.sexeP}</td>
                                    <td>${patient.groupeSanguinP}</td>
                                </tr>
                            </c:forEach>
                        </tbody>
                    </table>
                </c:when>
                
                <%-- LISTE DES DENTISTES --%>
                <c:when test="${action == 'dentistes'}">
                    <h3>Liste des Dentistes</h3>
                    <table class="data-table">
                        <thead>
                            <tr>
                                <th>ID</th>
                                <th>Nom</th>
                                <th>Prénom</th>
                                <th>Spécialité</th>
                                <th>Email</th>
                                <th>Téléphone</th>
                            </tr>
                        </thead>
                        <tbody>
                            <c:forEach var="dentiste" items="${dentistes}">
                                <tr>
                                    <td>${dentiste.idD}</td>
                                    <td>${dentiste.nomD}</td>
                                    <td>${dentiste.prenomD}</td>
                                    <td>${dentiste.specialiteD}</td>
                                    <td>${dentiste.emailD}</td>
                                    <td>${dentiste.telD}</td>
                                </tr>
                            </c:forEach>
                        </tbody>
                    </table>
                </c:when>
                
                <%-- LISTE DES RENDEZ-VOUS --%>
                <c:when test="${action == 'rendezvous'}">
                    <h3>Liste des Rendez-vous</h3>
                    <table class="data-table">
                        <thead>
                            <tr>
                                <th>ID</th>
                                <th>Patient</th>
                                <th>Dentiste</th>
                                <th>Date</th>
                                <th>Heure</th>
                                <th>Statut</th>
                            </tr>
                        </thead>
                        <tbody>
                            <c:forEach var="rdv" items="${rendezvous}">
                                <tr>
                                    <td>${rdv.idRv}</td>
                                    <td>${rdv.patient.nomP} ${rdv.patient.prenomP}</td>
                                    <td>Dr. ${rdv.dentiste.nomD} ${rdv.dentiste.prenomD}</td>
                                    <td>${rdv.dateRv}</td>
                                    <td>${rdv.heureRv}</td>
                                    <td>
                                        <span class="statut-badge statut-${rdv.statutRv}">
                                            ${rdv.statutRv}
                                        </span>
                                    </td>
                                </tr>
                            </c:forEach>
                        </tbody>
                    </table>
                </c:when>
                
                <%-- LISTE DES SERVICES --%>
                <c:when test="${action == 'services'}">
                    <h3>Liste des Services Médicaux</h3>
                    <table class="data-table">
                        <thead>
                            <tr>
                                <th>ID</th>
                                <th>Nom</th>
                                <th>Type</th>
                                <th>Description</th>
                                <th>Tarif</th>
                            </tr>
                        </thead>
                        <tbody>
                            <c:forEach var="service" items="${services}">
                                <tr>
                                    <td>${service.numSM}</td>
                                    <td>${service.nomSM}</td>
                                    <td>${service.typeSM}</td>
                                    <td>${service.descriptionSM}</td>
                                    <td>${service.tarifSM} DT</td>
                                </tr>
                            </c:forEach>
                        </tbody>
                    </table>
                </c:when>
            </c:choose>
        </div>
    </div>
</body>
</html>