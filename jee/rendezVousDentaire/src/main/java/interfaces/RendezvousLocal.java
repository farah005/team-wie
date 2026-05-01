package interfaces;

import java.util.Date;
import java.util.List;
import entities.Rendezvous;
import jakarta.ejb.Local;

@Local
public interface RendezvousLocal {
    
    // Opérations de base (CRUD)
    void create(Rendezvous rdv);
    Rendezvous find(Integer id);
    void update(Rendezvous rdv);
    void delete(Integer id);
    List<Rendezvous> findAll();
    
    // Recherches filtrées
    List<Rendezvous> findByPatient(Integer idPatient);
    List<Rendezvous> findByDentiste(Integer idDentiste);
    List<Rendezvous> findByDate(Date date);
    List<Rendezvous> findByStatut(String statut);
    List<Rendezvous> findByDentisteAndDate(Integer idDentiste, Date date);
    
    // Recherches pour le planning (A venir)
    List<Rendezvous> findUpcomingByDentiste(Integer idDentiste);
    List<Rendezvous> findUpcomingByPatient(Integer idPatient);
    
    // Statistiques et mises à jour rapides
    long countByStatut(String statut);
        // Mise à jour rapide du statut d'un rendez-vous
        void updateStatut(Integer idRv, String newStatut);
    
    // --- MÉTHODES DE VALIDATION MÉTIER ---
    
    /**
     * Vérifie si le dentiste n'a pas déjà un RDV sur ce créneau
     */
        // Vérifie si un dentiste a un créneau libre
        boolean isSlotAvailable(Integer idDentiste, Date date, String heure);
    
    /**
     * Vérifie si le patient n'a pas déjà un RDV ce jour-là
     */
        // Vérifie si un patient a déjà un RDV ce jour-là
        boolean patientADejaRDV(Integer idPatient, Date date);
}