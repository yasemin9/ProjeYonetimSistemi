import sqlite3

class DatabaseConnection:
    """
    SQLite veritabanı bağlantısını kolaylaştırmak için bir sınıf.
    """
    def __init__(self, db_name="project_management.db"):
        self.db_name = db_name
        self.connection = None
        self.cursor = None

    def connect(self):
        """
        Veritabanına bağlanır ve imleci oluşturur.
        """
        self.connection = sqlite3.connect(self.db_name)
        self.cursor = self.connection.cursor()

    def execute_query(self, query, parameters=()):
        """
        Veritabanında bir sorgu çalıştırır.
        """
        if self.connection is None:
            self.connect()
        self.cursor.execute(query, parameters)

    def fetch_all(self):
        """
        Çalıştırılan sorgunun tüm sonuçlarını döndürür.
        """
        return self.cursor.fetchall()

    def fetch_one(self):
        """
        Çalıştırılan sorgunun tek bir sonucunu döndürür.
        """
        return self.cursor.fetchone()

    def commit(self):
        """
        Değişiklikleri veritabanına yazar.
        """
        if self.connection:
            self.connection.commit()

    def close(self):
        """
        Veritabanı bağlantısını kapatır.
        """
        if self.connection:
            self.connection.close()
            self.connection = None
            self.cursor = None

    def __enter__(self):
        """
        Bağlam yöneticisi desteği için giriş metodu.
        """
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Bağlam yöneticisi desteği için çıkış metodu.
        """
        self.commit()
        self.close()

# Örnek Kullanım:
if __name__ == "__main__":
    with DatabaseConnection() as db:
        # Veritabanında bir tablo oluştur
        db.execute_query("""
            CREATE TABLE IF NOT EXISTS test_table (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL
            )
        """)
        db.commit()

        # Veri ekle
        db.execute_query("INSERT INTO test_table (name) VALUES (?)", ("Test",))
        db.commit()

        # Veri oku
        db.execute_query("SELECT * FROM test_table")
        results = db.fetch_all()
        print("Kayıtlar:", results)
