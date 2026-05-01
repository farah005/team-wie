package interfaces;
import java.util.List;

import entities.Dentiste;
import jakarta.ejb.Local;
@Local
public interface DentisteLocal {
	public void create(Dentiste dentiste);
	public Dentiste find(Integer id);
	public Dentiste authenticate(String email, String password);
	public List<Dentiste> findAll();
	public List<Dentiste> findBySpecialite(String specialite);
	public void update(Dentiste dentiste);
	public void delete(Integer id);
	public long count();
	
}