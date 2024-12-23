import tkinter as tk
from tkinter import ttk, messagebox

class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()

        # Ana pencere ayarları
        self.title("Proje Yönetim Sistemi")
        self.geometry("800x600")
        self.resizable(False, False)

        # Başlık kısmı
        header_label = tk.Label(self, text="Proje Yönetim Sistemi", font=("Arial", 24), bg="blue", fg="white")
        header_label.pack(fill=tk.X)

        # Proje listesi çerçevesi
        self.project_frame = ttk.LabelFrame(self, text="Projeler")
        self.project_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.project_listbox = tk.Listbox(self.project_frame, height=15, font=("Arial", 12))
        self.project_listbox.pack(fill=tk.BOTH, expand=True, side=tk.LEFT, padx=5, pady=5)

        scrollbar = tk.Scrollbar(self.project_frame, orient=tk.VERTICAL, command=self.project_listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.project_listbox.config(yscrollcommand=scrollbar.set)

        # Alt kısımda düğmeler
        button_frame = tk.Frame(self)
        button_frame.pack(fill=tk.X, padx=10, pady=10)

        add_project_btn = ttk.Button(button_frame, text="Yeni Proje Ekle", command=self.add_project)
        add_project_btn.pack(side=tk.LEFT, padx=5)

        view_project_btn = ttk.Button(button_frame, text="Projeyi Görüntüle", command=self.view_project)
        view_project_btn.pack(side=tk.LEFT, padx=5)

        delete_project_btn = ttk.Button(button_frame, text="Projeyi Sil", command=self.delete_project)
        delete_project_btn.pack(side=tk.LEFT, padx=5)

        # Placeholder projeler
        self.projects = []
        self.load_projects()

    def load_projects(self):
        # Placeholder veriler, daha sonra veritabanından alınacak
        self.projects = ["Proje 1", "Proje 2", "Proje 3"]
        for project in self.projects:
            self.project_listbox.insert(tk.END, project)

    def add_project(self):
        new_project = tk.simpledialog.askstring("Yeni Proje", "Proje adını girin:")
        if new_project:
            self.projects.append(new_project)
            self.project_listbox.insert(tk.END, new_project)
            messagebox.showinfo("Başarılı", f"'{new_project}' projesi eklendi!")

    def view_project(self):
        selected = self.project_listbox.curselection()
        if not selected:
            messagebox.showwarning("Hata", "Lütfen bir proje seçin!")
            return
        project_name = self.project_listbox.get(selected)
        messagebox.showinfo("Proje Detayı", f"Seçilen proje: {project_name}")

    def delete_project(self):
        selected = self.project_listbox.curselection()
        if not selected:
            messagebox.showwarning("Hata", "Lütfen bir proje seçin!")
            return
        project_name = self.project_listbox.get(selected)
        if messagebox.askyesno("Emin misiniz?", f"'{project_name}' projesini silmek istediğinizden emin misiniz?"):
            self.project_listbox.delete(selected)
            self.projects.remove(project_name)
            messagebox.showinfo("Başarılı", f"'{project_name}' projesi silindi!")

if __name__ == "__main__":
    app = MainWindow()
    app.mainloop()
