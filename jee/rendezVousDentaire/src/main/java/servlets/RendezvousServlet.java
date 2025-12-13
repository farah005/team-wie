package servlets;

import jakarta.servlet.ServletException;
import jakarta.servlet.annotation.WebServlet;
import jakarta.servlet.http.HttpServlet;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import jakarta.servlet.http.HttpSession;
import java.io.IOException;
import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.Date;

@WebServlet("/rendezvous")
public class RendezvousServlet extends HttpServlet {
    private static final long serialVersionUID = 1L;

    protected void doGet(HttpServletRequest request, HttpServletResponse response) 
            throws ServletException, IOException {
        String action = request.getParameter("action");
        HttpSession session = request.getSession(false);
        
        if (session == null || session.getAttribute("email") == null) {
            response.sendRedirect(request.getContextPath() + "/connexion");
            return;
        }
        
        if ("list".equals(action)) {
            listRendezvous(request, response);
        } else if ("view".equals(action)) {
            viewRendezvous(request, response);
        } else if ("byDate".equals(action)) {
            searchByDate(request, response);
        } else if ("byStatut".equals(action)) {
            searchByStatut(request, response);
        } else {
            // Afficher le formulaire de rendez-vous
            request.getRequestDispatcher("/WEB-INF/jsp/Rendezvous.jsp").forward(request, response);
        }
    }

    protected void doPost(HttpServletRequest request, HttpServletResponse response) 
            throws ServletException, IOException {
        String action = request.getParameter("action");
        
        if ("create".equals(action)) {
            createRendezvous(request, response);
        } else if ("update".equals(action)) {
            updateRendezvous(request, response);
        } else if ("delete".equals(action)) {
            deleteRendezvous(request, response);
        } else if ("updateStatut".equals(action)) {
            updateStatut(request, response);
        }
    }
    
    private void createRendezvous(HttpServletRequest request, HttpServletResponse response) 
            throws ServletException, IOException {
        try {
            String idPatientStr = request.getParameter("idPatient");
            String idDentisteStr = request.getParameter("idDentiste");
            String dateRvStr = request.getParameter("dateRv");
            String heureRv = request.getParameter("heureRv");
            String statut = request.getParameter("statut");
            String details = request.getParameter("details");
            
            // Validation
            if (idPatientStr == null || idDentisteStr == null || 
                dateRvStr == null || heureRv == null) {
                request.setAttribute("erreur", "Veuillez remplir tous les champs obligatoires");
                request.getRequestDispatcher("/WEB-INF/jsp/Rendezvous.jsp").forward(request, response);
                return;
            }
            
            Integer idPatient = Integer.parseInt(idPatientStr);
            Integer idDentiste = Integer.parseInt(idDentisteStr);
            
            SimpleDateFormat sdf = new SimpleDateFormat("yyyy-MM-dd");
            Date dateRv = sdf.parse(dateRvStr);
            
            // Créer l'entité Rendezvous
            // Rendezvous rdv = new Rendezvous();
            // rdv.setIdP(idPatient);
            // rdv.setIdD(idDentiste);
            // rdv.setDateRv(dateRv);
            // rdv.setHeureRv(heureRv);
            // rdv.setStatutRv(statut != null ? statut : "En attente");
            // rdv.setDetailsRv(details);
            
            // Appel au service EJB
            // rendezvousService.create(rdv);
            
            request.setAttribute("message", "Rendez-vous créé avec succès");
            request.getRequestDispatcher("/WEB-INF/jsp/Rendezvous.jsp").forward(request, response);
            
        } catch (ParseException e) {
            request.setAttribute("erreur", "Format de date invalide");
            request.getRequestDispatcher("/WEB-INF/jsp/Rendezvous.jsp").forward(request, response);
        }
    }
    
    private void updateRendezvous(HttpServletRequest request, HttpServletResponse response) 
            throws ServletException, IOException {
        String idStr = request.getParameter("id");
        // Logique de mise à jour
        response.sendRedirect(request.getContextPath() + "/rendezvous?action=list");
    }
    
    private void deleteRendezvous(HttpServletRequest request, HttpServletResponse response) 
            throws ServletException, IOException {
        String idStr = request.getParameter("id");
        if (idStr != null) {
            Integer id = Integer.parseInt(idStr);
            // rendezvousService.delete(id);
        }
        response.sendRedirect(request.getContextPath() + "/rendezvous?action=list");
    }
    
    private void listRendezvous(HttpServletRequest request, HttpServletResponse response) 
            throws ServletException, IOException {
        HttpSession session = request.getSession();
        String userType = (String) session.getAttribute("userType");
        
        if ("patient".equals(userType)) {
            // List<Rendezvous> rdvs = rendezvousService.findByPatient(patientId);
            // request.setAttribute("rendezvous", rdvs);
        } else if ("dentiste".equals(userType)) {
            // List<Rendezvous> rdvs = rendezvousService.findByDentiste(dentisteId);
            // request.setAttribute("rendezvous", rdvs);
        }
        
        request.getRequestDispatcher("/WEB-INF/jsp/Rendezvous.jsp").forward(request, response);
    }
    
    private void viewRendezvous(HttpServletRequest request, HttpServletResponse response) 
            throws ServletException, IOException {
        String idStr = request.getParameter("id");
        if (idStr != null) {
            Integer id = Integer.parseInt(idStr);
            // Rendezvous rdv = rendezvousService.find(id);
            // request.setAttribute("rendezvous", rdv);
        }
        request.getRequestDispatcher("/WEB-INF/jsp/DetailRendezvous.jsp").forward(request, response);
    }
    
    private void searchByDate(HttpServletRequest request, HttpServletResponse response) 
            throws ServletException, IOException {
        try {
            String dateStr = request.getParameter("date");
            SimpleDateFormat sdf = new SimpleDateFormat("yyyy-MM-dd");
            Date date = sdf.parse(dateStr);
            
            // List<Rendezvous> rdvs = rendezvousService.findByDate(date);
            // request.setAttribute("rendezvous", rdvs);
            
            request.getRequestDispatcher("/WEB-INF/jsp/Rendezvous.jsp").forward(request, response);
        } catch (ParseException e) {
            request.setAttribute("erreur", "Format de date invalide");
            request.getRequestDispatcher("/WEB-INF/jsp/Rendezvous.jsp").forward(request, response);
        }
    }
    
    private void searchByStatut(HttpServletRequest request, HttpServletResponse response) 
            throws ServletException, IOException {
        String statut = request.getParameter("statut");
        
        if (statut != null && !statut.isEmpty()) {
            // List<Rendezvous> rdvs = rendezvousService.findByStatut(statut);
            // request.setAttribute("rendezvous", rdvs);
        }
        
        request.getRequestDispatcher("/WEB-INF/jsp/Rendezvous.jsp").forward(request, response);
    }
    
    private void updateStatut(HttpServletRequest request, HttpServletResponse response) 
            throws ServletException, IOException {
        String idStr = request.getParameter("id");
        String newStatut = request.getParameter("newStatut");
        
        if (idStr != null && newStatut != null) {
            Integer id = Integer.parseInt(idStr);
            // Rendezvous rdv = rendezvousService.find(id);
            // rdv.setStatutRv(newStatut);
            // rendezvousService.update(rdv);
        }
        
        response.sendRedirect(request.getContextPath() + "/rendezvous?action=list");
    }
}