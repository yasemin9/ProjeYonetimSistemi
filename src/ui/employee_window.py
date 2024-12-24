import tkinter as tk
from tkinter import ttk, messagebox
from mysql.connector import connect, Error

class EmployeeWindow(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)

        self.title("Çalışan Yönetim Sistemi")
        self.geometry("700x500")
        self.resizable(False, False)

        # Başlık
        header_label = tk.Label(self, text="Çalışan Yönetim Sistemi", font=("Arial", 18))
        header_label.pack(pady=10)

        # Çalışanlar Çerçevesi
        employee_frame = ttk.LabelFrame(self, text="Çalışanlar")
        employee_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.employee_tree = ttk.Treeview(
            employee_frame, columns=("ID", "Ad", "Soyad", "Pozisyon"), show="headings"
        )
        self.employee_tree.heading("ID", text="ID")
        self.employee_tree.heading("Ad", text="Ad")
        self.employee_tree.heading("Soyad", text="Soyad")
        self.employee_tree.heading("Pozisyon", text="Pozisyon")

        self.employee_tree.column("ID", width=50, anchor=tk.CENTER)
        self.employee_tree.column("Ad", width=200)
        self.employee_tree.column("Soyad", width=200)
        self.employee_tree.column("Pozisyon", width=150)

        self.employee_tree.pack(fill=tk.BOTH, expand=True, side=tk.LEFT, padx=5, pady=5)

        scrollbar = ttk.Scrollbar(employee_frame, orient=tk.VERTICAL, command=self.employee_tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.employee_tree.config(yscrollcommand=scrollbar.set)

        # Çalışanları Yükleme
        self.load_employees()

        # Düğme Çerçevesi
        button_frame = tk.Frame(self)
        button_frame.pack(fill=tk.X, padx=10, pady=10)

        ttk.Button(button_frame, text="Çalışan Ekle", command=self.add_employee).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Çalışan Güncelle", command=self.update_employee).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Çalışan Sil", command=self.delete_employee).pack(side=tk.LEFT, padx=5)

    def load_employees(self):
        """Veritabanından çalışanları yükler."""
        for row in self.employee_tree.get_children():
            self.employee_tree.delete(row)

        try:
            connection = connect(
                host="localhost", database="project_management", user="root", password="2468"
            )
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM employees")
            employees = cursor.fetchall()
            for employee in employees:
                self.employee_tree.insert("", tk.END, values=employee)
        except Error as e:
            print(f"Veritabanı Hatası: {e}")
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    def add_employee(self):
        """Yeni bir çalışan eklemek için bir pencere açar."""
        EmployeeForm(self, "Ekle", self.load_employees)

    def update_employee(self):
        """Seçilen çalışanı güncellemek için bir pencere açar."""
        selected = self.employee_tree.selection()
        if not selected:
            messagebox.showwarning("Hata", "Güncellemek için bir çalışan seçin!")
            return

        employee_id = self.employee_tree.item(selected[0], "values")[0]
        EmployeeForm(self, "Güncelle", self.load_employees, employee_id)

    def delete_employee(self):
        """Seçilen çalışanı siler."""
        selected = self.employee_tree.selection()
        if not selected:
            messagebox.showwarning("Hata", "Silmek için bir çalışan seçin!")
            return

        employee_id = self.employee_tree.item(selected[0], "values")[0]

        confirm = messagebox.askyesno("Emin misiniz?", "Çalışanı silmek istediğinizden emin misiniz?")
        if not confirm:
            return

        try:
            connection = connect(
                host="localhost", database="project_management", user="root", password="2468"
            )
            cursor = connection.cursor()
            cursor.execute("DELETE FROM employees WHERE id = %s", (employee_id,))
            connection.commit()
            messagebox.showinfo("Başarılı", "Çalışan başarıyla silindi!")
            self.employee_tree.delete(selected[0])
        except Error as e:
            print(f"Veritabanı Hatası: {e}")
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

