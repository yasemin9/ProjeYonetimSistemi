package main.controllers;

import main.models.Employee;
import main.utils.Database;

import java.sql.*;
import java.util.ArrayList;
import java.util.List;

public class EmployeeController {
    public static List<Employee> getAllEmployees() {
        List<Employee> employees = new ArrayList<>();
        try (Connection conn = Database.getConnection()) {
            String query = "SELECT * FROM Employees";
            Statement stmt = conn.createStatement();
            ResultSet rs = stmt.executeQuery(query);

            while (rs.next()) {
                Employee employee = new Employee(
                        rs.getInt("id"),
                        rs.getString("name"),
                        rs.getString("position")
                );
                employees.add(employee);
            }
        } catch (SQLException e) {
            e.printStackTrace();
        }
        return employees;
    }
}
