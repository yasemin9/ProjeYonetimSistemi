import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import mysql.connector

# Veritabanı bağlantısı ve tablo oluşturma
conn = mysql.connector.connect(
    host="localhost",
    user="root",  # MySQL kullanıcı adınız
    password="2468",  # MySQL şifreniz
    database="project_management"  # Kullanılacak veritabanı
)
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS tasks (
    id INT AUTO_INCREMENT PRIMARY KEY,
    task_name VARCHAR(255) NOT NULL,
    assigned_to VARCHAR(255) NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    man_days INT NOT NULL,
    status ENUM('Tamamlanacak', 'Devam Ediyor', 'Tamamlandı') NOT NULL,
    delay_days INT DEFAULT 0
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

    def load_tasks(self):
        """Veritabanından görevleri yükler ve ağaç yapısına ekler."""
        self.tree.delete(*self.tree.get_children())
        query = "SELECT * FROM tasks"
        cursor.execute(query)
        rows = cursor.fetchall()

        for row in rows:
            self.tree.insert("", tk.END, values=row)

    def show_task_form(self):
        """Görev ekleme/düzenleme formunu gösterir."""
        self.info_frame.pack(fill=tk.BOTH, padx=10, pady=10)

    def cancel_task_form(self):
        """Görev ekleme/düzenleme formunu gizler."""
        self.info_frame.pack_forget()

    def save_task(self):
        """Görevi veritabanına kaydeder."""
        try:
            task_name = self.task_name.get()
            assigned_to = self.assigned_to.get()
            start_date = datetime.strptime(self.start_date.get(), "%Y-%m-%d").date()
            end_date = datetime.strptime(self.end_date.get(), "%Y-%m-%d").date()
            man_days = self.man_days.get()
            status = self.status.get()

            if not task_name or not assigned_to:
                messagebox.showwarning("Uyarı", "Tüm alanları doldurmalısınız.")
                return

            # Gecikme gün sayısını hesapla
            delay_days = max((datetime.now().date() - end_date).days, 0) if status == "Tamamlandı" else 0

            query = """
                INSERT INTO tasks (task_name, assigned_to, start_date, end_date, man_days, status, delay_days)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, (task_name, assigned_to, start_date, end_date, man_days, status, delay_days))
            conn.commit()

            self.load_tasks()
            messagebox.showinfo("Başarılı", "Görev kaydedildi.")
            self.cancel_task_form()
        except Exception as e:
            messagebox.showerror("Hata", f"Görev kaydedilirken bir hata oluştu: {e}")

    def delete_task(self):
        """Seçili görevi veritabanından siler."""
        try:
            selected_item = self.tree.selection()
            if not selected_item:
                messagebox.showwarning("Uyarı", "Silmek için bir görev seçmelisiniz.")
                return

            task_id = self.tree.item(selected_item)["values"][0]
            query = "DELETE FROM tasks WHERE id = %s"
            cursor.execute(query, (task_id,))
            conn.commit()

            self.load_tasks()
            messagebox.showinfo("Başarılı", "Görev silindi.")
        except Exception as e:
            messagebox.showerror("Hata", f"Görev silinirken bir hata oluştu: {e}")

    def edit_task(self):
        """Seçili görevi düzenlemek için formu doldurur."""
        try:
            selected_item = self.tree.selection()
            if not selected_item:
                messagebox.showwarning("Uyarı", "Düzenlemek için bir görev seçmelisiniz.")
                return

            task_data = self.tree.item(selected_item)["values"]

            self.task_name.set(task_data[1])
            self.assigned_to.set(task_data[2])
            self.start_date.set(task_data[3])
            self.end_date.set(task_data[4])
            self.man_days.set(task_data[5])
            self.status.set(task_data[6])
            self.delay_days.set(task_data[7])

            self.show_task_form()
        except Exception as e:
            messagebox.showerror("Hata", f"Görev düzenlenirken bir hata oluştu: {e}")

    def go_back(self):
        """Bir önceki pencereye geri döner."""
        if self.previous_window:
            self.destroy()
            self.previous_window.deiconify()
        else:
            self.destroy()


# Ana program
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Proje Yönetim Sistemi")
    root.geometry("400x300")

    def open_task_window():
        """Görev penceresini açar."""
        root.withdraw()
        TaskWindow(root)

    ttk.Button(root, text="Görevleri Yönet", command=open_task_window).pack(pady=20)

    root.mainloop()

    # Veritabanı bağlantısını kapat
    conn.close()

