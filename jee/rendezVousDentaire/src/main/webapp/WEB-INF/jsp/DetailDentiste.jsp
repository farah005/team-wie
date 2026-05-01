<%@ page language="java" contentType="text/html; charset=UTF-8" pageEncoding="UTF-8"%>
<%@ taglib uri="http://java.sun.com/jsp/jstl/core" prefix="c" %>

<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <title>Profil du Dr. ${dentiste.nomD} — Cabinet Sourire</title>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;600;700&family=Playfair+Display:wght@700&display=swap" rel="stylesheet">
    <link rel="stylesheet" type="text/css" href="${pageContext.request.contextPath}/css/mesStyles.css">
    <style>
        .profile-container {
            display: flex;
            gap: 50px;
            background: white;
            padding: 40px;
            border-radius: 20px;
            box-shadow: 0 15px 40px rgba(0,0,0,0.05);
            margin-top: 30px;
            align-items: center;
        }

        .profile-image {
            width: 300px;
            height: 400px;
            background: var(--bg-nude);
            border-radius: 15px;
            overflow: hidden;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 80px;
            border: 1px solid #EEE;
        }

        .profile-details {
            flex: 1;
        }

        .spec-label {
            color: var(--accent-rose);
            text-transform: uppercase;
            letter-spacing: 2px;
            font-weight: 700;
            font-size: 0.8rem;
            margin-bottom: 10px;
            display: block;
        }

        .info-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
            margin: 30px 0;
        }

        .info-item {
            padding: 15px;
            background: #FAFAFA;
            border-radius: 10px;
        }

        .info-item label {
            display: block;
            font-size: 0.75rem;
            color: #AAA;
            margin-bottom: 5px;
        }

        .info-item span {
            font-weight: 600;
            color: var(--primary-brown);
        }
    </style>
</head>
<body>
    <%@ include file="header.jsp" %>

    <div class="form-container" style="max-width: 1000px;">
        <a href="dentiste?action=list" style="text-decoration: none; color: #888; font-size: 0.9rem;">← Retour à la liste</a>
        
        <div class="profile-container">
            <div class="profile-image">
                <c:choose>
                    <c:when test="${not empty dentiste.photoD}">
                        <img src="${pageContext.request.contextPath}/uploads/${dentiste.photoD}" style="width:100%; height:100%; object-fit:cover;">
                    </c:when>
                    <c:otherwise>
                        ${dentiste.sexeD == 'M' ? '👨‍⚕️' : '👩‍⚕️'}
                    </c:otherwise>
                </c:choose>
            </div>

            <div class="profile-details">
                <span class="spec-label">${dentiste.specialiteD}</span>
                <h1 style="font-family: 'Playfair Display', serif; font-size: 2.8rem; margin-bottom: 10px;">
                    Dr. ${dentiste.prenomD} ${dentiste.nomD}
                </h1>
                
                <p style="color: #666; line-height: 1.6;">
                    Expert en soins dentaires avec une attention particulière portée au confort du patient et à l'excellence esthétique.
                </p>

                <div class="info-grid">
                    <div class="info-item">
                        <label>Email professionnel</label>
                        <span>${dentiste.emailD}</span>
                    </div>
                    <div class="info-item">
                        <label>Téléphone</label>
                        <span>${not empty dentiste.telD ? dentiste.telD : 'Non renseigné'}</span>
                    </div>
                    <div class="info-item">
                        <label>Sexe</label>
                        <span>${dentiste.sexeD == 'M' ? 'Masculin' : 'Féminin'}</span>
                    </div>
                    <div class="info-item">
                        <label>Disponibilité</label>
                        <span style="color: #27ae60;">● Actif</span>
                    </div>
                </div>

                <div style="margin-top: 40px; display: flex; gap: 15px;">
                    <a href="rendezvous?idDentiste=${dentiste.idD}" class="btn-primary" style="padding: 15px 40px; width: auto;">
                        Réserver une consultation
                    </a>
                </div>
            </div>
        </div>
    </div>
</body>
</html>