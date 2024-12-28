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

    conn.commit()
    conn.close()

# Veritabanına man_days sütunu eklemek için fonksiyon
def add_man_days_column(db_name="project_management.db"):
    with sqlite3.connect(db_name) as conn:
        cursor = conn.cursor()
        try:
            cursor.execute("ALTER TABLE tasks ADD COLUMN man_days INTEGER NOT NULL DEFAULT 0")
            print("man_days sütunu başarıyla eklendi.")
        except sqlite3.OperationalError:
            print("man_days sütunu zaten mevcut.")

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

def update_project(project_id, name, start_date, end_date, db_name="project_management.db"):
    with sqlite3.connect(db_name) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE projects SET name = ?, start_date = ?, end_date = ? WHERE id = ?",
            (name, start_date, end_date, project_id)
        )

def delete_project(project_id, db_name="project_management.db"):
    with sqlite3.connect(db_name) as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM projects WHERE id = ?", (project_id,))

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

def update_employee(employee_id, name, position, db_name="project_management.db"):
    with sqlite3.connect(db_name) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE employees SET name = ?, position = ? WHERE id = ?",
            (name, position, employee_id)
        )

def delete_employee(employee_id, db_name="project_management.db"):
    with sqlite3.connect(db_name) as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM employees WHERE id = ?", (employee_id,))

# CRUD İşlemleri (Görevler)

def create_task(project_id, employee_id, name, start_date, end_date, status, man_days, db_name="project_management.db"):
    with sqlite3.connect(db_name) as conn:
        cursor = conn.cursor()
        cursor.execute(
            """INSERT INTO tasks (project_id, employee_id, name, start_date, end_date, status, man_days) 
            VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (project_id, employee_id, name, start_date, end_date, status, man_days)
        )

def read_tasks(db_name="project_management.db"):
    with sqlite3.connect(db_name) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT tasks.id, projects.name AS project_name, employees.name AS employee_name, 
                   tasks.name, tasks.start_date, tasks.end_date, 
                   CASE tasks.status 
                       WHEN 0 THEN 'Tamamlanacak' 
                       WHEN 1 THEN 'Devam Ediyor' 
                       WHEN 2 THEN 'Tamamlandı' 
                   END AS status, tasks.man_days
            FROM tasks
            JOIN projects ON tasks.project_id = projects.id
            JOIN employees ON tasks.employee_id = employees.id
        """)
        return cursor.fetchall()

def update_task(task_id, name, start_date, end_date, status, man_days, db_name="project_management.db"):
    with sqlite3.connect(db_name) as conn:
        cursor = conn.cursor()
        cursor.execute(
            """UPDATE tasks 
            SET name = ?, start_date = ?, end_date = ?, status = ?, man_days = ? 
            WHERE id = ?""",
            (name, start_date, end_date, status, man_days, task_id)
        )

def delete_task(task_id, db_name="project_management.db"):
    with sqlite3.connect(db_name) as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))

# Proje Bitiş Tarihinin Güncellenmesi
def update_project_end_date(project_id, db_name="project_management.db"):
    connection = sqlite3.connect(db_name)
    cursor = connection.cursor()

    cursor.execute("""
        SELECT MAX(tasks.end_date)
        FROM tasks
        WHERE tasks.project_id = ? AND tasks.status != 2
    """, (project_id,))
    latest_end_date = cursor.fetchone()[0]

    if latest_end_date:
        cursor.execute("""
            UPDATE projects
            SET end_date = ?
            WHERE id = ?
        """, (latest_end_date, project_id))

    connection.commit()
    connection.close()
