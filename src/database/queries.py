import sqlite3

# Veritabanı Bağlantı Fonksiyonu
def get_db_connection(db_name="project_management.db"):
    connection = sqlite3.connect(db_name)
    connection.row_factory = sqlite3.Row  # Kolon isimleriyle veri çekebilmek için
    return connection

# Veritabanı ve Tablo Oluşturma
def create_database(db_name="project_management.db"):
    conn = get_db_connection(db_name)
    cursor = conn.cursor()

    # Projeler Tablosu
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS projects (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        start_date TEXT NOT NULL,
        end_date TEXT NOT NULL,
        status TEXT NOT NULL DEFAULT 'Devam Ediyor',
        delay_days INTEGER NOT NULL DEFAULT 0
    )
    """)

    # Çalışanlar Tablosu
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS employees (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        position TEXT NOT NULL
    )
    """)

    # Görevler Tablosu
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        project_id INTEGER NOT NULL,
        employee_id INTEGER NOT NULL,
        name TEXT NOT NULL,
        start_date TEXT NOT NULL,
        end_date TEXT NOT NULL,
        status TEXT NOT NULL,
        man_days INTEGER NOT NULL DEFAULT 0,
        FOREIGN KEY (project_id) REFERENCES projects(id),
        FOREIGN KEY (employee_id) REFERENCES employees(id)
    )
    """)

    # Çalışan-Görev İlişkisi Tablosu
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

# 'status' Kolonunun Projeler Tablosunda Olduğundan Emin Olma
def ensure_status_column(db_name="project_management.db"):
    conn = get_db_connection(db_name)
    cursor = conn.cursor()

    # 'status' kolonunun olup olmadığını kontrol et
    cursor.execute("PRAGMA table_info(projects);")
    columns = [column[1] for column in cursor.fetchall()]
    if "status" not in columns:
        cursor.execute("ALTER TABLE projects ADD COLUMN status TEXT NOT NULL DEFAULT 'Devam Ediyor';")
        conn.commit()

    conn.close()

# Proje Bitiş Tarihini ve Durumunu Güncelleme
def update_project_end_date_and_delay(project_id, db_name="project_management.db"):
    conn = get_db_connection(db_name)
    cursor = conn.cursor()

    # End_date'i en son görev bitiş tarihine göre güncelle
    cursor.execute("""
        UPDATE projects
        SET end_date = (SELECT MAX(end_date) FROM tasks WHERE project_id = ?),
            status = CASE
                        WHEN EXISTS (SELECT 1 FROM tasks WHERE project_id = ? AND status = 'Delayed')
                        THEN 'Delayed'
                        ELSE 'On Time'
                     END
        WHERE id = ?
    """, (project_id, project_id, project_id))

    conn.commit()
    conn.close()

# Görev CRUD İşlemleri
def create_task(project_id, employee_id, name, start_date, end_date, status, man_days, db_name="project_management.db"):
    conn = get_db_connection(db_name)
    cursor = conn.cursor()
    
    # Görevi tasks tablosuna ekle
    cursor.execute("""
        INSERT INTO tasks (project_id, employee_id, name, start_date, end_date, status, man_days)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (project_id, employee_id, name, start_date, end_date, status, man_days))
    task_id = cursor.lastrowid  # Yeni görev ID'sini al

    # employee_tasks tablosuna görevi ve çalışanı ilişkilendir
    cursor.execute("""
        INSERT INTO employee_tasks (employee_id, task_id)
        VALUES (?, ?)
    """, (employee_id, task_id))

    conn.commit()
    conn.close()
    return task_id

def read_tasks(db_name="project_management.db"):
    conn = get_db_connection(db_name)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT tasks.id, tasks.name AS task_name, tasks.status, tasks.man_days, 
               projects.name AS project_name, employees.name AS employee_name
        FROM tasks
        JOIN projects ON tasks.project_id = projects.id
        JOIN employees ON tasks.employee_id = employees.id
    """)
    tasks = cursor.fetchall()
    conn.close()
    return tasks

def update_task(id, project_id, employee_id, name, start_date, end_date, status, man_days, db_name="project_management.db"):
    conn = get_db_connection(db_name)
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE tasks
        SET project_id = ?, employee_id = ?, name = ?, start_date = ?, end_date = ?, 
            status = ?, man_days = ?
        WHERE id = ?
    """, (project_id, employee_id, name, start_date, end_date, status, man_days, id))
    conn.commit()
    conn.close()

def delete_task(id, db_name="project_management.db"):
    conn = get_db_connection(db_name)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tasks WHERE id = ?", (id,))
    conn.commit()
    conn.close()

# Çalışanları ve Görevleri Görüntüleme
def get_employee_task_details(employee_id, db_name="project_management.db"):
    conn = get_db_connection(db_name)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT tasks.id AS task_id, tasks.name AS task_name, tasks.status AS task_status, 
               projects.name AS project_name, tasks.start_date AS task_start_date, 
               tasks.end_date AS task_end_date
        FROM tasks
        JOIN projects ON tasks.project_id = projects.id
        JOIN employee_tasks ON tasks.id = employee_tasks.task_id
        WHERE employee_tasks.employee_id = ?
    """, (employee_id,))
    employee_tasks = cursor.fetchall()
    conn.close()
    return employee_tasks

# Çalışan Görevlerini Listeleme
def list_employee_tasks(employee_id):
    tasks = get_employee_task_details(employee_id)
    if not tasks:
        print("Bu çalışanın görevi yok.")
        return

    print(f"Çalışan {employee_id}'in Görevleri:")
    for task in tasks:
        print(f"Proje: {task['project_name']}, Görev: {task['task_name']}, Durum: {task['task_status']}, "
              f"Başlangıç: {task['task_start_date']}, Bitiş: {task['task_end_date']}")

# Başlangıçta veritabanı oluşturma
create_database()
ensure_status_column()

# Kullanıcıdan çalışan ID alıp görevlerini listeleyelim
employee_id = 1  # Bu kısmı test etmek için çalışan ID'sini buraya girebilirsiniz
list_employee_tasks(employee_id)
