import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

def main_window():
    def open_project_window():
        project_window = tk.Toplevel(root)
        project_window.title("Proje Yönetimi")
        project_window.geometry("400x300")

        ttk.Label(project_window, text="Proje Adı:").pack(pady=5)
        project_name_entry = ttk.Entry(project_window)
        project_name_entry.pack(pady=5)

        ttk.Label(project_window, text="Başlangıç Tarihi (YYYY-MM-DD):").pack(pady=5)
        start_date_entry = ttk.Entry(project_window)
        start_date_entry.pack(pady=5)

        ttk.Label(project_window, text="Bitiş Tarihi (YYYY-MM-DD):").pack(pady=5)
        end_date_entry = ttk.Entry(project_window)
        end_date_entry.pack(pady=5)

        def add_project():
            name = project_name_entry.get()
            start_date = start_date_entry.get()
            end_date = end_date_entry.get()

            if not name or not start_date or not end_date:
                messagebox.showerror("Hata", "Tüm alanları doldurunuz.")
                return

            connection = sqlite3.connect("project_management.db")
            cursor = connection.cursor()

            cursor.execute("INSERT INTO projects (name, start_date, end_date) VALUES (?, ?, ?)",
                           (name, start_date, end_date))

            connection.commit()
            connection.close()

            messagebox.showinfo("Başarılı", "Proje eklendi.")
            project_window.destroy()

        ttk.Button(project_window, text="Proje Ekle", command=add_project).pack(pady=20)

    def open_employee_window():
        employee_window = tk.Toplevel(root)
        employee_window.title("Çalışan Yönetimi")
        employee_window.geometry("400x300")

        ttk.Label(employee_window, text="Çalışan Adı:").pack(pady=5)
        employee_name_entry = ttk.Entry(employee_window)
        employee_name_entry.pack(pady=5)

        ttk.Label(employee_window, text="Pozisyon:").pack(pady=5)
        position_entry = ttk.Entry(employee_window)
        position_entry.pack(pady=5)

        def add_employee():
            name = employee_name_entry.get()
            position = position_entry.get()

            if not name or not position:
                messagebox.showerror("Hata", "Tüm alanları doldurunuz.")
                return

            connection = sqlite3.connect("project_management.db")
            cursor = connection.cursor()

            cursor.execute("INSERT INTO employees (name, position) VALUES (?, ?)", (name, position))

            connection.commit()
            connection.close()

            messagebox.showinfo("Başarılı", "Çalışan eklendi.")
            employee_window.destroy()

        ttk.Button(employee_window, text="Çalışan Ekle", command=add_employee).pack(pady=20)

    root = tk.Tk()
    root.title("Proje Yönetim Uygulaması")
    root.geometry("500x400")

    ttk.Label(root, text="Proje Yönetim Sistemi", font=("Arial", 16)).pack(pady=20)

    ttk.Button(root, text="Proje Yönetimi", command=open_project_window).pack(pady=10)
    ttk.Button(root, text="Çalışan Yönetimi", command=open_employee_window).pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    main_window()
