import tkinter as tk
from tkinter import ttk, messagebox
from database.queries import read_tasks, create_task, update_task_status, delete_task

class TaskWindow:
    def __init__(self, master):
        self.window = tk.Toplevel(master)
        self.window.title("Görevler")
        self.window.geometry("800x600")

        # Ana çerçeve
        self.main_frame = ttk.Frame(self.window, padding=10)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Görev Listeleme Bölümü
        ttk.Label(self.main_frame, text="Mevcut Görevler", font=("Arial", 14, "bold")).pack(pady=10)
        self.task_list_frame = ttk.Frame(self.main_frame)
        self.task_list_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        self.list_tasks()

        # Formlar Çerçevesi
        self.form_frame = ttk.Frame(self.main_frame)
        self.form_frame.pack(fill=tk.BOTH, expand=True)

        # Yeni Görev Ekleme Bölümü
        self.create_task_form()

        ttk.Separator(self.form_frame, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=10)

        # Görev Durumu Güncelleme Bölümü
        self.update_task_form()

        ttk.Separator(self.form_frame, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=10)

        # Görev Silme Bölümü
        self.delete_task_form()

    def list_tasks(self):
        """Görevleri listele"""
        for widget in self.task_list_frame.winfo_children():
            widget.destroy()  # Eski listeyi temizle

        tasks = read_tasks()
        if not tasks:
            ttk.Label(self.task_list_frame, text="Henüz görev bulunmamaktadır.", foreground="red").pack()
        else:
            columns = ("ID", "Adı", "Durum", "Başlangıç Tarihi", "Bitiş Tarihi")
            task_table = ttk.Treeview(self.task_list_frame, columns=columns, show="headings")
            for col in columns:
                task_table.heading(col, text=col)
                task_table.column(col, width=120)

            for task in tasks:
                task_table.insert("", tk.END, values=(task[0], task[1], task[3], task[2], task[4]))

            task_table.pack(fill=tk.BOTH, expand=True)

    def create_task_form(self):
        """Yeni görev ekleme formu oluştur"""
        ttk.Label(self.form_frame, text="Yeni Görev Ekle", font=("Arial", 12, "bold")).pack(pady=5)

        form_frame = ttk.Frame(self.form_frame)
        form_frame.pack(pady=5, fill=tk.X)

        ttk.Label(form_frame, text="Görev Adı:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.task_name = ttk.Entry(form_frame, width=30)
        self.task_name.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(form_frame, text="Başlangıç Tarihi (YYYY-MM-DD):").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.start_date = ttk.Entry(form_frame, width=30)
        self.start_date.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(form_frame, text="Bitiş Tarihi (YYYY-MM-DD):").grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
        self.end_date = ttk.Entry(form_frame, width=30)
        self.end_date.grid(row=2, column=1, padx=5, pady=5)

        ttk.Button(form_frame, text="Görev Ekle", command=self.add_task).grid(row=3, column=0, columnspan=2, pady=10)

    def update_task_form(self):
        """Görev durumu güncelleme formu oluştur"""
        ttk.Label(self.form_frame, text="Görev Durumu Güncelle", font=("Arial", 12, "bold")).pack(pady=5)

        form_frame = ttk.Frame(self.form_frame)
        form_frame.pack(pady=5, fill=tk.X)

        ttk.Label(form_frame, text="Görev ID:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.task_id = ttk.Entry(form_frame, width=30)
        self.task_id.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(form_frame, text="Yeni Durum:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.task_status = ttk.Combobox(form_frame, values=["Tamamlanacak", "Devam Ediyor", "Tamamlandı"], state="readonly", width=28)
        self.task_status.grid(row=1, column=1, padx=5, pady=5)
        self.task_status.set("Tamamlanacak")  # Varsayılan durum

        ttk.Button(form_frame, text="Durumu Güncelle", command=self.update_task_status).grid(row=2, column=0, columnspan=2, pady=10)

    def delete_task_form(self):
        """Görev silme formu oluştur"""
        ttk.Label(self.form_frame, text="Görev Sil", font=("Arial", 12, "bold")).pack(pady=5)

        form_frame = ttk.Frame(self.form_frame)
        form_frame.pack(pady=5, fill=tk.X)

        ttk.Label(form_frame, text="Görev ID:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.delete_task_id = ttk.Entry(form_frame, width=30)
        self.delete_task_id.grid(row=0, column=1, padx=5, pady=5)

        ttk.Button(form_frame, text="Görevi Sil", command=self.delete_task).grid(row=1, column=0, columnspan=2, pady=10)

    def add_task(self):
        """Yeni bir görev ekle"""
        name = self.task_name.get()
        start_date = self.start_date.get()
        end_date = self.end_date.get()

        if not name or not start_date or not end_date:
            messagebox.showerror("Hata", "Tüm alanları doldurun!")
            return

        create_task(name, start_date, end_date)
        messagebox.showinfo("Başarılı", "Görev başarıyla eklendi!")
        self.list_tasks()

    def update_task_status(self):
        """Görev durumunu güncelle"""
        task_id = self.task_id.get()
        status = self.task_status.get()

        if not task_id or not status:
            messagebox.showerror("Hata", "Görev ID'si ve yeni durumu doldurun!")
            return

        update_task_status(task_id, status)
        messagebox.showinfo("Başarılı", "Görev durumu başarıyla güncellendi!")
        self.list_tasks()

    def delete_task(self):
        """Bir görevi sil"""
        task_id = self.delete_task_id.get()

        if not task_id:
            messagebox.showerror("Hata", "Silmek için görev ID'si girin!")
            return

        delete_task(task_id)
        messagebox.showinfo("Başarılı", "Görev başarıyla silindi!")
        self.list_tasks()
