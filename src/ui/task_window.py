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

    # En son bitiş tarihini al
    cursor.execute("SELECT MAX(end_date) FROM tasks WHERE project_id = ?", (project_id,))
    max_end_date = cursor.fetchone()[0]

    if max_end_date:
        max_end_date = datetime.strptime(max_end_date, "%Y-%m-%d").date()
        current_date = datetime.now().date()

        # Gecikme kontrolü
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
            project_data = project_combobox.get().split(" - ")
            employee_data = employee_combobox.get().split(" - ")
            if len(project_data) < 2 or len(employee_data) < 2:
                messagebox.showerror("Hata", "Proje ve Çalışan seçiniz.")
                return

            project_id = project_data[0]
            employee_id = employee_data[0]
            task_name = task_name_entry.get().strip()
            start_date = start_date_entry.get().strip()
            end_date = end_date_entry.get().strip()
            status = status_combobox.get()
            man_days = man_days_entry.get().strip()

            if not (task_name and start_date and end_date and man_days):
                messagebox.showerror("Hata", "Tüm alanları doldurunuz.")
                return

            try:
                man_days = int(man_days)
                datetime.strptime(start_date, "%Y-%m-%d")
                datetime.strptime(end_date, "%Y-%m-%d")
            except ValueError:
                messagebox.showerror("Hata", "Tarih formatı veya adam-gün hatalı.")
                return

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

        # Proje ve çalışanları yükle
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
            SELECT tasks.id, projects.name, employees.name, tasks.name, tasks.start_date, tasks.end_date, tasks.status, tasks.man_days, projects.delay_days
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

    def edit_task():
        selected_item = task_list.selection()
        if not selected_item:
            messagebox.showerror("Hata", "Düzenlenecek bir görev seçin.")
            return

        task_id = task_list.item(selected_item, "values")[0]

        # Seçilen görevin bilgilerini al
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("""
            SELECT project_id, employee_id, name, start_date, end_date, status, man_days 
            FROM tasks WHERE id = ?
        """, (task_id,))
        task = cursor.fetchone()

        if task:
            project_id, employee_id, task_name, start_date, end_date, status, man_days = task

            # Düzenleme penceresini aç
            edit_window = tk.Toplevel(task_window)
            edit_window.title("Görev Düzenle")
            edit_window.geometry("400x450")

            ttk.Label(edit_window, text="Proje:").pack(pady=5)
            project_combobox = ttk.Combobox(edit_window)
            project_combobox.pack(pady=5)

            ttk.Label(edit_window, text="Çalışan:").pack(pady=5)
            employee_combobox = ttk.Combobox(edit_window)
            employee_combobox.pack(pady=5)

            ttk.Label(edit_window, text="Görev Adı:").pack(pady=5)
            task_name_entry = ttk.Entry(edit_window)
            task_name_entry.insert(0, task_name)
            task_name_entry.pack(pady=5)

            ttk.Label(edit_window, text="Başlangıç Tarihi (YYYY-MM-DD):").pack(pady=5)
            start_date_entry = ttk.Entry(edit_window)
            start_date_entry.insert(0, start_date)
            start_date_entry.pack(pady=5)

            ttk.Label(edit_window, text="Bitiş Tarihi (YYYY-MM-DD):").pack(pady=5)
            end_date_entry = ttk.Entry(edit_window)
            end_date_entry.insert(0, end_date)
            end_date_entry.pack(pady=5)

            ttk.Label(edit_window, text="Durum:").pack(pady=5)
            status_combobox = ttk.Combobox(edit_window, values=["Tamamlanacak", "Devam Ediyor", "Tamamlandı"])
            status_combobox.set(status)
            status_combobox.pack(pady=5)

            ttk.Label(edit_window, text="Adam-Gün:").pack(pady=5)
            man_days_entry = ttk.Entry(edit_window)
            man_days_entry.insert(0, str(man_days))
            man_days_entry.pack(pady=5)

            def save_edited_task():
                updated_project_data = project_combobox.get().split(" - ")
                updated_employee_data = employee_combobox.get().split(" - ")

                if len(updated_project_data) < 2 or len(updated_employee_data) < 2:
                    messagebox.showerror("Hata", "Proje ve Çalışan seçiniz.")
                    return

                updated_project_id = updated_project_data[0]
                updated_employee_id = updated_employee_data[0]
                updated_task_name = task_name_entry.get().strip()
                updated_start_date = start_date_entry.get().strip()
                updated_end_date = end_date_entry.get().strip()
                updated_status = status_combobox.get()
                updated_man_days = man_days_entry.get().strip()

                if not (updated_task_name and updated_start_date and updated_end_date and updated_man_days):
                    messagebox.showerror("Hata", "Tüm alanları doldurunuz.")
                    return

                try:
                    updated_man_days = int(updated_man_days)
                    datetime.strptime(updated_start_date, "%Y-%m-%d")
                    datetime.strptime(updated_end_date, "%Y-%m-%d")
                except ValueError:
                    messagebox.showerror("Hata", "Tarih formatı veya adam-gün hatalı.")
                    return

                cursor.execute("""
                    UPDATE tasks
                    SET project_id = ?, employee_id = ?, name = ?, start_date = ?, end_date = ?, status = ?, man_days = ?
                    WHERE id = ?
                """, (updated_project_id, updated_employee_id, updated_task_name, updated_start_date, updated_end_date, updated_status, updated_man_days, task_id))

                connection.commit()
                update_project_end_date_and_delay(updated_project_id)
                connection.close()

                messagebox.showinfo("Başarılı", "Görev başarıyla güncellendi.")
                refresh_task_list()
                edit_window.destroy()

            ttk.Button(edit_window, text="Kaydet", command=save_edited_task).pack(pady=10)

            # Proje ve çalışanları yükle
            connection = get_db_connection()
            cursor = connection.cursor()
            cursor.execute("SELECT id, name FROM projects")
            projects = cursor.fetchall()
            project_combobox["values"] = [f"{proj[0]} - {proj[1]}" for proj in projects]

            cursor.execute("SELECT id, name FROM employees")
            employees = cursor.fetchall()
            employee_combobox["values"] = [f"{emp[0]} - {emp[1]}" for emp in employees]

            connection.close()

    def return_to_main():
        task_window.destroy()

    task_window = tk.Toplevel()
    task_window.title("Görev Yönetimi")
    task_window.geometry("900x600")

    ttk.Button(task_window, text="Görev Ekle", command=add_task_window).pack(pady=10)
    ttk.Button(task_window, text="Sil", command=delete_task).pack(pady=5)
    ttk.Button(task_window, text="Düzenle", command=edit_task).pack(pady=5)
    ttk.Button(task_window, text="Geri Dön", command=return_to_main).pack(pady=5)

    task_list = ttk.Treeview(task_window, columns=("ID", "Proje", "Çalışan", "Görev", "Başlangıç", "Bitiş", "Durum", "Adam-Gün", "Gecikme Gün"), show="headings")
    task_list.heading("ID", text="ID")
    task_list.heading("Proje", text="Proje")
    task_list.heading("Çalışan", text="Çalışan")
    task_list.heading("Görev", text="Görev")
    task_list.heading("Başlangıç", text="Başlangıç Tarihi")
    task_list.heading("Bitiş", text="Bitiş Tarihi")
    task_list.heading("Durum", text="Durum")
    task_list.heading("Adam-Gün", text="Adam-Gün")
    task_list.heading("Gecikme Gün", text="Gecikme Gün")
    task_list.pack(fill=tk.BOTH, expand=True, pady=10)

    refresh_task_list()

