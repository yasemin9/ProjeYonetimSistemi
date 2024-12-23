import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime
from database.queries import read_projects, create_project, delete_project, update_project

class ProjectWindow:
    def __init__(self, master):
        self.master = master
        self.master.title("Proje Yönetimi")
        self.master.geometry("900x600")
        self.master.configure(bg="#f9f9f9")

        # Üst Başlık
        header_frame = tk.Frame(self.master, bg="#004080", height=50)
        header_frame.pack(fill=tk.X)
        header_label = tk.Label(
            header_frame, text="Proje Yönetimi", font=("Arial", 18, "bold"), bg="#004080", fg="#ffffff"
        )
        header_label.pack(pady=10)

        # Ana Çerçeve
        self.main_frame = tk.Frame(self.master, bg="#f9f9f9")
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Proje Listesi Çerçevesi
        self.list_frame = tk.Frame(self.main_frame, bg="#ffffff", relief=tk.RIDGE, bd=2)
        self.list_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 20))

        # Proje Listesi
        self.project_list = ttk.Treeview(
            self.list_frame,
            columns=("ID", "Name", "Start Date", "End Date", "Status", "Delay"),
            show="headings",
            height=15,
        )
        self.project_list.heading("ID", text="ID")
        self.project_list.heading("Name", text="Proje Adı")
        self.project_list.heading("Start Date", text="Başlangıç Tarihi")
        self.project_list.heading("End Date", text="Bitiş Tarihi")
        self.project_list.heading("Status", text="Durum")
        self.project_list.heading("Delay", text="Gecikme (gün)")
        for col in ("ID", "Name", "Start Date", "End Date", "Status", "Delay"):
            self.project_list.column(col, anchor=tk.CENTER, stretch=tk.YES)
        self.project_list.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Zebra Efekti
        self.project_list.tag_configure("evenrow", background="#f2f2f2")
        self.project_list.tag_configure("oddrow", background="#ffffff")

        # Sağ Buton Çerçevesi
        self.button_frame = tk.Frame(self.main_frame, bg="#f9f9f9")
        self.button_frame.pack(side=tk.RIGHT, fill=tk.Y)

        # Butonlar
        button_styles = {"font": ("Arial", 12), "width": 15}
        self.add_button = tk.Button(self.button_frame, text="Proje Ekle", command=self.add_project, **button_styles)
        self.add_button.pack(pady=10)

        self.edit_button = tk.Button(self.button_frame, text="Proje Düzenle", command=self.edit_project, **button_styles)
        self.edit_button.pack(pady=10)

        self.delete_button = tk.Button(self.button_frame, text="Proje Sil", command=self.delete_project, **button_styles)
        self.delete_button.pack(pady=10)

        # Alt Bilgi
        self.status_label = tk.Label(
            self.master,
            text="Hoşgeldiniz! Herhangi bir işlem yapmak için butonları kullanabilirsiniz.",
            font=("Arial", 10),
            bg="#f9f9f9",
            fg="#555",
            anchor="w",
        )
        self.status_label.pack(fill=tk.X, padx=20, pady=10)

        # Projeleri yükle
        self.refresh_projects()

    def refresh_projects(self):
        """Proje listesini yenile."""
        for item in self.project_list.get_children():
            self.project_list.delete(item)

        # Veritabanından projeleri al
        projects = read_projects()
        if not projects:
            messagebox.showerror("Hata", "Proje verisi alınamadı!")
            return

        # Projeleri listeye ekle
        for idx, project in enumerate(projects):
            try:
                delay = self.calculate_delay(project["end_date"], project["status"])
                tag = "evenrow" if idx % 2 == 0 else "oddrow"
                self.project_list.insert(
                    "",
                    tk.END,
                    values=(project["id"], project["name"], project["start_date"], project["end_date"], project["status"], delay),
                    tags=(tag,)
                )
            except Exception as e:
                print(f"Error loading project {project}: {e}")

    @staticmethod
    def calculate_delay(end_date_str, status):
        """Gecikmeyi hesapla."""
        end_date = datetime.strptime(end_date_str, "%Y-%m-%d")
        today = datetime.today()
        delay = (today - end_date).days if today > end_date and status != "Tamamlandı" else 0
        return delay

    def add_project(self):
        """Yeni bir proje ekle."""
        AddProjectWindow(self)

    def delete_project(self):
        """Seçili projeyi sil."""
        selected_item = self.project_list.selection()
        if not selected_item:
            messagebox.showerror("Hata", "Silmek için bir proje seçin.")
            return
        project_id = self.project_list.item(selected_item, "values")[0]
        delete_project(int(project_id))
        messagebox.showinfo("Başarılı", "Proje başarıyla silindi!")
        self.refresh_projects()

    def edit_project(self):
        """Seçili projeyi düzenle."""
        selected_item = self.project_list.selection()
        if not selected_item:
            messagebox.showerror("Hata", "Düzenlemek için bir proje seçin.")
            return
        project_id = self.project_list.item(selected_item, "values")[0]
        EditProjectWindow(self, project_id)


