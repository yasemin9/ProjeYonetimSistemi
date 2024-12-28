import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime

def open_task_window():
    def update_project_end_date_and_delay(project_id):
        connection = sqlite3.connect("project_management.db")
        cursor = connection.cursor()

        # En son bitiş tarihini al
        cursor.execute("""
            SELECT MAX(end_date) FROM tasks WHERE project_id = ?
        """, (project_id,))
        max_end_date = cursor.fetchone()[0]

        # Bitiş tarihi geçti mi kontrol et
        if max_end_date:
            current_date = datetime.now().date()

            # Eğer proje bitiş tarihi geçmişse, gecikmeyi hesapla
            if max_end_date < current_date:
                delay_days = (current_date - datetime.strptime(max_end_date, "%Y-%m-%d").date()).days

                # Gecikmeyi projeye dahil et
                cursor.execute("""
                    UPDATE projects
                    SET end_date = ?, status = 'Devam Ediyor', delay_days = ?
                    WHERE id = ?
                """, (max_end_date, delay_days, project_id))
            else:
                cursor.execute("""
                    UPDATE projects
                    SET end_date = ?, status = 'Tamamlanacak', delay_days = 0
                    WHERE id = ?
                """, (max_end_date, project_id))

            connection.commit()

        connection.close()

    def add_task_window():
        def save_task():
            project_id = project_combobox.get().split(" - ")[0]
            employee_id = employee_combobox.get().split(" - ")[0]
            task_name = task_name_entry.get()
            start_date = start_date_entry.get()
            end_date = end_date_entry.get()
            status = status_combobox.get()
            man_days = int(man_days_entry.get())  # Adam-gün hesaplama

            if not project_id or not employee_id or not task_name or not start_date or not end_date or not man_days:
                messagebox.showerror("Hata", "Tüm alanları doldurunuz.")
                return

            connection = sqlite3.connect("project_management.db")
            cursor = connection.cursor()

            cursor.execute("""
                INSERT INTO tasks (project_id, employee_id, name, start_date, end_date, status, man_days)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (project_id, employee_id, task_name, start_date, end_date, status, man_days))

            connection.commit()

            # Proje bitiş tarihini ve gecikmeyi güncelleme
            update_project_end_date_and_delay(project_id)

            connection.close()

            messagebox.showinfo("Başarılı", "Görev eklendi.")
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

        # Proje ve çalışanları yükleme
        connection = sqlite3.connect("project_management.db")
        cursor = connection.cursor()

        cursor.execute("SELECT id, name FROM projects")
        projects = cursor.fetchall()
        project_combobox["values"] = [f"{proj[0]} - {proj[1]}" for proj in projects]

        cursor.execute("SELECT id, name FROM employees")
        employees = cursor.fetchall()
        employee_combobox["values"] = [f"{emp[0]} - {emp[1]}" for emp in employees]

        connection.close()

    def delete_task():
        selected_item = task_list.selection()
        if not selected_item:
            messagebox.showerror("Hata", "Silmek için bir görev seçin.")
            return

        task_id = task_list.item(selected_item, "values")[0]
        connection = sqlite3.connect("project_management.db")
        cursor = connection.cursor()

        cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        connection.commit()
        connection.close()

        messagebox.showinfo("Başarılı", "Görev silindi.")
        refresh_task_list()

    def edit_task():
        selected_item = task_list.selection()
        if not selected_item:
            messagebox.showerror("Hata", "Düzenlemek için bir görev seçin.")
            return

        task_id = task_list.item(selected_item, "values")[0]

        # Düzenleme için pencere açma
        edit_window = tk.Toplevel(task_window)
        edit_window.title("Görev Düzenle")
        edit_window.geometry("400x450")

        # Mevcut görevi al
        connection = sqlite3.connect("project_management.db")
        cursor = connection.cursor()

        cursor.execute("""
            SELECT project_id, employee_id, name, start_date, end_date, status, man_days
            FROM tasks WHERE id = ?
        """, (task_id,))
        task_data = cursor.fetchone()

        if not task_data:
            messagebox.showerror("Hata", "Görev bulunamadı.")
            return

        connection.close()

        ttk.Label(edit_window, text="Proje:").pack(pady=5)
        project_combobox = ttk.Combobox(edit_window)
        project_combobox.pack(pady=5)

        ttk.Label(edit_window, text="Çalışan:").pack(pady=5)
        employee_combobox = ttk.Combobox(edit_window)
        employee_combobox.pack(pady=5)

        ttk.Label(edit_window, text="Görev Adı:").pack(pady=5)
        task_name_entry = ttk.Entry(edit_window)
        task_name_entry.pack(pady=5)

        ttk.Label(edit_window, text="Başlangıç Tarihi (YYYY-MM-DD):").pack(pady=5)
        start_date_entry = ttk.Entry(edit_window)
        start_date_entry.pack(pady=5)

        ttk.Label(edit_window, text="Bitiş Tarihi (YYYY-MM-DD):").pack(pady=5)
        end_date_entry = ttk.Entry(edit_window)
        end_date_entry.pack(pady=5)

        ttk.Label(edit_window, text="Durum:").pack(pady=5)
        status_combobox = ttk.Combobox(edit_window, values=["Tamamlanacak", "Devam Ediyor", "Tamamlandı"])
        status_combobox.pack(pady=5)

        ttk.Label(edit_window, text="Adam-Gün:").pack(pady=5)
        man_days_entry = ttk.Entry(edit_window)
        man_days_entry.pack(pady=5)

        # Proje ve çalışanları yükle
        connection = sqlite3.connect("project_management.db")
        cursor = connection.cursor()

        cursor.execute("SELECT id, name FROM projects")
        projects = cursor.fetchall()
        project_combobox["values"] = [f"{proj[0]} - {proj[1]}" for proj in projects]

        cursor.execute("SELECT id, name FROM employees")
        employees = cursor.fetchall()
        employee_combobox["values"] = [f"{emp[0]} - {emp[1]}" for emp in employees]

        connection.close()

        # Mevcut verileri giriş alanlarına yerleştirme
        project_combobox.set(f"{task_data[0]}")
        employee_combobox.set(f"{task_data[1]}")
        task_name_entry.insert(0, task_data[2])
        start_date_entry.insert(0, task_data[3])
        end_date_entry.insert(0, task_data[4])
        status_combobox.set(task_data[5])
        man_days_entry.insert(0, task_data[6])

        def save_edited_task():
            new_project_id = project_combobox.get().split(" - ")[0]
            new_employee_id = employee_combobox.get().split(" - ")[0]
            new_task_name = task_name_entry.get()
            new_start_date = start_date_entry.get()
            new_end_date = end_date_entry.get()
            new_status = status_combobox.get()
            new_man_days = int(man_days_entry.get())  # Adam-gün

            if not new_project_id or not new_employee_id or not new_task_name or not new_start_date or not new_end_date or not new_man_days:
                messagebox.showerror("Hata", "Tüm alanları doldurunuz.")
                return

            connection = sqlite3.connect("project_management.db")
            cursor = connection.cursor()

            cursor.execute("""
                UPDATE tasks
                SET project_id = ?, employee_id = ?, name = ?, start_date = ?, end_date = ?, status = ?, man_days = ?
                WHERE id = ?
            """, (new_project_id, new_employee_id, new_task_name, new_start_date, new_end_date, new_status, new_man_days, task_id))

            connection.commit()

            # Proje bitiş tarihini ve gecikmeyi güncelleme
            update_project_end_date_and_delay(new_project_id)

            connection.close()

            messagebox.showinfo("Başarılı", "Görev düzenlendi.")
            refresh_task_list()
            edit_window.destroy()

        ttk.Button(edit_window, text="Kaydet", command=save_edited_task).pack(pady=10)

    def refresh_task_list():
        for row in task_list.get_children():
            task_list.delete(row)

        connection = sqlite3.connect("project_management.db")
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

    def go_back():
        task_window.destroy()

    task_window = tk.Toplevel()
    task_window.title("Görev Yönetimi")
    task_window.geometry("900x600")

    ttk.Button(task_window, text="Görev Ekle", command=add_task_window).pack(pady=10)
    ttk.Button(task_window, text="Görev Düzenle", command=edit_task).pack(pady=5)
    ttk.Button(task_window, text="Görev Sil", command=delete_task).pack(pady=5)
    ttk.Button(task_window, text="Geri Dön", command=go_back).pack(pady=10)

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
