import tkinter as tk
from tkinter import ttk, messagebox
from database.queries import read_employees, create_employee, delete_employee, update_employee, read_employee_tasks

class EmployeeWindow(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.master.title("Yönetim Paneli")
        self.master.geometry("800x600")
        self.master.configure(bg="#f9f9f9")

        self.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        self.tab_control = ttk.Notebook(self)
        self.tab_control.pack(fill=tk.BOTH, expand=True)

        self.employee_tab = ttk.Frame(self.tab_control)
        self.tab_control.add(self.employee_tab, text="Çalışanlar")

        self.setup_employee_tab()

    def setup_employee_tab(self):
        """Çalışanlar sekmesini yapılandır."""
        ttk.Label(self.employee_tab, text="Çalışan Yönetimi", font=("Arial", 16)).pack(pady=10)

        self.employee_frame = ttk.Frame(self.employee_tab)
        self.employee_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.employee_list = ttk.Treeview(
            self.employee_frame,
            columns=("ID", "First Name", "Last Name"),
            show="headings",
            height=15
        )
        self.employee_list.heading("ID", text="ID")
        self.employee_list.heading("First Name", text="Ad")
        self.employee_list.heading("Last Name", text="Soyad")
        self.employee_list.column("ID", width=50, anchor=tk.CENTER)
        self.employee_list.column("First Name", width=150, anchor=tk.CENTER)
        self.employee_list.column("Last Name", width=150, anchor=tk.CENTER)
        self.employee_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))

        self.employee_list.bind("<ButtonRelease-1>", self.display_employee_details)

        self.details_frame = ttk.Frame(self.employee_frame)
        self.details_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        ttk.Label(self.details_frame, text="Çalışan Görev ve Proje Detayları", font=("Arial", 14)).pack(pady=5)
        self.details_text = tk.Text(self.details_frame, height=15, wrap=tk.WORD, state=tk.DISABLED)
        self.details_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.button_frame = ttk.Frame(self.employee_tab)
        self.button_frame.pack(fill=tk.X, pady=10)

        ttk.Button(self.button_frame, text="Çalışan Ekle", command=self.add_employee).pack(side=tk.LEFT, padx=5)
        ttk.Button(self.button_frame, text="Çalışan Sil", command=self.delete_employee).pack(side=tk.LEFT, padx=5)
        ttk.Button(self.button_frame, text="Çalışan Düzenle", command=self.edit_employee).pack(side=tk.LEFT, padx=5)

        self.refresh_employee_list()

    def refresh_employee_list(self):
        """Çalışan listesini yeniler."""
        for item in self.employee_list.get_children():
            self.employee_list.delete(item)

        employees = read_employees()
        for employee in employees:
            self.employee_list.insert("", tk.END, values=(employee[0], employee[1], employee[2]))

    def display_employee_details(self, event):
        """Seçili çalışanın görev ve proje bilgilerini gösterir."""
        selected_item = self.employee_list.selection()
        if not selected_item:
            return

        emp_id = self.employee_list.item(selected_item, "values")[0]
        tasks = read_employee_tasks(emp_id)

        self.details_text.configure(state=tk.NORMAL)
        self.details_text.delete(1.0, tk.END)
        
        if tasks:
            self.details_text.insert(tk.END, "Görevler ve Projeler:\n\n")
            for task in tasks:
                self.details_text.insert(tk.END, f"- {task['project_name']} - {task['task_name']}\n")
        else:
            self.details_text.insert(tk.END, "Bu çalışan için atanmış görev bulunmamaktadır.")

        self.details_text.configure(state=tk.DISABLED)

    def add_employee(self):
        """Yeni bir çalışan ekler."""
        AddEditEmployeeWindow(self, mode="add")

    def delete_employee(self):
        """Seçili çalışanı siler."""
        selected_item = self.employee_list.selection()
        if not selected_item:
            messagebox.showerror("Hata", "Lütfen bir çalışan seçin.")
            return

        emp_id = self.employee_list.item(selected_item, "values")[0]
        delete_employee(emp_id)
        messagebox.showinfo("Başarılı", "Çalışan başarıyla silindi.")
        self.refresh_employee_list()

    def edit_employee(self):
        """Seçili çalışanı düzenler."""
        selected_item = self.employee_list.selection()
        if not selected_item:
            messagebox.showerror("Hata", "Lütfen bir çalışan seçin.")
            return

        emp_id = self.employee_list.item(selected_item, "values")[0]
        AddEditEmployeeWindow(self, mode="edit", emp_id=emp_id)
