package entities;

import java.io.Serializable;
import java.math.BigDecimal;
import jakarta.persistence.*;

@Entity
@Table(name = "ActeMedical")
@NamedQueries({
    @NamedQuery(name = "ActeMedical.findAll", query = "SELECT a FROM ActeMedical a"),
    @NamedQuery(name = "ActeMedical.findByRendezvous", 
                query = "SELECT a FROM ActeMedical a WHERE a.rendezvous.idRv = :idRv")
})
public class ActeMedical implements Serializable {
    
    private static final long serialVersionUID = 1L;
    
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Column(name = "idAM")
    private Integer idAM;
    
    @ManyToOne(fetch = FetchType.EAGER)
    @JoinColumn(name = "idRv", referencedColumnName = "idRv", nullable = false)
    private Rendezvous rendezvous;
    
    @ManyToOne(fetch = FetchType.EAGER)
    @JoinColumn(name = "numSM", referencedColumnName = "numSM", nullable = false)
    private ServiceMedical serviceMedical;
    
    @Column(name = "descriptionAM", columnDefinition = "TEXT")
    private String descriptionAM;
    
    @Column(name = "tarifAM", precision = 6, scale = 2)
    private BigDecimal tarifAM;
    
    // Constructeurs
    public ActeMedical() {
    }
    
    public ActeMedical(Rendezvous rendezvous, ServiceMedical serviceMedical) {
        this.rendezvous = rendezvous;
        this.serviceMedical = serviceMedical;
        // Copier le tarif du service médical par défaut
        if (serviceMedical != null && serviceMedical.getTarifSM() != null) {
            this.tarifAM = serviceMedical.getTarifSM();
        }
    }
    
    public ActeMedical(Rendezvous rendezvous, ServiceMedical serviceMedical, 
                      String descriptionAM, BigDecimal tarifAM) {
        this.rendezvous = rendezvous;
        this.serviceMedical = serviceMedical;
        this.descriptionAM = descriptionAM;
        this.tarifAM = tarifAM;
    }
    
    // Getters et Setters
    public Integer getIdAM() {
        return idAM;
    }
    
    public void setIdAM(Integer idAM) {
        this.idAM = idAM;
    }
    
    public Rendezvous getRendezvous() {
        return rendezvous;
    }
    
    public void setRendezvous(Rendezvous rendezvous) {
        this.rendezvous = rendezvous;
    }
    
    public ServiceMedical getServiceMedical() {
        return serviceMedical;
    }
    
    public void setServiceMedical(ServiceMedical serviceMedical) {
        this.serviceMedical = serviceMedical;
        // Mettre à jour le tarif si le service change
        if (serviceMedical != null && serviceMedical.getTarifSM() != null && this.tarifAM == null) {
            this.tarifAM = serviceMedical.getTarifSM();
        }
    }
    
    public String getDescriptionAM() {
        return descriptionAM;
    }
    
    public void setDescriptionAM(String descriptionAM) {
        this.descriptionAM = descriptionAM;
    }
    
    public BigDecimal getTarifAM() {
        return tarifAM;
    }
    
    public void setTarifAM(BigDecimal tarifAM) {
        this.tarifAM = tarifAM;
    }
    
    // Méthodes utilitaires
    
    /**
     * Retourne le nom du service médical associé
     */
    public String getNomService() {
        return serviceMedical != null ? serviceMedical.getNomSM() : null;
    }
    
    /**
     * Retourne le type du service médical associé
     */
    public String getTypeService() {
        return serviceMedical != null ? serviceMedical.getTypeSM() : null;
    }
    
    /**
     * Retourne les informations du patient via le rendez-vous
     */
    public Patient getPatient() {
        return rendezvous != null ? rendezvous.getPatient() : null;
    }
    
    /**
     * Retourne les informations du dentiste via le rendez-vous
     */
    public Dentiste getDentiste() {
        return rendezvous != null ? rendezvous.getDentiste() : null;
    }
    
    // Méthodes hashCode, equals et toString
    @Override
    public int hashCode() {
        int hash = 0;
        hash += (idAM != null ? idAM.hashCode() : 0);
        return hash;
    }
    
    @Override
    public boolean equals(Object object) {
        if (!(object instanceof ActeMedical)) {
            return false;
        }
        ActeMedical other = (ActeMedical) object;
        if ((this.idAM == null && other.idAM != null) || 
            (this.idAM != null && !this.idAM.equals(other.idAM))) {
            return false;
        }
        return true;
    }
    
    @Override
    public String toString() {
        return "ActeMedical[idAM=" + idAM + ", service=" + 
               (serviceMedical != null ? serviceMedical.getNomSM() : "null") + 
               ", tarif=" + tarifAM + "]";
    }
}