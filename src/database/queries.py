import mysql.connector
from database.db_connection import connect_to_database

# Common function for executing queries
def execute_query(query, values=None):
    try:
        connection = connect_to_database()
        cursor = connection.cursor()
        cursor.execute(query, values)
        connection.commit()
        cursor.close()
        connection.close()
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False

# Common function for fetching data
def fetch_data(query, values=None):
    try:
        connection = connect_to_database()
        cursor = connection.cursor()
        cursor.execute(query, values)
        results = cursor.fetchall()
        cursor.close()
        connection.close()
        return results
    except Exception as e:
        print(f"Error: {e}")
        return []

# Projects
def create_project(name, start_date, end_date):
    query = "INSERT INTO projects (name, start_date, end_date) VALUES (%s, %s, %s)"
    values = (name, start_date, end_date)
    if execute_query(query, values):
        print(f"Project '{name}' has been successfully created.")

def read_projects():
    query = "SELECT project_id, name, start_date, end_date, status FROM projects"
    results = fetch_data(query)
    projects = [
        {'id': row[0], 'name': row[1], 'start_date': row[2], 'end_date': row[3], 'status': row[4]} 
        for row in results
    ]
    # Projeleri yazdırıyoruz
    for project in projects:
        print(project)
    return projects


def delete_project(project_id):
    query = "DELETE FROM projects WHERE project_id = %s"
    if execute_query(query, (project_id,)):
        print(f"Project ID {project_id} has been successfully deleted.")

def update_project(project_id, new_name, new_start_date=None, new_end_date=None, new_status=None):
    query = "UPDATE projects SET name = %s"
    values = [new_name]
    
    if new_start_date:
        query += ", start_date = %s"
        values.append(new_start_date)
    if new_end_date:
        query += ", end_date = %s"
        values.append(new_end_date)
    if new_status:  # Durum değişikliği ekliyoruz
        query += ", status = %s"
        values.append(new_status)

    query += " WHERE project_id = %s"
    values.append(project_id)

    if execute_query(query, tuple(values)):
        print(f"Project ID {project_id} has been successfully updated.")

# Employees
def create_employee(name, email, phone, position):
    query = "INSERT INTO employees (name, email, phone, position) VALUES (%s, %s, %s, %s)"
    values = (name, email, phone, position)
    if execute_query(query, values):
        print(f"Employee '{name}' has been successfully added.")

def read_employees():
    query = "SELECT * FROM employees"
    results = fetch_data(query)
    return [
        {'id': row[0], 'name': row[1], 'email': row[2], 'phone': row[3], 'position': row[4]} 
        for row in results
    ]

def delete_employee(employee_id):
    query = "DELETE FROM employees WHERE id = %s"
    if execute_query(query, (employee_id,)):
        print(f"Employee ID {employee_id} has been successfully deleted.")

def update_employee(employee_id, new_name, new_email, new_phone, new_position):
    query = "UPDATE employees SET name = %s, email = %s, phone = %s, position = %s WHERE id = %s"
    values = (new_name, new_email, new_phone, new_position, employee_id)
    if execute_query(query, values):
        print(f"Employee ID {employee_id} has been successfully updated.")

# Tasks
def create_task(project_id, name, start_date, end_date, status, assigned_to):
    query = """
    INSERT INTO tasks (project_id, name, start_date, end_date, status, assigned_to) 
    VALUES (%s, %s, %s, %s, %s, %s)
    """
    values = (project_id, name, start_date, end_date, status, assigned_to)
    if execute_query(query, values):
        print(f"Task '{name}' has been successfully created.")

def read_tasks():
    query = "SELECT * FROM tasks"
    results = fetch_data(query)
    return [
        {
            'id': row[0], 'project_id': row[1], 'name': row[2], 'start_date': row[3], 
            'end_date': row[4], 'status': row[5], 'assigned_to': row[6]
        } 
        for row in results
    ]

def delete_task(task_id):
    query = "DELETE FROM tasks WHERE id = %s"
    if execute_query(query, (task_id,)):
        print(f"Task ID {task_id} has been successfully deleted.")

def update_task_status(task_id, new_status):
    query = "UPDATE tasks SET status = %s WHERE id = %s"
    if execute_query(query, (new_status, task_id)):
        print(f"Task ID {task_id} has been successfully updated.")
