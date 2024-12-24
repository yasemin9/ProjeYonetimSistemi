import tkinter as tk
from ui.project_window import ProjectWindow
from ui.task_window import TaskWindow
from ui.employee_window import EmployeeWindow
from database.db_connection import DBConnection
from database.queries import Queries

def initialize_database():
    """Create tables if they do not exist."""
    db = DBConnection()
    db.connect()
    try:
        for query in Queries.create_tables():
            db.execute_query(query)
        print("Database initialized successfully.")
    except Exception as e:
        print(f"Error initializing database: {e}")
    finally:
        db.close()

class MainApplication(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Proje Yönetim Sistemi")
        self.geometry("600x400")
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self, text="Proje Yönetim Sistemi", font=("Arial", 16)).pack(pady=20)

        tk.Button(self, text="Projeler", command=self.open_project_window, width=20).pack(pady=10)
        tk.Button(self, text="Görevler", command=self.open_task_window, width=20).pack(pady=10)
        tk.Button(self, text="Çalışanlar", command=self.open_employee_window, width=20).pack(pady=10)
        tk.Button(self, text="Çıkış", command=self.quit, width=20).pack(pady=20)

    def open_project_window(self):
        self.withdraw()  # Hide the main window
        ProjectWindow(self)  # Open the ProjectWindow

    def open_task_window(self):
        self.withdraw()
        TaskWindow(self)

    def open_employee_window(self):
        self.withdraw()
        EmployeeWindow(self)

if __name__ == "__main__":
    initialize_database()
    app = MainApplication()
    app.mainloop()
