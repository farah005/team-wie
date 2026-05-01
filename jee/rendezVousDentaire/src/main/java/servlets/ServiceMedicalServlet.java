package servlets;

import jakarta.ejb.EJB;
import jakarta.servlet.ServletException;
import jakarta.servlet.annotation.WebServlet;
import jakarta.servlet.http.HttpServlet;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import java.io.IOException;
import java.math.BigDecimal;
import java.util.List;

import entities.ServiceMedical;
import interfaces.ServiceMedicalLocal;

@WebServlet("/service")
public class ServiceMedicalServlet extends HttpServlet {
    
    private static final long serialVersionUID = 1L;

    @EJB
    private ServiceMedicalLocal serviceMedicalService;

    @Override
    protected void doGet(HttpServletRequest request, HttpServletResponse response) 
            throws ServletException, IOException {
        String action = request.getParameter("action");
        
        try {
            if ("list".equals(action)) {
                List<ServiceMedical> services = serviceMedicalService.findAll();
                request.setAttribute("services", services);
                // fournir la liste des types pour les filtres
                List<String> types = serviceMedicalService.findAllTypes();
                request.setAttribute("types", types);
                request.getRequestDispatcher("/WEB-INF/jsp/ListeServices.jsp").forward(request, response);
                
            } else if ("edit".equals(action)) {
                // Charger les données pour le formulaire de modification
                String idStr = request.getParameter("id");
                if (idStr != null) {
                    ServiceMedical sm = serviceMedicalService.find(Integer.parseInt(idStr));
                    request.setAttribute("serviceToEdit", sm);
                }
                // types pour l'autocomplétion/selection
                List<String> types = serviceMedicalService.findAllTypes();
                request.setAttribute("types", types);
                request.getRequestDispatcher("/WEB-INF/jsp/Service.jsp").forward(request, response);
                
            } else {
                // Par défaut : afficher le formulaire vide
                List<String> types = serviceMedicalService.findAllTypes();
                request.setAttribute("types", types);
                request.getRequestDispatcher("/WEB-INF/jsp/Service.jsp").forward(request, response);
            }
        } catch (Exception e) {
            request.setAttribute("erreur", "Erreur lors du chargement : " + e.getMessage());
            request.getRequestDispatcher("/WEB-INF/jsp/Service.jsp").forward(request, response);
        }
    }

    @Override
    protected void doPost(HttpServletRequest request, HttpServletResponse response) 
            throws ServletException, IOException {
        String action = request.getParameter("action");
        
        // Restrict create/update/delete to authorized roles
        if ("create".equals(action) || "update".equals(action) || "delete".equals(action)) {
            String userType = (String) request.getSession().getAttribute("userType");
            if (!"aide-soignant".equalsIgnoreCase(userType) && !"dentiste".equalsIgnoreCase(userType)) {
                request.setAttribute("erreur", "Accès refusé : action réservée au personnel.");
                request.getRequestDispatcher("/WEB-INF/jsp/Service.jsp").forward(request, response);
                return;
            }
        }

        if ("create".equals(action)) {
            processCreate(request, response);
        } else if ("update".equals(action)) {
            processUpdate(request, response);
        } else if ("delete".equals(action)) {
            processDelete(request, response);
        } else if ("search".equals(action)) {
            processSearch(request, response);
        }
    }

    private void processCreate(HttpServletRequest request, HttpServletResponse response) 
            throws ServletException, IOException {
        try {
            ServiceMedical sm = mapRequestToService(request);
            serviceMedicalService.create(sm);
            
            // Redirection pour éviter la double soumission au refresh
            response.sendRedirect(request.getContextPath() + "/service?action=list");
        } catch (Exception e) {
            request.setAttribute("erreur", "Erreur de création : " + e.getMessage());
            request.getRequestDispatcher("/WEB-INF/jsp/Service.jsp").forward(request, response);
        }
    }

    private void processUpdate(HttpServletRequest request, HttpServletResponse response) 
            throws ServletException, IOException {
        try {
            String idStr = request.getParameter("id");
            if (idStr == null || idStr.isEmpty()) throw new Exception("ID manquant");

            ServiceMedical sm = mapRequestToService(request);
            sm.setNumSM(Integer.parseInt(idStr)); // On attache l'ID pour le merge
            
            serviceMedicalService.update(sm);
            response.sendRedirect(request.getContextPath() + "/service?action=list");
        } catch (Exception e) {
            request.setAttribute("erreur", "Erreur de mise à jour : " + e.getMessage());
            request.getRequestDispatcher("/WEB-INF/jsp/Service.jsp").forward(request, response);
        }
    }

    private void processDelete(HttpServletRequest request, HttpServletResponse response) 
            throws IOException {
        String idStr = request.getParameter("id");
        if (idStr != null) {
            serviceMedicalService.delete(Integer.parseInt(idStr));
        }
        response.sendRedirect(request.getContextPath() + "/service?action=list");
    }

    private void processSearch(HttpServletRequest request, HttpServletResponse response) 
            throws ServletException, IOException {
        String type = request.getParameter("typeRecherche");
        String nom = request.getParameter("nomRecherche");
        List<ServiceMedical> services = serviceMedicalService.search(nom, type);
        request.setAttribute("services", services);
        // renvoyer aussi la liste des types pour le formulaire
        List<String> types = serviceMedicalService.findAllTypes();
        request.setAttribute("types", types);
        request.getRequestDispatcher("/WEB-INF/jsp/Service.jsp").forward(request, response);
    }

    // Méthode utilitaire pour transformer les paramètres du formulaire en objet Entité
    private ServiceMedical mapRequestToService(HttpServletRequest request) throws Exception {
        String nom = request.getParameter("nom");
        String type = request.getParameter("type");
        String description = request.getParameter("description");
        String tarifStr = request.getParameter("tarif");

        if (nom == null || nom.isBlank() || type == null || type.isBlank()) {
            throw new Exception("Le nom et le type sont obligatoires.");
        }

        ServiceMedical sm = new ServiceMedical();
        sm.setNomSM(nom);
        sm.setTypeSM(type);
        sm.setDescriptionSM(description);
        
        if (tarifStr != null && !tarifStr.isBlank()) {
            sm.setTarifSM(new BigDecimal(tarifStr));
        } else {
            sm.setTarifSM(BigDecimal.ZERO);
        }
        
        return sm;
    }
}