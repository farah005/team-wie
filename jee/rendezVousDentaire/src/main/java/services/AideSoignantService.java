package services;

import entities.AideSoignant;
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
            // On s'assure que le statut est "Actif" par défaut si non précisé
            if (as.getStatutAS() == null) {
                as.setStatutAS("Actif");
            }
            em.persist(as);
        } catch (Exception e) {
            throw new RuntimeException("Erreur lors de la création : " + e.getMessage());
        }
    }

    @Override
    public AideSoignant find(Integer id) {
        return em.find(AideSoignant.class, id);
    }

    @Override
    public AideSoignant authenticate(String email, String password) {
        try {
           
            TypedQuery<AideSoignant> q = em.createQuery(
                "SELECT a FROM AideSoignant a WHERE a.emailAS = :email AND a.mdpAS = :pwd", 
                AideSoignant.class);
            q.setParameter("email", email);
            q.setParameter("pwd", password);
            return q.getSingleResult();
        } catch (NoResultException e) {
            return null; // Identifiants invalides
        }
    }

    @Override
    public List<AideSoignant> findAll() {
        return em.createQuery("SELECT a FROM AideSoignant a ORDER BY a.nomAS ASC", AideSoignant.class)
                 .getResultList();
    }

    @Override
    public void update(AideSoignant as) {
        try {
            // Le merge est utilisé pour mettre à jour une entité détachée
            em.merge(as);
        } catch (Exception e) {
            throw new RuntimeException("Erreur lors de la mise à jour : " + e.getMessage());
        }
    }

    @Override
    public void delete(Integer id) {
        try {
            AideSoignant as = em.find(AideSoignant.class, id);
            if (as != null) {
                em.remove(as);
            }
        } catch (Exception e) {
            throw new RuntimeException("Erreur lors de la suppression : " + e.getMessage());
        }
    }

    @Override
    public AideSoignant findByEmail(String email) {
        try {
            return em.createQuery("SELECT a FROM AideSoignant a WHERE a.emailAS = :email", AideSoignant.class)
                     .setParameter("email", email)
                     .getSingleResult();
        } catch (NoResultException e) {
            return null;
        }
    }

    @Override
    public boolean emailExists(String email) {
        Long count = em.createQuery("SELECT COUNT(a) FROM AideSoignant a WHERE a.emailAS = :email", Long.class)
                       .setParameter("email", email)
                       .getSingleResult();
        return count > 0;
    }

    @Override
    public List<AideSoignant> findByDentiste(Integer idDentiste) {
        // Cette requête permet de voir tous les aides-soignants rattachés à un docteur spécifique
        return em.createQuery("SELECT a FROM AideSoignant a WHERE a.dentiste.idD = :idD", AideSoignant.class)
                 .setParameter("idD", idDentiste)
                 .getResultList();
    }
}