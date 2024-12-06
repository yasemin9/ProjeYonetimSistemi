package main;

import main.controllers.ProjectController;
import main.models.Project;

import java.util.List;
import java.util.Scanner;

public class MainView {

    // Ana Scanner nesnesini sınıf seviyesinde tanımlıyoruz
    private static final Scanner scanner = new Scanner(System.in);

    public static void displayMainMenu() {
        int choice;

        do {
            System.out.println("=== Ana Menü ===");
            System.out.println("1. Projeleri Listele");
            System.out.println("2. Yeni Proje Ekle");
            System.out.println("3. Çıkış");
            System.out.print("Seçiminiz: ");
            choice = scanner.nextInt();

            switch (choice) {
                case 1:
                    listProjects();
                    break;
                case 2:
                    addProject();
                    break;
                case 3:
                    System.out.println("Çıkılıyor...");
                    break;
                default:
                    System.out.println("Geçersiz seçim. Tekrar deneyin.");
            }
        } while (choice != 3);
    }

    private static void listProjects() {
        List<Project> projects = ProjectController.getAllProjects();
        System.out.println("=== Projeler ===");
        for (Project project : projects) {
            System.out.println(project);
        }
    }

    private static void addProject() {
        // Kullanıcıdan veri almak için scanner nesnesini tekrar kullanıyoruz
        System.out.print("Proje Adı: ");
        String name = scanner.next();
        System.out.print("Başlangıç Tarihi (YYYY-MM-DD): ");
        String startDate = scanner.next();
        System.out.print("Bitiş Tarihi (YYYY-MM-DD): ");
        String endDate = scanner.next();

        Project project = new Project(0, name, java.time.LocalDate.parse(startDate), java.time.LocalDate.parse(endDate));
        ProjectController.addProject(project);

        System.out.println("Proje başarıyla eklendi!");
    }
}
