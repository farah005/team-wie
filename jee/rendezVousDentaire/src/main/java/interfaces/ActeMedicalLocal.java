package interfaces;
import java.util.List;

import entities.ActeMedical;
import jakarta.ejb.Local;
@Local
public interface ActeMedicalLocal {
	public void create(ActeMedical acte);
	public ActeMedical find(Integer id);
	 public List<ActeMedical> findAll();
	 public void update(ActeMedical acte);
	 public void delete(Integer id);

	 // Recherche des actes par rendez-vous
	 public List<ActeMedical> findByRendezvous(Integer idRv);
	
}

