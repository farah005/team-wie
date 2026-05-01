<%@ page language="java" contentType="text/html; charset=UTF-8" pageEncoding="UTF-8"%>
<%@ taglib uri="http://java.sun.com/jsp/jstl/core" prefix="c" %>
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <title>Inscription Aide-soignant</title>
    <link rel="stylesheet" type="text/css" href="${pageContext.request.contextPath}/css/mesStyles.css">
</head>
<body>
    <div class="form-container">
        <%-- Le titre s'adapte si on est en mode édition --%>
        <h2>${not empty aidesoignant ? "Modifier le profil" : "Inscription Aide-soignant"}</h2>
        <p>Gérez vos informations professionnelles</p>
        
        <%-- Affichage des messages d'erreur ou de succès --%>
        <c:if test="${not empty erreur}">
            <div class="error-message">${erreur}</div>
        </c:if>

        <!-- Afficher message provenant de la session après redirection -->
        <c:if test="${not empty sessionScope.message}">
            <div class="success-message">${sessionScope.message}</div>
            <c:remove var="message" scope="session" />
        </c:if>
        <c:if test="${not empty message}">
            <div class="success-message">${message}</div>
        </c:if>
        
        <form action="${pageContext.request.contextPath}/aidesoignant" method="post" enctype="multipart/form-data">
            <%-- Action dynamique : update si l'objet existe, sinon create --%>
            <input type="hidden" name="action" value="${not empty aidesoignant ? 'update' : 'create'}">
            
            <%-- ID caché pour la mise à jour --%>
            <c:if test="${not empty aidesoignant}">
                <input type="hidden" name="idAS" value="${aidesoignant.idAS}">
            </c:if>
            
            <div class="form-row">
                <div class="form-group">
                    <label for="nomAS">Nom * :</label>
                    <input type="text" id="nomAS" name="nomAS" value="${aidesoignant.nomAS}" required maxlength="100">
                </div>
                
                <div class="form-group">
                    <label for="prenomAS">Prénom * :</label>
                    <input type="text" id="prenomAS" name="prenomAS" value="${aidesoignant.prenomAS}" required maxlength="100">
                </div>
            </div>
            
            <div class="form-row">
                <div class="form-group">
                    <label for="emailAS">Email * :</label>
                    <input type="email" id="emailAS" name="emailAS" value="${aidesoignant.emailAS}" required maxlength="100">
                </div>
                
                <div class="form-group">
                    <label for="telephoneAS">Téléphone :</label>
                    <input type="tel" id="telephoneAS" name="telephoneAS" value="${aidesoignant.telAS}" maxlength="8" pattern="[0-9]{8}">
                </div>
            </div>
            
            <div class="form-row">
                <div class="form-group">
                    <label for="specialiteAS">Spécialité :</label>
                    <input type="text" id="specialiteAS" name="specialiteAS" value="${aidesoignant.specialisationAS}" 
                           placeholder="Ex: Chirurgie, Hygiène...">
                </div>
                
                <div class="form-group">
                    <label for="sexeAS">Sexe :</label>
                    <select id="sexeAS" name="sexeAS">
                        <option value="">Sélectionner</option>
                        <option value="M" ${aidesoignant.sexeAS == 'M' ? 'selected' : ''}>Masculin</option>
                        <option value="F" ${aidesoignant.sexeAS == 'F' ? 'selected' : ''}>Féminin</option>
                    </select>
                </div>
            </div>
            
            <div class="form-group">
                <label for="photoAS">Photo de profil :</label>
                <input type="file" id="photoAS" name="photoAS" accept="image/*">
                <c:if test="${not empty aidesoignant.photoAS}">
                    <small>Fichier actuel : ${aidesoignant.photoAS}</small>
                </c:if>
            </div>
            
            <div class="form-row">
                <div class="form-group">
                    <label for="mdpAS">Mot de passe ${empty aidesoignant ? '*' : '(laisser vide pour ne pas changer)'} :</label>
                    <input type="password" id="mdpAS" name="mdpAS" ${empty aidesoignant ? 'required' : ''} maxlength="10">
                </div>
                
                <div class="form-group">
                    <label for="confirmMdp">Confirmer mot de passe :</label>
                    <input type="password" id="confirmMdp" name="confirmMdp" ${empty aidesoignant ? 'required' : ''} maxlength="10">
                </div>
            </div>
            
            <div class="form-actions">
                <button type="submit" class="btn-primary">
                    ${not empty aidesoignant ? "Mettre à jour" : "Enregistrer"}
                </button>
                <a href="${pageContext.request.contextPath}/aidesoignant?action=list" class="btn-secondary" style="text-decoration:none; padding:10px;">Annuler</a>
            </div>
        </form>
        
        <c:if test="${empty aidesoignant}">
            <p class="form-footer">
                Déjà inscrit ? <a href="${pageContext.request.contextPath}/connexion">Se connecter</a>
            </p>
        </c:if>
    </div>
    
    <script>
        document.querySelector('form').addEventListener('submit', function(e) {
            var mdp = document.getElementById('mdpAS').value;
            var confirmMdp = document.getElementById('confirmMdp').value;
            
            if (mdp !== "" && mdp !== confirmMdp) {
                e.preventDefault();
                alert('Les mots de passe ne correspondent pas');
            }
        });
    </script>
</body>
</html>