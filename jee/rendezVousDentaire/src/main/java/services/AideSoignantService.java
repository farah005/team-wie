
// services/AideSoignantService.java (EJB)
package services;

import entities.AideSoignant;
import entities.Rendezvous;
import interfaces.AideSoignantLocal;
import jakarta.ejb.Stateless;
import jakarta.persistence.*;

import java.util.List;

@Stateless
public class AideSoignantService implements AideSoignantLocal {

    @PersistenceContext(unitName = "RendezVousPU")
    private EntityManager em;

    @Override
    public void create(AideSoignant as) {
        try {
            em.persist(as);
        } catch (Exception e) {
            throw new RuntimeException("Erreur lors de la création de l'aide-soignant: " + e.getMessage(), e);
        }
    }

    @Override
    public AideSoignant find(Integer id) {
        try {
            return em.find(AideSoignant.class, id);
        } catch (Exception e) {
            throw new RuntimeException("Erreur lors de la recherche de l'aide-soignant: " + e.getMessage(), e);
        }
    }

    @Override
    public AideSoignant authenticate(String email, String password) {
        try {
            TypedQuery<AideSoignant> q = em.createQuery(
                "SELECT a FROM AideSoignant a WHERE a.emailAS = :email AND a.mdpAS = :pwd", AideSoignant.class);
            q.setParameter("email", email);
            q.setParameter("pwd", password);
            return q.getSingleResult();
        } catch (NoResultException e) {
            return null;
        } catch (Exception e) {
            throw new RuntimeException("Erreur d'authentification: " + e.getMessage(), e);
        }
    }

    @Override
    public List<AideSoignant> findAll() {
        try {
            return em.createQuery(
                "SELECT a FROM AideSoignant a ORDER BY a.nomAS, a.prenomAS", AideSoignant.class)
                .getResultList();
        } catch (Exception e) {
            throw new RuntimeException("Erreur lors de la récupération des aides-soignants: " + e.getMessage(), e);
        }
    }

    @Override
    public void update(AideSoignant as) {
        try {
            if (as.getIdAS() == null) throw new IllegalArgumentException("ID manquant");
            AideSoignant existing = em.find(AideSoignant.class, as.getIdAS());
            if (existing == null) throw new IllegalArgumentException("Aide-soignant inexistant: " + as.getIdAS());
            em.merge(as);
        } catch (Exception e) {
            throw new RuntimeException("Erreur lors de la mise à jour: " + e.getMessage(), e);
        }
    }

    @Override
    public void delete(Integer id) {
        try {
            AideSoignant as = em.find(AideSoignant.class, id);
            if (as != null) em.remove(as);
            else throw new IllegalArgumentException("Aide-soignant non trouvé: " + id);
        } catch (Exception e) {
            throw new RuntimeException("Erreur lors de la suppression: " + e.getMessage(), e);
        }
    }

    // ===== Méthodes spécifiques =====

    @Override
    public boolean assignRendezvous(Integer idRendezvous, Integer idAideSoignant) {
        try {
            Rendezvous r = em.find(Rendezvous.class, idRendezvous);
            AideSoignant a = em.find(AideSoignant.class, idAideSoignant);
            if (r == null || a == null) return false;
            r.setAideSoignant(a);
            em.merge(r);
            return true;
        } catch (Exception e) {
            throw new RuntimeException("Erreur d'assignation du rendez-vous: " + e.getMessage(), e);
        }
    }

    @Override
    public boolean unassignRendezvous(Integer idRendezvous) {
        try {
            Rendezvous r = em.find(Rendezvous.class, idRendezvous);
            if (r == null) return false;
                       r.setAideSoignant(null);
            em.merge(r);
            return true;
        } catch (Exception e) {
            throw new RuntimeException("Erreur de désassignation: " + e.getMessage(), e);
        }
    }

    @Override
    public List<Rendezvous> findRendezvousByAideSoignant(Integer idAideSoignant) {
        try {
            TypedQuery<Rendezvous> q = em.createQuery(
                "SELECT r FROM Rendezvous r WHERE r.aideSoignant.idAS = :id ORDER BY r.date DESC", Rendezvous.class);
            q.setParameter("id", idAideSoignant);
            return q.getResultList();
        } catch (Exception e) {
            throw new RuntimeException("Erreur recherche RDV par aide-soignant: " + e.getMessage(), e);
        }
    }

    @Override
    public AideSoignant findByEmail(String email) {
        try {
            TypedQuery<AideSoignant> q = em.createQuery(
                "SELECT a FROM AideSoignant a WHERE a.emailAS = :email", AideSoignant.class);
            q.setParameter("email", email);
            return q.getSingleResult();
        } catch (NoResultException e) {
            return null;
        }
    }

    @Override
    public boolean emailExists(String email) {
        try {
            TypedQuery<Long> q = em.createQuery(
                "SELECT COUNT(a) FROM AideSoignant a WHERE a.emailAS = :email", Long.class);
            q.setParameter("email", email);
            return q.getSingleResult() > 0;
        } catch (Exception e) {
            return false;
        }
    }

    @Override
    public List<AideSoignant> findBySpecialite(String specialite) {
        try {
            TypedQuery<AideSoignant> q = em.createQuery(
                "SELECT a FROM AideSoignant a WHERE a.specialiteAS = :spec ORDER BY a.nomAS", AideSoignant.class);
            q.setParameter("spec", specialite);
            return q.getResultList();
        } catch (Exception e) {
            throw new RuntimeException("Erreur recherche par spécialité: " + e.getMessage(), e);
        }
    }
