package entities;

import java.io.Serializable;
import java.util.Date;
import jakarta.persistence.*;

/**
 * Entité JPA pour les Aides-Soignants
 * Représente le personnel d'assistance aux dentistes
 */
@Entity
@Table(name = "AideSoignant")
@NamedQueries({
    @NamedQuery(name = "AideSoignant.findAll", 
                query = "SELECT a FROM AideSoignant a ORDER BY a.nomAS, a.prenomAS"),
    @NamedQuery(name = "AideSoignant.findByEmail", 
                query = "SELECT a FROM AideSoignant a WHERE a.emailAS = :email"),
    @NamedQuery(name = "AideSoignant.findByDentiste", 
                query = "SELECT a FROM AideSoignant a WHERE a.dentiste.idD = :idDentiste")
})
public class AideSoignant implements Serializable {
    
    private static final long serialVersionUID = 1L;
    
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Column(name = "idAS", length = 8)
    private Integer idAS;
    
    @Column(name = "nomAS", length = 100, nullable = false)
    private String nomAS;
    
    @Column(name = "prenomAS", length = 100, nullable = false)
    private String prenomAS;
    
    @Column(name = "emailAS", length = 100, nullable = false, unique = true)
    private String emailAS;
    
    @Column(name = "mdpAS", length = 10)
    private String mdpAS;
    
    @Column(name = "telAS", length = 8)
    private Integer telAS;
    
    @Column(name = "sexeAS", length = 1)
    private String sexeAS;
    
    @Column(name = "photoAS", length = 100)
    private String photoAS;
    
    @Temporal(TemporalType.DATE)
    @Column(name = "dateEmbaucheAS")
    private Date dateEmbaucheAS;
    
    @Column(name = "diplomeAS", length = 200)
    private String diplomeAS;
    
    @Column(name = "experienceAS")
    private Integer experienceAS; // Nombre d'années d'expérience
    
    @Column(name = "specialisationAS", length = 100)
    private String specialisationAS; // Ex: Orthodontie, Implantologie, etc.
    
    @Column(name = "statutAS", length = 50)
    private String statutAS; // Actif, En congé, Inactif
    
    // Relation Many-to-One avec Dentiste
    // Un aide-soignant assiste un dentiste principal
    @ManyToOne(fetch = FetchType.EAGER)
    @JoinColumn(name = "idD", referencedColumnName = "idD")
    private Dentiste dentiste;
    
    // Constructeurs
    public AideSoignant() {
        this.statutAS = "Actif"; // Statut par défaut
        this.dateEmbaucheAS = new Date(); // Date d'embauche = aujourd'hui
    }
    
    public AideSoignant(String nomAS, String prenomAS, String emailAS) {
        this();
        this.nomAS = nomAS;
        this.prenomAS = prenomAS;
        this.emailAS = emailAS;
    }
    
    public AideSoignant(String nomAS, String prenomAS, String emailAS, String mdpAS) {
        this(nomAS, prenomAS, emailAS);
        this.mdpAS = mdpAS;
    }
    
    // Getters et Setters
    public Integer getIdAS() {
        return idAS;
    }
    
    public void setIdAS(Integer idAS) {
        this.idAS = idAS;
    }
    
    public String getNomAS() {
        return nomAS;
    }
    
    public void setNomAS(String nomAS) {
        this.nomAS = nomAS;
    }
    
    public String getPrenomAS() {
        return prenomAS;
    }
    
    public void setPrenomAS(String prenomAS) {
        this.prenomAS = prenomAS;
    }
    
    public String getEmailAS() {
        return emailAS;
    }
    
    public void setEmailAS(String emailAS) {
        this.emailAS = emailAS;
    }
    
    public String getMdpAS() {
        return mdpAS;
    }
    
    public void setMdpAS(String mdpAS) {
        this.mdpAS = mdpAS;
    }
    
    public Integer getTelAS() {
        return telAS;
    }
    
    public void setTelAS(Integer telAS) {
        this.telAS = telAS;
    }
    
    public String getSexeAS() {
        return sexeAS;
    }
    
    public void setSexeAS(String sexeAS) {
        this.sexeAS = sexeAS;
    }
    
    public String getPhotoAS() {
        return photoAS;
    }
    
    public void setPhotoAS(String photoAS) {
        this.photoAS = photoAS;
    }
    
    public Date getDateEmbaucheAS() {
        return dateEmbaucheAS;
    }
    
    public void setDateEmbaucheAS(Date dateEmbaucheAS) {
        this.dateEmbaucheAS = dateEmbaucheAS;
    }
    
    public String getDiplomeAS() {
        return diplomeAS;
    }
    
    public void setDiplomeAS(String diplomeAS) {
        this.diplomeAS = diplomeAS;
    }
    
    public Integer getExperienceAS() {
        return experienceAS;
    }
    
    public void setExperienceAS(Integer experienceAS) {
        this.experienceAS = experienceAS;
    }
    
    public String getSpecialisationAS() {
        return specialisationAS;
    }
    
    public void setSpecialisationAS(String specialisationAS) {
        this.specialisationAS = specialisationAS;
    }
    
    public String getStatutAS() {
        return statutAS;
    }
    
    public void setStatutAS(String statutAS) {
        this.statutAS = statutAS;
    }
    
    public Dentiste getDentiste() {
        return dentiste;
    }
    
    public void setDentiste(Dentiste dentiste) {
        this.dentiste = dentiste;
    }
    
    // Méthodes utilitaires
    
    /**
     * Retourne le nom complet de l'aide-soignant
     */
    public String getNomComplet() {
        return nomAS + " " + prenomAS;
    }
    
    /**
     * Vérifie si l'aide-soignant est actuellement actif
     */
    public boolean isActif() {
        return "Actif".equalsIgnoreCase(this.statutAS);
    }
    
    /**
     * Vérifie si l'aide-soignant a un dentiste assigné
     */
    public boolean hasDentiste() {
        return this.dentiste != null;
    }
    
    /**
     * Retourne le nom du dentiste assigné
     */
    public String getNomDentiste() {
        if (dentiste != null) {
            return "Dr. " + dentiste.getNomD() + " " + dentiste.getPrenomD();
        }
        return "Non assigné";
    }
    
    /**
     * Calcule l'ancienneté en années
     */
    public int getAnciennete() {
        if (dateEmbaucheAS == null) {
            return 0;
        }
        Date now = new Date();
        long diff = now.getTime() - dateEmbaucheAS.getTime();
        return (int) (diff / (1000L * 60 * 60 * 24 * 365));
    }
    
    // Méthodes hashCode, equals et toString
    @Override
    public int hashCode() {
        int hash = 0;
        hash += (idAS != null ? idAS.hashCode() : 0);
        return hash;
    }
    
    @Override
    public boolean equals(Object object) {
        if (!(object instanceof AideSoignant)) {
            return false;
        }
        AideSoignant other = (AideSoignant) object;
        if ((this.idAS == null && other.idAS != null) || 
            (this.idAS != null && !this.idAS.equals(other.idAS))) {
            return false;
        }
        return true;
    }
    
    @Override
    public String toString() {
        return "AideSoignant[idAS=" + idAS + 
               ", nom=" + nomAS + 
               ", prenom=" + prenomAS + 
               ", statut=" + statutAS + 
               ", dentiste=" + (dentiste != null ? dentiste.getNomD() : "null") + "]";
    }
}