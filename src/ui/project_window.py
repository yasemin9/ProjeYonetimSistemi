import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

def open_project_window():
    def add_project():
        project_name = project_name_entry.get()
        start_date = start_date_entry.get()
        end_date = end_date_entry.get()

        if not project_name or not start_date or not end_date:
            messagebox.showerror("Hata", "Tüm alanları doldurunuz.")
            return

        connection = sqlite3.connect("project_management.db")
        cursor = connection.cursor()

        cursor.execute("""
            INSERT INTO projects (name, start_date, end_date)
            VALUES (?, ?, ?)
        """, (project_name, start_date, end_date))

        connection.commit()
        connection.close()

        messagebox.showinfo("Başarılı", "Proje eklendi.")
        refresh_project_list()

    def delete_project():
        selected_item = project_list.selection()
        if not selected_item:
            messagebox.showerror("Hata", "Silmek için bir proje seçiniz.")
            return

        project_id = project_list.item(selected_item)["values"][0]
        connection = sqlite3.connect("project_management.db")
        cursor = connection.cursor()

        cursor.execute("DELETE FROM projects WHERE id = ?", (project_id,))
        connection.commit()
        connection.close()

        messagebox.showinfo("Başarılı", "Proje silindi.")
        refresh_project_list()

    def edit_project():
        selected_item = project_list.selection()
        if not selected_item:
            messagebox.showerror("Hata", "Düzenlemek için bir proje seçiniz.")
            return

        project_id = project_list.item(selected_item)["values"][0]
        project_name = project_list.item(selected_item)["values"][1]
        start_date = project_list.item(selected_item)["values"][2]
        end_date = project_list.item(selected_item)["values"][3]

        # Düzenleme penceresini aç
        def save_edited_project():
            new_name = new_project_name_entry.get()
            new_start_date = new_start_date_entry.get()
            new_end_date = new_end_date_entry.get()

            if not new_name or not new_start_date or not new_end_date:
                messagebox.showerror("Hata", "Tüm alanları doldurunuz.")
                return

            connection = sqlite3.connect("project_management.db")
            cursor = connection.cursor()

            cursor.execute("""
                UPDATE projects
                SET name = ?, start_date = ?, end_date = ?
                WHERE id = ?
            """, (new_name, new_start_date, new_end_date, project_id))

            connection.commit()
            connection.close()

            messagebox.showinfo("Başarılı", "Proje güncellendi.")
            refresh_project_list()
            edit_window.destroy()

        edit_window = tk.Toplevel()
        edit_window.title("Proje Düzenle")
        edit_window.geometry("400x300")

        ttk.Label(edit_window, text="Proje Adı:").pack(pady=5)
        new_project_name_entry = ttk.Entry(edit_window)
        new_project_name_entry.insert(0, project_name)
        new_project_name_entry.pack(pady=5)

        ttk.Label(edit_window, text="Başlangıç Tarihi (YYYY-MM-DD):").pack(pady=5)
        new_start_date_entry = ttk.Entry(edit_window)
        new_start_date_entry.insert(0, start_date)
        new_start_date_entry.pack(pady=5)

        ttk.Label(edit_window, text="Bitiş Tarihi (YYYY-MM-DD):").pack(pady=5)
        new_end_date_entry = ttk.Entry(edit_window)
        new_end_date_entry.insert(0, end_date)
        new_end_date_entry.pack(pady=5)

        ttk.Button(edit_window, text="Kaydet", command=save_edited_project).pack(pady=10)

    def refresh_project_list():
        for row in project_list.get_children():
            project_list.delete(row)

        connection = sqlite3.connect("project_management.db")
        cursor = connection.cursor()

        cursor.execute("SELECT id, name, start_date, end_date FROM projects")
        for row in cursor.fetchall():
            project_list.insert("", tk.END, values=row)

        connection.close()

    def show_add_form():
        project_name_label.pack(pady=5)
        project_name_entry.pack(pady=5)
        start_date_label.pack(pady=5)
        start_date_entry.pack(pady=5)
        end_date_label.pack(pady=5)
        end_date_entry.pack(pady=5)
        add_button.pack(pady=10)

    def go_back():
        project_window.destroy()

    project_window = tk.Toplevel()
    project_window.title("Proje Yönetimi")
    project_window.geometry("700x400")

    # Proje Ekleme Formu başlangıçta gizli olacak
    project_name_label = ttk.Label(project_window, text="Proje Adı:")
    project_name_entry = ttk.Entry(project_window)

    start_date_label = ttk.Label(project_window, text="Başlangıç Tarihi (YYYY-MM-DD):")
    start_date_entry = ttk.Entry(project_window)

    end_date_label = ttk.Label(project_window, text="Bitiş Tarihi (YYYY-MM-DD):")
    end_date_entry = ttk.Entry(project_window)

    add_button = ttk.Button(project_window, text="Proje Ekle", command=add_project)

    # Butonları hizalamak için bir Frame ekleyelim
    button_frame = ttk.Frame(project_window)
    button_frame.pack(pady=10)

    # Butonlar düzgün şekilde hizalanıyor
    ttk.Button(button_frame, text="Proje Ekle", command=show_add_form, width=20).pack(side=tk.LEFT, padx=10)
    ttk.Button(button_frame, text="Sil", command=delete_project, width=20).pack(side=tk.LEFT, padx=10)
    ttk.Button(button_frame, text="Düzenle", command=edit_project, width=20).pack(side=tk.LEFT, padx=10)
    ttk.Button(button_frame, text="Geri Dön", command=go_back, width=20).pack(side=tk.LEFT, padx=10)

    # Proje Listesi
    project_list = ttk.Treeview(project_window, columns=("ID", "Proje Adı", "Başlangıç", "Bitiş"), show="headings")
    project_list.heading("ID", text="ID")
    project_list.heading("Proje Adı", text="Proje Adı")
    project_list.heading("Başlangıç", text="Başlangıç Tarihi")
    project_list.heading("Bitiş", text="Bitiş Tarihi")

    project_list.column("ID", width=50, anchor="center")
    project_list.column("Proje Adı", width=200, anchor="center")
    project_list.column("Başlangıç", width=150, anchor="center")
    project_list.column("Bitiş", width=150, anchor="center")

    project_list.pack(fill=tk.BOTH, expand=True, pady=10)

    refresh_project_list()
