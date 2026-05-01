<%@ page language="java" contentType="text/html; charset=UTF-8" pageEncoding="UTF-8"%>
<%@ taglib uri="http://java.sun.com/jsp/jstl/core" prefix="c" %>
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Liste des Dentistes</title>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;700;800&display=swap" rel="stylesheet">
    <link rel="stylesheet" type="text/css" href="<%= request.getContextPath() %>/css/mesStyles.css">
</head>
<body>
    <div class="form-container">
        <h2>👨‍⚕️ Nos Dentistes</h2>
        <p>Choisissez le professionnel qui correspond à vos besoins</p>
        
        <div class="actions-bar">
            <a href="<%= request.getContextPath() %>/rendezvous" class="btn-primary">
                📅 Prendre rendez-vous
            </a>
            <a href="<%= request.getContextPath() %>/index.jsp" class="btn-secondary">
                🏠 Retour
            </a>
        </div>
        
        <!-- Filtres de recherche -->
        <div class="search-section">
            <h3>Rechercher un dentiste</h3>
            <div class="search-form">
                <input type="text" id="searchInput" placeholder="Rechercher par nom ou spécialité..." 
                       onkeyup="filterDentists()">
                <select id="specialiteFilter" onchange="filterDentists()">
                    <option value="">Toutes les spécialités</option>
                    <option value="Orthodontie">Orthodontie</option>
                    <option value="Chirurgie dentaire">Chirurgie dentaire</option>
                    <option value="Dentisterie générale">Dentisterie générale</option>
                    <option value="Parodontologie">Parodontologie</option>
                    <option value="Endodontie">Endodontie</option>
                </select>
            </div>
        </div>
        
        <!-- Liste des dentistes -->
        <c:choose>
            <c:when test="${empty dentistes}">
                <div class="empty-state">
                    <p>Aucun dentiste disponible pour le moment.</p>
                </div>
            </c:when>
            <c:otherwise>
                <div class="dentists-grid" id="dentistsGrid">
                    <c:forEach var="dentiste" items="${dentistes}">
                        <div class="dentist-card" data-specialite="${dentiste.specialiteD}">
                            <div class="dentist-photo">
                                <c:choose>
                                    <c:when test="${not empty dentiste.photoD}">
                                        <img src="<%= request.getContextPath() %>/uploads/${dentiste.photoD}" 
                                             alt="${dentiste.nomD}">
                                    </c:when>
                                    <c:otherwise>
                                        <div class="photo-placeholder">
                                            ${dentiste.sexeD == 'M' ? '👨‍⚕️' : '👩‍⚕️'}
                                        </div>
                                    </c:otherwise>
                                </c:choose>
                            </div>
                            
                            <div class="dentist-info">
                                <h3>Dr. ${dentiste.nomD} ${dentiste.prenomD}</h3>
                                <p class="specialite">
                                    <strong>🎓 Spécialité:</strong> ${dentiste.specialiteD}
                                </p>
                                <p class="contact">
                                    <strong>📧 Email:</strong> ${dentiste.emailD}
                                </p>
                                <c:if test="${not empty dentiste.telD}">
                                    <p class="contact">
                                        <strong>📞 Téléphone:</strong> ${dentiste.telD}
                                    </p>
                                </c:if>
                            </div>
                            
                            <div class="dentist-actions">
                                <a href="<%= request.getContextPath() %>/dentiste?action=view&id=${dentiste.idD}" 
                                   class="btn-secondary">
                                    👁️ Voir profil
                                </a>
                                <a href="<%= request.getContextPath() %>/rendezvous?idDentiste=${dentiste.idD}" 
                                   class="btn-primary">
                                    📅 Prendre RDV
                                </a>
                            </div>
                        </div>
                    </c:forEach>
                </div>
            </c:otherwise>
        </c:choose>
    </div>
    
    <style>
        .dentists-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
            gap: 25px;
            margin-top: 30px;
        }
        
        .dentist-card {
            background: white;
            border-radius: 15px;
            padding: 25px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
            transition: all 0.3s ease;
            border: 2px solid transparent;
        }
        
        .dentist-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 8px 25px rgba(0,0,0,0.15);
            border-color: #667eea;
        }
        
        .dentist-photo {
            text-align: center;
            margin-bottom: 20px;
        }
        
        .dentist-photo img {
            width: 120px;
            height: 120px;
            border-radius: 50%;
            object-fit: cover;
            border: 4px solid #667eea;
        }
        
        .photo-placeholder {
            width: 120px;
            height: 120px;
            margin: 0 auto;
            border-radius: 50%;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 60px;
        }
        
        .dentist-info h3 {
            color: #1e3c72;
            margin-bottom: 15px;
            font-size: 1.3em;
            text-align: center;
        }
        
        .dentist-info p {
            margin: 10px 0;
            color: #666;
            font-size: 0.95em;
        }
        
        .specialite {
            background: #f0f4ff;
            padding: 8px 12px;
            border-radius: 5px;
            margin: 15px 0;
        }
        
        .dentist-actions {
            display: flex;
            gap: 10px;
            margin-top: 20px;
        }
        
        .dentist-actions a {
            flex: 1;
            text-align: center;
            padding: 10px;
            font-size: 0.9em;
        }
    </style>
    
    <script>
        function filterDentists() {
            const searchInput = document.getElementById('searchInput').value.toLowerCase();
            const specialiteFilter = document.getElementById('specialiteFilter').value;
            const cards = document.querySelectorAll('.dentist-card');
            
            cards.forEach(card => {
                const text = card.textContent.toLowerCase();
                const specialite = card.getAttribute('data-specialite');
                
                const matchesSearch = text.includes(searchInput);
                const matchesSpecialite = !specialiteFilter || specialite === specialiteFilter;
                
                if (matchesSearch && matchesSpecialite) {
                    card.style.display = 'block';
                } else {
                    card.style.display = 'none';
                }
            });
        }
    </script>
</body>
</html>