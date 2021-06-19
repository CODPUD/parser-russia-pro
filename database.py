import sqlite3
from settings import DB_ROOT

class DatabaseInterface:
    def __init__(self) -> None:
        ''' Creates connection to database and cursor '''
        self.conn = sqlite3.connect(DB_ROOT)
        self.cur = self.conn.cursor()
        
        self.create_table()

    def execute(self, query, data=()):
        self.cur.execute(query, data)
        self.conn.commit()
        return self.cur
    
    def create_table(self):
        ''' Creates the table post if not exists '''
        return self.execute(query="CREATE TABLE IF NOT EXISTS \
            post(id INTEGER PRIMARY KEY AUTOINCREMENT,\
                title TEXT NOT NULL, \
                description TEXT NOT NULL, \
                href TEXT NOT NULL, \
                news_id INTEGER NOT NULL\
                )")
    
    def add_post(self, data):
        ''' Add new post to database '''
        return self.execute(query="INSERT INTO post(title, description, href, news_id) VALUES(?,?,?,?)", data=data)
    
    def __del__(self):
        self.conn.close()