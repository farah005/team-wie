package services;

import java.util.Date;
import java.util.List;
import entities.Rendezvous;
import interfaces.RendezvousLocal;
import jakarta.ejb.Stateless;
import jakarta.persistence.EntityManager;
import jakarta.persistence.PersistenceContext;
import jakarta.persistence.TypedQuery;
import jakarta.persistence.TemporalType;

@Stateless
public class RendezvousService implements RendezvousLocal {
    
    @PersistenceContext(unitName = "RendezVousPU")
    private EntityManager em;

    @Override
    public void create(Rendezvous rdv) {
        try {
            em.persist(rdv);
        } catch (Exception e) {
            throw new RuntimeException("Erreur lors de la création du rendez-vous: " + e.getMessage(), e);
        }
    }

    @Override
    public Rendezvous find(Integer id) {
        try {
            return em.find(Rendezvous.class, id);
        } catch (Exception e) {
            throw new RuntimeException("Erreur lors de la recherche du rendez-vous: " + e.getMessage(), e);
        }
    }

    @Override
    public List<Rendezvous> findAll() {
        try {
            TypedQuery<Rendezvous> query = em.createQuery(
                "SELECT r FROM Rendezvous r ORDER BY r.dateRv DESC, r.heureRv DESC", 
                Rendezvous.class
            );
            return query.getResultList();
        } catch (Exception e) {
            throw new RuntimeException("Erreur lors de la récupération des rendez-vous: " + e.getMessage(), e);
        }
    }

    @Override
    public List<Rendezvous> findByPatient(Integer idPatient) {
        try {
            TypedQuery<Rendezvous> query = em.createQuery(
                "SELECT r FROM Rendezvous r WHERE r.patient.idP = :idPatient " +
                "ORDER BY r.dateRv DESC, r.heureRv DESC", 
                Rendezvous.class
            );
            query.setParameter("idPatient", idPatient);
            return query.getResultList();
        } catch (Exception e) {
            throw new RuntimeException("Erreur lors de la recherche des rendez-vous du patient: " + e.getMessage(), e);
        }
    }

    @Override
    public List<Rendezvous> findByDentiste(Integer idDentiste) {
        try {
            TypedQuery<Rendezvous> query = em.createQuery(
                "SELECT r FROM Rendezvous r WHERE r.dentiste.idD = :idDentiste " +
                "ORDER BY r.dateRv DESC, r.heureRv DESC", 
                Rendezvous.class
            );
            query.setParameter("idDentiste", idDentiste);
            return query.getResultList();
        } catch (Exception e) {
            throw new RuntimeException("Erreur lors de la recherche des rendez-vous du dentiste: " + e.getMessage(), e);
        }
    }

    @Override
    public List<Rendezvous> findByDate(Date date) {
        try {
            TypedQuery<Rendezvous> query = em.createQuery(
                "SELECT r FROM Rendezvous r WHERE r.dateRv = :date " +
                "ORDER BY r.heureRv", 
                Rendezvous.class
            );
            query.setParameter("date", date, TemporalType.DATE);
            return query.getResultList();
        } catch (Exception e) {
            throw new RuntimeException("Erreur lors de la recherche des rendez-vous par date: " + e.getMessage(), e);
        }
    }

    @Override
    public List<Rendezvous> findByStatut(String statut) {
        try {
            TypedQuery<Rendezvous> query = em.createQuery(
                "SELECT r FROM Rendezvous r WHERE r.statutRv = :statut " +
                "ORDER BY r.dateRv DESC, r.heureRv DESC", 
                Rendezvous.class
            );
            query.setParameter("statut", statut);
            return query.getResultList();
        } catch (Exception e) {
            throw new RuntimeException("Erreur lors de la recherche des rendez-vous par statut: " + e.getMessage(), e);
        }
    }

    @Override
    public void update(Rendezvous rdv) {
        try {
            if (rdv.getIdRv() == null) {
                throw new IllegalArgumentException("L'ID du rendez-vous ne peut pas être null");
            }
            
            Rendezvous existingRdv = em.find(Rendezvous.class, rdv.getIdRv());
            if (existingRdv == null) {
                throw new IllegalArgumentException("Rendez-vous non trouvé avec l'ID: " + rdv.getIdRv());
            }
            
            em.merge(rdv);
        } catch (Exception e) {
            throw new RuntimeException("Erreur lors de la mise à jour du rendez-vous: " + e.getMessage(), e);
        }
    }

    @Override
    public void delete(Integer id) {
        try {
            Rendezvous rdv = em.find(Rendezvous.class, id);
            if (rdv != null) {
                em.remove(rdv);
            } else {
                throw new IllegalArgumentException("Rendez-vous non trouvé avec l'ID: " + id);
            }
        } catch (Exception e) {
            throw new RuntimeException("Erreur lors de la suppression du rendez-vous: " + e.getMessage(), e);
        }
    }
    
    // Méthodes utilitaires supplémentaires
    
