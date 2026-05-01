package services;

import java.util.List;
import entities.ServiceMedical;
import interfaces.ServiceMedicalLocal;
import jakarta.ejb.Stateless;
import jakarta.persistence.EntityManager;
import jakarta.persistence.NoResultException;
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
            throw new RuntimeException("Erreur création service: " + e.getMessage());
        }
    }

    @Override
    public ServiceMedical find(Integer id) {
        return em.find(ServiceMedical.class, id);
    }

    @Override
    public ServiceMedical findByNom(String nom) {
        try {
            return em.createQuery("SELECT s FROM ServiceMedical s WHERE s.nomSM = :nom", ServiceMedical.class)
                     .setParameter("nom", nom)
                     .getSingleResult();
        } catch (NoResultException e) {
            return null;
        }
    }

    @Override
    public List<ServiceMedical> findAll() {
        return em.createQuery("SELECT s FROM ServiceMedical s ORDER BY s.nomSM", ServiceMedical.class)
                 .getResultList();
    }

    @Override
    public List<ServiceMedical> findByType(String type) {
        return em.createQuery("SELECT s FROM ServiceMedical s WHERE s.typeSM LIKE :type ORDER BY s.nomSM", ServiceMedical.class)
                 .setParameter("type", "%" + type + "%")
                 .getResultList();
    }

    @Override
    public List<ServiceMedical> search(String nom, String type) {
        StringBuilder jpql = new StringBuilder("SELECT s FROM ServiceMedical s WHERE 1=1");
        if (nom != null && !nom.isBlank()) {
            jpql.append(" AND LOWER(s.nomSM) LIKE :nom");
        }
        if (type != null && !type.isBlank()) {
            jpql.append(" AND LOWER(s.typeSM) LIKE :type");
        }
        jpql.append(" ORDER BY s.nomSM");

        TypedQuery<ServiceMedical> query = em.createQuery(jpql.toString(), ServiceMedical.class);
        if (nom != null && !nom.isBlank()) {
            query.setParameter("nom", "%" + nom.toLowerCase() + "%");
        }
        if (type != null && !type.isBlank()) {
            query.setParameter("type", "%" + type.toLowerCase() + "%");
        }
        return query.getResultList();
    }

    @Override
    public void update(ServiceMedical service) {
        try {
            if (service.getNumSM() == null) {
                throw new IllegalArgumentException("ID manquant pour la mise à jour");
            }
            em.merge(service);
        } catch (Exception e) {
            throw new RuntimeException("Erreur mise à jour service: " + e.getMessage());
        }
    }

    @Override
    public void delete(Integer id) {
        try {
            ServiceMedical service = em.find(ServiceMedical.class, id);
            if (service != null) {
                em.remove(service);
            }
        } catch (Exception e) {
            throw new RuntimeException("Erreur suppression service: " + e.getMessage());
        }
    }

    @Override
    public List<String> findAllTypes() {
        return em.createQuery("SELECT DISTINCT s.typeSM FROM ServiceMedical s ORDER BY s.typeSM", String.class)
                 .getResultList();
    }

    @Override
    public long count() {
        return em.createQuery("SELECT COUNT(s) FROM ServiceMedical s", Long.class).getSingleResult();
    }

    @Override
    public List<ServiceMedical> findTopExpensive(int limit) {
        return em.createQuery("SELECT s FROM ServiceMedical s ORDER BY s.tarifSM DESC", ServiceMedical.class)
                 .setMaxResults(limit)
                 .getResultList();
    }
}