package servlets;

import jakarta.servlet.ServletException;
import jakarta.servlet.annotation.MultipartConfig;
import jakarta.servlet.annotation.WebServlet;
import jakarta.servlet.http.HttpServlet;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import java.io.IOException;

@WebServlet("/dentiste")
@MultipartConfig
public class DentisteServlet extends HttpServlet {
    private static final long serialVersionUID = 1L;

    protected void doGet(HttpServletRequest request, HttpServletResponse response) 
            throws ServletException, IOException {
        String action = request.getParameter("action");
        
        if ("list".equals(action)) {
            // Récupérer la liste des dentistes
            // List<Dentiste> dentistes = dentisteService.findAll();
            // request.setAttribute("dentistes", dentistes);
            request.getRequestDispatcher("/WEB-INF/jsp/Dentistes.jsp").forward(request, response);
        } else if ("view".equals(action)) {
            String idStr = request.getParameter("id");
            if (idStr != null) {
                Integer id = Integer.parseInt(idStr);
                // Dentiste dentiste = dentisteService.find(id);
                // request.setAttribute("dentiste", dentiste);
            }
            request.getRequestDispatcher("/WEB-INF/jsp/DetailDentiste.jsp").forward(request, response);
        } else {
            // Afficher le formulaire d'aide-soignant
            request.getRequestDispatcher("/WEB-INF/jsp/AideSoignant.jsp").forward(request, response);
        }
    }

    protected void doPost(HttpServletRequest request, HttpServletResponse response) 
            throws ServletException, IOException {
        String action = request.getParameter("action");
        
        if ("create".equals(action)) {
            createDentiste(request, response);
        } else if ("update".equals(action)) {
            updateDentiste(request, response);
        } else if ("delete".equals(action)) {
            deleteDentiste(request, response);
        }
    }
    
    private void createDentiste(HttpServletRequest request, HttpServletResponse response) 
            throws ServletException, IOException {
        String nom = request.getParameter("nom");
        String prenom = request.getParameter("prenom");
        String email = request.getParameter("email");
        String mdp = request.getParameter("mdp");
        String specialite = request.getParameter("specialite");
        String sexe = request.getParameter("sexe");
        String telStr = request.getParameter("telephone");
        
        // Validation
        if (nom == null || prenom == null || email == null || mdp == null) {
            request.setAttribute("erreur", "Veuillez remplir tous les champs obligatoires");
            request.getRequestDispatcher("/WEB-INF/jsp/AideSoignant.jsp").forward(request, response);
            return;
        }
        
        Integer tel = null;
        if (telStr != null && !telStr.isEmpty()) {
            tel = Integer.parseInt(telStr);
        }
        
        // Créer l'entité Dentiste
        // Dentiste dentiste = new Dentiste();
        // dentiste.setNomD(nom);
        // dentiste.setPrenomD(prenom);
        // dentiste.setEmailD(email);
        // dentiste.setMdpD(mdp);
        // dentiste.setSpecialiteD(specialite);
        // dentiste.setSexeD(sexe);
        // dentiste.setTelD(tel);
        
        // Appel au service EJB
        // dentisteService.create(dentiste);
        
        request.setAttribute("message", "Inscription réussie ! Votre profil d'aide-soignant a été créé.");
        request.getRequestDispatcher("/WEB-INF/jsp/AideSoignant.jsp").forward(request, response);
    }
    
    private void updateDentiste(HttpServletRequest request, HttpServletResponse response) 
            throws ServletException, IOException {
        String idStr = request.getParameter("id");
        // Logique de mise à jour
        response.sendRedirect(request.getContextPath() + "/dentiste?action=list");
    }
    
    private void deleteDentiste(HttpServletRequest request, HttpServletResponse response) 
            throws ServletException, IOException {
        String idStr = request.getParameter("id");
        if (idStr != null) {
            Integer id = Integer.parseInt(idStr);
            // dentisteService.delete(id);
        }
        response.sendRedirect(request.getContextPath() + "/dentiste?action=list");
    }
}