    /**
     * Recherche des rendez-vous entre deux dates
     */
    public List<Rendezvous> findByDateRange(Date startDate, Date endDate) {
        try {
            TypedQuery<Rendezvous> query = em.createQuery(
                "SELECT r FROM Rendezvous r WHERE r.dateRv BETWEEN :startDate AND :endDate " +
                "ORDER BY r.dateRv, r.heureRv", 
                Rendezvous.class
            );
            query.setParameter("startDate", startDate, TemporalType.DATE);
            query.setParameter("endDate", endDate, TemporalType.DATE);
            return query.getResultList();
        } catch (Exception e) {
            throw new RuntimeException("Erreur lors de la recherche par période: " + e.getMessage(), e);
        }
    }
    
    /**
     * Recherche des rendez-vous d'un patient pour une date donnée
     */
    public List<Rendezvous> findByPatientAndDate(Integer idPatient, Date date) {
        try {
            TypedQuery<Rendezvous> query = em.createQuery(
                "SELECT r FROM Rendezvous r WHERE r.patient.idP = :idPatient AND r.dateRv = :date " +
                "ORDER BY r.heureRv", 
                Rendezvous.class
            );
            query.setParameter("idPatient", idPatient);
            query.setParameter("date", date, TemporalType.DATE);
            return query.getResultList();
        } catch (Exception e) {
            throw new RuntimeException("Erreur lors de la recherche: " + e.getMessage(), e);
        }
    }
    
    /**
     * Recherche des rendez-vous d'un dentiste pour une date donnée
     */
    public List<Rendezvous> findByDentisteAndDate(Integer idDentiste, Date date) {
        try {
            TypedQuery<Rendezvous> query = em.createQuery(
                "SELECT r FROM Rendezvous r WHERE r.dentiste.idD = :idDentiste AND r.dateRv = :date " +
                "ORDER BY r.heureRv", 
                Rendezvous.class
            );
            query.setParameter("idDentiste", idDentiste);
            query.setParameter("date", date, TemporalType.DATE);
            return query.getResultList();
        } catch (Exception e) {
            throw new RuntimeException("Erreur lors de la recherche: " + e.getMessage(), e);
        }
    }
    
    /**
     * Compte les rendez-vous par statut
     */
    public long countByStatut(String statut) {
        try {
            TypedQuery<Long> query = em.createQuery(
                "SELECT COUNT(r) FROM Rendezvous r WHERE r.statutRv = :statut", 
                Long.class
            );
            query.setParameter("statut", statut);
            return query.getSingleResult();
        } catch (Exception e) {
            return 0;
        }
    }
    
    /**
     * Recherche les rendez-vous à venir pour un patient
     */
    public List<Rendezvous> findUpcomingByPatient(Integer idPatient) {
        try {
            TypedQuery<Rendezvous> query = em.createQuery(
                "SELECT r FROM Rendezvous r WHERE r.patient.idP = :idPatient " +
                "AND r.dateRv >= CURRENT_DATE " +
                "AND r.statutRv NOT IN ('Annulé', 'Terminé') " +
                "ORDER BY r.dateRv, r.heureRv", 
                Rendezvous.class
            );
            query.setParameter("idPatient", idPatient);
            return query.getResultList();
        } catch (Exception e) {
            throw new RuntimeException("Erreur lors de la recherche: " + e.getMessage(), e);
        }
    }
    
    /**
     * Recherche les rendez-vous à venir pour un dentiste
     */
    public List<Rendezvous> findUpcomingByDentiste(Integer idDentiste) {
        try {
            TypedQuery<Rendezvous> query = em.createQuery(
                "SELECT r FROM Rendezvous r WHERE r.dentiste.idD = :idDentiste " +
                "AND r.dateRv >= CURRENT_DATE " +
                "AND r.statutRv NOT IN ('Annulé', 'Terminé') " +
                "ORDER BY r.dateRv, r.heureRv", 
                Rendezvous.class
            );
            query.setParameter("idDentiste", idDentiste);
            return query.getResultList();
        } catch (Exception e) {
            throw new RuntimeException("Erreur lors de la recherche: " + e.getMessage(), e);
        }
    }
    
    /**
     * Vérifie si un créneau est disponible
     */
    public boolean isSlotAvailable(Integer idDentiste, Date date, String heure) {
        try {
            TypedQuery<Long> query = em.createQuery(
                "SELECT COUNT(r) FROM Rendezvous r WHERE r.dentiste.idD = :idDentiste " +
                "AND r.dateRv = :date AND r.heureRv = :heure " +
                "AND r.statutRv NOT IN ('Annulé')", 
                Long.class
            );
            query.setParameter("idDentiste", idDentiste);
            query.setParameter("date", date, TemporalType.DATE);
            query.setParameter("heure", heure);
            
            return query.getSingleResult() == 0;
        } catch (Exception e) {
            return false;
        }
    }
    
    /**
     * Met à jour le statut d'un rendez-vous
     */
    public void updateStatut(Integer idRv, String newStatut) {
        try {
            Rendezvous rdv = em.find(Rendezvous.class, idRv);
            if (rdv != null) {
                rdv.setStatutRv(newStatut);
                em.merge(rdv);
            }
        } catch (Exception e) {
            throw new RuntimeException("Erreur lors de la mise à jour du statut: " + e.getMessage(), e);
        }
    }
}