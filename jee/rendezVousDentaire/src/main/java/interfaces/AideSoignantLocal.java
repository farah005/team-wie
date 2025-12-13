
// interfaces/AideSoignantLocal.java
package interfaces;

import java.util.List;
import entities.AideSoignant;
import entities.Rendezvous;

public interface AideSoignantLocal {
    void create(AideSoignant as);
    AideSoignant find(Integer id);
    AideSoignant authenticate(String email, String password);
    List<AideSoignant> findAll    List<AideSoignant> findAll();
    void update(AideSoignant as);
    void delete(Integer id);

    // Méthodes spécifiques à l’aide-soignant
    boolean assignRendezvous(Integer idRendezvous, Integer idAideSoignant);
    boolean unassignRendezvous(Integer idRendezvous);
    List<Rendezvous> findRendezvousByAideSoignant(Integer idAideSoignant);
    AideSoignant findByEmail(String email);
    boolean emailExists(String email);
    List<AideSoignant> findBySpecialite(String specialite);
}