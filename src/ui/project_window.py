import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime
from database.queries import read_projects, create_project, delete_project, update_project

class ProjectWindow(tk.Frame):  # Frame sınıfından türedik
    def __init__(self, master):
        super().__init__(master)  # Frame sınıfından türettiğimiz için super().__init__(master) kullanıyoruz
        self.master = master
        self.master.title("Proje Yönetimi")
        self.master.geometry("1000x700")
        self.master.configure(bg="#f9f9f9")

        # Üst Başlık
        header_frame = tk.Frame(self, bg="#004080", height=60)
        header_frame.pack(fill=tk.X)
        header_label = tk.Label(
            header_frame, text="Proje Yönetimi", font=("Arial", 20, "bold"), bg="#004080", fg="#ffffff"
        )
        header_label.pack(pady=10)

        # Ana Çerçeve
        self.main_frame = tk.Frame(self, bg="#f9f9f9")
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Proje Listesi Çerçevesi
        self.list_frame = tk.Frame(self.main_frame, bg="#ffffff", relief=tk.RIDGE, bd=2)
        self.list_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 20))

        # Proje Listesi
        self.project_list = ttk.Treeview(
            self.list_frame,
            columns=("ID", "Name", "Start Date", "End Date", "Status", "Delay"),
            show="headings",
            height=20,
        )
        self.project_list.heading("ID", text="ID")
        self.project_list.heading("Name", text="Proje Adı")
        self.project_list.heading("Start Date", text="Başlangıç Tarihi")
        self.project_list.heading("End Date", text="Bitiş Tarihi")
        self.project_list.heading("Status", text="Durum")
        self.project_list.heading("Delay", text="Gecikme (gün)")

        for col in ("ID", "Name", "Start Date", "End Date", "Status", "Delay"):
            self.project_list.column(col, anchor=tk.CENTER, stretch=tk.YES, width=120)
        
        self.project_list.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Zebra Efekti
        self.project_list.tag_configure("evenrow", background="#f2f2f2")
        self.project_list.tag_configure("oddrow", background="#ffffff")

        # Sağ Buton Çerçevesi
        self.button_frame = tk.Frame(self.main_frame, bg="#f9f9f9")
        self.button_frame.pack(side=tk.RIGHT, fill=tk.Y)

        # Butonlar
        button_styles = {"font": ("Arial", 12), "width": 20}
        self.add_button = tk.Button(self.button_frame, text="Proje Ekle", command=self.add_project, **button_styles)
        self.add_button.pack(pady=15)

        self.edit_button = tk.Button(self.button_frame, text="Proje Düzenle", command=self.edit_project, **button_styles)
        self.edit_button.pack(pady=15)

        self.delete_button = tk.Button(self.button_frame, text="Proje Sil", command=self.delete_project, **button_styles)
        self.delete_button.pack(pady=15)

        # Alt Bilgi
        self.status_label = tk.Label(
            self,  # self, çünkü artık Frame sınıfından türedi
            text="Hoşgeldiniz! İşlem yapmak için butonları kullanabilirsiniz.",
            font=("Arial", 12),
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
        try:
            projects = read_projects()
            if not projects:
                messagebox.showinfo("Bilgi", "Gösterilecek proje bulunamadı.")
                return

            # Projeleri listeye ekle
            for idx, project in enumerate(projects):
                delay = self.calculate_delay(project["end_date"], project["status"])
                tag = "evenrow" if idx % 2 == 0 else "oddrow"
                self.project_list.insert(
                    "",
                    tk.END,
                    values=(
                        project["id"],
                        project["name"],
                        project["start_date"],
                        project["end_date"],
                        project["status"],
                        delay,
                    ),
                    tags=(tag,),
                )
        except Exception as e:
            messagebox.showerror("Hata", f"Proje verisi alınırken bir hata oluştu: {e}")

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
        try:
            delete_project(int(project_id))
            messagebox.showinfo("Başarılı", "Proje başarıyla silindi!")
            self.refresh_projects()
        except Exception as e:
            messagebox.showerror("Hata", f"Proje silinemedi: {e}")

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
        self.window.geometry("400x400")
        self.window.transient(parent.master)
        self.window.grab_set()

        # Proje Adı
        tk.Label(self.window, text="Proje Adı:", font=("Arial", 12)).pack(pady=10)
        self.name_entry = tk.Entry(self.window, width=40)
        self.name_entry.pack(pady=5)

        # Başlangıç Tarihi
        tk.Label(self.window, text="Başlangıç Tarihi (YYYY-MM-DD):", font=("Arial", 12)).pack(pady=10)
        self.start_date_entry = tk.Entry(self.window, width=40)
        self.start_date_entry.pack(pady=5)

        # Bitiş Tarihi
        tk.Label(self.window, text="Bitiş Tarihi (YYYY-MM-DD):", font=("Arial", 12)).pack(pady=10)
        self.end_date_entry = tk.Entry(self.window, width=40)
        self.end_date_entry.pack(pady=5)

        # Kaydet Butonu
        tk.Button(self.window, text="Kaydet", command=self.save_project, font=("Arial", 12), bg="#004080", fg="white").pack(pady=20)

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
        try:
            create_project(name, start_date, end_date)
            messagebox.showinfo("Başarılı", f"Proje '{name}' başarıyla eklendi.")
            self.parent.refresh_projects()
            self.window.destroy()
        except Exception as e:
            messagebox.showerror("Hata", f"Proje eklenemedi: {e}")

# Test etme
if __name__ == "__main__":
    root = tk.Tk()
    app = ProjectWindow(root)
    root.mainloop()
