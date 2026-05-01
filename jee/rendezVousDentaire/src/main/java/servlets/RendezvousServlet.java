package servlets;

import jakarta.ejb.EJB;
import jakarta.servlet.ServletException;
import jakarta.servlet.annotation.WebServlet;
import jakarta.servlet.http.HttpServlet;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import jakarta.servlet.http.HttpSession;
import interfaces.DentisteLocal;
import interfaces.PatientLocal;
import interfaces.RendezvousLocal;
import entities.Rendezvous;
import entities.Patient;
import entities.Dentiste;

import java.io.IOException;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.List;

@WebServlet("/rendezvous")
public class RendezvousServlet extends HttpServlet {
    private static final long serialVersionUID = 1L;

    @EJB
    private RendezvousLocal RendezvousService;
    @EJB
    private PatientLocal PatientService;
    @EJB
    private DentisteLocal DentisteService;

    private static final String VUE_FORMULAIRE = "/WEB-INF/jsp/Rendezvous.jsp";
    private static final String VUE_DETAIL = "/WEB-INF/jsp/DetailRendezvous.jsp";

    @Override
    protected void doGet(HttpServletRequest request, HttpServletResponse response) 
            throws ServletException, IOException {
        
        HttpSession session = request.getSession(false);
        if (session == null || session.getAttribute("idConnecte") == null) {
            response.sendRedirect(request.getContextPath() + "/connexion");
            return;
        }

        // Charger toujours la liste des dentistes pour le formulaire <select>
        try {
            List<Dentiste> lesDentistes = DentisteService.findAll();
            request.setAttribute("lesDentistes", lesDentistes);
        } catch (Exception e) {
            request.setAttribute("erreur", "Erreur chargement dentistes : " + e.getMessage());
        }

        String action = request.getParameter("action");
        if ("view".equals(action)) {
            viewRendezvous(request, response);
        } else if ("delete".equals(action)) {
            deleteRendezvous(request, response);
        } else {
            listRendezvous(request, response);
        }
    }

    @Override
    protected void doPost(HttpServletRequest request, HttpServletResponse response) 
            throws ServletException, IOException {
        
        HttpSession session = request.getSession(false);
        if (session == null || session.getAttribute("idConnecte") == null) {
            response.sendRedirect(request.getContextPath() + "/connexion");
            return;
        }

        String action = request.getParameter("action");
        if ("create".equals(action)) {
            createRendezvous(request, response);
        } else if ("updateStatut".equals(action)) {
            updateStatut(request, response);
        }
    }
    
    // --- LOGIQUE METIER ---

    private void listRendezvous(HttpServletRequest request, HttpServletResponse response) 
            throws ServletException, IOException {
        HttpSession session = request.getSession();
        String userType = (String) session.getAttribute("userType");
        Integer idConnecte = (Integer) session.getAttribute("idConnecte");

        List<Rendezvous> liste;
        if ("patient".equals(userType)) {
            liste = RendezvousService.findByPatient(idConnecte);
        } else {
            liste = RendezvousService.findAll();
        }

        request.setAttribute("listeRdvs", liste);
        request.getRequestDispatcher(VUE_FORMULAIRE).forward(request, response);
    }

