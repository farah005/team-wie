package services;

import java.math.BigDecimal;
import java.util.List;
import entities.ActeMedical;
import interfaces.ActeMedicalLocal;
import jakarta.ejb.Stateless;
import jakarta.persistence.EntityManager;
import jakarta.persistence.PersistenceContext;
import jakarta.persistence.TypedQuery;

@Stateless
public class ActeMedicalService implements ActeMedicalLocal {
    
    @PersistenceContext(unitName = "RendezVousPU")
    private EntityManager em;

    @Override
    public void create(ActeMedical acte) {
        try {
            em.persist(acte);
        } catch (Exception e) {
            throw new RuntimeException("Erreur lors de la création de l'acte médical: " + e.getMessage(), e);
        }
    }

    @Override
    public ActeMedical find(Integer id) {
        try {
            return em.find(ActeMedical.class, id);
        } catch (Exception e) {
            throw new RuntimeException("Erreur lors de la recherche de l'acte médical: " + e.getMessage(), e);
        }
    }

    @Override
    public List<ActeMedical> findAll() {
        try {
            TypedQuery<ActeMedical> query = em.createQuery(
                "SELECT a FROM ActeMedical a ORDER BY a.idAM DESC", 
                ActeMedical.class
            );
            return query.getResultList();
        } catch (Exception e) {
            throw new RuntimeException("Erreur lors de la récupération des actes médicaux: " + e.getMessage(), e);
        }
    }

    @Override
    public void update(ActeMedical acte) {
        try {
            if (acte.getIdAM() == null) {
                throw new IllegalArgumentException("L'ID de l'acte médical ne peut pas être null");
            }
            
            ActeMedical existingActe = em.find(ActeMedical.class, acte.getIdAM());
            if (existingActe == null) {
                throw new IllegalArgumentException("Acte médical non trouvé avec l'ID: " + acte.getIdAM());
            }
            
            em.merge(acte);
        } catch (Exception e) {
            throw new RuntimeException("Erreur lors de la mise à jour de l'acte médical: " + e.getMessage(), e);
        }
    }

    @Override
    public void delete(Integer id) {
        try {
            ActeMedical acte = em.find(ActeMedical.class, id);
            if (acte != null) {
                em.remove(acte);
            } else {
                throw new IllegalArgumentException("Acte médical non trouvé avec l'ID: " + id);
            }
        } catch (Exception e) {
            throw new RuntimeException("Erreur lors de la suppression de l'acte médical: " + e.getMessage(), e);
        }
    }
    
    // Méthodes utilitaires supplémentaires
    
    /**
     * Recherche tous les actes médicaux d'un rendez-vous
     */
    public List<ActeMedical> findByRendezvous(Integer idRv) {
        try {
            TypedQuery<ActeMedical> query = em.createQuery(
                "SELECT a FROM ActeMedical a WHERE a.rendezvous.idRv = :idRv " +
                "ORDER BY a.idAM", 
                ActeMedical.class
            );
            query.setParameter("idRv", idRv);
            return query.getResultList();
        } catch (Exception e) {
            throw new RuntimeException("Erreur lors de la recherche des actes par rendez-vous: " + e.getMessage(), e);
        }
    }
    
    /**
     * Recherche tous les actes médicaux utilisant un service médical
     */
    public List<ActeMedical> findByServiceMedical(Integer numSM) {
        try {
            TypedQuery<ActeMedical> query = em.createQuery(
                "SELECT a FROM ActeMedical a WHERE a.serviceMedical.numSM = :numSM " +
                "ORDER BY a.idAM DESC", 
                ActeMedical.class
            );
            query.setParameter("numSM", numSM);
            return query.getResultList();
        } catch (Exception e) {
            throw new RuntimeException("Erreur lors de la recherche des actes par service: " + e.getMessage(), e);
        }
    }
    
    /**
     * Calcule le coût total des actes d'un rendez-vous
     */
    public BigDecimal calculateTotalCostByRendezvous(Integer idRv) {
        try {
            TypedQuery<BigDecimal> query = em.createQuery(
                "SELECT SUM(a.tarifAM) FROM ActeMedical a WHERE a.rendezvous.idRv = :idRv", 
                BigDecimal.class
            );
            query.setParameter("idRv", idRv);
            
            BigDecimal result = query.getSingleResult();
            return result != null ? result : BigDecimal.ZERO;
        } catch (Exception e) {
            return BigDecimal.ZERO;
        }
    }
    
    /**
     * Recherche les actes médicaux d'un patient via ses rendez-vous
     */
    public List<ActeMedical> findByPatient(Integer idPatient) {
        try {
            TypedQuery<ActeMedical> query = em.createQuery(
                "SELECT a FROM ActeMedical a WHERE a.rendezvous.patient.idP = :idPatient " +
                "ORDER BY a.rendezvous.dateRv DESC", 
                ActeMedical.class
            );
            query.setParameter("idPatient", idPatient);
            return query.getResultList();
        } catch (Exception e) {
            throw new RuntimeException("Erreur lors de la recherche des actes par patient: " + e.getMessage(), e);
        }
    }
    
