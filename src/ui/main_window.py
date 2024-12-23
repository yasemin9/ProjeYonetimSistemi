import tkinter as tk
from tkinter import font

from ui.project_window import ProjectWindow
from ui.employee_window import EmployeeWindow
from ui.task_window import TaskWindow

class MainWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Proje Yönetim Sistemi")
        self.root.geometry("800x500")
        self.root.config(bg="#f4f4f9")  # Arka plan rengini değiştirdik

        # Yazı tipi ve boyut ayarları
        self.title_font = font.Font(family="Helvetica", size=40, weight="bold")
        self.subtitle_font = font.Font(family="Arial", size=12, slant="italic")
        self.menu_font = font.Font(family="Arial", size=12)

        # Başlık
        self.title_label = tk.Label(self.root, text="Proje Yönetim Sistemi", font=self.title_font, bg="#f4f4f9", fg="#2c3e50", relief="solid", bd=1)
        self.title_label.pack(pady=(50, 20))  # Üstten ve alttan boşluk ekledik

        # Alt başlık (slogan)
        self.subtitle_label = tk.Label(self.root, text="Projelerinizi Kolayca Yönetin", font=self.subtitle_font, bg="#f4f4f9", fg="#7f8c8d")
        self.subtitle_label.pack()

        # Menü Çubuğu
        menu_bar = tk.Menu(root, bg="#34495e", fg="white")
        root.config(menu=menu_bar)

        # Projeler Menüsü
        project_menu = tk.Menu(menu_bar, tearoff=0, bg="#34495e", fg="white", font=self.menu_font)
        project_menu.add_command(label="Projeleri Görüntüle", command=self.show_project_screen)
        menu_bar.add_cascade(label="Projeler", menu=project_menu)

        # Çalışanlar Menüsü
        employee_menu = tk.Menu(menu_bar, tearoff=0, bg="#34495e", fg="white", font=self.menu_font)
        employee_menu.add_command(label="Çalışanları Görüntüle", command=self.show_employee_screen)
        menu_bar.add_cascade(label="Çalışanlar", menu=employee_menu)

        # Görevler Menüsü
        task_menu = tk.Menu(menu_bar, tearoff=0, bg="#34495e", fg="white", font=self.menu_font)
        task_menu.add_command(label="Görevleri Görüntüle", command=self.show_task_screen)
        menu_bar.add_cascade(label="Görevler", menu=task_menu)

        # Alt düğme çubuğu (isteğe bağlı)
        self.footer = tk.Label(self.root, text="© 2024 Proje Yönetim Sistemi | Geliştirildi", font=("Arial", 8), bg="#f4f4f9", fg="#7f8c8d")
        self.footer.pack(side="bottom", fill="x", pady=10)

        # Ekranlar (Frame'ler)
        self.project_frame = None
        self.employee_frame = None
        self.task_frame = None

        # Başlangıçta bir ekran yok
        self.current_frame = None

    def show_project_screen(self):
        self.show_screen(self.project_frame, ProjectWindow)

    def show_employee_screen(self):
        self.show_screen(self.employee_frame, EmployeeWindow)

    def show_task_screen(self):
        self.show_screen(self.task_frame, TaskWindow)

    def show_screen(self, frame_variable, frame_class):
        """Ekranı gösterme yardımcı fonksiyonu"""
        # Önce mevcut ekranı gizle
        if self.current_frame is not None:
            self.current_frame.pack_forget()

        # Eğer ekran daha önce oluşturulmadıysa, o zaman oluştur
        if frame_variable is None:
            frame_variable = frame_class(self.root)
        
        # Yeni ekranı göster
        frame_variable.pack(fill="both", expand=True)
        
        # Şu anki ekranı güncelle
        self.current_frame = frame_variable

if __name__ == "__main__":
    root = tk.Tk()
    app = MainWindow(root)
    root.mainloop()
