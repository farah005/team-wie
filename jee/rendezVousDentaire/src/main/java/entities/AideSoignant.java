package entities;

import java.io.Serializable;
import java.util.Date;
import jakarta.persistence.*;

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
    @Column(name = "idAS")
    private Integer idAS;

    @Column(name = "nomAS", length = 100, nullable = false)
    private String nomAS;
    
    @Column(name = "prenomAS", length = 100, nullable = false)
    private String prenomAS;
    
    @Column(name = "emailAS", length = 100, nullable = false, unique = true)
    private String emailAS;
    
    @Column(name = "mdpAS", length = 255) // Augmenté pour la sécurité (hachage)
    private String mdpAS;
    
    @Column(name = "telAS", length = 20) // Changé en String pour conserver le "0"
    private String telAS;
    
    @Column(name = "sexeAS", length = 1)
    private String sexeAS;
    
    @Column(name = "photoAS", length = 255)
    private String photoAS;
    
    @Temporal(TemporalType.DATE)
    @Column(name = "dateEmbaucheAS")
    private Date dateEmbaucheAS;
    
    @Column(name = "diplomeAS", length = 200)
    private String diplomeAS;
    
    @Column(name = "experienceAS")
    private Integer experienceAS; 
    
    @Column(name = "specialisationAS", length = 100)
    private String specialisationAS; 
    
    @Column(name = "statutAS", length = 50)
    private String statutAS; 

    @ManyToOne(fetch = FetchType.EAGER)
    @JoinColumn(name = "idD", referencedColumnName = "idD")
    private Dentiste dentiste;
    
    // --- Constructeurs ---
    public AideSoignant() {
        this.statutAS = "Actif";
        this.dateEmbaucheAS = new Date();
    }
    
    public AideSoignant(String nomAS, String prenomAS, String emailAS, String mdpAS) {
        this();
        this.nomAS = nomAS;
        this.prenomAS = prenomAS;
        this.emailAS = emailAS;
        this.mdpAS = mdpAS;
    }

    // --- Getters et Setters ---
    public Integer getIdAS() { return idAS; }
    public void setIdAS(Integer idAS) { this.idAS = idAS; }

    public String getNomAS() { return nomAS; }
    public void setNomAS(String nomAS) { this.nomAS = nomAS; }

    public String getPrenomAS() { return prenomAS; }
    public void setPrenomAS(String prenomAS) { this.prenomAS = prenomAS; }

    public String getEmailAS() { return emailAS; }
    public void setEmailAS(String emailAS) { this.emailAS = emailAS; }

    public String getMdpAS() { return mdpAS; }
    public void setMdpAS(String mdpAS) { this.mdpAS = mdpAS; }

    public String getTelAS() { return telAS; }
    public void setTelAS(String telAS) { this.telAS = telAS; }

    public String getSexeAS() { return sexeAS; }
    public void setSexeAS(String sexeAS) { this.sexeAS = sexeAS; }

    public String getPhotoAS() { return photoAS; }
    public void setPhotoAS(String photoAS) { this.photoAS = photoAS; }

    public Date getDateEmbaucheAS() { return dateEmbaucheAS; }
    public void setDateEmbaucheAS(Date dateEmbaucheAS) { this.dateEmbaucheAS = dateEmbaucheAS; }

    public String getDiplomeAS() { return diplomeAS; }
    public void setDiplomeAS(String diplomeAS) { this.diplomeAS = diplomeAS; }

    public Integer getExperienceAS() { return experienceAS; }
    public void setExperienceAS(Integer experienceAS) { this.experienceAS = experienceAS; }

    public String getSpecialisationAS() { return specialisationAS; }
    public void setSpecialisationAS(String specialisationAS) { this.specialisationAS = specialisationAS; }

    public String getStatutAS() { return statutAS; }
    public void setStatutAS(String statutAS) { this.statutAS = statutAS; }

    public Dentiste getDentiste() { return dentiste; }
    public void setDentiste(Dentiste dentiste) { this.dentiste = dentiste; }

    // --- Méthodes Métier ---
    public String getNomComplet() { return nomAS + " " + prenomAS; }
    public boolean isActif() { return "Actif".equalsIgnoreCase(this.statutAS); }
    public boolean hasDentiste() { return this.dentiste != null; }

    @Override
    public String toString() {
        return "AideSoignant[idAS=" + idAS + ", nom=" + nomAS + ", statut=" + statutAS + "]";
    }
}