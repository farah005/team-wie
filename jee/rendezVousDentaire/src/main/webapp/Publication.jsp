<%@ page language="java" contentType="text/html; charset=UTF-8" pageEncoding="UTF-8"%>
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Publications</title>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;700;800&display=swap" rel="stylesheet">
    <link rel="stylesheet" type="text/css" href="<%= request.getContextPath() %>/css/mesStyles.css">
</head>
<body>
    <div class="form-container">
        <h2>Gestion des Publications</h2>
        <p>Uploadez et partagez des documents, images ou fichiers</p>
        
        <% if (request.getAttribute("erreur") != null) { %>
            <div class="error-message">
                <%= request.getAttribute("erreur") %>
            </div>
        <% } %>
        
        <% if (request.getAttribute("message") != null) { %>
            <div class="success-message">
                <%= request.getAttribute("message") %>
            </div>
        <% } %>
        
        <!-- Formulaire d'upload -->
        <div class="upload-section">
            <h3>Publier un nouveau fichier</h3>
            <form action="<%= request.getContextPath() %>/publication" method="post" 
                  enctype="multipart/form-data">
                <input type="hidden" name="action" value="upload">
                
                <div class="form-group">
                    <label for="titre">Titre de la publication * :</label>
                    <input type="text" id="titre" name="titre" required maxlength="200" 
                           placeholder="Ex: Conseils d'hygiène dentaire">
                </div>
                
                <div class="form-group">
                    <label for="description">Description :</label>
                    <textarea id="description" name="description" rows="4" 
                              placeholder="Décrivez votre publication..."></textarea>
                </div>
                
                <div class="form-group file-upload-wrapper">
                    <label for="file">Sélectionner un fichier * :</label>
                    <input type="file" id="file" name="file" required 
                           accept=".pdf,.doc,.docx,.jpg,.jpeg,.png,.gif">
                    <small class="form-text">
                        Formats acceptés: PDF, Word, Images (JPG, PNG, GIF). Taille max: 10 MB
                    </small>
                </div>
                
                <div class="form-actions">
                    <button type="submit" class="btn-primary">
                        📤 Publier
                    </button>
                    <button type="reset" class="btn-secondary">Réinitialiser</button>
                </div>
            </form>
        </div>
        
        <hr>
        
        <!-- Bouton pour voir toutes les publications -->
        <div class="view-publications">
            <a href="<%= request.getContextPath() %>/publication?action=list" class="btn-primary">
                📋 Voir toutes les publications
            </a>
        </div>
        
        <!-- Aperçu du fichier sélectionné -->
        <div id="filePreview" class="file-preview" style="display:none;">
            <h4>Aperçu du fichier</h4>
            <div id="previewContent"></div>
        </div>
    </div>
    
    <script>
        document.getElementById('file').addEventListener('change', function(e) {
            var file = e.target.files[0];
            var preview = document.getElementById('filePreview');
            var previewContent = document.getElementById('previewContent');
            
            if (file) {
                preview.style.display = 'block';
                
                var fileInfo = '<p><strong>Nom:</strong> ' + file.name + '</p>';
                fileInfo += '<p><strong>Type:</strong> ' + file.type + '</p>';
                fileInfo += '<p><strong>Taille:</strong> ' + (file.size / 1024 / 1024).toFixed(2) + ' MB</p>';
                
                previewContent.innerHTML = fileInfo;
                
                // Si c'est une image, afficher l'aperçu
                if (file.type.startsWith('image/')) {
                    var reader = new FileReader();
                    reader.onload = function(e) {
                        var img = '<img src="' + e.target.result + '" style="max-width:300px; margin-top:10px;">';
                        previewContent.innerHTML += img;
                    }
                    reader.readAsDataURL(file);
                }
            } else {
                preview.style.display = 'none';
            }
        });
    </script>
</body>
</html>