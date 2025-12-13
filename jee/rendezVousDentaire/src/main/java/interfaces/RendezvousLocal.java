package interfaces;
import java.util.Date;
import java.util.List;

import entities.Rendezvous;
import jakarta.ejb.Local;
@Local
public interface RendezvousLocal {
	public void create(Rendezvous rdv);
	public Rendezvous find(Integer id);
	public List<Rendezvous> findAll();
	public List<Rendezvous> findByPatient(Integer idPatient);
	public List<Rendezvous> findByDentiste(Integer idDentiste);
	public List<Rendezvous> findByDate(Date date);
	public List<Rendezvous> findByStatut(String statut);
	public void update(Rendezvous rdv);
	public void delete(Integer id);
	
}