package servlets;

import jakarta.servlet.ServletException;
import jakarta.servlet.annotation.WebServlet;
import jakarta.servlet.http.HttpServlet;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import jakarta.servlet.http.HttpSession;
import java.io.IOException;

@WebServlet("/connexion")
public class ConnexionServlet extends HttpServlet {
    private static final long serialVersionUID = 1L;

    protected void doGet(HttpServletRequest request, HttpServletResponse response) 
            throws ServletException, IOException {
        request.getRequestDispatcher("/connexion.jsp").forward(request, response);
    }

    protected void doPost(HttpServletRequest request, HttpServletResponse response) 
            throws ServletException, IOException {
        String email = request.getParameter("email");
        String password = request.getParameter("password");
        String userType = request.getParameter("userType");
        
        HttpSession session = request.getSession();
        
        if (email == null || password == null || userType == null) {
            request.setAttribute("erreur", "Veuillez remplir tous les champs");
            request.getRequestDispatcher("/connexion.jsp").forward(request, response);
            return;
        }
        
        // Simulation de l'authentification (remplacer par l'appel EJB réel)
        if ("patient".equals(userType)) {
            // Patient authentication
            session.setAttribute("userType", "patient");
            session.setAttribute("email", email);
            response.sendRedirect(request.getContextPath() + "/rendezvous");
        } else if ("dentiste".equals(userType)) {
            // Dentiste authentication
            session.setAttribute("userType", "dentiste");
            session.setAttribute("email", email);
            response.sendRedirect(request.getContextPath() + "/rendezvous");
        } else {
            request.setAttribute("erreur", "Type d'utilisateur invalide");
            request.getRequestDispatcher("/connexion.jsp").forward(request, response);
        }
    }
}