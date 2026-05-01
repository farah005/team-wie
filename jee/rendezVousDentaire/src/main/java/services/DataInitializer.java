package services;

import jakarta.annotation.PostConstruct;
import jakarta.ejb.EJB;
import jakarta.ejb.Singleton;
import jakarta.ejb.Startup;
import entities.Dentiste;
import interfaces.DentisteLocal;

@Singleton
@Startup // S'exécute automatiquement au démarrage du serveur
public class DataInitializer {

    @EJB
    private DentisteLocal dentisteService;

    @PostConstruct
    public void init() {
        // On vérifie si la base est vide avant d'ajouter
        if (dentisteService.findAll().isEmpty()) {
            
            Dentiste d1 = new Dentiste("Aloui", "Ahmed", "ahmed@sourire.tn");
            d1.setMdpD("123456a");
            d1.setSpecialiteD("orthodontiste");
            d1.setSexeD("M");
            d1.setTelD(22333444);
            dentisteService.create(d1);

            Dentiste d2 = new Dentiste("Trabelsi", "Sonia", "sonia@sourire.tn");
            d2.setMdpD("123456s");
            d2.setSpecialiteD("parodontiste");
            d2.setSexeD("F");
            d2.setTelD(55666777);
            dentisteService.create(d2);

            Dentiste d3 = new Dentiste("Elmaghrbi", "Wael", "wael@sourire.tn");
            d1.setMdpD("123456w");
            d1.setSpecialiteD("endodontiste");
            d1.setSexeD("M");
            d1.setTelD(53689241);
            dentisteService.create(d3);
            System.out.println(">>> 3 Dentistes de test insérés avec succès !");
        }
    }
}