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

@WebServlet("/patient")
@MultipartConfig
public class InscriptionPatientServlet extends HttpServlet {
    private static final long serialVersionUID = 1L;

    protected void doGet(HttpServletRequest request, HttpServletResponse response) 
            throws ServletException, IOException {
        String action = request.getParameter("action");
        
        if ("list".equals(action)) {
            // Afficher la liste des patients (pour admin/dentiste)
            // List<Patient> patients = patientService.findAll();
            // request.setAttribute("patients", patients);
            request.getRequestDispatcher("/WEB-INF/jsp/Patients.jsp").forward(request, response);
        } else {
            // Afficher le formulaire d'inscription
            request.getRequestDispatcher("/WEB-INF/jsp/Patient.jsp").forward(request, response);
        }
    }

    protected void doPost(HttpServletRequest request, HttpServletResponse response) 
            throws ServletException, IOException {
        String action = request.getParameter("action");
        
        if ("create".equals(action)) {
            createPatient(request, response);
        } else if ("update".equals(action)) {
            updatePatient(request, response);
        } else if ("delete".equals(action)) {
            deletePatient(request, response);
        }
    }
    
    private void createPatient(HttpServletRequest request, HttpServletResponse response) 
            throws ServletException, IOException {
        try {
            String nom = request.getParameter("nom");
            String prenom = request.getParameter("prenom");
            String email = request.getParameter("email");
            String dateNaissanceStr = request.getParameter("dateNaissance");
            String groupeSanguin = request.getParameter("groupeSanguin");
            String sexe = request.getParameter("sexe");
            String recouvrement = request.getParameter("recouvrement");
            String mdp = request.getParameter("mdp");
            
            // Validation basique
            if (nom == null || prenom == null || email == null || mdp == null) {
                request.setAttribute("erreur", "Veuillez remplir tous les champs obligatoires");
                request.getRequestDispatcher("/WEB-INF/jsp/Patient.jsp").forward(request, response);
                return;
            }
            
            // Conversion de la date
            Date dateNaissance = null;
            if (dateNaissanceStr != null && !dateNaissanceStr.isEmpty()) {
                SimpleDateFormat sdf = new SimpleDateFormat("yyyy-MM-dd");
                dateNaissance = sdf.parse(dateNaissanceStr);
            }
            
            // Créer l'entité Patient
            // Patient patient = new Patient();
            // patient.setNomP(nom);
            // patient.setPrenomP(prenom);
            // patient.setEmailP(email);
            // patient.setDateNP(dateNaissance);
            // patient.setGroupeSanguinP(groupeSanguin);
            // patient.setSexeP(sexe);
            // patient.setRecouvrementP(recouvrement);
            // patient.setMdpP(mdp);
            
            // Appel au service EJB
            // patientService.create(patient);
            
            // Redirection vers la page de validation
            request.getRequestDispatcher("/WEB-INF/jsp/validerInscription.jsp").forward(request, response);
            
        } catch (ParseException e) {
            request.setAttribute("erreur", "Format de date invalide");
            request.getRequestDispatcher("/WEB-INF/jsp/Patient.jsp").forward(request, response);
        }
    }
    
    private void updatePatient(HttpServletRequest request, HttpServletResponse response) 
            throws ServletException, IOException {
        // Logique de mise à jour
        String idStr = request.getParameter("id");
        // Récupérer et mettre à jour le patient
        response.sendRedirect(request.getContextPath() + "/patient?action=list");
    }
    
    private void deletePatient(HttpServletRequest request, HttpServletResponse response) 
            throws ServletException, IOException {
        String idStr = request.getParameter("id");
        if (idStr != null) {
            Integer id = Integer.parseInt(idStr);
            // patientService.delete(id);
        }
        response.sendRedirect(request.getContextPath() + "/patient?action=list");
    }
}