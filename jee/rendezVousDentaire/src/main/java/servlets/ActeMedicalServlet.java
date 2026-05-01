   package servlets;

import jakarta.servlet.ServletException;
import jakarta.servlet.annotation.WebServlet;
import jakarta.servlet.http.HttpServlet;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import jakarta.ejb.EJB;
import java.io.IOException;
import java.math.BigDecimal;
import java.util.List;

import interfaces.ActeMedicalLocal;
import interfaces.RendezvousLocal;
import interfaces.ServiceMedicalLocal;

import entities.ActeMedical;
import entities.Rendezvous;
import entities.ServiceMedical;

@WebServlet("/actemedical")
public class ActeMedicalServlet extends HttpServlet {
    @EJB
    private ActeMedicalLocal acteMedicalService;
    @EJB
    private RendezvousLocal rendezvousService;
    @EJB
    private ServiceMedicalLocal serviceMedicalService;
    private static final long serialVersionUID = 1L;

    protected void doGet(HttpServletRequest request, HttpServletResponse response) 
            throws ServletException, IOException {
        String action = request.getParameter("action");
        
        // fournir la liste des services pour le formulaire
        try {
            request.setAttribute("services", serviceMedicalService.findAll());
        } catch (Exception ignored) {}

        if ("list".equals(action)) {
            listActes(request, response);
        } else if ("view".equals(action)) {
            viewActe(request, response);
        } else if ("byRendezvous".equals(action)) {
            listByRendezvous(request, response);
        } else if ("new".equals(action)) {
            // Préparer le formulaire pour un nouvel acte (éventuellement pré-rempli par idRv)
            request.getRequestDispatcher("/WEB-INF/jsp/ActeMedical.jsp").forward(request, response);
        } else {
            // Afficher le formulaire d'acte médical
            request.getRequestDispatcher("/WEB-INF/jsp/ActeMedical.jsp").forward(request, response);
        }
    }

    protected void doPost(HttpServletRequest request, HttpServletResponse response) 
            throws ServletException, IOException {
        String action = request.getParameter("action");
        
        if ("create".equals(action)) {
            createActe(request, response);
        } else if ("update".equals(action)) {
            updateActe(request, response);
        } else if ("delete".equals(action)) {
            deleteActe(request, response);
        }
    }
    
    private void createActe(HttpServletRequest request, HttpServletResponse response) 
            throws ServletException, IOException {
        String idRvStr = request.getParameter("idRv");
        String numSMStr = request.getParameter("numSM");
        String description = request.getParameter("description");
        String tarifStr = request.getParameter("tarif");
        
        // Validation
        if (idRvStr == null || numSMStr == null) {
            request.setAttribute("erreur", "Veuillez remplir tous les champs obligatoires");
            request.getRequestDispatcher("/WEB-INF/jsp/ActeMedical.jsp").forward(request, response);
            return;
        }
        
        Integer idRv = Integer.parseInt(idRvStr);
        Integer numSM = Integer.parseInt(numSMStr);
        
        BigDecimal tarif = null;
        if (tarifStr != null && !tarifStr.isEmpty()) {
            tarif = new BigDecimal(tarifStr);
        }
        
        // Récupérer les entités liées
        Rendezvous rdv = rendezvousService.find(idRv);
        ServiceMedical sm = serviceMedicalService.find(numSM);
        if (rdv == null || sm == null) {
            request.setAttribute("erreur", "Rendez-vous ou service médical introuvable.");
            request.setAttribute("services", serviceMedicalService.findAll());
            request.getRequestDispatcher("/WEB-INF/jsp/ActeMedical.jsp").forward(request, response);
            return;
        }

        // Autoriser la création d'un acte uniquement si le rendez-vous est terminé
        String statut = rdv.getStatutRv();
        if (statut == null || !"Terminé".equalsIgnoreCase(statut.trim())) {
            request.setAttribute("erreur", "Impossible d'enregistrer un acte : le rendez-vous n'est pas terminé.");
            request.setAttribute("services", serviceMedicalService.findAll());
            request.getRequestDispatcher("/WEB-INF/jsp/DetailRendezvous.jsp").forward(request, response);
            return;
        }

        // Créer l'entité ActeMedical
        ActeMedical acte = new ActeMedical();
        acte.setRendezvous(rdv);
        acte.setServiceMedical(sm);
        acte.setDescriptionAM(description);
        acte.setTarifAM(tarif);

        // Appel au service EJB
        acteMedicalService.create(acte);
        
        request.setAttribute("message", "Acte médical créé avec succès");
        request.getRequestDispatcher("/WEB-INF/jsp/ActeMedical.jsp").forward(request, response);
    }
    
    private void updateActe(HttpServletRequest request, HttpServletResponse response) 
            throws ServletException, IOException {
        String idStr = request.getParameter("id");
        // Logique de mise à jour
        response.sendRedirect(request.getContextPath() + "/actemedical?action=list");
    }
    
    private void deleteActe(HttpServletRequest request, HttpServletResponse response) 
            throws ServletException, IOException {
        String idStr = request.getParameter("id");
        if (idStr != null) {
            Integer id = Integer.parseInt(idStr);
                  acteMedicalService.delete(id);
        }
        response.sendRedirect(request.getContextPath() + "/actemedical?action=list");
    }
    
    private void listActes(HttpServletRequest request, HttpServletResponse response) 
            throws ServletException, IOException {
         List<ActeMedical> actes = acteMedicalService.findAll();
         request.setAttribute("actes", actes);
        request.getRequestDispatcher("/WEB-INF/jsp/ListeActes.jsp").forward(request, response);
    }
    
    private void viewActe(HttpServletRequest request, HttpServletResponse response) 
            throws ServletException, IOException {
        String idStr = request.getParameter("id");
        if (idStr != null) {
            Integer id = Integer.parseInt(idStr);
            ActeMedical acte = acteMedicalService.find(id);
            request.setAttribute("acte", acte);
        }
        request.getRequestDispatcher("/WEB-INF/jsp/DetailActe.jsp").forward(request, response);
    }
    
    private void listByRendezvous(HttpServletRequest request, HttpServletResponse response) 
            throws ServletException, IOException {
        String idRvStr = request.getParameter("idRv");
        if (idRvStr != null) {
            Integer idRv = Integer.parseInt(idRvStr);
            List<ActeMedical> actes = acteMedicalService.findByRendezvous(idRv);
            request.setAttribute("actes", actes);
        }
        request.getRequestDispatcher("/WEB-INF/jsp/ListeActes.jsp").forward(request, response);
    }
}