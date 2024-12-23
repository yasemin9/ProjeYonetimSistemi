import mysql.connector
from mysql.connector import Error

def connect_to_database():
    """
    Veritabanına bağlanır ve bağlantı nesnesini döner.
    """
    try:
        # MySQL bağlantısı oluşturma
        connection = mysql.connector.connect(
            host="localhost",
            user="root",  # MySQL kullanıcı adı
            password="admin",  # MySQL şifresi
            database="project_management"  # Kullanılacak veritabanı
        )
        if connection.is_connected():
            print("Veritabanı bağlantısı başarılı!")
            return connection
    except Error as err:
        # Hata durumunda ayrıntılı mesajlar gösterilir
        if err.errno == 1049:
            print("Error: Veritabanı bulunamadı. Lütfen 'project_management' veritabanının mevcut olduğundan emin olun.")
        elif err.errno == 1045:
            print("Error: Kullanıcı adı veya şifre yanlış.")
        elif err.errno == 2003:
            print("Error: Veritabanı sunucusuna bağlanılamıyor. 'localhost' ve '3306' portunu kontrol edin.")
        else:
            print(f"Error: {err}")
        return None
    finally:
        # Başarısız bir bağlantı durumunda kapatma işlemi yapılırsa buradan eklenebilir
        pass
