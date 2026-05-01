package servlets;

import jakarta.ejb.EJB;
import jakarta.servlet.ServletException;
import jakarta.servlet.annotation.MultipartConfig;
import jakarta.servlet.annotation.WebServlet;
import jakarta.servlet.http.HttpServlet;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import java.io.IOException;
import java.text.SimpleDateFormat;

import entities.Patient;
import interfaces.PatientLocal;

@WebServlet("/patient")
@MultipartConfig 
public class InscriptionPatientServlet extends HttpServlet {
    private static final long serialVersionUID = 1L;

    @EJB
    private PatientLocal patientService; 

    protected void doGet(HttpServletRequest request, HttpServletResponse response) 
            throws ServletException, IOException {
        
        String action = request.getParameter("action");
        
        if ("list".equals(action)) {
            // Pour l'aide-soignant : voir tous les patients
            request.setAttribute("patients", patientService.findAll());
            request.getRequestDispatcher("/WEB-INF/jsp/Patients.jsp").forward(request, response);
        } else {
            // Par défaut : afficher le formulaire d'inscription
            request.getRequestDispatcher("/WEB-INF/jsp/Patient.jsp").forward(request, response);
        }
    }

    protected void doPost(HttpServletRequest request, HttpServletResponse response) 
            throws ServletException, IOException {
        
        String action = request.getParameter("action");
        
        if ("create".equals(action)) {
            createPatient(request, response);
        } else if ("delete".equals(action)) {
            deletePatient(request, response);
        }
    }
    
    private void createPatient(HttpServletRequest request, HttpServletResponse response) 
            throws ServletException, IOException {
        try {
            // 1. Récupération des paramètres du formulaire
            String nom = request.getParameter("nom");
            String prenom = request.getParameter("prenom");
            String email = request.getParameter("email");
            String mdp = request.getParameter("mdp");
            String dateNStr = request.getParameter("dateNaissance");
            String sexe = request.getParameter("sexe");
            String groupe = request.getParameter("groupeSanguin");
            String recouvrement = request.getParameter("recouvrement");

            // 2. Validation minimale
            if (nom == null || email == null || mdp == null) {
                request.setAttribute("erreur", "Les champs avec * sont obligatoires.");
                request.getRequestDispatcher("/WEB-INF/jsp/Patient.jsp").forward(request, response);
                return;
            }

            // 3. Création de l'objet Patient
            Patient patient = new Patient();
            patient.setNomP(nom);
            patient.setPrenomP(prenom);
            patient.setEmailP(email);
            patient.setMdpP(mdp);
            patient.setSexeP(sexe);
            patient.setGroupeSanguinP(groupe);
            patient.setRecouvrementP(recouvrement);

            // Conversion de la date
            if (dateNStr != null && !dateNStr.isEmpty()) {
                SimpleDateFormat sdf = new SimpleDateFormat("yyyy-MM-dd");
                patient.setDateNP(sdf.parse(dateNStr));
            }

            // 4. Appel de l'EJB pour enregistrer en base de données
            patientService.create(patient);

            // 5. Redirection vers la page de connexion avec un message de succès
            // Note : On utilise requestScope pour passer le message si on fait un forward
            request.setAttribute("message", "Votre compte a été créé avec succès ! Vous pouvez maintenant vous connecter.");
            request.getRequestDispatcher("/WEB-INF/jsp/connexion.jsp").forward(request, response);

        } catch (Exception e) {
            request.setAttribute("erreur", "Erreur lors de l'inscription : " + e.getMessage());
            request.getRequestDispatcher("/WEB-INF/jsp/Patient.jsp").forward(request, response);
        }
    }

    private void deletePatient(HttpServletRequest request, HttpServletResponse response) 
            throws ServletException, IOException {
        String idStr = request.getParameter("id");
        if (idStr != null) {
            try {
                patientService.delete(Integer.parseInt(idStr));
            } catch (Exception e) {
                // Gestion d'erreur silencieuse ou log
            }
        }
        response.sendRedirect(request.getContextPath() + "/patient?action=list");
    }
}