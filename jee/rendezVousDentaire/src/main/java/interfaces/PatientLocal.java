package interfaces;
import java.util.List;

import entities.Patient;
import jakarta.ejb.Local;
@Local
public interface PatientLocal {
	public void create(Patient patient);
	public Patient find(Integer id);
	public Patient authenticate(String email, String password);
	public List<Patient> findAll();
	public void update(Patient patient);
	public void delete(Integer id);
}