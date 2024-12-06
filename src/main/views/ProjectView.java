package main.views;

import main.controllers.TaskController;
import main.models.Project;
import main.models.Task;

import java.util.List;
import java.util.Scanner;

public class ProjectView {

    public static void displayProjectDetails(Project project) {
        try (Scanner scanner = new Scanner(System.in)) { // try-with-resources kullanarak scanner'ı otomatik olarak kapatıyoruz
            System.out.println("=== Proje Detayları ===");
            System.out.println("Proje Adı: " + project.getName());
            System.out.println("Başlangıç Tarihi: " + project.getStartDate());
            System.out.println("Bitiş Tarihi: " + project.getEndDate());

            // Görevleri listele
            List<Task> tasks = TaskController.getAllTasksByProjectId(project.getId());
            if (tasks.isEmpty()) {
                System.out.println("Bu projede henüz görev bulunmamaktadır.");
            } else {
                System.out.println("Projeye Ait Görevler:");
                for (Task task : tasks) {
                    System.out.println(task.getName() + " | Durum: " + task.getStatus());
                }
            }

            System.out.println("\n1. Görev Ekle");
            System.out.println("2. Ana Menüye Dön");
            System.out.print("Seçiminiz: ");
            int choice = scanner.nextInt();

            switch (choice) {
                case 1:
                    addTaskToProject(project);
                    break;
                case 2:
                    return;
                default:
                    System.out.println("Geçersiz seçim. Ana menüye dönülüyor...");
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    private static void addTaskToProject(Project project) {
        try (Scanner scanner = new Scanner(System.in)) { // try-with-resources kullanarak scanner'ı otomatik olarak kapatıyoruz
            System.out.print("Görev Adı: ");
            String taskName = scanner.nextLine();
            System.out.print("Başlangıç Tarihi (YYYY-MM-DD): ");
            String startDate = scanner.nextLine();
            System.out.print("Bitiş Tarihi (YYYY-MM-DD): ");
            String endDate = scanner.nextLine();

            // Görevi kaydet
            Task task = new Task(0, taskName, java.time.LocalDate.parse(startDate), java.time.LocalDate.parse(endDate), "Tamamlanacak", project);
            TaskController.addTaskToProject(task, project);

            System.out.println("Görev başarıyla eklendi!");
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
