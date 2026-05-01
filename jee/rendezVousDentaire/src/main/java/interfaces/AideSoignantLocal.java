package interfaces;

import java.util.List;
import entities.AideSoignant;
import entities.Rendezvous;
import jakarta.ejb.Local;

@Local
public interface AideSoignantLocal {
    void create(AideSoignant as);
    AideSoignant find(Integer id);
    AideSoignant authenticate(String email, String password);
    List<AideSoignant> findAll();
    void update(AideSoignant as);
    void delete(Integer id);
    
    // Méthodes métier spécifiques
    AideSoignant findByEmail(String email);
    List<AideSoignant> findByDentiste(Integer idDentiste);
    boolean emailExists(String email);
}