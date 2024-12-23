import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

class TaskWindow(tk.Toplevel):
    def __init__(self, master, previous_window=None):
        super().__init__(master)

        self.title("Görev Detayları")
        self.geometry("600x400")
        self.resizable(False, False)

        self.previous_window = previous_window  # Reference to the previous window

        self.task_name = tk.StringVar()
        self.assigned_to = tk.StringVar()
        self.start_date = tk.StringVar()
        self.end_date = tk.StringVar()
        self.man_days = tk.IntVar()
        self.status = tk.StringVar(value="Tamamlanacak")
        self.delay_days = tk.IntVar(value=0)

        # Başlık
        header_label = tk.Label(self, text="Görev Detayları", font=("Arial", 20))
        header_label.pack(pady=10)

        # Görev bilgileri çerçevesi
        info_frame = ttk.LabelFrame(self, text="Görev Bilgileri")
        info_frame.pack(fill=tk.BOTH, padx=10, pady=10, expand=True)

        ttk.Label(info_frame, text="Görev Adı:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        ttk.Entry(info_frame, textvariable=self.task_name, width=30).grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(info_frame, text="Atanan Kişi:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        ttk.Entry(info_frame, textvariable=self.assigned_to, width=30).grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(info_frame, text="Başlangıç Tarihi (YYYY-MM-DD):").grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
        ttk.Entry(info_frame, textvariable=self.start_date, width=15).grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(info_frame, text="Bitiş Tarihi (YYYY-MM-DD):").grid(row=3, column=0, padx=5, pady=5, sticky=tk.W)
        ttk.Entry(info_frame, textvariable=self.end_date, width=15).grid(row=3, column=1, padx=5, pady=5)

        ttk.Label(info_frame, text="Adam/Gün:").grid(row=4, column=0, padx=5, pady=5, sticky=tk.W)
        ttk.Entry(info_frame, textvariable=self.man_days, width=10).grid(row=4, column=1, padx=5, pady=5)

        ttk.Label(info_frame, text="Durum:").grid(row=5, column=0, padx=5, pady=5, sticky=tk.W)
        ttk.Combobox(info_frame, textvariable=self.status, values=["Tamamlanacak", "Devam Ediyor", "Tamamlandı"], width=15).grid(row=5, column=1, padx=5, pady=5)

        ttk.Label(info_frame, text="Gecikme Gün Sayısı:").grid(row=6, column=0, padx=5, pady=5, sticky=tk.W)
        ttk.Entry(info_frame, textvariable=self.delay_days, width=10, state="readonly").grid(row=6, column=1, padx=5, pady=5)

        # Kaydet düğmesi
        save_button = ttk.Button(self, text="Görevi Kaydet", command=self.save_task)
        save_button.pack(pady=10)

        # Geri Dön düğmesi
        back_button = ttk.Button(self, text="Geri Dön", command=self.go_back)
        back_button.pack(pady=10)


        ttk.Button(button_frame, text="Geri Dön", command=self.go_back).pack(side=tk.LEFT, padx=5)
        self.saved_task = None

    def save_task(self):
        # Alanların doluluğunu kontrol et
        if not self.task_name.get() or not self.assigned_to.get() or not self.start_date.get() or not self.end_date.get() or not self.man_days.get():
            messagebox.showwarning("Hata", "Lütfen tüm alanları doldurun!")
            return

        # Tarih formatlarını kontrol et
        try:
            start_date = datetime.strptime(self.start_date.get(), "%Y-%m-%d")
            end_date = datetime.strptime(self.end_date.get(), "%Y-%m-%d")
            if start_date > end_date:
                messagebox.showwarning("Hata", "Başlangıç tarihi, bitiş tarihinden sonra olamaz!")
                return
        except ValueError:
            messagebox.showwarning("Hata", "Tarih formatı hatalı! Lütfen YYYY-MM-DD formatında girin.")
            return

        # Gecikme gün sayısını hesapla
        today = datetime.today()
        if end_date < today:
            delay = (today - end_date).days
            self.delay_days.set(delay)
        else:
            self.delay_days.set(0)

        # Görevi kaydet
        self.saved_task = {
            "task_name": self.task_name.get(),
            "assigned_to": self.assigned_to.get(),
            "start_date": self.start_date.get(),
            "end_date": self.end_date.get(),
            "man_days": self.man_days.get(),
            "status": self.status.get(),
            "delay_days": self.delay_days.get()
        }

        messagebox.showinfo("Başarılı", "Görev başarıyla kaydedildi!")
        self.destroy()

    def go_back(self):
        if self.previous_window:
            self.previous_window.deiconify()  # Show the previous window
        self.destroy()  # Close this window


    def go_back(self):
        # Geri gitmek için bu fonksiyonu ekliyoruz
        self.destroy()  # Mevcut pencereyi kapat
        self.master.deiconify()  # Ana pencereyi göster
 


if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()  # Ana pencereyi gizle
    previous_window = tk.Toplevel(root)  # Simulate a previous window
    previous_window.title("Previous Window")
    previous_window.geometry("400x300")

    app = TaskWindow(root, previous_window)  # Pass the previous window to the TaskWindow
    app.mainloop()
