import tkinter as tk
from tkinter import messagebox, simpledialog
from tkinter import ttk  # Modern görünümler için ttk kullanıyoruz
from database.queries import read_employees, create_employee, delete_employee, update_employee

class EmployeeWindow:
    def __init__(self, master):
        # Yeni bir pencere oluşturuyoruz.
        self.master = tk.Toplevel(master)
        self.master.title("Çalışan Yönetimi")
        self.master.geometry("600x400")  # Pencere boyutu
        self.master.configure(bg="#f5f5f5")

        # Başlık
        self.title_label = tk.Label(self.master, text="Çalışan Yönetimi", font=("Arial", 16, "bold"), bg="#f5f5f5", fg="#333")
        self.title_label.pack(pady=10)

        # Ana Çerçeve
        self.main_frame = tk.Frame(self.master, bg="#f5f5f5")
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Çalışan Listesi Çerçevesi
        self.list_frame = tk.Frame(self.main_frame, bg="#ffffff", relief=tk.RIDGE, bd=2)
        self.list_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))

        # Çalışan Listesi
        self.employee_list = tk.Listbox(self.list_frame, font=("Arial", 12), fg="#333", selectbackground="#0078d7", activestyle="none")
        self.employee_list.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Buton Çerçevesi
        self.button_frame = tk.Frame(self.main_frame, bg="#f5f5f5")
        self.button_frame.pack(side=tk.RIGHT, fill=tk.Y)

        # Çalışan Ekleme Alanı
        tk.Label(self.button_frame, text="Çalışan Ekle", font=("Arial", 12, "bold"), bg="#f5f5f5").pack(pady=5)
        tk.Label(self.button_frame, text="Ad:", bg="#f5f5f5").pack(anchor="w", padx=5)
        self.employee_name = ttk.Entry(self.button_frame)
        self.employee_name.pack(fill=tk.X, padx=5)
        
        tk.Label(self.button_frame, text="Pozisyon:", bg="#f5f5f5").pack(anchor="w", padx=5)
        self.employee_position = ttk.Entry(self.button_frame)
        self.employee_position.pack(fill=tk.X, padx=5)

        self.add_button = ttk.Button(self.button_frame, text="Ekle", command=self.add_employee)
        self.add_button.pack(pady=5, padx=5, fill=tk.X)

        # Çalışan Silme Alanı
        tk.Label(self.button_frame, text="Çalışan Sil", font=("Arial", 12, "bold"), bg="#f5f5f5").pack(pady=5)
        tk.Label(self.button_frame, text="ID:", bg="#f5f5f5").pack(anchor="w", padx=5)
        self.employee_id = ttk.Entry(self.button_frame)
        self.employee_id.pack(fill=tk.X, padx=5)

        self.delete_button = ttk.Button(self.button_frame, text="Sil", command=self.delete_employee)
        self.delete_button.pack(pady=5, padx=5, fill=tk.X)

        # Çalışan Düzenleme Alanı
        tk.Label(self.button_frame, text="Çalışan Düzenle", font=("Arial", 12, "bold"), bg="#f5f5f5").pack(pady=5)
        tk.Label(self.button_frame, text="ID:", bg="#f5f5f5").pack(anchor="w", padx=5)
        self.edit_employee_id = ttk.Entry(self.button_frame)
        self.edit_employee_id.pack(fill=tk.X, padx=5)

        tk.Label(self.button_frame, text="Yeni Ad:", bg="#f5f5f5").pack(anchor="w", padx=5)
        self.edit_employee_name = ttk.Entry(self.button_frame)
        self.edit_employee_name.pack(fill=tk.X, padx=5)

        tk.Label(self.button_frame, text="Yeni Pozisyon:", bg="#f5f5f5").pack(anchor="w", padx=5)
        self.edit_employee_position = ttk.Entry(self.button_frame)
        self.edit_employee_position.pack(fill=tk.X, padx=5)

        self.edit_button = ttk.Button(self.button_frame, text="Düzenle", command=self.update_employee)
        self.edit_button.pack(pady=5, padx=5, fill=tk.X)

        # Çalışanları Listele
        self.refresh_employees()

    def refresh_employees(self):
        """Çalışan listesini yenile."""
        self.employee_list.delete(0, tk.END)
        employees = read_employees()
        for employee in employees:
            self.employee_list.insert(tk.END, f"{employee[0]} - {employee[1]} ({employee[2]})")

    def add_employee(self):
        """Yeni bir çalışan ekle."""
        name = self.employee_name.get()
        position = self.employee_position.get()
        if not name or not position:
            messagebox.showerror("Hata", "Ad ve pozisyon alanları boş olamaz.")
            return
        create_employee(name, position)
        messagebox.showinfo("Başarılı", "Çalışan başarıyla eklendi.")
        self.refresh_employees()

    def delete_employee(self):
        """Bir çalışanı sil."""
        emp_id = self.employee_id.get()
        if not emp_id:
            messagebox.showerror("Hata", "Silmek için çalışan ID'si girin.")
            return
        delete_employee(emp_id)
        messagebox.showinfo("Başarılı", "Çalışan başarıyla silindi.")
        self.refresh_employees()

    def update_employee(self):
        """Bir çalışanın bilgilerini düzenle."""
        emp_id = self.edit_employee_id.get()
        new_name = self.edit_employee_name.get()
        new_position = self.edit_employee_position.get()

        if not emp_id or not new_name or not new_position:
            messagebox.showerror("Hata", "Tüm alanları doldurun.")
            return

        update_employee(emp_id, new_name, new_position)
        messagebox.showinfo("Başarılı", "Çalışan başarıyla güncellendi.")
        self.refresh_employees()
