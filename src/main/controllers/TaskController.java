package main.controllers;

import main.models.Task;
import main.models.Project;

import java.util.ArrayList;
import java.util.List;

public class TaskController {

    private static List<Task> taskList = new ArrayList<>();  // Görevlerin saklanacağı liste

    // Yeni bir görevi projeye ekleme
    public static void addTaskToProject(Task task, Project project) {
        taskList.add(task);  // Yeni görev listeye eklenir
    }

    // Çalışan ID'sine göre görevleri al
    public static List<Task> getAllTasksByEmployeeId(int employeeId) {
        List<Task> tasks = new ArrayList<>();  // Çalışan için görevler
        for (Task task : taskList) {
            if (task.getProject().getId() == employeeId) {  // Eğer görev o çalışanın projesine aitse
                tasks.add(task);
            }
        }
        return tasks;  // Görev listesi döndürülür
    }

    // Tüm görevleri listele
    public static List<Task> getAllTasks() {
        return taskList;  // Tüm görevleri döndür
    }

    // Görev ID'sine göre bir görev getirme
    public static Task getTaskById(int taskId) {
        for (Task task : taskList) {
            if (task.getId() == taskId) {
                return task;  // Görev bulunduysa döndür
            }
        }
        return null;  // Eğer görev bulunamazsa null döndür
    }

    // Görev durumunu güncelleme
    public static void updateTaskStatus(int taskId, String newStatus) {
        Task task = getTaskById(taskId);
        if (task != null) {
            task.setStatus(newStatus);  // Görev bulunduysa, durumunu güncelle
        }
    }

    // Görev silme
    public static void removeTask(int taskId) {
        Task task = getTaskById(taskId);
        if (task != null) {
            taskList.remove(task);  // Görev bulunduysa, listeden çıkar
        }
    }

    // Projeye görev ekleme (yardımcı metod)
    public static void addTask(Task task, Project project) {
        task.setProject(project);  // Göreve proje ataması yap
        addTaskToProject(task, project);  // Yeni görevi listeye ekle
    }

    // Tüm görevleri projeye göre filtreleme
    public static List<Task> getTasksByProject(Project project) {
        List<Task> projectTasks = new ArrayList<>();
        for (Task task : taskList) {
            if (task.getProject().equals(project)) {
                projectTasks.add(task);  // Eğer görev, belirtilen proje ile eşleşiyorsa, listeye ekle
            }
        }
        return projectTasks;  // Belirtilen projeye ait görevler döndürülür
    }

    // Bu metodun gereksiz olduğunu belirledik ve kaldırdık
    // public static void addTaskToProject(Task task, Project project) {
    //     // TODO Auto-generated method stub
    //     throw new UnsupportedOperationException("Unimplemented method 'addTaskToProject'");
    // }

    // Projeye ait görevleri listeleme
    public static List<Task> getAllTasksByProjectId(int projectId) {
        List<Task> tasks = new ArrayList<>();
        for (Task task : taskList) {
            if (task.getProject().getId() == projectId) {  // Proje ID'si ile eşleşen görevleri al
                tasks.add(task);
            }
        }
        return tasks;  // Projeye ait görevleri döndür
    }
}
