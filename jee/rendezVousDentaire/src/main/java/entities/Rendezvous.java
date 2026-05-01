package entities;

import java.io.Serializable;
import java.util.Date;
import java.util.List;
import jakarta.persistence.*;

@Entity
@Table(name = "Rendezvous")
@NamedQueries({
    @NamedQuery(name = "Rendezvous.findAll", query = "SELECT r FROM Rendezvous r"),
    @NamedQuery(name = "Rendezvous.findByPatient", 
                query = "SELECT r FROM Rendezvous r WHERE r.patient.idP = :idPatient"),
    @NamedQuery(name = "Rendezvous.findByDentiste", 
                query = "SELECT r FROM Rendezvous r WHERE r.dentiste.idD = :idDentiste"),
    @NamedQuery(name = "Rendezvous.findByStatut", 
                query = "SELECT r FROM Rendezvous r WHERE r.statutRv = :statut")
})
public class Rendezvous implements Serializable {
    
    private static final long serialVersionUID = 1L;
    
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Column(name = "idRv")
    private Integer idRv;
    
    @ManyToOne(fetch = FetchType.EAGER)
    @JoinColumn(name = "idP", referencedColumnName = "idP", nullable = false)
    private Patient patient;
    
    @ManyToOne(fetch = FetchType.EAGER)
    @JoinColumn(name = "idD", referencedColumnName = "idD", nullable = false)
    private Dentiste dentiste;
    
    @Temporal(TemporalType.DATE)
    @Column(name = "dateRv", nullable = false)
    private Date dateRv;
    
    @Column(name = "heureRv", nullable = false)
    private String heureRv;
    
    @Column(name = "statutRv", length = 100, nullable = false)
    private String statutRv;
    
    @Column(name = "detailsRv", columnDefinition = "TEXT")
    private String detailsRv;
    
    // Relation One-to-Many avec ActeMedical
    @OneToMany(mappedBy = "rendezvous", cascade = CascadeType.ALL, fetch = FetchType.LAZY)
    private List<ActeMedical> acteMedicalList;
    
    // Constructeurs
    public Rendezvous() {
        this.statutRv = "En attente"; // Statut par défaut
    }
    
    public Rendezvous(Patient patient, Dentiste dentiste, Date dateRv, String heureRv) {
        this.patient = patient;
        this.dentiste = dentiste;
        this.dateRv = dateRv;
        this.heureRv = heureRv;
        this.statutRv = "En attente";
    }
    
    // Getters et Setters
    public Integer getIdRv() {
        return idRv;
    }
    
    public void setIdRv(Integer idRv) {
        this.idRv = idRv;
    }
    
    public Patient getPatient() {
        return patient;
    }
    
    public void setPatient(Patient patient) {
        this.patient = patient;
    }
    
    public Dentiste getDentiste() {
        return dentiste;
    }
    
    public void setDentiste(Dentiste dentiste) {
        this.dentiste = dentiste;
    }
    
    public Date getDateRv() {
        return dateRv;
    }
    
    public void setDateRv(Date dateRv) {
        this.dateRv = dateRv;
    }
    
    public String getHeureRv() {
        return heureRv;
    }
    
    public void setHeureRv(String heureRv) {
        this.heureRv = heureRv;
    }
    
    public String getStatutRv() {
        return statutRv;
    }
    
    public void setStatutRv(String statutRv) {
        this.statutRv = statutRv;
    }
    
    public String getDetailsRv() {
        return detailsRv;
    }
    
    public void setDetailsRv(String detailsRv) {
        this.detailsRv = detailsRv;
    }
    
    public List<ActeMedical> getActeMedicalList() {
        return acteMedicalList;
    }
    
    public void setActeMedicalList(List<ActeMedical> acteMedicalList) {
        this.acteMedicalList = acteMedicalList;
    }
    
    // Méthodes utilitaires
    
    /**
     * Vérifie si le rendez-vous est confirmé
     */
    public boolean isConfirme() {
        return "Confirmé".equalsIgnoreCase(this.statutRv);
    }
    
    /**
     * Vérifie si le rendez-vous est annulé
     */
    public boolean isAnnule() {
        return "Annulé".equalsIgnoreCase(this.statutRv);
    }
    
    /**
     * Vérifie si le rendez-vous est terminé
     */
    public boolean isTermine() {
        return "Terminé".equalsIgnoreCase(this.statutRv);
    }
    
    // Méthodes hashCode, equals et toString
    @Override
    public int hashCode() {
        int hash = 0;
        hash += (idRv != null ? idRv.hashCode() : 0);
        return hash;
    }
    
    @Override
    public boolean equals(Object object) {
        if (!(object instanceof Rendezvous)) {
            return false;
        }
        Rendezvous other = (Rendezvous) object;
        if ((this.idRv == null && other.idRv != null) || 
            (this.idRv != null && !this.idRv.equals(other.idRv))) {
            return false;
        }
        return true;
    }
    
    @Override
    public String toString() {
        return "Rendezvous[idRv=" + idRv + ", date=" + dateRv + 
               ", heure=" + heureRv + ", statut=" + statutRv + "]";
    }

	public void setAideSoignant(AideSoignant a) {
		// TODO Auto-generated method stub
		
	}
}