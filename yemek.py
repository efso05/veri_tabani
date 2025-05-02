import sqlite3
from datetime import datetime

con = sqlite3.connect('yemek.db')
cursor = con.cursor()

class DB_Manager:
    def create_tables(self):
        con = sqlite3.connect(self.database)
        with con:
            con.execute("""CREATE TABLE yemek(
                        adı TEXT,
                        fiyat INTEGER,
                        porsiyon_basina_agirlik)