    private void createRendezvous(HttpServletRequest request, HttpServletResponse response) 
            throws ServletException, IOException {
        try {
            Integer idP = Integer.parseInt(request.getParameter("idPatient"));
            Integer idD = Integer.parseInt(request.getParameter("idDentiste"));
            String dateStr = request.getParameter("dateRv");
            String heureRv = request.getParameter("heureRv");
            String details = request.getParameter("details");

            Date dateRv = new SimpleDateFormat("yyyy-MM-dd").parse(dateStr);

            // --- 1. SÉCURITÉ : DISPONIBILITÉ DENTISTE ---
            if (!RendezvousService.isSlotAvailable(idD, dateRv, heureRv)) {
                request.setAttribute("erreur", "Ce créneau horaire est déjà réservé pour ce dentiste.");
                listRendezvous(request, response);
                return;
            }

            // --- 2. SÉCURITÉ : UN SEUL RDV PAR PATIENT PAR JOUR ---
            if (RendezvousService.patientADejaRDV(idP, dateRv)) {
                request.setAttribute("erreur", "Le patient possède déjà un rendez-vous à cette date.");
                listRendezvous(request, response);
                return;
            }

            // Création si les tests passent
            Patient patient = PatientService.find(idP);
            Dentiste dentiste = DentisteService.find(idD);

            Rendezvous rdv = new Rendezvous();
            rdv.setPatient(patient);
            rdv.setDentiste(dentiste);
            rdv.setDateRv(dateRv);
            rdv.setHeureRv(heureRv);
            rdv.setStatutRv("En attente");
            rdv.setDetailsRv(details);

            RendezvousService.create(rdv);
            request.setAttribute("message", "Rendez-vous enregistré avec succès !");
            
        } catch (Exception e) {
            request.setAttribute("erreur", "Erreur lors de la prise de RDV : " + e.getMessage());
        }
        listRendezvous(request, response);
    }

    private void updateStatut(HttpServletRequest request, HttpServletResponse response) 
            throws ServletException, IOException {
        try {
            Integer id = Integer.parseInt(request.getParameter("id"));
            String nouveauStatut = request.getParameter("statut");
            HttpSession session = request.getSession();
            String userType = (String) session.getAttribute("userType");

            // Contrôle d'autorisation : seuls les membres du personnel
            // (aide-soignant ou dentiste) peuvent changer le statut
            if (nouveauStatut != null) {
                String s = nouveauStatut.trim();
                boolean isPrivilegedChange = s.equalsIgnoreCase("Confirmé")
                        || s.equalsIgnoreCase("Terminé")
                        || s.equalsIgnoreCase("Annulé");
                if (isPrivilegedChange) {
                    if (userType == null || !("aide-soignant".equalsIgnoreCase(userType)
                            || "dentiste".equalsIgnoreCase(userType))) {
                        request.setAttribute("erreur", "Accès refusé : statut réservé au personnel.");
                        listRendezvous(request, response);
                        return;
                    }
                }
            }

            // Enregistrer exactement le statut fourni (pas de conversion automatique)
            RendezvousService.updateStatut(id, nouveauStatut);
            request.setAttribute("message", "Le rendez-vous est désormais : " + nouveauStatut);
        } catch (Exception e) {
            request.setAttribute("erreur", "Impossible de mettre à jour le statut.");
        }
        listRendezvous(request, response);
    }

    private void deleteRendezvous(HttpServletRequest request, HttpServletResponse response) 
            throws ServletException, IOException {
        HttpSession session = request.getSession();
        if (!"aide-soignant".equals(session.getAttribute("userType"))) {
            request.setAttribute("erreur", "Accès refusé : Seul l'aide-soignant peut supprimer un RDV.");
        } else {
            try {
                Integer id = Integer.parseInt(request.getParameter("id"));
                RendezvousService.delete(id);
                request.setAttribute("message", "Le rendez-vous a été supprimé.");
            } catch (Exception e) {
                request.setAttribute("erreur", "Erreur lors de la suppression.");
            }
        }
        listRendezvous(request, response);
    }

    private void viewRendezvous(HttpServletRequest request, HttpServletResponse response) 
            throws ServletException, IOException {
        try {
            Integer id = Integer.parseInt(request.getParameter("id"));
            Rendezvous rdv = RendezvousService.find(id);
            if (rdv != null) {
                request.setAttribute("rdv", rdv);
                request.getRequestDispatcher(VUE_DETAIL).forward(request, response);
            } else {
                throw new Exception();
            }
        } catch (Exception e) {
            response.sendRedirect("rendezvous?action=list");
        }
    }
}