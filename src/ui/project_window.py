import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from mysql.connector import Error

# Veritabanı bağlantısı fonksiyonu
def create_connection():
    try:
        connection = mysql.connector.connect(
            host="localhost",  # Veritabanı sunucusunun adresi
            database="project_management",  # Veritabanı adı
            user="root",  # Kullanıcı adı
            password="admin"  # Şifre
        )

        if connection.is_connected():
            print("Veritabanına bağlanıldı!")
            return connection
        else:
            print("Bağlantı sağlanamadı!")
            return None
    except Error as e:
        print(f"Hata: {e}")
        return None

class ProjectWindow(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)

        self.title("Projeleri Yönet")
        self.geometry("800x600")
        self.resizable(False, False)

        # Başlık
        header_label = tk.Label(self, text="Projeleri Yönet", font=("Arial", 20))
        header_label.pack(pady=10)

        # Proje listeleme çerçevesi
        project_frame = ttk.LabelFrame(self, text="Projeler")
        project_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.project_tree = ttk.Treeview(project_frame, columns=("Ad", "Başlangıç Tarihi", "Bitiş Tarihi"), show="headings")
        self.project_tree.heading("Ad", text="Proje Adı")
        self.project_tree.heading("Başlangıç Tarihi", text="Başlangıç Tarihi")
        self.project_tree.heading("Bitiş Tarihi", text="Bitiş Tarihi")
        self.project_tree.column("Ad", width=200)
        self.project_tree.column("Başlangıç Tarihi", width=150)
        self.project_tree.column("Bitiş Tarihi", width=150)
        self.project_tree.pack(fill=tk.BOTH, expand=True, side=tk.LEFT, padx=5, pady=5)

        scrollbar = ttk.Scrollbar(project_frame, orient=tk.VERTICAL, command=self.project_tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.project_tree.config(yscrollcommand=scrollbar.set)

        # Projeleri veritabanından çekme
        self.load_project_data()

        # Alt düğme çerçevesi
        button_frame = tk.Frame(self)
        button_frame.pack(fill=tk.X, padx=10, pady=10)

        ttk.Button(button_frame, text="Proje Ekle", command=self.add_project).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Proje Sil", command=self.delete_project).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Proje Güncelle", command=self.update_project).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Geri Dön", command=self.go_back).pack(side=tk.LEFT, padx=5)

    def load_project_data(self):
        """Projeleri veritabanından yükler."""
        connection = create_connection()
        if connection:
            cursor = connection.cursor()
            try:
                cursor.execute("SELECT * FROM projects")
                projects = cursor.fetchall()
                for project in projects:
                    self.project_tree.insert("", tk.END, values=(project[1], project[2], project[3]))

            except Error as e:
                print(f"Veritabanı hatası: {e}")
            finally:
                cursor.close()
                connection.close()

    def add_project(self):
        project_window = ProjectEditWindow(self)
        self.wait_window(project_window)

        if project_window.new_project:
            # Yeni projeyi veritabanına kaydetme
            connection = create_connection()
            if connection:
                cursor = connection.cursor()
                try:
                    query = """INSERT INTO projects (name, start_date, end_date) 
                               VALUES (%s, %s, %s)"""
                    cursor.execute(query, (
                        project_window.new_project["name"],
                        project_window.new_project["start_date"],
                        project_window.new_project["end_date"]
                    ))
                    connection.commit()
                    messagebox.showinfo("Başarılı", "Proje başarıyla eklendi!")
                    self.project_tree.insert("", tk.END, values=(
                        project_window.new_project["name"],
                        project_window.new_project["start_date"],
                        project_window.new_project["end_date"]
                    ))
                except Error as e:
                    print(f"Veritabanı hatası: {e}")
                    messagebox.showerror("Hata", "Proje eklenemedi.")
                finally:
                    cursor.close()
                    connection.close()

    def delete_project(self):
        selected_item = self.project_tree.selection()
        if not selected_item:
            messagebox.showwarning("Hata", "Lütfen bir proje seçin!")
            return

        for item in selected_item:
            project_name = self.project_tree.item(item, "values")[0]

            # Veritabanından projeyi silme
            connection = create_connection()
            if connection:
                cursor = connection.cursor()
                try:
                    query = """DELETE FROM projects WHERE name = %s"""
                    cursor.execute(query, (project_name,))
                    connection.commit()
                    messagebox.showinfo("Başarılı", "Proje başarıyla silindi!")
                except Error as e:
                    print(f"Veritabanı hatası: {e}")
                    messagebox.showerror("Hata", "Proje silinemedi.")
                finally:
                    cursor.close()
                    connection.close()

            # Listeyi güncelle
            self.project_tree.delete(item)

    def update_project(self):
        selected_item = self.project_tree.selection()
        if not selected_item:
            messagebox.showwarning("Hata", "Lütfen bir proje seçin!")
            return

        # Proje güncelleme penceresini aç
        project_name = self.project_tree.item(selected_item[0], "values")[0]
        project_window = ProjectEditWindow(self, project_name)
        self.wait_window(project_window)

        if project_window.new_project:
            # Veritabanında projeyi güncelleme
            connection = create_connection()
            if connection:
                cursor = connection.cursor()
                try:
                    query = """UPDATE projects 
                               SET name = %s, start_date = %s, end_date = %s 
                               WHERE name = %s"""
                    cursor.execute(query, (
                        project_window.new_project["name"],
                        project_window.new_project["start_date"],
                        project_window.new_project["end_date"],
                        project_name
                    ))
                    connection.commit()
                    messagebox.showinfo("Başarılı", "Proje başarıyla güncellendi!")
                except Error as e:
                    print(f"Veritabanı hatası: {e}")
                    messagebox.showerror("Hata", "Proje güncellenemedi.")
                finally:
                    cursor.close()
                    connection.close()

            # Görünümü güncelle
            self.project_tree.item(selected_item[0], values=(
                project_window.new_project["name"],
                project_window.new_project["start_date"],
                project_window.new_project["end_date"]
            ))

    def go_back(self):
        self.destroy()

