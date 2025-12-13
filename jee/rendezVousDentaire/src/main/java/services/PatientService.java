package services;

import java.util.List;
import entities.Patient;
import interfaces.PatientLocal;
import jakarta.ejb.Stateless;
import jakarta.persistence.EntityManager;
import jakarta.persistence.NoResultException;
import jakarta.persistence.PersistenceContext;
import jakarta.persistence.TypedQuery;

@Stateless
public class PatientService implements PatientLocal {
    
    @PersistenceContext(unitName = "RendezVousPU")
    private EntityManager em;

    @Override
    public void create(Patient patient) {
        try {
            em.persist(patient);
        } catch (Exception e) {
            throw new RuntimeException("Erreur lors de la création du patient: " + e.getMessage(), e);
        }
    }

    @Override
    public Patient find(Integer id) {
        try {
            return em.find(Patient.class, id);
        } catch (Exception e) {
            throw new RuntimeException("Erreur lors de la recherche du patient: " + e.getMessage(), e);
        }
    }

    @Override
    public Patient authenticate(String email, String password) {
        try {
            TypedQuery<Patient> query = em.createQuery(
                "SELECT p FROM Patient p WHERE p.emailP = :email AND p.mdpP = :password", 
                Patient.class
            );
            query.setParameter("email", email);
            query.setParameter("password", password);
            
            return query.getSingleResult();
        } catch (NoResultException e) {
            // Aucun patient trouvé avec ces identifiants
            return null;
        } catch (Exception e) {
            throw new RuntimeException("Erreur lors de l'authentification: " + e.getMessage(), e);
        }
    }

    @Override
    public List<Patient> findAll() {
        try {
            TypedQuery<Patient> query = em.createQuery(
                "SELECT p FROM Patient p ORDER BY p.nomP, p.prenomP", 
                Patient.class
            );
            return query.getResultList();
        } catch (Exception e) {
            throw new RuntimeException("Erreur lors de la récupération des patients: " + e.getMessage(), e);
        }
    }

    @Override
    public void update(Patient patient) {
        try {
            if (patient.getIdP() == null) {
                throw new IllegalArgumentException("L'ID du patient ne peut pas être null");
            }
            
            Patient existingPatient = em.find(Patient.class, patient.getIdP());
            if (existingPatient == null) {
                throw new IllegalArgumentException("Patient non trouvé avec l'ID: " + patient.getIdP());
            }
            
            em.merge(patient);
        } catch (Exception e) {
            throw new RuntimeException("Erreur lors de la mise à jour du patient: " + e.getMessage(), e);
        }
    }

    @Override
    public void delete(Integer id) {
        try {
            Patient patient = em.find(Patient.class, id);
            if (patient != null) {
                em.remove(patient);
            } else {
                throw new IllegalArgumentException("Patient non trouvé avec l'ID: " + id);
            }
        } catch (Exception e) {
            throw new RuntimeException("Erreur lors de la suppression du patient: " + e.getMessage(), e);
        }
    }
    
    // Méthodes utilitaires supplémentaires
    
    /**
     * Recherche un patient par email
     */
    public Patient findByEmail(String email) {
        try {
            TypedQuery<Patient> query = em.createQuery(
                "SELECT p FROM Patient p WHERE p.emailP = :email", 
                Patient.class
            );
            query.setParameter("email", email);
            return query.getSingleResult();
        } catch (NoResultException e) {
            return null;
        }
    }
    
    /**
     * Vérifie si un email existe déjà
     */
    public boolean emailExists(String email) {
        try {
            TypedQuery<Long> query = em.createQuery(
                "SELECT COUNT(p) FROM Patient p WHERE p.emailP = :email", 
                Long.class
            );
            query.setParameter("email", email);
            return query.getSingleResult() > 0;
        } catch (Exception e) {
            return false;
        }
    }
    
    /**
     * Recherche des patients par groupe sanguin
     */
    public List<Patient> findByGroupeSanguin(String groupeSanguin) {
        try {
            TypedQuery<Patient> query = em.createQuery(
                "SELECT p FROM Patient p WHERE p.groupeSanguinP = :groupe", 
                Patient.class
            );
            query.setParameter("groupe", groupeSanguin);
            return query.getResultList();
        } catch (Exception e) {
            throw new RuntimeException("Erreur lors de la recherche par groupe sanguin: " + e.getMessage(), e);
        }
    }
}