class AddProjectWindow:
    def __init__(self, parent):
        self.parent = parent
        self.window = tk.Toplevel(parent.master)
        self.window.title("Proje Ekle")
        self.window.geometry("400x300")
        self.window.transient(parent.master)
        self.window.grab_set()

        # Proje Adı
        tk.Label(self.window, text="Proje Adı:").pack(pady=5)
        self.name_entry = tk.Entry(self.window, width=30)
        self.name_entry.pack(pady=5)

        # Başlangıç Tarihi
        tk.Label(self.window, text="Başlangıç Tarihi (YYYY-MM-DD):").pack(pady=5)
        self.start_date_entry = tk.Entry(self.window, width=30)
        self.start_date_entry.pack(pady=5)

        # Bitiş Tarihi
        tk.Label(self.window, text="Bitiş Tarihi (YYYY-MM-DD):").pack(pady=5)
        self.end_date_entry = tk.Entry(self.window, width=30)
        self.end_date_entry.pack(pady=5)

        # Kaydet Butonu
        tk.Button(self.window, text="Kaydet", command=self.save_project).pack(pady=20)

    def save_project(self):
        """Yeni projeyi kaydet."""
        name = self.name_entry.get()
        start_date = self.start_date_entry.get()
        end_date = self.end_date_entry.get()

        # Tarih doğrulama
        try:
            datetime.strptime(start_date, "%Y-%m-%d")
            datetime.strptime(end_date, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Hata", "Tarih formatı geçersiz! (YYYY-MM-DD)")
            return

        # Veritabanına kaydet
        create_project(name, start_date, end_date)
        messagebox.showinfo("Başarılı", f"Proje '{name}' başarıyla eklendi.")
        self.parent.refresh_projects()
        self.window.destroy()


class EditProjectWindow:
    def __init__(self, parent, project_id):
        self.parent = parent
        self.project_id = project_id
        self.window = tk.Toplevel(parent.master)
        self.window.title("Proje Düzenle")
        self.window.geometry("400x400")
        self.window.transient(parent.master)
        self.window.grab_set()

        # Proje Adı
        tk.Label(self.window, text="Proje Adı:").pack(pady=5)
        self.name_entry = tk.Entry(self.window, width=30)
        self.name_entry.pack(pady=5)

        # Başlangıç Tarihi
        tk.Label(self.window, text="Başlangıç Tarihi (YYYY-MM-DD):").pack(pady=5)
        self.start_date_entry = tk.Entry(self.window, width=30)
        self.start_date_entry.pack(pady=5)

        # Bitiş Tarihi
        tk.Label(self.window, text="Bitiş Tarihi (YYYY-MM-DD):").pack(pady=5)
        self.end_date_entry = tk.Entry(self.window, width=30)
        self.end_date_entry.pack(pady=5)

        # Durum
        tk.Label(self.window, text="Durum:").pack(pady=5)
        self.status_entry = tk.Entry(self.window, width=30)
        self.status_entry.pack(pady=5)

        # Kaydet Butonu
        tk.Button(self.window, text="Kaydet", command=self.save_changes).pack(pady=20)

        # Proje bilgilerini çekip dolduralım
        self.load_project_data()

    def load_project_data(self):
        """Seçilen proje bilgilerini yükle."""
        projects = read_projects()  # Burada projeleri veritabanından alıyoruz
        project = next((p for p in projects if p['id'] == self.project_id), None)
        if project:
            self.name_entry.insert(0, project["name"])
            self.start_date_entry.insert(0, project["start_date"])
            self.end_date_entry.insert(0, project["end_date"])
            self.status_entry.insert(0, project["status"])

    def save_changes(self):
        """Düzenlenen proje bilgisini kaydet."""
        name = self.name_entry.get()
        start_date = self.start_date_entry.get()
        end_date = self.end_date_entry.get()
        status = self.status_entry.get()

        # Tarih doğrulama
        try:
            datetime.strptime(start_date, "%Y-%m-%d")
            datetime.strptime(end_date, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Hata", "Tarih formatı geçersiz! (YYYY-MM-DD)")
            return

        # Veritabanına kaydet
        update_project(self.project_id, name, start_date, end_date, status)
        messagebox.showinfo("Başarılı", f"Proje '{name}' başarıyla güncellendi.")
        self.parent.refresh_projects()
        self.window.destroy()
