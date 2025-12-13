
package servlets;

import jakarta.servlet.ServletException;
import jakarta.servlet.annotation.MultipartConfig;
import jakarta.servlet.annotation.WebServlet;
import jakarta.servlet.http.HttpServlet;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;

import java.io.IOException;
import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.Date;

@WebServlet("/aidesoignant")
@MultipartConfig
public class AideSoignantServlet extends HttpServlet {
    private static final long serialVersionUID = 1L;

    @Override
    protected void doGet(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {
        String action = request.getParameter("action");

        if ("list".equals(action)) {
            // Afficher la liste des aide-soignants
            // List<AideSoignant> aides = aideSoignantService.findAll();
            // request.setAttribute("aides", aides);
            request.getRequestDispatcher("/WEB-INF/jsp/AideSoignants.jsp").forward(request, response);

        } else {
            // Afficher le formulaire (création par défaut / édition si param id)
            // Si tu veux précharger pour edit :
            // String idStr = request.getParameter("id");
            // if (idStr != null && !idStr.isBlank()) {
            //     Integer id = Integer.valueOf(idStr);
            //     AideSoignant as = aideSoignantService.find(id);
            //     request.setAttribute("aidesoignant", as);
            // }
            request.getRequestDispatcher("/WEB-INF/jsp/AideSoignant.jsp").forward(request, response);
        }
    }

    @Override
    protected void doPost(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {
        String action = request.getParameter("action");

        if ("create".equals(action)) {
            createAideSoignant(request, response);
        } else if ("update".equals(action)) {
            updateAideSoignant(request, response);
        } else if ("delete".equals(action)) {
            deleteAideSoignant(request, response);
        } else {
            // action non reconnue -> retourner vers la liste
            response.sendRedirect(request.getContextPath() + "/aidesoignant?action=list");
        }
    }

    private void createAideSoignant(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {
        try {
            String nom = request.getParameter("nomAS");
            String prenom = request.getParameter("prenomAS");
            String email = request.getParameter("emailAS");
            String mdp = request.getParameter("mdpAS"); // à hasher en prod
            String specialite = request.getParameter("specialiteAS");
            String telephone = request.getParameter("telephoneAS");

            // Exemple d’info optionnelle : date d’embauche
            String dateEmbaucheStr = request.getParameter("dateEmbaucheAS");
            Date dateEmbauche = null;
            if (dateEmbaucheStr != null && !dateEmbaucheStr.isBlank()) {
                dateEmbauche = new SimpleDateFormat("yyyy-MM-dd").parse(dateEmbaucheStr);
            }

            // Validation basique (comme dans ton servlet patient)
            if (isBlank(nom) || isBlank(prenom) || isBlank(email) || isBlank(mdp)) {
                request.setAttribute("erreur", "Veuillez remplir tous les champs obligatoires");
                request.getRequestDispatcher("/WEB-INF/jsp/AideSoignant.jsp").forward(request, response);
                return;
            }

            // Créer l'entité (exemple — à décommenter si tu as l’entité définie)
            // AideSoignant as = new AideSoignant();
            // as.setNomAS(nom);
            // as.setPrenomAS(prenom);
            // as.setEmailAS(email);
            // as.setMdpAS(mdp);
            // as.setSpecialiteAS(specialite);
            // as.setTelephoneAS(telephone);
            // as.setDateEmbaucheAS(dateEmbauche);

            // Appel au service
            // aideSoignantService.create(as);

            // Redirection/confirmation (comme pour patient)
            // request.getRequestDispatcher("/WEB-INF/jsp/validerAideSoignant.jsp").forward(request, response);
            // ou vers la liste :
            response.sendRedirect(request.getContextPath() + "/aidesoignant?action=list");

        } catch (ParseException e) {
            request.setAttribute("erreur", "Format de date invalide");
            request.getRequestDispatcher("/WEB-INF/jsp/AideSoignant.jsp").forward(request, response);
        } catch (Exception e) {
            request.setAttribute("erreur", "Erreur lors de la création : " + e.getMessage());
            request.getRequestDispatcher("/WEB-INF/jsp/AideSoignant.jsp").forward(request, response);
        }
    }

    private void updateAideSoignant(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {
        try {
            String idStr = request.getParameter("idAS");
            if (isBlank(idStr)) {
                request.setAttribute("erreur", "Identifiant manquant");
                request.getRequestDispatcher("/WEB-INF/jsp/AideSoignants.jsp").forward(request, response);
                return;
            }
            Integer id = Integer.valueOf(idStr);

            String nom = request.getParameter("nomAS");
            String prenom = request.getParameter("prenomAS");
            String email = request.getParameter("emailAS");
            String mdp = request.getParameter("mdpAS"); // si non vide, on met à jour; à hasher en prod
            String specialite = request.getParameter("specialiteAS");
            String telephone = request.getParameter("telephoneAS");
            String dateEmbaucheStr = request.getParameter("dateEmbaucheAS");
            Date dateEmbauche = null;
            if (dateEmbaucheStr != null && !dateEmbaucheStr.isBlank()) {
                dateEmbauche = new SimpleDateFormat("yyyy-MM-dd").parse(dateEmbaucheStr);
            }

            // AideSoignant as = aideSoignantService.find(id);
            // if (as == null) {
            //     request.setAttribute("erreur", "Aide-soignant introuvable");
            //     request.getRequestDispatcher("/WEB-INF/jsp/AideSoignants.jsp").forward(request, response);
            //     return;
            // }
            // as.setNomAS(nom);
            // as.setPrenomAS(prenom);
            // as.setEmailAS(email);
            // if (!isBlank(mdp)) as.setMdpAS(mdp);
            // as.setSpecialiteAS(specialite);
            // as.setTelephoneAS(telephone);
            // as.setDateEmbaucheAS(dateEmbauche);

            // aideSoignantService.update(as);

            response.sendRedirect(request.getContextPath() + "/aidesoignant?action=list");

        } catch (ParseException e) {
            request.setAttribute("erreur", "Format de date invalide");
            request.getRequestDispatcher("/WEB-INF/jsp/AideSoignant.jsp").forward(request, response);
        } catch (Exception e) {
            request.setAttribute("erreur", "Erreur lors de la mise à jour : " + e.getMessage());
            request.getRequestDispatcher("/WEB-INF/jsp/AideSoignant.jsp").forward(request, response);
        }
    }

    private void deleteAideSoignant(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {
        try {
            String idStr = request.getParameter("id");
            if (idStr != null && !idStr.isBlank()) {
                Integer id = Integer.valueOf(idStr);
                // aideSoignantService.delete(id);
            }
            response.sendRedirect(request.getContextPath() + "/aidesoignant?action=list");
        } catch (Exception e) {
            request.setAttribute("erreur", "Erreur lors de la suppression : " + e.getMessage());
            request.getRequestDispatcher("/WEB-INF/jsp/AideSoignants.jsp").forward(request, response);
        }
    }

    // Utilitaire
    private boolean isBlank(String s    private boolean isBlank(String s) {
        return s == null || s.trim().isEmpty();
    }
}