class ProjectEditWindow(tk.Toplevel):
    def __init__(self, master, project_name=None):
        super().__init__(master)
        self.title("Proje Ekle/Düzenle")
        self.geometry("400x400")

        self.new_project = None

        # Proje adı
        self.project_name = tk.StringVar(value=project_name if project_name else "")
        self.start_date = tk.StringVar()
        self.end_date = tk.StringVar()

        # Başlık
        header_label = tk.Label(self, text="Proje Detayları", font=("Arial", 16))
        header_label.pack(pady=10)

        # Proje bilgileri çerçevesi
        info_frame = ttk.LabelFrame(self, text="Proje Bilgileri")
        info_frame.pack(fill=tk.X, padx=10, pady=10)

        ttk.Label(info_frame, text="Proje Adı:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        ttk.Entry(info_frame, textvariable=self.project_name, width=30).grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(info_frame, text="Başlangıç Tarihi (YYYY-MM-DD):").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        ttk.Entry(info_frame, textvariable=self.start_date, width=15).grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(info_frame, text="Bitiş Tarihi (YYYY-MM-DD):").grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
        ttk.Entry(info_frame, textvariable=self.end_date, width=15).grid(row=2, column=1, padx=5, pady=5)

        # Ekleme ve Güncelleme butonu
        button_frame = tk.Frame(self)
        button_frame.pack(pady=10)

        ttk.Button(button_frame, text="Kaydet", command=self.save_project).pack(padx=5)

    def save_project(self):
        self.new_project = {
            "name": self.project_name.get(),
            "start_date": self.start_date.get(),
            "end_date": self.end_date.get()
        }
        self.destroy()
