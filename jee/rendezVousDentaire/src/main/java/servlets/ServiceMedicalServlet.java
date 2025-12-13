package servlets;

import jakarta.servlet.ServletException;
import jakarta.servlet.annotation.WebServlet;
import jakarta.servlet.http.HttpServlet;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import java.io.IOException;
import java.math.BigDecimal;

@WebServlet("/service")
public class ServiceMedicalServlet extends HttpServlet {
    private static final long serialVersionUID = 1L;

    protected void doGet(HttpServletRequest request, HttpServletResponse response) 
            throws ServletException, IOException {
        String action = request.getParameter("action");
        
        if ("list".equals(action)) {
            // Récupérer tous les services
            // List<ServiceMedical> services = serviceMedicalService.findAll();
            // request.setAttribute("services", services);
            request.getRequestDispatcher("/WEB-INF/jsp/ListeServices.jsp").forward(request, response);
        } else if ("view".equals(action)) {
            String idStr = request.getParameter("id");
            if (idStr != null) {
                Integer id = Integer.parseInt(idStr);
                // ServiceMedical service = serviceMedicalService.find(id);
                // request.setAttribute("service", service);
            }
            request.getRequestDispatcher("/WEB-INF/jsp/DetailService.jsp").forward(request, response);
        } else {
            // Afficher le formulaire de service
            request.getRequestDispatcher("/WEB-INF/jsp/Service.jsp").forward(request, response);
        }
    }

    protected void doPost(HttpServletRequest request, HttpServletResponse response) 
            throws ServletException, IOException {
        String action = request.getParameter("action");
        
        if ("create".equals(action)) {
            createService(request, response);
        } else if ("update".equals(action)) {
            updateService(request, response);
        } else if ("delete".equals(action)) {
            deleteService(request, response);
        } else if ("search".equals(action)) {
            searchService(request, response);
        }
    }
    
    private void createService(HttpServletRequest request, HttpServletResponse response) 
            throws ServletException, IOException {
        String nom = request.getParameter("nom");
        String type = request.getParameter("type");
        String description = request.getParameter("description");
        String tarifStr = request.getParameter("tarif");
        
        // Validation
        if (nom == null || type == null) {
            request.setAttribute("erreur", "Veuillez remplir tous les champs obligatoires");
            request.getRequestDispatcher("/WEB-INF/jsp/Service.jsp").forward(request, response);
            return;
        }
        
        BigDecimal tarif = null;
        if (tarifStr != null && !tarifStr.isEmpty()) {
            tarif = new BigDecimal(tarifStr);
        }
        
        // Créer l'entité ServiceMedical
        // ServiceMedical service = new ServiceMedical();
        // service.setNomSM(nom);
        // service.setTypeSM(type);
        // service.setDescriptionSM(description);
        // service.setTarifSM(tarif);
        
        // Appel au service EJB
        // serviceMedicalService.create(service);
        
        request.setAttribute("message", "Service médical créé avec succès");
        request.getRequestDispatcher("/WEB-INF/jsp/Service.jsp").forward(request, response);
    }
    
    private void updateService(HttpServletRequest request, HttpServletResponse response) 
            throws ServletException, IOException {
        String idStr = request.getParameter("id");
        // Logique de mise à jour
        response.sendRedirect(request.getContextPath() + "/service?action=list");
    }
    
    private void deleteService(HttpServletRequest request, HttpServletResponse response) 
            throws ServletException, IOException {
        String idStr = request.getParameter("id");
        if (idStr != null) {
            Integer id = Integer.parseInt(idStr);
            // serviceMedicalService.delete(id);
        }
        response.sendRedirect(request.getContextPath() + "/service?action=list");
    }
    
    private void searchService(HttpServletRequest request, HttpServletResponse response) 
            throws ServletException, IOException {
        String type = request.getParameter("typeRecherche");
        
        if (type != null && !type.isEmpty()) {
            // List<ServiceMedical> services = serviceMedicalService.findByType(type);
            // request.setAttribute("services", services);
        }
        
        request.getRequestDispatcher("/WEB-INF/jsp/Service.jsp").forward(request, response);
    }
}