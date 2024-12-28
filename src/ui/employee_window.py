import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

def open_employee_window():
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
        refresh_employee_list()
        hide_employee_form()

    def delete_employee():
        selected_item = employee_list.selection()
        if not selected_item:
            messagebox.showerror("Hata", "Silmek için bir çalışan seçiniz.")
            return

        employee_id = employee_list.item(selected_item)["values"][0]
        connection = sqlite3.connect("project_management.db")
        cursor = connection.cursor()

        cursor.execute("DELETE FROM employees WHERE id = ?", (employee_id,))
        connection.commit()
        connection.close()

        messagebox.showinfo("Başarılı", "Çalışan silindi.")
        refresh_employee_list()

    def edit_employee():
        selected_item = employee_list.selection()
        if not selected_item:
            messagebox.showerror("Hata", "Düzenlemek için bir çalışan seçiniz.")
            return

        employee_id = employee_list.item(selected_item)["values"][0]
        employee_name = employee_list.item(selected_item)["values"][1]
        position = employee_list.item(selected_item)["values"][2]

        def save_edited_employee():
            new_name = new_employee_name_entry.get()
            new_position = new_position_entry.get()

            if not new_name or not new_position:
                messagebox.showerror("Hata", "Tüm alanları doldurunuz.")
                return

            connection = sqlite3.connect("project_management.db")
            cursor = connection.cursor()

            cursor.execute("""
                UPDATE employees
                SET name = ?, position = ?
                WHERE id = ?
            """, (new_name, new_position, employee_id))

            connection.commit()
            connection.close()

            messagebox.showinfo("Başarılı", "Çalışan güncellendi.")
            refresh_employee_list()
            edit_window.destroy()

        edit_window = tk.Toplevel()
        edit_window.title("Çalışan Düzenle")
        edit_window.geometry("400x300")

        ttk.Label(edit_window, text="Çalışan Adı:").pack(pady=5)
        new_employee_name_entry = ttk.Entry(edit_window)
        new_employee_name_entry.insert(0, employee_name)
        new_employee_name_entry.pack(pady=5)

        ttk.Label(edit_window, text="Pozisyon:").pack(pady=5)
        new_position_entry = ttk.Entry(edit_window)
        new_position_entry.insert(0, position)
        new_position_entry.pack(pady=5)

        ttk.Button(edit_window, text="Kaydet", command=save_edited_employee).pack(pady=10)

    def view_employee_details():
        # Seçilen çalışanı al
        selected_item = employee_list.selection()
        if not selected_item:
            messagebox.showerror("Hata", "Detaylarını görmek için bir çalışan seçiniz.")
            return

        # Seçilen çalışanın ID'sini al
        employee_id = employee_list.item(selected_item)["values"][0]
        print(f"Employee ID: {employee_id}")  # Debugging line

        # Veritabanı bağlantısı kur ve görevleri çek
        connection = sqlite3.connect("project_management.db")
        cursor = connection.cursor()

        cursor.execute("""
            SELECT projects.name, tasks.name, tasks.status
            FROM employees
            JOIN employee_tasks ON employees.id = employee_tasks.employee_id
            JOIN tasks ON employee_tasks.task_id = tasks.id
            JOIN projects ON tasks.project_id = projects.id
            WHERE employees.id = ?
        """, (employee_id,))

        tasks = cursor.fetchall()
        connection.close()

        # Eğer çalışan için görev yoksa uyarı ver
        if not tasks:
            messagebox.showinfo("Bilgi", "Bu çalışanın görevi yok.")
            return

        # Detaylar penceresini oluştur
        details_window = tk.Toplevel()
        details_window.title("Çalışan Detayları")
        details_window.geometry("600x400")

        # Başlık etiketi
        ttk.Label(details_window, text="Çalışanın Görev Detayları:").pack(pady=10)

        # Treeview widget'ı oluştur
        details_list = ttk.Treeview(details_window, columns=("Proje", "Görev", "Durum"), show="headings")
        details_list.heading("Proje", text="Proje")
        details_list.heading("Görev", text="Görev")
        details_list.heading("Durum", text="Durum")
        details_list.pack(fill=tk.BOTH, expand=True, pady=10)

        # Veritabanından gelen görevleri Treeview'a ekle
        for task in tasks:
            details_list.insert("", tk.END, values=task)

    def refresh_employee_list():
        for row in employee_list.get_children():
            employee_list.delete(row)

        connection = sqlite3.connect("project_management.db")
        cursor = connection.cursor()

        cursor.execute("SELECT id, name, position FROM employees")
        for row in cursor.fetchall():
            employee_list.insert("", tk.END, values=row)

        connection.close()

    def show_employee_form():
        employee_form_frame.pack(pady=10)
        button_frame.pack_forget()

    def hide_employee_form():
        employee_form_frame.pack_forget()
        button_frame.pack(pady=10)

    def go_back_to_main():
        employee_window.destroy()

    employee_window = tk.Toplevel()
    employee_window.title("Çalışan Yönetimi")
    employee_window.geometry("600x400")

    employee_form_frame = ttk.Frame(employee_window)

    ttk.Label(employee_form_frame, text="Çalışan Adı:").pack(pady=5)
    employee_name_entry = ttk.Entry(employee_form_frame)
    employee_name_entry.pack(pady=5)

    ttk.Label(employee_form_frame, text="Pozisyon:").pack(pady=5)
    position_entry = ttk.Entry(employee_form_frame)
    position_entry.pack(pady=5)

    ttk.Button(employee_form_frame, text="Ekle", command=add_employee, width=20).pack(pady=5)
    employee_form_frame.pack_forget()

    button_frame = ttk.Frame(employee_window)
    button_frame.pack(pady=10)

    ttk.Button(button_frame, text="Çalışan Ekle", command=show_employee_form, width=20).pack(side=tk.LEFT, padx=5)
    ttk.Button(button_frame, text="Sil", command=delete_employee, width=20).pack(side=tk.LEFT, padx=5)
    ttk.Button(button_frame, text="Düzenle", command=edit_employee, width=20).pack(side=tk.LEFT, padx=5)
    ttk.Button(button_frame, text="Detayları Gör", command=view_employee_details, width=20).pack(side=tk.LEFT, padx=5)
    ttk.Button(button_frame, text="Geri Dön", command=go_back_to_main, width=20).pack(side=tk.LEFT, padx=5)

    employee_list = ttk.Treeview(employee_window, columns=("ID", "Ad", "Pozisyon"), show="headings")
    employee_list.heading("ID", text="ID")
    employee_list.heading("Ad", text="Ad")
    employee_list.heading("Pozisyon", text="Pozisyon")
    employee_list.pack(fill=tk.BOTH, expand=True, pady=10)

    refresh_employee_list()