class EmployeeForm(tk.Toplevel):
    def __init__(self, master, action, reload_callback, employee_id=None):
        super().__init__(master)

        self.title(f"Çalışan {action}")
        self.geometry("400x300")
        self.resizable(False, False)

        self.reload_callback = reload_callback
        self.employee_id = employee_id

        # Çalışan Bilgileri
        self.first_name = tk.StringVar()
        self.last_name = tk.StringVar()
        self.position = tk.StringVar()

        if employee_id:
            self.load_employee_data()

        tk.Label(self, text=f"Çalışan {action}", font=("Arial", 16)).pack(pady=10)

        form_frame = ttk.Frame(self)
        form_frame.pack(pady=10, padx=20)

        ttk.Label(form_frame, text="Ad:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        ttk.Entry(form_frame, textvariable=self.first_name).grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(form_frame, text="Soyad:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        ttk.Entry(form_frame, textvariable=self.last_name).grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(form_frame, text="Pozisyon:").grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
        ttk.Entry(form_frame, textvariable=self.position).grid(row=2, column=1, padx=5, pady=5)

        ttk.Button(self, text="Kaydet", command=self.save_employee).pack(pady=20)

    def load_employee_data(self):
        """Veritabanından seçili çalışanın bilgilerini yükler."""
        try:
            connection = connect(
                host="localhost", database="project_management", user="root", password="2468"
            )
            cursor = connection.cursor()
            cursor.execute("SELECT first_name, last_name, position FROM employees WHERE id = %s", (self.employee_id,))
            employee = cursor.fetchone()
            if employee:
                self.first_name.set(employee[0])
                self.last_name.set(employee[1])
                self.position.set(employee[2])
        except Error as e:
            print(f"Veritabanı Hatası: {e}")
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    def save_employee(self):
        """Çalışan bilgilerini kaydeder veya günceller."""
        first_name = self.first_name.get()
        last_name = self.last_name.get()
        position = self.position.get()

        if not first_name or not last_name or not position:
            messagebox.showerror("Hata", "Tüm alanlar doldurulmalıdır!")
            return

        try:
            connection = connect(
                host="localhost", database="project_management", user="root", password="2468"
            )
            cursor = connection.cursor()

            # Yeni çalışan ekleme veya var olanı güncelleme
            if self.employee_id:
                query = "UPDATE employees SET first_name = %s, last_name = %s, position = %s WHERE id = %s"
                cursor.execute(query, (first_name, last_name, position, self.employee_id))
            else:
                query = "INSERT INTO employees (first_name, last_name, position) VALUES (%s, %s, %s)"
                cursor.execute(query, (first_name, last_name, position))

            connection.commit()
            messagebox.showinfo("Başarılı", "Çalışan başarıyla kaydedildi!")
            self.destroy()
            self.reload_callback()  # Çalışanlar güncellendikten sonra listeyi yenileyin

        except Error as e:
            print(f"Veritabanı Hatası: {e}")
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()


class EmployeeWindow(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)

        self.title("Çalışan Yönetim Sistemi")
        self.geometry("700x500")
        self.resizable(False, False)

        # Başlık
        header_label = tk.Label(self, text="Çalışan Yönetim Sistemi", font=("Arial", 18))
        header_label.pack(pady=10)

        # Çalışanlar Çerçevesi
        employee_frame = ttk.LabelFrame(self, text="Çalışanlar")
        employee_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.employee_tree = ttk.Treeview(
            employee_frame, columns=("ID", "Ad", "Soyad", "Pozisyon"), show="headings"
        )
        self.employee_tree.heading("ID", text="ID")
        self.employee_tree.heading("Ad", text="Ad")
        self.employee_tree.heading("Soyad", text="Soyad")
        self.employee_tree.heading("Pozisyon", text="Pozisyon")

        self.employee_tree.column("ID", width=50, anchor=tk.CENTER)
        self.employee_tree.column("Ad", width=200)
        self.employee_tree.column("Soyad", width=200)
        self.employee_tree.column("Pozisyon", width=150)

        self.employee_tree.pack(fill=tk.BOTH, expand=True, side=tk.LEFT, padx=5, pady=5)

        scrollbar = ttk.Scrollbar(employee_frame, orient=tk.VERTICAL, command=self.employee_tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.employee_tree.config(yscrollcommand=scrollbar.set)

        # Çalışanları Yükleme
        self.load_employees()

        # Düğme Çerçevesi
        button_frame = tk.Frame(self)
        button_frame.pack(fill=tk.X, padx=10, pady=10)

        ttk.Button(button_frame, text="Çalışan Ekle", command=self.add_employee).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Çalışan Güncelle", command=self.update_employee).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Çalışan Sil", command=self.delete_employee).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Geri Dön", command=self.go_back).pack(side=tk.LEFT, padx=5)

    def load_employees(self):
        """Veritabanından çalışanları yükler."""
        for row in self.employee_tree.get_children():
            self.employee_tree.delete(row)

        try:
            connection = connect(
                host="localhost", database="project_management", user="root", password="2468"
            )
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM employees")
            employees = cursor.fetchall()
            for employee in employees:
                self.employee_tree.insert("", tk.END, values=employee)
        except Error as e:
            print(f"Veritabanı Hatası: {e}")
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    def add_employee(self):
        """Yeni bir çalışan eklemek için bir pencere açar."""
        EmployeeForm(self, "Ekle", self.load_employees)

    def update_employee(self):
        """Seçilen çalışanı güncellemek için bir pencere açar."""
        selected = self.employee_tree.selection()
        if not selected:
            messagebox.showwarning("Hata", "Güncellemek için bir çalışan seçin!")
            return

        employee_id = self.employee_tree.item(selected[0], "values")[0]
        EmployeeForm(self, "Güncelle", self.load_employees, employee_id)

    def delete_employee(self):
        """Seçilen çalışanı siler."""
        selected = self.employee_tree.selection()
        if not selected:
            messagebox.showwarning("Hata", "Silmek için bir çalışan seçin!")
            return

        employee_id = self.employee_tree.item(selected[0], "values")[0]

        confirm = messagebox.askyesno("Emin misiniz?", "Çalışanı silmek istediğinizden emin misiniz?")
        if not confirm:
            return

        try:
            connection = connect(
                host="localhost", database="project_management", user="root", password="2468"
            )
            cursor = connection.cursor()
            cursor.execute("DELETE FROM employees WHERE id = %s", (employee_id,))
            connection.commit()
            messagebox.showinfo("Başarılı", "Çalışan başarıyla silindi!")
            self.employee_tree.delete(selected[0])
        except Error as e:
            print(f"Veritabanı Hatası: {e}")
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
    def go_back(self):
    # Geri gitmek için bu fonksiyonu ekliyoruz
        self.destroy()  # Mevcut pencereyi kapat
        self.master.deiconify()  # Ana pencereyi göster            
