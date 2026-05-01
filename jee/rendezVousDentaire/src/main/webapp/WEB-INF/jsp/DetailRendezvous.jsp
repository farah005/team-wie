<%@ page language="java" contentType="text/html; charset=UTF-8" pageEncoding="UTF-8"%>
<%@ taglib uri="http://java.sun.com/jsp/jstl/core" prefix="c" %>
<%@ taglib uri="http://java.sun.com/jsp/jstl/fmt" prefix="fmt" %>

<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <title>Détails du Rendez-vous</title>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" type="text/css" href="<%= request.getContextPath() %>/css/mesStyles.css">
    <style>
        .detail-card {
            background: white;
            max-width: 700px;
            margin: 50px auto;
            padding: 40px;
            border-radius: 20px;
            box-shadow: 0 15px 35px rgba(0,0,0,0.07);
        }
        .detail-header {
            border-bottom: 1px solid #E5E1DA;
            padding-bottom: 20px;
            margin-bottom: 30px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .info-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 30px;
        }
        .info-group label {
            display: block;
            font-size: 0.75rem;
            text-transform: uppercase;
            color: #A39382;
            letter-spacing: 1px;
            margin-bottom: 5px;
        }
        .info-group p {
            font-size: 1.1rem;
            color: #4A3F35;
            font-weight: 600;
            margin: 0;
        }
        .motif-box {
            margin-top: 30px;
            padding: 20px;
            background: #F9F7F2;
            border-radius: 12px;
            border-left: 4px solid #D4AF37;
        }
        .status-pill {
            padding: 6px 15px;
            border-radius: 50px;
            font-size: 0.8rem;
            font-weight: bold;
        }
        .btn-back {
            display: inline-block;
            margin-top: 30px;
            text-decoration: none;
            color: #A39382;
            font-size: 0.9rem;
            transition: color 0.3s;
        }
        .btn-back:hover { color: #4A3F35; }
    </style>
</head>
<body>
    <div class="detail-card">
        <c:if test="${not empty erreur}">
            <div style="color: red; padding: 10px; border: 1px solid #f5c6cb; background: #f8d7da; margin-bottom: 12px;">
                ${erreur}
            </div>
        </c:if>
        <div class="detail-header">
            <h2 style="margin:0;">Fiche Rendez-vous #${rdv.idRv}</h2>
            <span class="status-pill ${rdv.statutRv.toLowerCase().replace(' ', '.')}">
                ${rdv.statutRv}
            </span>
        </div>

        <div class="info-grid">
            <div class="info-group">
                <label>Patient</label>
                <p>${rdv.patient.nom} ${rdv.patient.prenom}</p>
                <small>ID: ${rdv.patient.id}</small>
            </div>

            <div class="info-group">
                <label>Praticien</label>
                <p>Dr. ${rdv.dentiste.nomD}</p>
                <small>${rdv.dentiste.specialite}</small>
            </div>

            <div class="info-group">
                <label>Date du rendez-vous</label>
                <p><fmt:formatDate value="${rdv.dateRv}" pattern="EEEE dd MMMM yyyy" /></p>
            </div>

            <div class="info-group">
                <label>Heure</label>
                <p>${rdv.heureRv}</p>
            </div>
        </div>

        <div class="motif-box">
            <label style="font-size: 0.7rem; color: #A39382; text-transform: uppercase;">Motif de la visite</label>
            <p style="margin-top: 10px; color: #6B5B4B;">
                ${empty rdv.detailsRv ? 'Aucun détail supplémentaire fourni.' : rdv.detailsRv}
            </p>
        </div>

        <div style="text-align: center; display:flex; gap:12px; justify-content:center; align-items:center; margin-top:20px;">
            <a href="rendezvous?action=list" class="btn-back">← Retour au planning</a>

            <!-- Bouton visible au personnel pour marquer manuellement comme Terminé -->
            <c:if test="${sessionScope.userType == 'aide-soignant' || sessionScope.userType == 'dentiste'}">
                <c:if test="${rdv.statutRv == 'Confirmé'}">
                    <form action="${pageContext.request.contextPath}/rendezvous" method="post" style="display:inline;">
                        <input type="hidden" name="action" value="updateStatut" />
                        <input type="hidden" name="id" value="${rdv.idRv}" />
                        <input type="hidden" name="statut" value="Terminé" />
                        <button type="submit" class="btn-primary" style="padding:10px 18px;" onclick="return confirm('Confirmer la fin du rendez-vous ?');">Marquer comme terminé</button>
                    </form>
                </c:if>

                <!-- Si déjà terminé, proposer d'ajouter un acte -->
                <c:if test="${rdv.statutRv == 'Terminé'}">
                    <a href="${pageContext.request.contextPath}/actemedical?action=new&idRv=${rdv.idRv}" class="btn-primary" style="padding:10px 18px; text-decoration:none;">+ Enregistrer un acte</a>
                </c:if>
            </c:if>

            <a href="${pageContext.request.contextPath}/actemedical?action=byRendezvous&idRv=${rdv.idRv}" class="btn-secondary" style="text-decoration:none;">Voir actes liés</a>
        </div>
    </div>
</body>
</html>