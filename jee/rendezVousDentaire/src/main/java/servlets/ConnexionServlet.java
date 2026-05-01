package servlets;

import jakarta.ejb.EJB;
import jakarta.servlet.ServletException;
import jakarta.servlet.annotation.WebServlet;
import jakarta.servlet.http.HttpServlet;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import jakarta.servlet.http.HttpSession;
import java.io.IOException;

import interfaces.AideSoignantLocal;
import interfaces.PatientLocal;
import entities.AideSoignant;
import entities.Patient;
import interfaces.DentisteLocal;
import entities.Dentiste;

@WebServlet("/connexion")
public class ConnexionServlet extends HttpServlet {
    private static final long serialVersionUID = 1L;

    @EJB
    private PatientLocal patientService;
    @EJB
    private AideSoignantLocal AideSoignantService;
    @EJB
    private DentisteLocal DentisteService;
    @Override
    protected void doGet(HttpServletRequest request, HttpServletResponse response) 
            throws ServletException, IOException {
        // Si l'utilisateur est déjà connecté, on le redirige directement vers les rendez-vous
        if (request.getSession().getAttribute("idConnecte") != null) {
            response.sendRedirect(request.getContextPath() + "/rendezvous");
            return;
        }
        request.getRequestDispatcher("/WEB-INF/jsp/connexion.jsp").forward(request, response);
    }

    @Override
    protected void doPost(HttpServletRequest request, HttpServletResponse response) 
            throws ServletException, IOException {
        
        String email = request.getParameter("email");
        String password = request.getParameter("password");
        String userType = request.getParameter("userType");
        
        // 1. Validation des champs
        if (email == null || email.isEmpty() || password == null || password.isEmpty() || userType == null) {
            request.setAttribute("erreur", "Veuillez remplir tous les champs.");
            request.getRequestDispatcher("/WEB-INF/jsp/connexion.jsp").forward(request, response);
            return;
        }

        try {
            Integer idConnecte = null;
            String nomAffiche = "";

            // 2. Vérification des identifiants
            if ("patient".equals(userType)) {
                Patient p = patientService.findByEmail(email); 
              
                if (p != null && p.getMdpP().equals(password)) {
                    idConnecte = p.getIdP();
                    nomAffiche = p.getPrenomP() + " " + p.getNomP();
                }
            } 
            else if ("aide-soignant".equals(userType)) {
                AideSoignant as = AideSoignantService.findByEmail(email);
                
                if (as != null && as.getMdpAS().equals(password)) {
                    idConnecte = as.getIdAS(); 
                    nomAffiche = as.getPrenomAS() + " " + as.getNomAS();
                }
            } else if ("dentiste".equals(userType)) {
                Dentiste d = DentisteService.authenticate(email, password);
                if (d != null) {
                    idConnecte = d.getIdD();
                    nomAffiche = d.getPrenomD() + " " + d.getNomD();
                }
            }

            // 3. Création de la session et redirection
            if (idConnecte != null) {
                HttpSession session = request.getSession();
                session.setAttribute("idConnecte", idConnecte);
                session.setAttribute("userType", userType);
                session.setAttribute("email", email);
                session.setAttribute("nomUtilisateur", nomAffiche);
                
                // IMPORTANT : On utilise sendRedirect pour changer d'URL proprement
                response.sendRedirect(request.getContextPath() + "/rendezvous");
            } else {
                request.setAttribute("erreur", "Email ou mot de passe incorrect.");
                request.getRequestDispatcher("/WEB-INF/jsp/connexion.jsp").forward(request, response);
            }

        } catch (Exception e) {
            request.setAttribute("erreur", "Erreur technique : " + e.getMessage());
            request.getRequestDispatcher("/WEB-INF/jsp/connexion.jsp").forward(request, response);
        }
    }
}