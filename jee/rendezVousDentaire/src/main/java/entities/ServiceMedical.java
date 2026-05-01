package entities;

import java.io.Serializable;
import java.math.BigDecimal;
import jakarta.persistence.*;

@Entity
@Table(name = "ServiceMedical")
public class ServiceMedical implements Serializable {
    private static final long serialVersionUID = 1L;

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Integer numSM;

    @Column(nullable = false, length = 100)
    private String nomSM;

    @Column(nullable = false, length = 100)
    private String typeSM;

    @Column(columnDefinition = "TEXT")
    private String descriptionSM;

    @Column(precision = 10, scale = 2)
    private BigDecimal tarifSM;

    // Constructeurs
    public ServiceMedical() {}

    // Getters et Setters
    public Integer getNumSM() { return numSM; }
    public void setNumSM(Integer numSM) { this.numSM = numSM; }
    public String getNomSM() { return nomSM; }
    public void setNomSM(String nomSM) { this.nomSM = nomSM; }
    public String getTypeSM() { return typeSM; }
    public void setTypeSM(String typeSM) { this.typeSM = typeSM; }
    public String getDescriptionSM() { return descriptionSM; }
    public void setDescriptionSM(String descriptionSM) { this.descriptionSM = descriptionSM; }
    public BigDecimal getTarifSM() { return tarifSM; }
    public void setTarifSM(BigDecimal tarifSM) { this.tarifSM = tarifSM; }
}