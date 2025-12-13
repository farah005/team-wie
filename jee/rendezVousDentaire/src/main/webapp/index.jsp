<%@ page language="java" contentType="text/html; charset=UTF-8" pageEncoding="UTF-8"%>
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Plateforme de Rendez-vous Dentaires</title>
    <link rel="stylesheet" type="text/css" href="<%= request.getContextPath() %>/css/mesStyles.css">
</head>
<body>
    <!-- Zone 1 : En-tête -->
    <header>
        <div class="logo">
            <a href="<%= request.getContextPath() %>/">
                <img src="<%= request.getContextPath() %>/images/logo.png" alt="Logo" width="80">
            </a>
        </div>
        <h1>Un sourire en un clic — Rendez-vous dentaires simplifiés</h1>
        <nav>
            <a href="<%= request.getContextPath() %>/connexion">Connexion</a>
            <a href="<%= request.getContextPath() %>/patient">Patient</a>
            <a href="<%= request.getContextPath() %>/dentiste">Aide-soignant</a>
            <a href="<%= request.getContextPath() %>/service">Service</a>
            <a href="<%= request.getContextPath() %>/publication">Publication</a>
            <a href="<%= request.getContextPath() %>/rendezvous">Rendez-vous</a>
        </nav>
    </header>

    <!-- Zone 2 : Contenu principal -->
    <main class="home">
        <!-- HERO -->
        <section class="hero">
            <div class="hero-text">
                <h2>Votre sourire, notre priorité</h2>
                <p>Réservez en quelques secondes chez un professionnel près de chez vous — simple, rapide et fiable.</p>
                <div class="hero-cta">
                    <a class="btn btn-primary" href="<%= request.getContextPath() %>/rendezvous">Prendre rendez-vous</a>
                    <a class="btn btn-secondary" href="<%= request.getContextPath() %>/service">Découvrir les services</a>
                </div>
                <p class="hero-sub">
                    <span class="badge">Disponibilités en temps réel</span>
                    <span class="badge">Rappel SMS & Email</span>
                    <span class="badge">Sécurité des données</span>
                </p>
            </div>
            <div class="hero-visual">
                <img src="<%= request.getContextPath() %>/images/hero.png" alt="Sourire" />
            </div>
        </section>
    </main>

    <!-- Zone 3 : Pied de page -->
    <footer>
        <div class="footer-inner">
            <p>Contact: <a href="mailto:votre.email@exemple.com">votre.email@exemple.com</a></p>
            <p>&copy; <%= java.time.Year.now() %> Plateforme Rendez-vous Dentaires — Tous droits réservés</p>
        </div>
    </footer>
</body>
</html>