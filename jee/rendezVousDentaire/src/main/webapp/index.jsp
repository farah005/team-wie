<%@ page language="java" contentType="text/html; charset=UTF-8" pageEncoding="UTF-8"%>
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <title>Make sure to smile everyday</title>
    <link rel="stylesheet" type="text/css" href="<%= request.getContextPath() %>/css/mesStyles.css">
</head>
<body>

    <header>
        <div class="logo">
            <img src="<%= request.getContextPath() %>/uploads/dent.jpg" alt="Logo" width="60">
        </div>
        <nav>
            <a href="<%= request.getContextPath() %>/connexion">Connexion</a>
            <a href="<%= request.getContextPath() %>/patient">Patient</a>
            <a href="<%= request.getContextPath() %>/aidesoignant">Aide-soignant</a>
            <a href="<%= request.getContextPath() %>/service">Service</a>
            <a href="<%= request.getContextPath() %>/publication">Publication</a>
            <a href="<%= request.getContextPath() %>/rendezvous">Rendez-vous</a>
            <a href="<%= request.getContextPath() %>/dentiste">Dentiste</a>
        </nav>
    </header>

    <main>
        <section class="hero-container">
            <div class="hero-visual">
                <img src="<%= request.getContextPath() %>/uploads/dentiste.jpg" alt="Background">
                <p>Le cabinet est ouvert de 08:00 à 18:00 uniquement</p>
            </div>

            <div class="hero-actions">
                <h1>Votre sourire, notre priorité</h1>
                
                <div class="button-stack">
       
                    <a href="<%= request.getContextPath() %>/connexion" class="btn-luxury">
                        Espace Personnel
                    </a>
                </div>
            </div>
        </section>
    </main>

    <footer>
        <p>&copy; 2025 Plateforme Dentaire Luxe — Tous droits réservés</p>
        <p> Contacter nous : Smile@gmail.com</p>
        
    </footer>

</body>
</html>