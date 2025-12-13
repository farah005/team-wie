package interfaces;
import java.util.List;

import entities.ServiceMedical;
import jakarta.ejb.Local;
@Local
public interface ServiceMedicalLocal {
	 public void delete(Integer id);
	 public ServiceMedical find(Integer id);
	 public List<ServiceMedical> findAll();
	 public List<ServiceMedical> findByType(String type);
	 public void update(ServiceMedical service);
	 public void create(ServiceMedical service);
	
	
}