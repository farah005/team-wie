package servlets;

import jakarta.ejb.EJB;
import jakarta.servlet.ServletException;
import jakarta.servlet.annotation.MultipartConfig;
import jakarta.servlet.annotation.WebServlet;
import jakarta.servlet.http.HttpServlet;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import jakarta.servlet.http.Part;

import java.io.IOException;
import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.List;

import entities.AideSoignant;
import interfaces.AideSoignantLocal;

@WebServlet("/aidesoignant")
@MultipartConfig(fileSizeThreshold = 1024 * 1024, maxFileSize = 1024 * 1024 * 5)
public class AideSoignantServlet extends HttpServlet {
    
    private static final long serialVersionUID = 1L;

    @EJB
    private AideSoignantLocal aideSoignantService;

    @Override
    protected void doGet(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {
        String action = request.getParameter("action");

        if ("list".equals(action)) {
            List<AideSoignant> aides = aideSoignantService.findAll();
            request.setAttribute("aides", aides);
            // On affiche la page de liste
            request.getRequestDispatcher("/WEB-INF/jsp/AideSoignant.jsp").forward(request, response);
        } else {
            // Affichage du formulaire pour création ou édition
            String idStr = request.getParameter("id");
            if (idStr != null && !idStr.isBlank()) {
                Integer id = Integer.valueOf(idStr);
                AideSoignant as = aideSoignantService.find(id);
                request.setAttribute("aidesoignant", as);
            }
            request.getRequestDispatcher("/WEB-INF/jsp/AideSoignant.jsp").forward(request, response);
        }
    }

    @Override
    protected void doPost(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {
        String action = request.getParameter("action");

        if ("create".equals(action)) {
            processCreateOrUpdate(request, response, true);
        } else if ("update".equals(action)) {
            processCreateOrUpdate(request, response, false);
        } else if ("delete".equals(action)) {
            deleteAideSoignant(request, response);
        } else {
            response.sendRedirect(request.getContextPath() + "/aidesoignant?action=list");
        }
    }

    private void processCreateOrUpdate(HttpServletRequest request, HttpServletResponse response, boolean isCreate)
            throws ServletException, IOException {
        try {
            String idStr = request.getParameter("idAS");
            String nom = request.getParameter("nomAS");
            String prenom = request.getParameter("prenomAS");
            String email = request.getParameter("emailAS");
            String mdp = request.getParameter("mdpAS");
            String specialite = request.getParameter("specialiteAS");
            String telephone = request.getParameter("telephoneAS");
            String dateEmbaucheStr = request.getParameter("dateEmbaucheAS");

            // Validation des champs obligatoires
            if (isBlank(nom) || isBlank(prenom) || isBlank(email) || (isCreate && isBlank(mdp))) {
                request.setAttribute("erreur", "Veuillez remplir tous les champs obligatoires");
                request.getRequestDispatcher("/WEB-INF/jsp/AideSoignant.jsp").forward(request, response);
                return;
            }

            AideSoignant as;
            if (isCreate) {
                as = new AideSoignant();
            } else {
                as = aideSoignantService.find(Integer.parseInt(idStr));
            }

            as.setNomAS(nom);
            as.setPrenomAS(prenom);
            as.setEmailAS(email);
            if (!isBlank(mdp)) as.setMdpAS(mdp);
            as.setSpecialisationAS(specialite);
            as.setTelAS(telephone);

            if (!isBlank(dateEmbaucheStr)) {
                as.setDateEmbaucheAS(new SimpleDateFormat("yyyy-MM-dd").parse(dateEmbaucheStr));
            }

            // Gestion de la photo
            Part part = request.getPart("photoAS");
            if (part != null && part.getSize() > 0) {
                as.setPhotoAS(part.getSubmittedFileName());
            }

            if (isCreate) {
                aideSoignantService.create(as);
                // Placer un message de succès dans la session pour affichage après redirection
                request.getSession().setAttribute("message", "Inscription de l'aide-soignant réussie.");
            } else {
                aideSoignantService.update(as);
            }

            response.sendRedirect(request.getContextPath() + "/aidesoignant?action=list");

        } catch (Exception e) {
            request.setAttribute("erreur", "Erreur de traitement : " + e.getMessage());
            request.getRequestDispatcher("/WEB-INF/jsp/AideSoignant.jsp").forward(request, response);
        }
    }

    private void deleteAideSoignant(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {
        try {
            String idStr = request.getParameter("id");
            if (!isBlank(idStr)) {
                aideSoignantService.delete(Integer.valueOf(idStr));
            }
            response.sendRedirect(request.getContextPath() + "/aidesoignant?action=list");
        } catch (Exception e) {
            request.setAttribute("erreur", "Erreur lors de la suppression : " + e.getMessage());
            request.getRequestDispatcher("/WEB-INF/jsp/ListeAideSoignant.jsp").forward(request, response);
        }
    }

    // Méthode utilitaire de validation corrigée
    private boolean isBlank(String str) {
        return str == null || str.trim().isEmpty();
    }
}