package interfaces;

import java.util.List;
import entities.ServiceMedical;
import jakarta.ejb.Local;

@Local
public interface ServiceMedicalLocal {
    void create(ServiceMedical service);
    ServiceMedical find(Integer id);
    ServiceMedical findByNom(String nom);
    List<ServiceMedical> findAll();
    List<ServiceMedical> findByType(String type);
    List<ServiceMedical> search(String nom, String type);
    List<ServiceMedical> findTopExpensive(int limit);
    List<String> findAllTypes();
    void update(ServiceMedical service);
    void delete(Integer id);
    long count();
}