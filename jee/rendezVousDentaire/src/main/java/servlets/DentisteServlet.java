package servlets;

import jakarta.ejb.EJB;
import jakarta.servlet.ServletException;
import jakarta.servlet.annotation.MultipartConfig;
import jakarta.servlet.annotation.WebServlet;
import jakarta.servlet.http.HttpServlet;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import java.io.IOException;
import java.util.List;

import entities.Dentiste;
import interfaces.DentisteLocal;

@WebServlet("/dentiste")
@MultipartConfig(
    fileSizeThreshold = 1024 * 1024 * 1, // 1 MB
    maxFileSize = 1024 * 1024 * 10,      // 10 MB
    maxRequestSize = 1024 * 1024 * 100   // 100 MB
)
public class DentisteServlet extends HttpServlet {
    private static final long serialVersionUID = 1L;

    @EJB
    private DentisteLocal dentisteService; 

    @Override
    protected void doGet(HttpServletRequest request, HttpServletResponse response) 
            throws ServletException, IOException {
        
        String action = request.getParameter("action");
        
        // Par défaut (action nulle ou "list"), on affiche le catalogue des dentistes
        if (action == null || "list".equals(action)) {
            List<Dentiste> dentistes = dentisteService.findAll();
            request.setAttribute("dentistes", dentistes);
            request.getRequestDispatcher("/WEB-INF/jsp/Dentiste.jsp").forward(request, response);
        } 
        
        // Afficher le profil détaillé d'un dentiste
        else if ("view".equals(action)) {
            String idStr = request.getParameter("id");
            if (idStr != null) {
                Integer id = Integer.parseInt(idStr);
                Dentiste dentiste = dentisteService.find(id);
                request.setAttribute("dentiste", dentiste);
            }
            request.getRequestDispatcher("/WEB-INF/jsp/DetailDentiste.jsp").forward(request, response);
        } 
        
        // Afficher le formulaire de création (Espace Aide-Soignant)
        else if ("addForm".equals(action)) {
            request.getRequestDispatcher("/WEB-INF/jsp/AideSoignant.jsp").forward(request, response);
        }
    }

    @Override
    protected void doPost(HttpServletRequest request, HttpServletResponse response) 
            throws ServletException, IOException {
        
        String action = request.getParameter("action");
        
        if ("create".equals(action)) {
            processCreateDentiste(request, response);
        } else if ("update".equals(action)) {
            processUpdateDentiste(request, response);
        } else if ("delete".equals(action)) {
            processDeleteDentiste(request, response);
        }
    }
    
    private void processCreateDentiste(HttpServletRequest request, HttpServletResponse response) 
            throws ServletException, IOException {
        
        try {
            // Extraction des paramètres
            String nom = request.getParameter("nom");
            String prenom = request.getParameter("prenom");
            String email = request.getParameter("email");
            String mdp = request.getParameter("mdp");
            String specialite = request.getParameter("specialite");
            String sexe = request.getParameter("sexe");
            String telStr = request.getParameter("telephone");
            
            // Validation simple
            if (nom == null || email == null || mdp == null) {
                request.setAttribute("erreur", "Les champs Nom, Email et Mot de passe sont obligatoires.");
                request.getRequestDispatcher("/WEB-INF/jsp/AideSoignant.jsp").forward(request, response);
                return;
            }
            
            // Création de l'objet
            Dentiste dentiste = new Dentiste();
            dentiste.setNomD(nom);
            dentiste.setPrenomD(prenom);
            dentiste.setEmailD(email);
            dentiste.setMdpD(mdp);
            dentiste.setSpecialiteD(specialite);
            dentiste.setSexeD(sexe);
            
            if (telStr != null && !telStr.isEmpty()) {
                dentiste.setTelD(Integer.parseInt(telStr));
            }
            
            // Enregistrement via EJB
            dentisteService.create(dentiste);
            
            // Redirection vers la liste pour éviter le double-envoi du formulaire (PRG Pattern)
            response.sendRedirect(request.getContextPath() + "/dentiste?action=list&msg=success");
            
        } catch (Exception e) {
            request.setAttribute("erreur", "Erreur lors de la création : " + e.getMessage());
            request.getRequestDispatcher("/WEB-INF/jsp/AideSoignant.jsp").forward(request, response);
        }
    }
    
    private void processUpdateDentiste(HttpServletRequest request, HttpServletResponse response) 
            throws ServletException, IOException {
        // Logique de mise à jour simplifiée
        String idStr = request.getParameter("id");
        if (idStr != null) {
            Integer id = Integer.parseInt(idStr);
            Dentiste d = dentisteService.find(id);
            if (d != null) {
                d.setNomD(request.getParameter("nom"));
                d.setSpecialiteD(request.getParameter("specialite"));
                dentisteService.update(d);
            }
        }
        response.sendRedirect(request.getContextPath() + "/dentiste?action=list");
    }
    
    private void processDeleteDentiste(HttpServletRequest request, HttpServletResponse response) 
            throws ServletException, IOException {
        String idStr = request.getParameter("id");
        if (idStr != null) {
            dentisteService.delete(Integer.parseInt(idStr));
        }
        response.sendRedirect(request.getContextPath() + "/dentiste?action=list");
    }
}