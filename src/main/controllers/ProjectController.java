package main.controllers;

import main.models.Project;
import main.utils.Database;

import java.sql.*;
import java.util.ArrayList;
import java.util.List;

public class ProjectController {
    public static List<Project> getAllProjects() {
        List<Project> projects = new ArrayList<>();
        try (Connection conn = Database.getConnection()) {
            String query = "SELECT * FROM Projects";
            Statement stmt = conn.createStatement();
            ResultSet rs = stmt.executeQuery(query);

            while (rs.next()) {
                Project project = new Project(
                        rs.getInt("id"),
                        rs.getString("name"),
                        rs.getDate("start_date").toLocalDate(),
                        rs.getDate("end_date").toLocalDate()
                );
                projects.add(project);
            }
        } catch (SQLException e) {
            e.printStackTrace();
        }
        return projects;
    }

    public static void addProject(Project project) {
        try (Connection conn = Database.getConnection()) {
            String query = "INSERT INTO Projects (name, start_date, end_date) VALUES (?, ?, ?)";
            PreparedStatement pstmt = conn.prepareStatement(query);
            pstmt.setString(1, project.getName());
            pstmt.setDate(2, Date.valueOf(project.getStartDate()));
            pstmt.setDate(3, Date.valueOf(project.getEndDate()));
            pstmt.executeUpdate();
        } catch (SQLException e) {
            e.printStackTrace();
        }
    }
}
