package interfaces;

import java.util.List;
import entities.Patient;
import jakarta.ejb.Local;

@Local
public interface PatientLocal {
    void create(Patient patient);
    Patient find(Integer id);
    Patient authenticate(String email, String password);
    Patient findByEmail(String email); 
    List<Patient> findAll();
    void update(Patient patient);
    void delete(Integer id);
}