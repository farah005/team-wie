package servlets;

import jakarta.servlet.ServletException;
import jakarta.servlet.annotation.MultipartConfig;
import jakarta.servlet.annotation.WebServlet;
import jakarta.servlet.http.HttpServlet;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import jakarta.servlet.http.Part;
import java.io.File;
import java.io.IOException;

@WebServlet("/publication")
@MultipartConfig(
    fileSizeThreshold = 1024 * 1024 * 2, // 2MB
    maxFileSize = 1024 * 1024 * 10,      // 10MB
    maxRequestSize = 1024 * 1024 * 50    // 50MB
)
public class PublicationServlet extends HttpServlet {
    private static final long serialVersionUID = 1L;
    private static final String UPLOAD_DIRECTORY = "uploads";

    protected void doGet(HttpServletRequest request, HttpServletResponse response) 
            throws ServletException, IOException {
        String action = request.getParameter("action");
        
        if ("list".equals(action)) {
            // Récupérer toutes les publications
            // List<Publication> publications = publicationService.findAll();
            // request.setAttribute("publications", publications);
            request.getRequestDispatcher("/WEB-INF/jsp/Publications.jsp").forward(request, response);
        } else {
            // Afficher le formulaire de publication
            request.getRequestDispatcher("/WEB-INF/jsp/Publication.jsp").forward(request, response);
        }
    }

    protected void doPost(HttpServletRequest request, HttpServletResponse response) 
            throws ServletException, IOException {
        String action = request.getParameter("action");
        
        if ("upload".equals(action)) {
            uploadPublication(request, response);
        } else if ("delete".equals(action)) {
            deletePublication(request, response);
        }
    }
    
    private void uploadPublication(HttpServletRequest request, HttpServletResponse response) 
            throws ServletException, IOException {
        try {
            // Récupérer le fichier uploadé
            Part filePart = request.getPart("file");
            String titre = request.getParameter("titre");
            String description = request.getParameter("description");
            
            if (filePart == null || titre == null) {
                request.setAttribute("erreur", "Veuillez sélectionner un fichier et fournir un titre");
                request.getRequestDispatcher("/WEB-INF/jsp/Publication.jsp").forward(request, response);
                return;
            }
            
            String fileName = getFileName(filePart);
            
            // Créer le répertoire d'upload s'il n'existe pas
            String uploadPath = getServletContext().getRealPath("") + File.separator + UPLOAD_DIRECTORY;
            File uploadDir = new File(uploadPath);
            if (!uploadDir.exists()) {
                uploadDir.mkdir();
            }
            
            // Sauvegarder le fichier
            String filePath = uploadPath + File.separator + fileName;
            filePart.write(filePath);
            
            // Créer l'entité Publication
            // Publication publication = new Publication();
            // publication.setTitre(titre);
            // publication.setDescription(description);
            // publication.setCheminFichier(UPLOAD_DIRECTORY + "/" + fileName);
            // publication.setDatePublication(new Date());
            
            // Appel au service EJB
            // publicationService.create(publication);
            
            request.setAttribute("message", "Publication uploadée avec succès : " + fileName);
            request.getRequestDispatcher("/WEB-INF/jsp/Publication.jsp").forward(request, response);
            
        } catch (Exception e) {
            request.setAttribute("erreur", "Erreur lors de l'upload : " + e.getMessage());
            request.getRequestDispatcher("/WEB-INF/jsp/Publication.jsp").forward(request, response);
        }
    }
    
    private void deletePublication(HttpServletRequest request, HttpServletResponse response) 
            throws ServletException, IOException {
        String idStr = request.getParameter("id");
        if (idStr != null) {
            Integer id = Integer.parseInt(idStr);
            // Publication publication = publicationService.find(id);
            
            // Supprimer le fichier physique
            // String uploadPath = getServletContext().getRealPath("") + File.separator + publication.getCheminFichier();
            // File file = new File(uploadPath);
            // if (file.exists()) {
            //     file.delete();
            // }
            
            // publicationService.delete(id);
        }
        response.sendRedirect(request.getContextPath() + "/publication?action=list");
    }
    
    private String getFileName(Part part) {
        String contentDisposition = part.getHeader("content-disposition");
        String[] tokens = contentDisposition.split(";");
        for (String token : tokens) {
            if (token.trim().startsWith("filename")) {
                return token.substring(token.indexOf('=') + 2, token.length() - 1);
            }
        }
        return "";
    }
}