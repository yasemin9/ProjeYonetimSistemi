CREATE DATABASE ProjectManagement;

USE ProjectManagement;

CREATE TABLE Employees (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    position VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE Projects (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE Tasks (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    status ENUM('Tamamlanacak', 'Devam Ediyor', 'Tamamlandı') DEFAULT 'Tamamlanacak',
    employee_id INT,
    project_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (employee_id) REFERENCES Employees(id),
    FOREIGN KEY (project_id) REFERENCES Projects(id)
);

-- Örnek veriler:
INSERT INTO Employees (name, position) VALUES 
('Ahmet Yılmaz', 'Developer'),
('Ayşe Kaya', 'Tester'),
('Mehmet Can', 'Manager');

INSERT INTO Projects (name, start_date, end_date) VALUES 
('Proje A', '2024-01-01', '2024-06-01'),
('Proje B', '2024-02-01', '2024-07-01');

INSERT INTO Tasks (name, start_date, end_date, status, employee_id, project_id) VALUES
('Görev 1', '2024-01-10', '2024-01-20', 'Tamamlanacak', 1, 1),
('Görev 2', '2024-01-15', '2024-01-25', 'Devam Ediyor', 2, 1),
('Görev 3', '2024-02-01', '2024-02-10', 'Tamamlandı', 3, 2);
