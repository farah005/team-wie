<%@ page language="java" contentType="text/html; charset=UTF-8" pageEncoding="UTF-8"%>
<%@ taglib uri="http://java.sun.com/jsp/jstl/core" prefix="c" %>
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <title>Publication — Cabinet Sourire</title>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" type="text/css" href="${pageContext.request.contextPath}/css/mesStyles.css">
</head>
<body>

    <div class="container">
        <div class="header-box">
            <h2>Découvrez les dernières avancées en dentisterie</h2>
        </div>

        <%-- Section des messages flash (Erreur/Succès) --%>
        <% if (request.getAttribute("message") != null) { %>
            <div style="color: green; margin-bottom: 15px; font-weight: bold;">
                ${message}
            </div>
        <% } %>
        
        <% if (request.getAttribute("erreur") != null) { %>
            <div style="color: red; margin-bottom: 15px; font-weight: bold;">
                ${erreur}
            </div>
        <% } %>

        <%-- NOUVEAU : BLOC POUR VOIR LA PUBLICATION PUBLIÉE MAINTENANT --%>
        <c:if test="${not empty dernierTitre}">
            <div style="background: #f0fdf4; border: 1px solid #16a34a; border-radius: 12px; padding: 20px; margin-bottom: 30px;">
                <h3 style="color: #16a34a; margin-top: 0;">✅ Publication publiée avec succès !</h3>
                <div style="display: flex; gap: 20px; align-items: flex-start;">
                    <div style="flex: 1;">
                        <p><strong>Titre :</strong> ${dernierTitre}</p>
                        <p><strong>Type :</strong> ${dernierType}</p>
                        <p><strong>Description :</strong> ${derniereDesc}</p>
                        <p><strong>Fichier :</strong> 
                            <a href="${pageContext.request.contextPath}/uploads/${dernierFichier}" target="_blank" style="color: #007bff; font-weight: bold;">
                                ${dernierFichier} (Ouvrir)
                            </a>
                        </p>
                    </div>
                </div>
            </div>
        </c:if>

        <%-- FORMULAIRE --%>
        <form action="${pageContext.request.contextPath}/publication?action=upload" method="post" enctype="multipart/form-data">
            <div class="form-grid">
                
                <div class="form-group">
                    <label>Titre</label>
                    <input type="text" name="titre" placeholder="Saisir le titre de publication" required>
                </div>

                <div class="form-group">
                    <label>Fichier (PDF ou Image)</label>
                    <input type="file" name="file" required>
                </div>

                <div class="form-group">
                    <label>Date de publication</label>
                    <input type="date" name="dateP">
                </div>

                <div class="form-group">
                    <label>Type de publication</label>
                    <select name="typeP">
                        <option value="">[Choisir catégorie]</option>
                        <option value="Article">Article scientifique</option>
                        <option value="Etude">Étude de cas</option>
                        <option value="Lancement">Lancement d'un produit ou service</option>
                        <option value="Innovation">Actualités/innovation</option>
                    </select>
                </div>

                <div class="form-group full-width">
                    <label>Résumé / Description</label>
                    <textarea name="description" placeholder="Saisir la description associée"></textarea>
                </div>
            </div>

            <div class="button-container">
                <button type="submit" class="btn-save">Enregistrer</button>
                <button type="reset" class="btn-cancel">Annuler</button>
            </div>
        </form>
    </div>
</body>
</html>