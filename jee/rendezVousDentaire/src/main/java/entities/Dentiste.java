package entities;

import java.io.Serializable;
import java.util.List;
import jakarta.persistence.*;

@Entity
@Table(name = "Dentiste")
@NamedQueries({
    @NamedQuery(name = "Dentiste.findAll", query = "SELECT d FROM Dentiste d"),
    @NamedQuery(name = "Dentiste.findByEmail", query = "SELECT d FROM Dentiste d WHERE d.emailD = :email"),
    @NamedQuery(name = "Dentiste.findBySpecialite", query = "SELECT d FROM Dentiste d WHERE d.specialiteD LIKE :specialite")
})
public class Dentiste implements Serializable {
    
    private static final long serialVersionUID = 1L;
    
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Column(name = "idD", length = 8)
    private Integer idD;
    
    @Column(name = "nomD", length = 100, nullable = false)
    private String nomD;
    
    @Column(name = "prenomD", length = 100, nullable = false)
    private String prenomD;
    
    @Column(name = "emailD", length = 100, nullable = false, unique = true)
    private String emailD;
    
    @Column(name = "mdpD", length = 10)
    private String mdpD;
    
    @Column(name = "specialiteD", length = 100)
    private String specialiteD;
    
    @Column(name = "sexeD", length = 1)
    private String sexeD;
    
    @Column(name = "telD", length = 8)
    private Integer telD;
    
    @Column(name = "photoD", length = 100)
    private String photoD;
    
    // Relation One-to-Many avec Rendezvous
    @OneToMany(mappedBy = "dentiste", cascade = CascadeType.ALL, fetch = FetchType.LAZY)
    private List<Rendezvous> rendezvousList;
    
    // Constructeurs
    public Dentiste() {
    }
    
    public Dentiste(String nomD, String prenomD, String emailD) {
        this.nomD = nomD;
        this.prenomD = prenomD;
        this.emailD = emailD;
    }
    
    // Getters et Setters
    public Integer getIdD() {
        return idD;
    }
    
    public void setIdD(Integer idD) {
        this.idD = idD;
    }
    
    public String getNomD() {
        return nomD;
    }
    
    public void setNomD(String nomD) {
        this.nomD = nomD;
    }
    
    public String getPrenomD() {
        return prenomD;
    }
    
    public void setPrenomD(String prenomD) {
        this.prenomD = prenomD;
    }
    
    public String getEmailD() {
        return emailD;
    }
    
    public void setEmailD(String emailD) {
        this.emailD = emailD;
    }
    
    public String getMdpD() {
        return mdpD;
    }
    
    public void setMdpD(String mdpD) {
        this.mdpD = mdpD;
    }
    
    public String getSpecialiteD() {
        return specialiteD;
    }
    
    public void setSpecialiteD(String specialiteD) {
        this.specialiteD = specialiteD;
    }
    
    public String getSexeD() {
        return sexeD;
    }
    
    public void setSexeD(String sexeD) {
        this.sexeD = sexeD;
    }
    
    public Integer getTelD() {
        return telD;
    }
    
    public void setTelD(Integer telD) {
        this.telD = telD;
    }
    
    public String getPhotoD() {
        return photoD;
    }
    
    public void setPhotoD(String photoD) {
        this.photoD = photoD;
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
        hash += (idD != null ? idD.hashCode() : 0);
        return hash;
    }
    
    @Override
    public boolean equals(Object object) {
        if (!(object instanceof Dentiste)) {
            return false;
        }
        Dentiste other = (Dentiste) object;
        if ((this.idD == null && other.idD != null) || 
            (this.idD != null && !this.idD.equals(other.idD))) {
            return false;
        }
        return true;
    }
    
    @Override
    public String toString() {
        return "Dentiste[idD=" + idD + ", nom=" + nomD + ", prenom=" + prenomD + 
               ", specialite=" + specialiteD + "]";
    }
}