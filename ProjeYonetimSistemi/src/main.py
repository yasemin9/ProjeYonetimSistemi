

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from ui.project_window import open_project_window
from ui.employee_window import open_employee_window
from ui.task_window import open_task_window
from ui.main_window import main_window
#from ui.details_window import open_details_window
from database.queries import create_database
 
def main_window():
    # Ana pencereyi oluştur
    root = tk.Tk()
    root.title("Proje Yönetim Uygulaması")
    root.geometry("600x400")

    # Başlık
    ttk.Label(root, text="Proje Yönetim Sistemi", font=("Arial", 18)).pack(pady=20)

    # Butonlar
    ttk.Button(root, text="Proje Yönetimi", command=open_project_window).pack(pady=10)
    ttk.Button(root, text="Çalışan Yönetimi", command=open_employee_window).pack(pady=10)
    ttk.Button(root, text="Görev Yönetimi", command=open_task_window).pack(pady=10)
    #ttk.Button(root, text="Detay Raporları", command=open_details_window).pack(pady=10)

    # Çıkış butonu
    ttk.Button(root, text="Çıkış", command=root.quit).pack(pady=20)

    # Ana pencereyi başlat
    root.mainloop()

if __name__ == "__main__":
    # Veritabanını oluştur
    create_database()

    # Ana pencereyi başlat
    main_window()
