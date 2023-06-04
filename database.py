import sqlite3


class DatabaseManager:
    def __init__(self):
        self.conn = sqlite3.connect('db.sqlite3', check_same_thread=False)
        self.c = self.conn.cursor()
        self.create_table()

    def __del__(self):
        self.c.close()
        self.conn.close()

    def create_table(self):

        self.c.execute(
            'CREATE TABLE IF NOT EXISTS urls (id INTEGER PRIMARY KEY AUTOINCREMENT , link TEXT)')

        self.c.execute(
            'CREATE TABLE IF NOT EXISTS yt (id INTEGER PRIMARY KEY AUTOINCREMENT , link TEXT)')

        self.c.execute(
            'CREATE TABLE IF NOT EXISTS channels (id INTEGER PRIMARY KEY AUTOINCREMENT , link TEXT)')

        self.conn.commit()

    def drop_table(self):
        self.c.execute('DROP TABLE IF EXISTS urls')
        self.c.execute('DROP TABLE IF EXISTS yt')
        self.c.execute('DROP TABLE IF EXISTS channels')

        self.conn.commit()

    def get_all_urls(self):
        self.c.execute('SELECT * FROM urls')
        return self.c.fetchall()

    def get_all_yt(self):
        self.c.execute('SELECT * FROM yt')
        return self.c.fetchall()

    def get_all_channels(self):
        self.c.execute('SELECT * FROM channels')
        return self.c.fetchall()

    def insert_url(self, url):
        self.c.execute('INSERT INTO urls (link) VALUES (?)', (url,))
        self.conn.commit()

    def insert_yt(self, url):
        self.c.execute('INSERT INTO yt (link) VALUES (?)', (url,))
        self.conn.commit()

    def insert_channel(self, url):
        self.c.execute('INSERT INTO channels (link) VALUES (?)', (url,))
        self.conn.commit()

    def insert_urls(self, urls):
        for url in urls:
            self.insert_url(url)

    def insert_yts(self, urls):
        for url in urls:
            self.insert_yt(url)

    def insert_channels(self, urls):
        for url in urls:
            self.insert_channel(url)

    def update_url(self, url):
        self.c.execute('UPDATE urls SET link=?', (url,))
        self.conn.commit()

    def update_yt(self, url):
        self.c.execute('UPDATE yt SET link=?', (url,))
        self.conn.commit()

    def update_channel(self, url):
        self.c.execute('UPDATE channels SET link=?', (url,))
        self.conn.commit()

    def delete_url(self, id):
        self.c.execute('DELETE FROM urls WHERE id=?', (id,))
        self.conn.commit()

    def delete_yt(self, id):
        self.c.execute('DELETE FROM yt WHERE id=?', (id,))
        self.conn.commit()

    def delete_channel(self, id):
        self.c.execute('DELETE FROM channels WHERE id=?', (id,))
        self.conn.commit()


if __name__ == '__main__':
    db = DatabaseManager()
    db.insert_url('https://www.youtube.com/watch?v=1')
    db.insert_url('https://www.youtube.com/watch?v=2')
    db.insert_url('https://www.youtube.com/watch?v=3')
    db.insert_url('https://www.youtube.com/watch?v=4')

    db.insert_channel('https://www.youtube.com/channel/1')
    db.insert_channel('https://www.youtube.com/channel/2')
    db.insert_channel('https://www.youtube.com/channel/3')
    db.insert_channel('https://www.youtube.com/channel/4')

    db.insert_yt('https://www.youtube.com/watch?v=1')
    db.insert_yt('https://www.youtube.com/watch?v=2')
    db.insert_yt('https://www.youtube.com/channel/3')
    db.insert_yt('https://www.youtube.com/channel/4')

    print(db.get_all_urls())
    print(db.get_all_yt())
    print(db.get_all_channels())