    /**
     * Recherche les actes médicaux effectués par un dentiste
     */
    public List<ActeMedical> findByDentiste(Integer idDentiste) {
        try {
            TypedQuery<ActeMedical> query = em.createQuery(
                "SELECT a FROM ActeMedical a WHERE a.rendezvous.dentiste.idD = :idDentiste " +
                "ORDER BY a.rendezvous.dateRv DESC", 
                ActeMedical.class
            );
            query.setParameter("idDentiste", idDentiste);
            return query.getResultList();
        } catch (Exception e) {
            throw new RuntimeException("Erreur lors de la recherche des actes par dentiste: " + e.getMessage(), e);
        }
    }
    
    /**
     * Compte le nombre d'actes médicaux
     */
    public long count() {
        try {
            TypedQuery<Long> query = em.createQuery(
                "SELECT COUNT(a) FROM ActeMedical a", 
                Long.class
            );
            return query.getSingleResult();
        } catch (Exception e) {
            return 0;
        }
    }
    
    /**
     * Compte le nombre d'actes pour un rendez-vous
     */
    public long countByRendezvous(Integer idRv) {
        try {
            TypedQuery<Long> query = em.createQuery(
                "SELECT COUNT(a) FROM ActeMedical a WHERE a.rendezvous.idRv = :idRv", 
                Long.class
            );
            query.setParameter("idRv", idRv);
            return query.getSingleResult();
        } catch (Exception e) {
            return 0;
        }
    }
    
    /**
     * Recherche les actes médicaux dans une fourchette de tarif
     */
    public List<ActeMedical> findByTarifRange(BigDecimal minTarif, BigDecimal maxTarif) {
        try {
            TypedQuery<ActeMedical> query = em.createQuery(
                "SELECT a FROM ActeMedical a WHERE a.tarifAM BETWEEN :min AND :max " +
                "ORDER BY a.tarifAM", 
                ActeMedical.class
            );
            query.setParameter("min", minTarif);
            query.setParameter("max", maxTarif);
            return query.getResultList();
        } catch (Exception e) {
            throw new RuntimeException("Erreur lors de la recherche par tarif: " + e.getMessage(), e);
        }
    }
    
    /**
     * Obtient les actes les plus coûteux
     */
    public List<ActeMedical> findTopExpensive(int limit) {
        try {
            TypedQuery<ActeMedical> query = em.createQuery(
                "SELECT a FROM ActeMedical a ORDER BY a.tarifAM DESC", 
                ActeMedical.class
            );
            query.setMaxResults(limit);
            return query.getResultList();
        } catch (Exception e) {
            throw new RuntimeException("Erreur lors de la récupération des actes: " + e.getMessage(), e);
        }
    }
    
    /**
     * Recherche les actes par mot-clé dans la description
     */
    public List<ActeMedical> searchByDescription(String keyword) {
        try {
            TypedQuery<ActeMedical> query = em.createQuery(
                "SELECT a FROM ActeMedical a WHERE LOWER(a.descriptionAM) LIKE LOWER(:keyword) " +
                "ORDER BY a.idAM DESC", 
                ActeMedical.class
            );
            query.setParameter("keyword", "%" + keyword + "%");
            return query.getResultList();
        } catch (Exception e) {
            throw new RuntimeException("Erreur lors de la recherche par description: " + e.getMessage(), e);
        }
    }
    
    /**
     * Calcule le revenu total généré par tous les actes
     */
    public BigDecimal calculateTotalRevenue() {
        try {
            TypedQuery<BigDecimal> query = em.createQuery(
                "SELECT SUM(a.tarifAM) FROM ActeMedical a", 
                BigDecimal.class
            );
            BigDecimal result = query.getSingleResult();
            return result != null ? result : BigDecimal.ZERO;
        } catch (Exception e) {
            return BigDecimal.ZERO;
        }
    }
    
    /**
     * Calcule le revenu généré par un dentiste
     */
    public BigDecimal calculateRevenueByDentiste(Integer idDentiste) {
        try {
            TypedQuery<BigDecimal> query = em.createQuery(
                "SELECT SUM(a.tarifAM) FROM ActeMedical a " +
                "WHERE a.rendezvous.dentiste.idD = :idDentiste", 
                BigDecimal.class
            );
            query.setParameter("idDentiste", idDentiste);
            BigDecimal result = query.getSingleResult();
            return result != null ? result : BigDecimal.ZERO;
        } catch (Exception e) {
            return BigDecimal.ZERO;
        }
    }
}