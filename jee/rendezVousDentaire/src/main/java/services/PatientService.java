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

    /**
     * Enregistre un nouveau patient
     */
    @Override
    public void create(Patient patient) {
        try {
            em.persist(patient);
        } catch (Exception e) {
            throw new RuntimeException("Erreur lors de la création du patient : " + e.getMessage());
        }
    }

    /**
     * Trouve un patient par son ID (Clé primaire)
     */
    @Override
    public Patient find(Integer id) {
        if (id == null) return null;
        return em.find(Patient.class, id);
    }

    /**
     * Authentification : recherche par email et mot de passe
     */
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
            return null; // Identifiants incorrects
        } catch (Exception e) {
            throw new RuntimeException("Erreur lors de l'authentification : " + e.getMessage());
        }
    }

    /**
     * Recherche un patient par son adresse email uniquement
     */
    @Override
    public Patient findByEmail(String email) {
        try {
            // Utilisation de la NamedQuery définie dans l'entité Patient
            return em.createNamedQuery("Patient.findByEmail", Patient.class)
                     .setParameter("email", email)
                     .getSingleResult();
        } catch (NoResultException e) {
            return null;
        } catch (Exception e) {
            throw new RuntimeException("Erreur recherche email : " + e.getMessage());
        }
    }

    /**
     * Récupère la liste de tous les patients enregistrés
     */
    @Override
    public List<Patient> findAll() {
        try {
            return em.createNamedQuery("Patient.findAll", Patient.class).getResultList();
        } catch (Exception e) {
            throw new RuntimeException("Erreur lors de la récupération de la liste : " + e.getMessage());
        }
    }

    /**
     * Met à jour les informations d'un patient
     */
    @Override
    public void update(Patient patient) {
        try {
            if (patient.getIdP() != null && em.find(Patient.class, patient.getIdP()) != null) {
                em.merge(patient);
            } else {
                throw new IllegalArgumentException("Patient inexistant pour mise à jour.");
            }
        } catch (Exception e) {
            throw new RuntimeException("Erreur mise à jour : " + e.getMessage());
        }
    }

    /**
     * Supprime un patient de la base de données
     */
    @Override
    public void delete(Integer id) {
        try {
            Patient patient = find(id);
            if (patient != null) {
                em.remove(patient);
            }
        } catch (Exception e) {
            throw new RuntimeException("Erreur lors de la suppression : " + e.getMessage());
        }
    }

    /**
     * Méthode utilitaire : recherche par groupe sanguin
     */
    public List<Patient> findByGroupeSanguin(String groupeSanguin) {
        TypedQuery<Patient> query = em.createQuery(
            "SELECT p FROM Patient p WHERE p.groupeSanguinP = :groupe", 
            Patient.class
        );
        query.setParameter("groupe", groupeSanguin);
        return query.getResultList();
    }
}