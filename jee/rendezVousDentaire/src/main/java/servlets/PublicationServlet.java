package servlets;

import jakarta.servlet.ServletException;
import jakarta.servlet.annotation.MultipartConfig;
import jakarta.servlet.annotation.WebServlet;
import jakarta.servlet.http.HttpServlet;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import jakarta.servlet.http.HttpSession;
import jakarta.servlet.http.Part;
import java.io.File;
import java.io.IOException; 
import java.io.InputStream;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.nio.file.StandardCopyOption;
import java.util.logging.Level;
import java.util.logging.Logger;
@WebServlet("/publication")
@MultipartConfig(
    fileSizeThreshold = 1024 * 1024 * 2, // 2MB
    maxFileSize = 1024 * 1024 * 10,      // 10MB
    maxRequestSize = 1024 * 1024 * 50    // 50MB
)
public class PublicationServlet extends HttpServlet {
    private static final long serialVersionUID = 1L;
    private static final String UPLOAD_DIRECTORY = "uploads";
    private static final Logger LOGGER = Logger.getLogger(PublicationServlet.class.getName());

    protected void doGet(HttpServletRequest request, HttpServletResponse response) 
            throws ServletException, IOException {
        String action = request.getParameter("action");
        
        if ("list".equals(action)) {
            // Récupérer toutes les publications
            // List<Publication> publications = publicationService.findAll();
            // request.setAttribute("publications", publications);
            //request.getRequestDispatcher("/WEB-INF/jsp/Publication.jsp").forward(request, response);
        } else {
            // Si demande de view (après POST redirect), récupérer depuis la session
            if ("view".equals(action)) {
                HttpSession session = request.getSession(false);
                if (session != null) {
                    Object titre = session.getAttribute("dernierTitre");
                    Object desc = session.getAttribute("derniereDesc");
                    Object type = session.getAttribute("dernierType");
                    Object fichier = session.getAttribute("dernierFichier");
                    if (titre != null) request.setAttribute("dernierTitre", titre);
                    if (desc != null) request.setAttribute("derniereDesc", desc);
                    if (type != null) request.setAttribute("dernierType", type);
                    if (fichier != null) request.setAttribute("dernierFichier", fichier);
                    // Nettoyer les attributs de session pour ne pas les réafficher
                    session.removeAttribute("dernierTitre");
                    session.removeAttribute("derniereDesc");
                    session.removeAttribute("dernierType");
                    session.removeAttribute("dernierFichier");
                }
                request.getRequestDispatcher("/WEB-INF/jsp/PublicationDetail.jsp").forward(request, response);
                return;
            }

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
        // 1. Récupération des données (noms synchronisés avec la JSP)
        Part filePart = request.getPart("file"); // Correspond à name="file"
        String titre = request.getParameter("titre");
        String description = request.getParameter("description");
        String typeP = request.getParameter("typeP");
        
        if (filePart == null || filePart.getSize() == 0 || titre == null || titre.isEmpty()) {
            request.setAttribute("erreur", "Veuillez remplir le titre et choisir un fichier.");
            request.getRequestDispatcher("/WEB-INF/jsp/Publication.jsp").forward(request, response);
            return;
        }

        // 2. Traitement du fichier
        String fileName = sanitizeFileName(getFileName(filePart));
        String uploadPath = getServletContext().getRealPath("") + File.separator + UPLOAD_DIRECTORY;
        Path uploadDir = Paths.get(uploadPath);
        if (Files.notExists(uploadDir)) {
            Files.createDirectories(uploadDir);
        }

        Path filePath = uploadDir.resolve(fileName);
        try (InputStream input = filePart.getInputStream()) {
            Files.copy(input, filePath, StandardCopyOption.REPLACE_EXISTING);
        }

        // 3. Stocker les infos en session puis rediriger (Post-Redirect-Get)
        HttpSession session = request.getSession();
        session.setAttribute("dernierTitre", titre);
        session.setAttribute("derniereDesc", description);
        session.setAttribute("dernierType", typeP);
        session.setAttribute("dernierFichier", fileName);

        // 4. Redirect vers la page de détail pour afficher la publication publiée
        response.sendRedirect(request.getContextPath() + "/publication?action=view");

    } catch (Exception e) {
        LOGGER.log(Level.SEVERE, "Erreur upload", e);
        request.setAttribute("erreur", "Erreur : " + e.getMessage());
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
        if (contentDisposition == null) {
            return "";
        }
        for (String token : contentDisposition.split(";")) {
            token = token.trim();
            if (token.startsWith("filename=")) {
                String name = token.substring(token.indexOf('=') + 1).trim();
                if (name.startsWith("\"") && name.endsWith("\"")) {
                    name = name.substring(1, name.length() - 1);
                }
                return Paths.get(name).getFileName().toString();
            }
        }
        return "";
    }

    private String sanitizeFileName(String filename) {
        if (filename == null || filename.isBlank()) return "unnamed";
        return filename.replaceAll("[^a-zA-Z0-9._-]", "_");
    }
}