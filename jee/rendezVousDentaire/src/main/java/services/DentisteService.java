package services;

import java.util.List;
import entities.Dentiste;
import interfaces.DentisteLocal;
import jakarta.ejb.Stateless;
import jakarta.persistence.EntityManager;
import jakarta.persistence.NoResultException;
import jakarta.persistence.PersistenceContext;
import jakarta.persistence.TypedQuery;

@Stateless
public class DentisteService implements DentisteLocal {
    
    @PersistenceContext(unitName = "RendezVousPU")
    private EntityManager em;

    @Override
    public void create(Dentiste dentiste) {
        try {
            em.persist(dentiste);
        } catch (Exception e) {
            throw new RuntimeException("Erreur lors de la création du dentiste: " + e.getMessage(), e);
        }
    }

    @Override
    public Dentiste find(Integer id) {
        try {
            return em.find(Dentiste.class, id);
        } catch (Exception e) {
            throw new RuntimeException("Erreur lors de la recherche du dentiste: " + e.getMessage(), e);
        }
    }

    @Override
    public Dentiste authenticate(String email, String password) {
        try {
            TypedQuery<Dentiste> query = em.createQuery(
                "SELECT d FROM Dentiste d WHERE d.emailD = :email AND d.mdpD = :password", 
                Dentiste.class
            );
            query.setParameter("email", email);
            query.setParameter("password", password);
            
            return query.getSingleResult();
        } catch (NoResultException e) {
            // Aucun dentiste trouvé avec ces identifiants
            return null;
        } catch (Exception e) {
            throw new RuntimeException("Erreur lors de l'authentification: " + e.getMessage(), e);
        }
    }

    @Override
    public List<Dentiste> findAll() {
        try {
            TypedQuery<Dentiste> query = em.createQuery(
                "SELECT d FROM Dentiste d ORDER BY d.nomD, d.prenomD", 
                Dentiste.class
            );
            return query.getResultList();
        } catch (Exception e) {
            throw new RuntimeException("Erreur lors de la récupération des dentistes: " + e.getMessage(), e);
        }
    }

    @Override
    public void update(Dentiste dentiste) {
        try {
            if (dentiste.getIdD() == null) {
                throw new IllegalArgumentException("L'ID du dentiste ne peut pas être null");
            }
            
            Dentiste existingDentiste = em.find(Dentiste.class, dentiste.getIdD());
            if (existingDentiste == null) {
                throw new IllegalArgumentException("Dentiste non trouvé avec l'ID: " + dentiste.getIdD());
            }
            
            em.merge(dentiste);
        } catch (Exception e) {
            throw new RuntimeException("Erreur lors de la mise à jour du dentiste: " + e.getMessage(), e);
        }
    }

    @Override
    public void delete(Integer id) {
        try {
            Dentiste dentiste = em.find(Dentiste.class, id);
            if (dentiste != null) {
                em.remove(dentiste);
            } else {
                throw new IllegalArgumentException("Dentiste non trouvé avec l'ID: " + id);
            }
        } catch (Exception e) {
            throw new RuntimeException("Erreur lors de la suppression du dentiste: " + e.getMessage(), e);
        }
    }
    
    /**
     * Recherche des dentistes par spécialité
     */
    public List<Dentiste> findBySpecialite(String specialite) {
        try {
            TypedQuery<Dentiste> query = em.createQuery(
                "SELECT d FROM Dentiste d WHERE d.specialiteD LIKE :specialite ORDER BY d.nomD", 
                Dentiste.class
            );
            query.setParameter("specialite", "%" + specialite + "%");
            return query.getResultList();
        } catch (Exception e) {
            throw new RuntimeException("Erreur lors de la recherche par spécialité: " + e.getMessage(), e);
        }
    }
    
    /**
     * Compte le nombre de dentistes
     */
    public long count() {
        try {
            TypedQuery<Long> query = em.createQuery(
                "SELECT COUNT(d) FROM Dentiste d", 
                Long.class
            );
            return query.getSingleResult();
        } catch (Exception e) {
            return 0;
        }
    }
    
   
}