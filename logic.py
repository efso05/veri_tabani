import sqlite3
from config import DATABASE

class DB_Manager:
    def __init__(self, database):
        self.database = database 

    def connect_db(self):
        """ Veritabanı bağlantısı oluşturur. """
        return sqlite3.connect(self.database)

    def drop_tables(self):
        """ Veritabanındaki tüm tabloları siler. """
        conn = self.connect_db()
        cursor = conn.cursor()
        tables = ["projects", "skills", "project_skills", "status", "images"]
        
        try:
            for table in tables:
                cursor.execute(f"DROP TABLE IF EXISTS {table}")
            conn.commit()
            print("Tüm tablolar başarıyla silindi.")
        except sqlite3.Error as e:
            print(f"Hata oluştu: {e}")
        finally:
            conn.close()

    def create_tables(self):
        """ Gerekli tabloları oluşturur. """
        conn = self.connect_db()
        with conn:
            conn.execute('''CREATE TABLE IF NOT EXISTS projects (
                            project_id INTEGER PRIMARY KEY,
                            user_id INTEGER,
                            project_name TEXT NOT NULL,
                            description TEXT,
                            url TEXT,
                            status_id INTEGER,
                            FOREIGN KEY(status_id) REFERENCES status(status_id)
                        )''') 
            conn.execute('''CREATE TABLE IF NOT EXISTS skills (
                            skill_id INTEGER PRIMARY KEY,
                            skill_name TEXT
                        )''')
            conn.execute('''CREATE TABLE IF NOT EXISTS project_skills (
                            project_id INTEGER,
                            skill_id INTEGER,
                            FOREIGN KEY(project_id) REFERENCES projects(project_id),
                            FOREIGN KEY(skill_id) REFERENCES skills(skill_id)
                        )''')
            conn.execute('''CREATE TABLE IF NOT EXISTS status (
                            status_id INTEGER PRIMARY KEY,
                            status_name TEXT
                        )''')
            conn.execute('''CREATE TABLE IF NOT EXISTS images (
                            id INTEGER PRIMARY KEY,
                            name TEXT,
                            png_data BLOB
                        )''')
            conn.commit()

    def insert_statuses(self):
        """ Status tablosuna gerekli durumları ekler. """
        conn = self.connect_db()
        cursor = conn.cursor()

        status_list = [("Devam Ediyor",), ("Tamamlandı",), ("Beklemede",)]
        
        try:
            cursor.executemany("INSERT OR IGNORE INTO status (status_name) VALUES (?)", status_list)
            conn.commit()
            print("Durumlar başarıyla eklendi.")
        except sqlite3.Error as e:
            print(f"Hata oluştu: {e}")
        finally:
            conn.close()

    def insert_project(self, data):
        """ Proje ekleme metodu. """
        sql = """INSERT INTO projects 
        (user_id, project_name, url, status_id) 
        values(?, ?, ?, ?)"""
        conn = self.connect_db()
        with conn:
            conn.executemany(sql, data)
            conn.commit()

    def convert_to_binary(self, filename):
        """ Dosyayı BLOB formatına çevirir. """
        with open(filename, "rb") as file:
            return file.read()

    def insert_png(self, image_name):
        """ PNG dosyasını veritabanına ekler. """
        conn = self.connect_db()
        cursor = conn.cursor()

        try:
            image_data = self.convert_to_binary(image_name)
            insert_query = "INSERT INTO images (name, png_data) VALUES (?, ?)"
            cursor.execute(insert_query, (image_name, image_data))
            conn.commit()
            print("PNG dosyası başarıyla veritabanına eklendi!")
        except sqlite3.Error as e:
            print(f"Hata oluştu: {e}")
        finally:
            conn.close()

    def update_project_status(self, project_id, new_status):
        """ Belirtilen proje ID'sinin durumunu günceller. """
        conn = self.connect_db()
        cursor = conn.cursor()

        cursor.execute("SELECT status_id FROM status WHERE status_name = ?", (new_status,))
        status_id_result = cursor.fetchone()

        if not status_id_result:
            print(f"Hata: '{new_status}' adlı durum bulunamadı. Lütfen status tablosunu kontrol edin.")
            return

        status_id = status_id_result[0]

        try:
            sql = "UPDATE projects SET status_id = ? WHERE project_id = ?"
            cursor.execute(sql, (status_id, project_id))
            conn.commit()
            print(f"Proje {project_id} başarıyla '{new_status}' olarak güncellendi.")
        except sqlite3.Error as e:
            print(f"Hata oluştu: {e}")
        finally:
            conn.close()

if __name__ == '__main__':
    manager = DB_Manager(DATABASE)
    manager.drop_tables()  # Tüm tabloları sil (veritabanını sıfırla)
    manager.create_tables()  # Sonra tekrar oluştur
    manager.insert_statuses()  # Durumları ekle
    manager.insert_png("kratos.png")  # PNG ekleme işlemi
    manager.insert_project([(3, "Otonom Araç", "https://dahamevcutdeğil.com", 2)])
    manager.update_project_status(3, "Tamamlandı")  # Örnek durum güncelleme
