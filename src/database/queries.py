class Queries:
    @staticmethod
    def create_tables():
        return [
            """
            CREATE TABLE IF NOT EXISTS employees (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                role VARCHAR(255),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS projects (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                start_date DATE NOT NULL,
                end_date DATE NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS tasks (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                employee_id INT,
                project_id INT,
                start_date DATE NOT NULL,
                end_date DATE NOT NULL,
                work_days INT NOT NULL,
                status ENUM('Tamamlanacak', 'Devam Ediyor', 'Tamamlandı') DEFAULT 'Tamamlanacak',
                delay_days INT DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (employee_id) REFERENCES employees (id) ON DELETE SET NULL,
                FOREIGN KEY (project_id) REFERENCES projects (id) ON DELETE CASCADE
            )
            """
        ]

    @staticmethod
    def insert_employee():
        return """
        INSERT INTO employees (name, role) VALUES (%s, %s)
        """

    @staticmethod
    def insert_project():
        return """
        INSERT INTO projects (name, start_date, end_date) VALUES (%s, %s, %s)
        """

    @staticmethod
    def insert_task():
        return """
        INSERT INTO tasks (name, employee_id, project_id, start_date, end_date, work_days, status) 
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """

    @staticmethod
    def update_task_status():
        return """
        UPDATE tasks SET status = %s, delay_days = %s WHERE id = %s
        """

    @staticmethod
    def fetch_employees():
        return """
        SELECT * FROM employees
        """

    @staticmethod
    def fetch_projects():
        return """
        SELECT * FROM projects
        """

    @staticmethod
    def fetch_tasks_by_project():
        return """
        SELECT tasks.*, employees.name as employee_name 
        FROM tasks 
        LEFT JOIN employees ON tasks.employee_id = employees.id
        WHERE tasks.project_id = %s
        """

    @staticmethod
    def fetch_tasks_by_employee():
        return """
        SELECT tasks.*, projects.name as project_name 
        FROM tasks 
        LEFT JOIN projects ON tasks.project_id = projects.id
        WHERE tasks.employee_id = %s
        """
