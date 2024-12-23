import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

class ProjectWindow(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)

        self.title("Proje Detayları")
        self.geometry("800x600")
        self.resizable(False, False)

        # Proje bilgileri
        self.project_name = tk.StringVar()
        self.start_date = tk.StringVar()
        self.end_date = tk.StringVar()
        self.tasks = []  # Görevlerin tutulduğu liste

        # Başlık
        header_label = tk.Label(self, text="Proje Detayları", font=("Arial", 20))
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

        # Görev listesi çerçevesi
        task_frame = ttk.LabelFrame(self, text="Görevler")
        task_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.task_tree = ttk.Treeview(task_frame, columns=("Ad", "Başlangıç", "Adam/Gün", "Durum"), show="headings")
        self.task_tree.heading("Ad", text="Görev Adı")
        self.task_tree.heading("Başlangıç", text="Başlangıç Tarihi")
        self.task_tree.heading("Adam/Gün", text="Adam/Gün")
        self.task_tree.heading("Durum", text="Durum")
        self.task_tree.column("Ad", width=200)
        self.task_tree.column("Başlangıç", width=150)
        self.task_tree.column("Adam/Gün", width=100)
        self.task_tree.column("Durum", width=150)
        self.task_tree.pack(fill=tk.BOTH, expand=True, side=tk.LEFT, padx=5, pady=5)

        scrollbar = ttk.Scrollbar(task_frame, orient=tk.VERTICAL, command=self.task_tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.task_tree.config(yscrollcommand=scrollbar.set)

        # Alt düğme çerçevesi
        button_frame = tk.Frame(self)
        button_frame.pack(fill=tk.X, padx=10, pady=10)

        ttk.Button(button_frame, text="Görev Ekle", command=self.add_task).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Görev Sil", command=self.delete_task).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Görevi Güncelle", command=self.update_task).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Kaydet", command=self.save_project).pack(side=tk.RIGHT, padx=5)
        # Back button to go back to the main screen
        ttk.Button(button_frame, text="Geri Dön", command=self.go_back).pack(side=tk.LEFT, padx=5)

    def add_task(self):
        # Görev ekleme penceresi aç
        task_window = TaskWindow(self)
        self.wait_window(task_window)

        # Eğer yeni görev dönerse listeye ekle
        if task_window.new_task:
            self.tasks.append(task_window.new_task)
            self.task_tree.insert("", tk.END, values=(
                task_window.new_task["name"],
                task_window.new_task["start_date"],
                task_window.new_task["man_days"],
                task_window.new_task["status"]
            ))

    def delete_task(self):
        selected_item = self.task_tree.selection()
        if not selected_item:
            messagebox.showwarning("Hata", "Lütfen bir görev seçin!")
            return

        for item in selected_item:
            self.task_tree.delete(item)
            index = self.task_tree.index(item)
            del self.tasks[index]

        messagebox.showinfo("Başarılı", "Seçilen görev(ler) silindi!")

    def update_task(self):
        # Güncelleme işlemleri eklenebilir
        pass

    def save_project(self):
        if not self.project_name.get() or not self.start_date.get() or not self.end_date.get():
            messagebox.showwarning("Hata", "Lütfen tüm proje bilgilerini doldurun!")
            return

        try:
            start_date = datetime.strptime(self.start_date.get(), "%Y-%m-%d")
            end_date = datetime.strptime(self.end_date.get(), "%Y-%m-%d")
            if start_date >= end_date:
                messagebox.showwarning("Hata", "Bitiş tarihi başlangıç tarihinden önce olamaz!")
                return
        except ValueError:
            messagebox.showwarning("Hata", "Tarih formatı hatalı! Lütfen YYYY-MM-DD formatında girin.")
            return

        messagebox.showinfo("Başarılı", f"'{self.project_name.get()}' projesi başarıyla kaydedildi!")

    def go_back(self):
        # Geri gitmek için bu fonksiyonu ekliyoruz
        self.destroy()  # Mevcut pencereyi kapat
        self.master.deiconify()  # Ana pencereyi göster

class TaskWindow(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.new_task = None

        self.title("Görev Ekle")
        self.geometry("400x300")
        self.resizable(False, False)

        self.task_name = tk.StringVar()
        self.start_date = tk.StringVar()
        self.man_days = tk.IntVar()
        self.status = tk.StringVar(value="Tamamlanacak")

        ttk.Label(self, text="Görev Adı:").pack(pady=5)
        ttk.Entry(self, textvariable=self.task_name).pack(pady=5)

        ttk.Label(self, text="Başlangıç Tarihi (YYYY-MM-DD):").pack(pady=5)
        ttk.Entry(self, textvariable=self.start_date).pack(pady=5)

        ttk.Label(self, text="Adam/Gün:").pack(pady=5)
        ttk.Entry(self, textvariable=self.man_days).pack(pady=5)

        ttk.Label(self, text="Durum:").pack(pady=5)
        ttk.Combobox(self, textvariable=self.status, values=["Tamamlanacak", "Devam Ediyor", "Tamamlandı"]).pack(pady=5)

        ttk.Button(self, text="Ekle", command=self.save_task).pack(pady=10)

    def save_task(self):
        if not self.task_name.get() or not self.start_date.get() or not self.man_days.get():
            messagebox.showwarning("Hata", "Lütfen tüm alanları doldurun!")
            return

        try:
            datetime.strptime(self.start_date.get(), "%Y-%m-%d")
        except ValueError:
            messagebox.showwarning("Hata", "Tarih formatı hatalı! Lütfen YYYY-MM-DD formatında girin.")
            return

        self.new_task = {
            "name": self.task_name.get(),
            "start_date": self.start_date.get(),
            "man_days": self.man_days.get(),
            "status": self.status.get()
        }
        self.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()  # Ana pencereyi gizle
    app = ProjectWindow(root)  # 'root' parametresi geçilir
    app.mainloop()
