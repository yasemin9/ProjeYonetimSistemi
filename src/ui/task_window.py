import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime

# Veritabanı bağlantısını yönetmek için bir yardımcı işlev
def get_db_connection():
    return sqlite3.connect("project_management.db")

# Proje bitiş tarihi ve gecikme kontrolü
def update_project_end_date_and_delay(project_id):
    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT MAX(end_date) FROM tasks WHERE project_id = ?", (project_id,))
    max_end_date = cursor.fetchone()[0]

    if max_end_date:
        max_end_date = datetime.strptime(max_end_date, "%Y-%m-%d").date()
        current_date = datetime.now().date()

        if max_end_date < current_date:
            delay_days = (current_date - max_end_date).days
            cursor.execute("""
                UPDATE projects
                SET end_date = ?, status = 'Gecikmeli', delay_days = ?
                WHERE id = ?
            """, (max_end_date, delay_days, project_id))
        else:
            cursor.execute("""
                UPDATE projects
                SET end_date = ?, status = 'Zamanında', delay_days = 0
                WHERE id = ?
            """, (max_end_date, project_id))

    connection.commit()
    connection.close()

# Görev Yönetim Penceresi
def open_task_window():
    def add_task_window():
        def save_task():
            try:
                project_data = project_combobox.get().split(" - ")
                employee_data = employee_combobox.get().split(" - ")

                if len(project_data) < 2 or len(employee_data) < 2:
                    messagebox.showerror("Hata", "Proje ve Çalışan seçiniz.")
                    return

                project_id = int(project_data[0])
                employee_id = int(employee_data[0])
                task_name = task_name_entry.get().strip()
                start_date = start_date_entry.get().strip()
                end_date = end_date_entry.get().strip()
                status = status_combobox.get()
                man_days = int(man_days_entry.get().strip())

                datetime.strptime(start_date, "%Y-%m-%d")
                datetime.strptime(end_date, "%Y-%m-%d")

                connection = get_db_connection()
                cursor = connection.cursor()

                cursor.execute("""
                    INSERT INTO tasks (project_id, employee_id, name, start_date, end_date, status, man_days)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (project_id, employee_id, task_name, start_date, end_date, status, man_days))

                connection.commit()
                update_project_end_date_and_delay(project_id)
                connection.close()

                messagebox.showinfo("Başarılı", "Görev başarıyla eklendi.")
                refresh_task_list()
                add_window.destroy()

            except ValueError:
                messagebox.showerror("Hata", "Lütfen tüm alanları doğru şekilde doldurun.")
            except sqlite3.Error as e:
                messagebox.showerror("Hata", f"Veritabanı hatası: {e}")

        add_window = tk.Toplevel(task_window)
        add_window.title("Görev Ekle")
        add_window.geometry("400x450")

        ttk.Label(add_window, text="Proje:").pack(pady=5)
        project_combobox = ttk.Combobox(add_window)
        project_combobox.pack(pady=5)

        ttk.Label(add_window, text="Çalışan:").pack(pady=5)
        employee_combobox = ttk.Combobox(add_window)
        employee_combobox.pack(pady=5)

        ttk.Label(add_window, text="Görev Adı:").pack(pady=5)
        task_name_entry = ttk.Entry(add_window)
        task_name_entry.pack(pady=5)

        ttk.Label(add_window, text="Başlangıç Tarihi (YYYY-MM-DD):").pack(pady=5)
        start_date_entry = ttk.Entry(add_window)
        start_date_entry.pack(pady=5)

        ttk.Label(add_window, text="Bitiş Tarihi (YYYY-MM-DD):").pack(pady=5)
        end_date_entry = ttk.Entry(add_window)
        end_date_entry.pack(pady=5)

        ttk.Label(add_window, text="Durum:").pack(pady=5)
        status_combobox = ttk.Combobox(add_window, values=["Tamamlanacak", "Devam Ediyor", "Tamamlandı"])
        status_combobox.pack(pady=5)

        ttk.Label(add_window, text="Adam-Gün:").pack(pady=5)
        man_days_entry = ttk.Entry(add_window)
        man_days_entry.pack(pady=5)

        ttk.Button(add_window, text="Kaydet", command=save_task).pack(pady=10)

        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT id, name FROM projects")
        projects = cursor.fetchall()
        project_combobox["values"] = [f"{proj[0]} - {proj[1]}" for proj in projects]

        cursor.execute("SELECT id, name FROM employees")
        employees = cursor.fetchall()
        employee_combobox["values"] = [f"{emp[0]} - {emp[1]}" for emp in employees]

        connection.close()

    def refresh_task_list():
        for row in task_list.get_children():
            task_list.delete(row)

        connection = get_db_connection()
        cursor = connection.cursor()

        cursor.execute("""
            SELECT tasks.id, projects.name, employees.name, tasks.name, tasks.start_date, tasks.end_date, tasks.status, tasks.man_days
            FROM tasks
            JOIN projects ON tasks.project_id = projects.id
            JOIN employees ON tasks.employee_id = employees.id
        """)

        for row in cursor.fetchall():
            task_list.insert("", tk.END, values=row)

        connection.close()

    def delete_task():
        selected_item = task_list.selection()
        if not selected_item:
            messagebox.showerror("Hata", "Silinecek bir görev seçin.")
            return

        task_id = task_list.item(selected_item, "values")[0]
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        connection.commit()
        connection.close()

        messagebox.showinfo("Başarılı", "Görev başarıyla silindi.")
        refresh_task_list()


    def go_back():
        task_window.destroy()
        
    def edit_task():
        selected_item = task_list.selection()
        if not selected_item:
            messagebox.showerror("Hata", "Düzenlenecek bir görev seçin.")
            return

        task_data = task_list.item(selected_item, "values")
        task_id = task_data[0]
        project_name = task_data[1]
        employee_name = task_data[2]
        task_name = task_data[3]
        start_date = task_data[4]
        end_date = task_data[5]
        status = task_data[6]
        man_days = task_data[7]

        def save_changes():
            try:
                project_data = project_combobox.get().split(" - ")
                employee_data = employee_combobox.get().split(" - ")

                if len(project_data) < 2 or len(employee_data) < 2:
                    messagebox.showerror("Hata", "Proje ve Çalışan seçiniz.")
                    return

                project_id = int(project_data[0])
                employee_id = int(employee_data[0])
                updated_task_name = task_name_entry.get().strip()
                updated_start_date = start_date_entry.get().strip()
                updated_end_date = end_date_entry.get().strip()
                updated_status = status_combobox.get()
                updated_man_days = int(man_days_entry.get().strip())

                datetime.strptime(updated_start_date, "%Y-%m-%d")
                datetime.strptime(updated_end_date, "%Y-%m-%d")

                connection = get_db_connection()
                cursor = connection.cursor()

                cursor.execute("""
                    UPDATE tasks
                    SET project_id = ?, employee_id = ?, name = ?, start_date = ?, end_date = ?, status = ?, man_days = ?
                    WHERE id = ?
                """, (project_id, employee_id, updated_task_name, updated_start_date, updated_end_date, updated_status, updated_man_days, task_id))

                connection.commit()
                update_project_end_date_and_delay(project_id)
                connection.close()

                refresh_task_list()
                messagebox.showinfo("Başarılı", "Görev başarıyla güncellendi.")
                edit_window.destroy()

            except ValueError:
                messagebox.showerror("Hata", "Lütfen tüm alanları doğru şekilde doldurun.")
            except sqlite3.Error as e:
                messagebox.showerror("Hata", f"Veritabanı hatası: {e}")

    
           

        edit_window = tk.Toplevel(task_window)
        edit_window.title("Görev Düzenle")
        edit_window.geometry("400x450")

        ttk.Label(edit_window, text="Proje:").pack(pady=5)
        project_combobox = ttk.Combobox(edit_window)
        project_combobox.pack(pady=5)
        project_combobox.set(f"{project_name} - {task_data[1]}")

        ttk.Label(edit_window, text="Çalışan:").pack(pady=5)
        employee_combobox = ttk.Combobox(edit_window)
        employee_combobox.pack(pady=5)
        employee_combobox.set(f"{employee_name} - {task_data[2]}")

        ttk.Label(edit_window, text="Görev Adı:").pack(pady=5)
        task_name_entry = ttk.Entry(edit_window)
        task_name_entry.pack(pady=5)
        task_name_entry.insert(0, task_name)

        ttk.Label(edit_window, text="Başlangıç Tarihi (YYYY-MM-DD):").pack(pady=5)
        start_date_entry = ttk.Entry(edit_window)
        start_date_entry.pack(pady=5)
        start_date_entry.insert(0, start_date)

        ttk.Label(edit_window, text="Bitiş Tarihi (YYYY-MM-DD):").pack(pady=5)
        end_date_entry = ttk.Entry(edit_window)
        end_date_entry.pack(pady=5)
        end_date_entry.insert(0, end_date)

        ttk.Label(edit_window, text="Durum:").pack(pady=5)
        status_combobox = ttk.Combobox(edit_window, values=["Tamamlanacak", "Devam Ediyor", "Tamamlandı"])
        status_combobox.pack(pady=5)
        status_combobox.set(status)

        ttk.Label(edit_window, text="Adam-Gün:").pack(pady=5)
        man_days_entry = ttk.Entry(edit_window)
        man_days_entry.pack(pady=5)
        man_days_entry.insert(0, man_days)

        ttk.Button(edit_window, text="Kaydet", command=save_changes).pack(pady=10)

        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT id, name FROM projects")
        projects = cursor.fetchall()
        project_combobox["values"] = [f"{proj[0]} - {proj[1]}" for proj in projects]

        cursor.execute("SELECT id, name FROM employees")
        employees = cursor.fetchall()
        employee_combobox["values"] = [f"{emp[0]} - {emp[1]}" for emp in employees]

        connection.close()

    task_window = tk.Toplevel()
    task_window.title("Görevler")
    task_window.geometry("1200x600")

    task_list = ttk.Treeview(task_window, columns=("ID", "Proje", "Çalışan", "Görev", "Başlangıç Tarihi", "Bitiş Tarihi", "Durum", "Adam-Gün"), show="headings")
    task_list.pack(fill=tk.BOTH, expand=True)

    task_list.heading("ID", text="ID")
    task_list.heading("Proje", text="Proje")
    task_list.heading("Çalışan", text="Çalışan")
    task_list.heading("Görev", text="Görev")
    task_list.heading("Başlangıç Tarihi", text="Başlangıç Tarihi")
    task_list.heading("Bitiş Tarihi", text="Bitiş Tarihi")
    task_list.heading("Durum", text="Durum")
    task_list.heading("Adam-Gün", text="Adam-Gün")

    task_list.column("ID", width=50, anchor=tk.CENTER)
    task_list.column("Proje", width=150, anchor=tk.CENTER)
    task_list.column("Çalışan", width=150, anchor=tk.CENTER)
    task_list.column("Görev", width=150, anchor=tk.CENTER)
    task_list.column("Başlangıç Tarihi", width=120, anchor=tk.CENTER)
    task_list.column("Bitiş Tarihi", width=120, anchor=tk.CENTER)
    task_list.column("Durum", width=120, anchor=tk.CENTER)
    task_list.column("Adam-Gün", width=100, anchor=tk.CENTER)

    ttk.Button(task_window, text="Yeni Görev Ekle", command=add_task_window).pack(side=tk.LEFT, padx=10)
    ttk.Button(task_window, text="Görev Düzenle", command=edit_task).pack(side=tk.LEFT, padx=10)
    ttk.Button(task_window, text="Görev Sil", command=delete_task).pack(side=tk.LEFT, padx=10)
    ttk.Button(task_window, text="Geri Dön", command=go_back).pack(side=tk.LEFT, padx=10)

    refresh_task_list()
