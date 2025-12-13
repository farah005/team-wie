package entities;

import java.io.Serializable;
import java.math.BigDecimal;
import java.util.List;
import jakarta.persistence.*;

@Entity
@Table(name = "ServiceMedical")
@NamedQueries({
    @NamedQuery(name = "ServiceMedical.findAll", query = "SELECT s FROM ServiceMedical s"),
    @NamedQuery(name = "ServiceMedical.findByType", query = "SELECT s FROM ServiceMedical s WHERE s.typeSM LIKE :type")
})
public class ServiceMedical implements Serializable {
    
    private static final long serialVersionUID = 1L;
    
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Column(name = "numSM")
    private Integer numSM;
    
    @Column(name = "nomSM", length = 100, nullable = false)
    private String nomSM;
    
    @Column(name = "typeSM", length = 100, nullable = false)
    private String typeSM;
    
    @Column(name = "descriptionSM", columnDefinition = "TEXT")
    private String descriptionSM;
    
    @Column(name = "tarifSM", precision = 6, scale = 2)
    private BigDecimal tarifSM;
    
    // Relation One-to-Many avec ActeMedical
    @OneToMany(mappedBy = "serviceMedical", cascade = CascadeType.ALL, fetch = FetchType.LAZY)
    private List<ActeMedical> acteMedicalList;
    
    // Constructeurs
    public ServiceMedical() {
    }
    
    public ServiceMedical(String nomSM, String typeSM) {
        this.nomSM = nomSM;
        this.typeSM = typeSM;
    }
    
    public ServiceMedical(String nomSM, String typeSM, BigDecimal tarifSM) {
        this.nomSM = nomSM;
        this.typeSM = typeSM;
        this.tarifSM = tarifSM;
    }
    
    // Getters et Setters
    public Integer getNumSM() {
        return numSM;
    }
    
    public void setNumSM(Integer numSM) {
        this.numSM = numSM;
    }
    
    public String getNomSM() {
        return nomSM;
    }
    
    public void setNomSM(String nomSM) {
        this.nomSM = nomSM;
    }
    
    public String getTypeSM() {
        return typeSM;
    }
    
    public void setTypeSM(String typeSM) {
        this.typeSM = typeSM;
    }
    
    public String getDescriptionSM() {
        return descriptionSM;
    }
    
    public void setDescriptionSM(String descriptionSM) {
        this.descriptionSM = descriptionSM;
    }
    
    public BigDecimal getTarifSM() {
        return tarifSM;
    }
    
    public void setTarifSM(BigDecimal tarifSM) {
        this.tarifSM = tarifSM;
    }
    
    public List<ActeMedical> getActeMedicalList() {
        return acteMedicalList;
    }
    
    public void setActeMedicalList(List<ActeMedical> acteMedicalList) {
        this.acteMedicalList = acteMedicalList;
    }
    
    // Méthodes hashCode, equals et toString
    @Override
    public int hashCode() {
        int hash = 0;
        hash += (numSM != null ? numSM.hashCode() : 0);
        return hash;
    }
    
    @Override
    public boolean equals(Object object) {
        if (!(object instanceof ServiceMedical)) {
            return false;
        }
        ServiceMedical other = (ServiceMedical) object;
        if ((this.numSM == null && other.numSM != null) || 
            (this.numSM != null && !this.numSM.equals(other.numSM))) {
            return false;
        }
        return true;
    }
    
    @Override
    public String toString() {
        return "ServiceMedical[numSM=" + numSM + ", nom=" + nomSM + 
               ", type=" + typeSM + ", tarif=" + tarifSM + "]";
    }
}