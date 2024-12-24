import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import sqlite3

# Veritabanı bağlantısı ve tablo oluşturma
conn = sqlite3.connect("tasks.db")
cursor = conn.cursor()
cursor.execute('''
CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    task_name TEXT NOT NULL,
    assigned_to TEXT NOT NULL,
    start_date TEXT NOT NULL,
    end_date TEXT NOT NULL,
    man_days INTEGER NOT NULL,
    status TEXT NOT NULL,
    delay_days INTEGER DEFAULT 0
)
''')
conn.commit()

class TaskWindow(tk.Toplevel):
    def __init__(self, master, previous_window=None):
        super().__init__(master)

        self.title("Görev Detayları")
        self.geometry("800x600")
        self.resizable(False, False)

        self.previous_window = previous_window

        # Görev bilgileri için değişkenler
        self.task_name = tk.StringVar()
        self.assigned_to = tk.StringVar()
        self.start_date = tk.StringVar()
        self.end_date = tk.StringVar()
        self.man_days = tk.IntVar()
        self.status = tk.StringVar(value="Tamamlanacak")
        self.delay_days = tk.IntVar(value=0)

        # Başlık etiketi
        header_label = tk.Label(self, text="Görev Detayları", font=("Arial", 20))
        header_label.pack(pady=10)

        # Görev tablosu
        self.tree = ttk.Treeview(self, columns=("ID", "Adı", "Atanan", "Başlangıç", "Bitiş", "Adam/Gün", "Durum", "Gecikme"), show="headings")
        self.tree.pack(fill=tk.BOTH, expand=True, pady=10)

        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)

        # Düğmeler
        button_frame = tk.Frame(self)
        button_frame.pack(pady=10)

        ttk.Button(button_frame, text="Görev Ekle", command=self.show_task_form).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Görev Sil", command=self.delete_task).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Görev Düzenle", command=self.edit_task).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Kaydet", command=self.save_task).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Geri Dön", command=self.go_back).pack(side=tk.LEFT, padx=5)

        self.load_tasks()

        # Görev bilgileri giriş çerçevesi (Başlangıçta gizli)
        self.info_frame = ttk.LabelFrame(self, text="Görev Bilgileri")

        ttk.Label(self.info_frame, text="Görev Adı:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        ttk.Entry(self.info_frame, textvariable=self.task_name, width=30).grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(self.info_frame, text="Atanan Kişi:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        ttk.Entry(self.info_frame, textvariable=self.assigned_to, width=30).grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(self.info_frame, text="Başlangıç Tarihi (YYYY-MM-DD):").grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
        ttk.Entry(self.info_frame, textvariable=self.start_date, width=15).grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(self.info_frame, text="Bitiş Tarihi (YYYY-MM-DD):").grid(row=3, column=0, padx=5, pady=5, sticky=tk.W)
        ttk.Entry(self.info_frame, textvariable=self.end_date, width=15).grid(row=3, column=1, padx=5, pady=5)

        ttk.Label(self.info_frame, text="Adam/Gün:").grid(row=4, column=0, padx=5, pady=5, sticky=tk.W)
        ttk.Entry(self.info_frame, textvariable=self.man_days, width=10).grid(row=4, column=1, padx=5, pady=5)

        ttk.Label(self.info_frame, text="Durum:").grid(row=5, column=0, padx=5, pady=5, sticky=tk.W)
        ttk.Combobox(self.info_frame, textvariable=self.status, values=["Tamamlanacak", "Devam Ediyor", "Tamamlandı"], width=15).grid(row=5, column=1, padx=5, pady=5)

        ttk.Label(self.info_frame, text="Gecikme Gün Sayısı:").grid(row=6, column=0, padx=5, pady=5, sticky=tk.W)
        ttk.Entry(self.info_frame, textvariable=self.delay_days, width=10, state="readonly").grid(row=6, column=1, padx=5, pady=5)

        save_button_frame = tk.Frame(self.info_frame)
        save_button_frame.grid(row=7, columnspan=2, pady=10)

        ttk.Button(save_button_frame, text="Görev Kaydet", command=self.save_task).pack(side=tk.LEFT, padx=5)
        ttk.Button(save_button_frame, text="İptal", command=self.cancel_task_form).pack(side=tk.LEFT, padx=5)

    def show_task_form(self):
        """Görev bilgileri formunu göster"""
        self.info_frame.pack(fill=tk.BOTH, padx=10, pady=10, expand=True)

    def cancel_task_form(self):
        """Görev bilgileri formunu gizle"""
        self.info_frame.pack_forget()

    def load_tasks(self):
        """Görevleri yükle ve tabloyu güncelle"""
        for row in self.tree.get_children():
            self.tree.delete(row)

        cursor.execute("SELECT * FROM tasks")
        for task in cursor.fetchall():
            self.tree.insert("", tk.END, values=task)

    def save_task(self):
        """Yeni görev kaydet"""
        if not self.task_name.get() or not self.assigned_to.get() or not self.start_date.get() or not self.end_date.get() or not self.man_days.get():
            messagebox.showwarning("Hata", "Lütfen tüm alanları doldurun!")
            return

        try:
            start_date = datetime.strptime(self.start_date.get(), "%Y-%m-%d")
            end_date = datetime.strptime(self.end_date.get(), "%Y-%m-%d")
            if start_date > end_date:
                messagebox.showwarning("Hata", "Başlangıç tarihi, bitiş tarihinden sonra olamaz!")
                return
        except ValueError:
            messagebox.showwarning("Hata", "Tarih formatı hatalı! Lütfen YYYY-MM-DD formatında girin.")
            return

        today = datetime.today()
        if end_date < today:
            delay = (today - end_date).days
            self.delay_days.set(delay)
        else:
            self.delay_days.set(0)

        cursor.execute('''
        INSERT INTO tasks (task_name, assigned_to, start_date, end_date, man_days, status, delay_days)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (self.task_name.get(), self.assigned_to.get(), self.start_date.get(), self.end_date.get(), self.man_days.get(), self.status.get(), self.delay_days.get()))
        conn.commit()

        messagebox.showinfo("Başarılı", "Görev başarıyla kaydedildi!")
        self.info_frame.pack_forget()
        self.load_tasks()

    def delete_task(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Hata", "Lütfen silmek için bir görev seçin!")
            return

        task_id = self.tree.item(selected_item, "values")[0]
        confirm = messagebox.askyesno("Onay", "Bu görevi silmek istediğinizden emin misiniz?")
        if confirm:
            cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
            conn.commit()
            self.load_tasks()
            messagebox.showinfo("Başarılı", "Görev başarıyla silindi!")

    def edit_task(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Hata", "Lütfen düzenlemek için bir görev seçin!")
            return

        task_id = self.tree.item(selected_item, "values")[0]
        cursor.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
        task = cursor.fetchone()

        if task:
            self.task_name.set(task[1])
            self.assigned_to.set(task[2])
            self.start_date.set(task[3])
            self.end_date.set(task[4])
            self.man_days.set(task[5])
            self.status.set(task[6])
            self.delay_days.set(task[7])

            self.show_task_form()

    def go_back(self):
        # Geri gitmek için bu fonksiyonu ekliyoruz
        self.destroy()  # Mevcut pencereyi kapat
        self.master.deiconify()  # Ana pencereyi göster

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    TaskWindow(root)
    root.mainloop()
    conn.close()
