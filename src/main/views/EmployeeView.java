package main.views;

import main.controllers.TaskController;
import main.models.Employee;
import main.models.Task;

import java.util.List;
import java.util.Scanner;

public class EmployeeView {

    private static final Scanner scanner = new Scanner(System.in);  // Scanner nesnesini burada tek seferde oluşturuyoruz

    public static void displayEmployeeDetails(Employee employee) {

        System.out.println("=== Çalışan Detayları ===");
        System.out.println("Çalışan Adı: " + employee.getName());
        System.out.println("Pozisyon: " + employee.getPosition());

        // Çalışanın görevlerini listele
        List<Task> tasks = getEmployeeTasks(employee);
        if (tasks.isEmpty()) {
            System.out.println("Bu çalışanın görevleri yok.");
        } else {
            System.out.println("Çalışana Ait Görevler:");
            for (Task task : tasks) {
                System.out.println(task.getName() + " | Proje: " + task.getProjectName() + " | Durum: " + task.getStatus());
            }
        }

        System.out.println("\n1. Ana Menüye Dön");
        System.out.print("Seçiminiz: ");
        int choice = scanner.nextInt();

        if (choice == 1) {
            return;
        } else {
            System.out.println("Geçersiz seçim. Ana menüye dönülüyor...");
        }
    }

    private static List<Task> getEmployeeTasks(Employee employee) {
        // Burada çalışanla ilgili görevleri almak için bir kontrol yapılır.
        // Örneğin, bir görev listeleme fonksiyonu kullanılabilir.
        return TaskController.getAllTasksByEmployeeId(employee.getId());
    }
}
