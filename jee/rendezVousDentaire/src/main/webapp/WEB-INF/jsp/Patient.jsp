<%@ page language="java" contentType="text/html; charset=UTF-8" pageEncoding="UTF-8"%>
<%@ taglib uri="http://java.sun.com/jsp/jstl/core" prefix="c" %>

<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <title>Inscription — Cabinet Sourire</title>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" type="text/css" href="${pageContext.request.contextPath}/css/mesStyles.css">
    <style>
        /* Styles spécifiques au formulaire d'inscription */
        .form-container { max-width: 650px; margin: 40px auto; background: white; padding: 30px; border-radius: 15px; box-shadow: 0 10px 30px rgba(0,0,0,0.08); }
        .form-row { display: flex; gap: 20px; margin-bottom: 15px; }
        .form-group { flex: 1; display: flex; flex-direction: column; }
        label { font-weight: 600; color: #4A3F35; margin-bottom: 5px; font-size: 0.9rem; }
        input, select { padding: 10px; border: 1px solid #E5E1DA; border-radius: 8px; font-family: inherit; }
        .required { color: #C0392B; }
        .form-footer { text-align: center; margin-top: 20px; font-size: 0.9rem; color: #6B5B4B; }
    </style>
</head>
<body>
    <%-- Inclusion du Header (Barre de navigation) --%>
    <%@ include file="header.jsp" %>

    <div class="form-container">
        <h2 style="color: #4A3F35; text-align: center; margin-top: 0;">Créer mon dossier patient</h2>
        <p style="text-align: center; color: #888; margin-bottom: 25px;">Rejoignez notre cabinet pour gérer vos soins en ligne.</p>
        
        <%-- Zone des Messages d'erreur --%>
        <c:if test="${not empty erreur}">
            <div class="error-message" style="background: #FDECEC; color: #C0392B; padding: 12px; border-radius: 8px; margin-bottom: 20px; border: 1px solid #FACCCC; font-size: 0.85rem;">
                <strong>⚠️ Erreur :</strong> ${erreur}
            </div>
        </c:if>
        
        <form action="${pageContext.request.contextPath}/patient" method="post" enctype="multipart/form-data" id="registerForm">
            <input type="hidden" name="action" value="create">
            
            <div class="form-row">
                <div class="form-group">
                    <label>Nom <span class="required">*</span></label>
                    <input type="text" name="nom" required placeholder="Dupont">
                </div>
                <div class="form-group">
                    <label>Prénom <span class="required">*</span></label>
                    <input type="text" name="prenom" required placeholder="Jean">
                </div>
            </div>
            
            <div class="form-row">
                <div class="form-group">
                    <label>Email <span class="required">*</span></label>
                    <input type="email" name="email" required placeholder="jean.dupont@email.com">
                </div>
                <div class="form-group">
                    <label>Date de naissance</label>
                    <input type="date" id="dateNaissance" name="dateNaissance">
                </div>
            </div>
            
            <div class="form-row">
                <div class="form-group">
                    <label>Sexe</label>
                    <select name="sexe">
                        <option value="">Sélectionner</option>
                        <option value="M">Masculin</option>
                        <option value="F">Féminin</option>
                    </select>
                </div>
                <div class="form-group">
                    <label>Groupe sanguin</label>
                    <select name="groupeSanguin">
                        <option value="">Inconnu</option>
                        <option value="A">A</option>
                        <option value="B">B</option>
                        <option value="O">O</option>
                        <option value="AB">AB</option>
                    </select>
                </div>
            </div>
            
            <div class="form-group" style="margin-bottom: 15px;">
                <label>Recouvrement social (N° Assurance)</label>
                <input type="text" name="recouvrement" placeholder="Ex: CNAM, Mutuelle...">
            </div>
            
            <div class="form-group" style="margin-bottom: 15px;">
                <label>Photo de profil</label>
                <input type="file" name="photo" accept="image/*">
            </div>
            
            <div class="form-row">
                <div class="form-group">
                    <label>Mot de passe <span class="required">*</span></label>
                    <input type="password" id="mdp" name="mdp" required minlength="4">
                </div>
                <div class="form-group">
                    <label>Confirmation <span class="required">*</span></label>
                    <input type="password" id="confirmMdp" required minlength="4">
                </div>
            </div>
            
            <button type="submit" class="btn-primary" style="margin-top: 20px;">Finaliser l'inscription</button>
        </form>
        
        <p class="form-footer">
            Déjà inscrit ? <a href="${pageContext.request.contextPath}/connexion" style="color: #4A3F35; font-weight: 700; text-decoration: none;">Connectez-vous ici</a>
        </p>
    </div>

    <script>
        // Validation de la correspondance des mots de passe
        document.getElementById('registerForm').addEventListener('submit', function(e) {
            const mdp = document.getElementById('mdp').value;
            const confirm = document.getElementById('confirmMdp').value;
            
            if (mdp !== confirm) {
                e.preventDefault();
                alert('Les mots de passe ne correspondent pas.');
            }
        });

        // Désactiver les dates futures
        document.getElementById('dateNaissance').max = new Date().toISOString().split('T')[0];
    </script>
</body>
</html>