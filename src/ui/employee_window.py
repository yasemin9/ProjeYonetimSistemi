import tkinter as tk
from tkinter import ttk, messagebox

class EmployeeWindow(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)

        self.title("Çalışan Yönetimi")
        self.geometry("800x600")
        self.resizable(False, False)

        self.employee_name = tk.StringVar()
        self.employee_role = tk.StringVar()
        self.project_tasks = []
        self.completed_tasks = 0
        self.incomplete_tasks = 0

        # Başlık
        header_label = tk.Label(self, text="Çalışan Yönetimi", font=("Arial", 20))
        header_label.pack(pady=10)

        # Çalışan Bilgileri Çerçevesi
        info_frame = ttk.LabelFrame(self, text="Çalışan Bilgileri")
        info_frame.pack(fill=tk.BOTH, padx=10, pady=10, expand=True)

        ttk.Label(info_frame, text="Ad Soyad:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        ttk.Entry(info_frame, textvariable=self.employee_name, width=30).grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(info_frame, text="Görev:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        ttk.Entry(info_frame, textvariable=self.employee_role, width=30).grid(row=1, column=1, padx=5, pady=5)

        # Görev Yönetimi
        task_frame = ttk.LabelFrame(self, text="Çalışanın Görevleri")
        task_frame.pack(fill=tk.BOTH, padx=10, pady=10, expand=True)

        self.task_listbox = tk.Listbox(task_frame, height=10, width=50)
        self.task_listbox.pack(side=tk.LEFT, padx=5, pady=5, fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(task_frame, orient=tk.VERTICAL, command=self.task_listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.task_listbox.config(yscrollcommand=scrollbar.set)

        # Görevleri Yükle
        self.load_tasks_button = ttk.Button(task_frame, text="Görevleri Yükle", command=self.load_tasks)
        self.load_tasks_button.pack(pady=5)

        # Çalışan Performansı
        performance_frame = ttk.LabelFrame(self, text="Performans Bilgileri")
        performance_frame.pack(fill=tk.BOTH, padx=10, pady=10, expand=True)

        ttk.Label(performance_frame, text="Tamamlanan Görevler:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.completed_label = ttk.Label(performance_frame, text=f"{self.completed_tasks}")
        self.completed_label.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)

        ttk.Label(performance_frame, text="Tamamlanmayan Görevler:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.incomplete_label = ttk.Label(performance_frame, text=f"{self.incomplete_tasks}")
        self.incomplete_label.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)

        # Kaydet Butonu
        save_button = ttk.Button(self, text="Çalışanı Kaydet", command=self.save_employee)
        save_button.pack(pady=10)

     # Geri Dön düğmesi
        back_button = ttk.Button(self, text="Geri Dön", command=self.go_back)
        back_button.pack(pady=10)
        ttk.Button(button_frame, text="Geri Dön", command=self.go_back).pack(side=tk.LEFT, padx=5)
        
        self.saved_employee = None

    def load_tasks(self):
        # Çalışanın görevlerini listeye yükle
        self.project_tasks = [
            {"name": "Görev 1", "status": "Tamamlandı"},
            {"name": "Görev 2", "status": "Devam Ediyor"},
            {"name": "Görev 3", "status": "Tamamlanacak"},
        ]
        
        self.task_listbox.delete(0, tk.END)
        self.completed_tasks = 0
        self.incomplete_tasks = 0

        for task in self.project_tasks:
            self.task_listbox.insert(tk.END, f"{task['name']} - {task['status']}")
            if task['status'] == "Tamamlandı":
                self.completed_tasks += 1
            else:
                self.incomplete_tasks += 1

        self.completed_label.config(text=f"{self.completed_tasks}")
        self.incomplete_label.config(text=f"{self.incomplete_tasks}")

    def save_employee(self):
        if not self.employee_name.get() or not self.employee_role.get():
            messagebox.showwarning("Hata", "Lütfen tüm alanları doldurun!")
            return

        self.saved_employee = {
            "name": self.employee_name.get(),
            "role": self.employee_role.get(),
            "tasks": self.project_tasks,
            "completed_tasks": self.completed_tasks,
            "incomplete_tasks": self.incomplete_tasks
        }

        messagebox.showinfo("Başarılı", "Çalışan başarıyla kaydedildi!")
        self.destroy()



    def go_back(self):
        # Geri gitmek için bu fonksiyonu ekliyoruz
        self.destroy()  # Mevcut pencereyi kapat
        self.master.deiconify()  # Ana pencereyi göster


if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()  # Ana pencereyi gizle
    app = EmployeeWindow(root)  # Burada root'u 'master' olarak geçiyoruz
    app.mainloop()
