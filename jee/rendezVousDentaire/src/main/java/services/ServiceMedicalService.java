package services;

import java.util.List;
import entities.ServiceMedical;
import interfaces.ServiceMedicalLocal;
import jakarta.ejb.Stateless;
import jakarta.persistence.EntityManager;
import jakarta.persistence.PersistenceContext;
import jakarta.persistence.TypedQuery;

@Stateless
public class ServiceMedicalService implements ServiceMedicalLocal {
    
    @PersistenceContext(unitName = "RendezVousPU")
    private EntityManager em;

    @Override
    public void create(ServiceMedical service) {
        try {
            em.persist(service);
        } catch (Exception e) {
            throw new RuntimeException("Erreur lors de la création du service médical: " + e.getMessage(), e);
        }
    }

    @Override
    public ServiceMedical find(Integer id) {
        try {
            return em.find(ServiceMedical.class, id);
        } catch (Exception e) {
            throw new RuntimeException("Erreur lors de la recherche du service médical: " + e.getMessage(), e);
        }
    }

    @Override
    public List<ServiceMedical> findAll() {
        try {
            TypedQuery<ServiceMedical> query = em.createQuery(
                "SELECT s FROM ServiceMedical s ORDER BY s.nomSM", 
                ServiceMedical.class
            );
            return query.getResultList();
        } catch (Exception e) {
            throw new RuntimeException("Erreur lors de la récupération des services médicaux: " + e.getMessage(), e);
        }
    }

    @Override
    public List<ServiceMedical> findByType(String type) {
        try {
            TypedQuery<ServiceMedical> query = em.createQuery(
                "SELECT s FROM ServiceMedical s WHERE s.typeSM LIKE :type ORDER BY s.nomSM", 
                ServiceMedical.class
            );
            query.setParameter("type", "%" + type + "%");
            return query.getResultList();
        } catch (Exception e) {
            throw new RuntimeException("Erreur lors de la recherche par type: " + e.getMessage(), e);
        }
    }

    @Override
    public void update(ServiceMedical service) {
        try {
            if (service.getNumSM() == null) {
                throw new IllegalArgumentException("L'ID du service médical ne peut pas être null");
            }
            
            ServiceMedical existingService = em.find(ServiceMedical.class, service.getNumSM());
            if (existingService == null) {
                throw new IllegalArgumentException("Service médical non trouvé avec l'ID: " + service.getNumSM());
            }
            
            em.merge(service);
        } catch (Exception e) {
            throw new RuntimeException("Erreur lors de la mise à jour du service médical: " + e.getMessage(), e);
        }
    }

    @Override
    public void delete(Integer id) {
        try {
            ServiceMedical service = em.find(ServiceMedical.class, id);
            if (service != null) {
                em.remove(service);
            } else {
                throw new IllegalArgumentException("Service médical non trouvé avec l'ID: " + id);
            }
        } catch (Exception e) {
            throw new RuntimeException("Erreur lors de la suppression du service médical: " + e.getMessage(), e);
        }
    }
    
    // Méthodes utilitaires supplémentaires
    
    /**
     * Recherche un service par nom
     */
    public ServiceMedical findByNom(String nom) {
        try {
            TypedQuery<ServiceMedical> query = em.createQuery(
                "SELECT s FROM ServiceMedical s WHERE s.nomSM = :nom", 
                ServiceMedical.class
            );
            query.setParameter("nom", nom);
            return query.getSingleResult();
        } catch (Exception e) {
            return null;
        }
    }
    
    /**
     * Recherche des services dans une fourchette de tarif
     */
    public List<ServiceMedical> findByTarifRange(Double minTarif, Double maxTarif) {
        try {
            TypedQuery<ServiceMedical> query = em.createQuery(
                "SELECT s FROM ServiceMedical s WHERE s.tarifSM BETWEEN :min AND :max ORDER BY s.tarifSM", 
                ServiceMedical.class
            );
            query.setParameter("min", minTarif);
            query.setParameter("max", maxTarif);
            return query.getResultList();
        } catch (Exception e) {
            throw new RuntimeException("Erreur lors de la recherche par tarif: " + e.getMessage(), e);
        }
    }
    
    /**
     * Obtient tous les types de services distincts
     */
    public List<String> findAllTypes() {
        try {
            TypedQuery<String> query = em.createQuery(
                "SELECT DISTINCT s.typeSM FROM ServiceMedical s ORDER BY s.typeSM", 
                String.class
            );
            return query.getResultList();
        } catch (Exception e) {
            throw new RuntimeException("Erreur lors de la récupération des types: " + e.getMessage(), e);
        }
    }
    
    /**
     * Compte le nombre de services
     */
    public long count() {
        try {
            TypedQuery<Long> query = em.createQuery(
                "SELECT COUNT(s) FROM ServiceMedical s", 
                Long.class
            );
            return query.getSingleResult();
        } catch (Exception e) {
            return 0;
        }
    }
    
    /**
     * Recherche des services avec description
     */
    public List<ServiceMedical> searchByKeyword(String keyword) {
        try {
            TypedQuery<ServiceMedical> query = em.createQuery(
                "SELECT s FROM ServiceMedical s WHERE " +
                "LOWER(s.nomSM) LIKE LOWER(:keyword) OR " +
                "LOWER(s.typeSM) LIKE LOWER(:keyword) OR " +
                "LOWER(s.descriptionSM) LIKE LOWER(:keyword) " +
                "ORDER BY s.nomSM", 
                ServiceMedical.class
            );
            query.setParameter("keyword", "%" + keyword + "%");
            return query.getResultList();
        } catch (Exception e) {
            throw new RuntimeException("Erreur lors de la recherche par mot-clé: " + e.getMessage(), e);
        }
    }
    
    /**
     * Obtient les services les plus chers
     */
    public List<ServiceMedical> findTopExpensive(int limit) {
        try {
            TypedQuery<ServiceMedical> query = em.createQuery(
                "SELECT s FROM ServiceMedical s ORDER BY s.tarifSM DESC", 
                ServiceMedical.class
            );
            query.setMaxResults(limit);
            return query.getResultList();
        } catch (Exception e) {
            throw new RuntimeException("Erreur lors de la récupération des services: " + e.getMessage(), e);
        }
    }
}