package entities;

import java.io.Serializable;
import java.util.Date;
import java.util.List;
import jakarta.persistence.*;

@Entity
@Table(name = "Patient")
@NamedQueries({
    @NamedQuery(name = "Patient.findAll", query = "SELECT p FROM Patient p"),
    @NamedQuery(name = "Patient.findByEmail", query = "SELECT p FROM Patient p WHERE p.emailP = :email")
})
public class Patient implements Serializable {
    
    private static final long serialVersionUID = 1L;
    
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Column(name = "idP", length = 8)
    private Integer idP;
    
    @Column(name = "nomP", length = 100, nullable = false)
    private String nomP;
    
    @Column(name = "prenomP", length = 100, nullable = false)
    private String prenomP;
    
    @Column(name = "emailP", length = 100, nullable = false, unique = true)
    private String emailP;
    
    @Temporal(TemporalType.DATE)
    @Column(name = "dateNP")
    private Date dateNP;
    
    @Column(name = "photoP", length = 100)
    private String photoP;
    
    @Column(name = "groupeSanguinP", length = 2)
    private String groupeSanguinP;
    
    @Column(name = "sexeP", length = 1)
    private String sexeP;
    
    @Column(name = "mdpP", length = 10)
    private String mdpP;
    
    @Column(name = "recouvrementP", length = 100)
    private String recouvrementP;
    
    // Relation One-to-Many avec Rendezvous
    @OneToMany(mappedBy = "patient", cascade = CascadeType.ALL, fetch = FetchType.LAZY)
    private List<Rendezvous> rendezvousList;
    
    // Constructeurs
    public Patient() {
    }
    
    public Patient(String nomP, String prenomP, String emailP) {
        this.nomP = nomP;
        this.prenomP = prenomP;
        this.emailP = emailP;
    }
    
    // Getters et Setters
    public Integer getIdP() {
        return idP;
    }
    
    public void setIdP(Integer idP) {
        this.idP = idP;
    }
    
    public String getNomP() {
        return nomP;
    }
    
    public void setNomP(String nomP) {
        this.nomP = nomP;
    }
    
    public String getPrenomP() {
        return prenomP;
    }
    
    public void setPrenomP(String prenomP) {
        this.prenomP = prenomP;
    }
    
    public String getEmailP() {
        return emailP;
    }
    
    public void setEmailP(String emailP) {
        this.emailP = emailP;
    }
    
    public Date getDateNP() {
        return dateNP;
    }
    
    public void setDateNP(Date dateNP) {
        this.dateNP = dateNP;
    }
    
    public String getPhotoP() {
        return photoP;
    }
    
    public void setPhotoP(String photoP) {
        this.photoP = photoP;
    }
    
    public String getGroupeSanguinP() {
        return groupeSanguinP;
    }
    
    public void setGroupeSanguinP(String groupeSanguinP) {
        this.groupeSanguinP = groupeSanguinP;
    }
    
    public String getSexeP() {
        return sexeP;
    }
    
    public void setSexeP(String sexeP) {
        this.sexeP = sexeP;
    }
    
    public String getMdpP() {
        return mdpP;
    }
    
    public void setMdpP(String mdpP) {
        this.mdpP = mdpP;
    }
    
    public String getRecouvrementP() {
        return recouvrementP;
    }
    
    public void setRecouvrementP(String recouvrementP) {
        this.recouvrementP = recouvrementP;
    }
    
    public List<Rendezvous> getRendezvousList() {
        return rendezvousList;
    }
    
    public void setRendezvousList(List<Rendezvous> rendezvousList) {
        this.rendezvousList = rendezvousList;
    }
    
    // Méthodes hashCode, equals et toString
    @Override
    public int hashCode() {
        int hash = 0;
        hash += (idP != null ? idP.hashCode() : 0);
        return hash;
    }
    
    @Override
    public boolean equals(Object object) {
        if (!(object instanceof Patient)) {
            return false;
        }
        Patient other = (Patient) object;
        if ((this.idP == null && other.idP != null) || 
            (this.idP != null && !this.idP.equals(other.idP))) {
            return false;
        }
        return true;
    }
    
    @Override
    public String toString() {
        return "Patient[idP=" + idP + ", nom=" + nomP + ", prenom=" + prenomP + "]";
    }
}