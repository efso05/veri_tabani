import sqlite3
from datetime import datetime

con = sqlite3.connect('deneme.db')
cursor = con.cursor()

class DB_Manager:
    def create_tables(self):
        con = sqlite3.connect(self.database)
        with con:
            con.execute("""CREATE TABLE projects(
                                        project_id INTEGER PRIMARY KEY,
                                        user_id INTEGER,
                                        project_name TEXT,
                                        description TEXT,
                                        url TEXT,
                                        status_id INTEGER,
                                        FORGEIN KEY (status_id) REFERENCES status (status))""")