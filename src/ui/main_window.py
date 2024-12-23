import tkinter as tk
from ui.project_window import ProjectWindow
from ui.employee_window import EmployeeWindow
from ui.task_window import TaskWindow

class MainWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Proje Yönetim Sistemi")
        self.root.geometry("600x400")

        # Menü Çubuğu
        menu_bar = tk.Menu(root)
        root.config(menu=menu_bar)

        # Projeler Menüsü
        project_menu = tk.Menu(menu_bar, tearoff=0)
        project_menu.add_command(label="Projeleri Görüntüle", command=self.open_project_window)
        menu_bar.add_cascade(label="Projeler", menu=project_menu)

        # Çalışanlar Menüsü
        employee_menu = tk.Menu(menu_bar, tearoff=0)
        employee_menu.add_command(label="Çalışanları Görüntüle", command=self.open_employee_window)
        menu_bar.add_cascade(label="Çalışanlar", menu=employee_menu)

        # Görevler Menüsü
        task_menu = tk.Menu(menu_bar, tearoff=0)
        task_menu.add_command(label="Görevleri Görüntüle", command=self.open_task_window)
        menu_bar.add_cascade(label="Görevler", menu=task_menu)

    def open_project_window(self):
        ProjectWindow(self.root)

    def open_employee_window(self):
        EmployeeWindow(self.root)

    def open_task_window(self):
        TaskWindow(self.root)

if __name__ == "__main__":
    root = tk.Tk()
    app = MainWindow(root)
    root.mainloop()
