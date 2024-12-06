package main.models;

import java.time.LocalDate;

public class Task {
    private int id;
    private String name;
    private LocalDate startDate;
    private LocalDate endDate;
    private String status;
    private Project project;  // Proje nesnesi ekledik

    // Constructor
    public Task(int id, String name, LocalDate startDate, LocalDate endDate, String status, Project project) {
        this.id = id;
        this.name = name;
        this.startDate = startDate;
        this.endDate = endDate;
        this.status = status;
        this.project = project;  // Proje nesnesini constructor'a ekledik
    }

    // Getter ve Setter'lar
    public int getId() {
        return id;
    }

    public void setId(int id) {
        this.id = id;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public LocalDate getStartDate() {
        return startDate;
    }

    public void setStartDate(LocalDate startDate) {
        this.startDate = startDate;
    }

    public LocalDate getEndDate() {
        return endDate;
    }

    public void setEndDate(LocalDate endDate) {
        this.endDate = endDate;
    }

    public String getStatus() {
        return status;
    }

    public void setStatus(String status) {
        this.status = status;
    }

    public Project getProject() {
        return project;  // Proje nesnesini döndüren metod
    }

    public String getProjectName() {
        return project.getName();  // Proje adını döndüren metod
    }

    @Override
    public String toString() {
        return "Task{" +
                "id=" + id +
                ", name='" + name + '\'' +
                ", startDate=" + startDate +
                ", endDate=" + endDate +
                ", status='" + status + '\'' +
                ", project=" + project.getName() +  // Proje adını toString içinde gösteriyoruz
                '}';
    }

    public void setProject(Project project) {
        this.project = project;  // Projeyi set eden setter metodu
    }
}
