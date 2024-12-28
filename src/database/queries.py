import sqlite3

# Veritabanı ve tabloları oluşturma
def create_database(db_name="project_management.db"):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    # Projeler tablosu oluştur
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS projects (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        start_date TEXT NOT NULL,
        end_date TEXT NOT NULL
    )
    """)

    # Çalışanlar tablosu oluştur
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS employees (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        position TEXT NOT NULL
    )
    """)

    # Görevler tablosu oluştur
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        project_id INTEGER NOT NULL,
        employee_id INTEGER NOT NULL,
        name TEXT NOT NULL,
        start_date TEXT NOT NULL,
        end_date TEXT NOT NULL,
        status INTEGER NOT NULL,  -- 0: Tamamlanacak, 1: Devam Ediyor, 2: Tamamlandı
        man_days INTEGER NOT NULL DEFAULT 0,
        FOREIGN KEY (project_id) REFERENCES projects(id),
        FOREIGN KEY (employee_id) REFERENCES employees(id)
    )
    """)

    # Çalışan ile görev ilişkisi tablosu oluştur
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS employee_tasks (
        employee_id INTEGER NOT NULL,
        task_id INTEGER NOT NULL,
        FOREIGN KEY (employee_id) REFERENCES employees(id),
        FOREIGN KEY (task_id) REFERENCES tasks(id)
    )
    """)

    conn.commit()
    conn.close()

# CRUD İşlemleri (Projeler)
def create_project(name, start_date, end_date, db_name="project_management.db"):
    with sqlite3.connect(db_name) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO projects (name, start_date, end_date) VALUES (?, ?, ?)",
            (name, start_date, end_date)
        )

def read_projects(db_name="project_management.db"):
    with sqlite3.connect(db_name) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, start_date, end_date FROM projects")
        return cursor.fetchall()

# CRUD İşlemleri (Çalışanlar)
def create_employee(name, position, db_name="project_management.db"):
    with sqlite3.connect(db_name) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO employees (name, position) VALUES (?, ?)", (name, position)
        )

def read_employees(db_name="project_management.db"):
    with sqlite3.connect(db_name) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, position FROM employees")
        return cursor.fetchall()

# CRUD İşlemleri (Görevler)
def create_task(project_id, employee_id, name, start_date, end_date, status, man_days, db_name="project_management.db"):
    with sqlite3.connect(db_name) as conn:
        cursor = conn.cursor()
        cursor.execute(
            """INSERT INTO tasks (project_id, employee_id, name, start_date, end_date, status, man_days) 
            VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (project_id, employee_id, name, start_date, end_date, status, man_days)
        )
        task_id = cursor.lastrowid

        # Employee-Task ilişkisini ekle
        cursor.execute(
            "INSERT INTO employee_tasks (employee_id, task_id) VALUES (?, ?)",
            (employee_id, task_id)
        )

# Çalışan detaylarını getirme
def get_employee_details(employee_id, db_name="project_management.db"):
    with sqlite3.connect(db_name) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT tasks.id, tasks.name AS task_name, tasks.status, tasks.man_days, projects.name AS project_name
            FROM tasks
            JOIN employee_tasks ON tasks.id = employee_tasks.task_id
            JOIN projects ON tasks.project_id = projects.id
            WHERE employee_tasks.employee_id = ?
        """, (employee_id,))
        return cursor.fetchall()

# Örnek Kullanım:
if __name__ == "__main__":
    create_database()

    # Örnek CRUD işlemleri
    create_project("Proje 1", "2024-01-01", "2024-12-31")
    create_employee("Ahmet Yılmaz", "Yazılım Mühendisi")
    create_task(1, 1, "Görev 1", "2024-01-02", "2024-01-10", 0, 5)

    # Çalışan detaylarını görüntüleme
    employee_details = get_employee_details(1)
    for detail in employee_details:
        print(detail)
