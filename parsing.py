import requests
import xml.etree.ElementTree as ET
from datetime import datetime
from setup import password, database_name, host, user
import mysql.connector


class DatabaseConnector:
    connect = None

    def __new__(cls, *args, **kwargs):
        if not cls.connect:
            cls.connect = object.__new__(cls, *args, **kwargs)
        return cls.connect

    def __init__(self):
        self.database = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database_name,
        )
        self.cursor = self.database.cursor(buffered=True)
        self.cursor.execute("SELECT id, url FROM rss "
                            "ORDER BY id;")
        self.rss_id = {url.strip(): number for number, url in self.cursor.fetchall()}
        self.rss_urls = list(self.rss_id.keys())

    def __del__(self):
        self.database.commit()
        self.database.close()


class ParsingPart:
    def __init__(self):
        self.database = DatabaseConnector()

    def get_links(self):
        for url in self.database.rss_urls:
            if url.strip() == '':
                break
            root = ET.fromstring(requests.get(url.strip()).text)
            for item in root.iter('item'):
                date = datetime.strptime(item.find('pubDate').text.replace(' GMT', ''), '%a, %d %b %Y %H:%M:%S')
                try:
                    self.database.cursor.execute(
                        "INSERT INTO jurusalem_post (url, publication_date, rss_row) VALUES (%s, %s, %s)",
                        (item.find('link').text, date, self.database.rss_id[url.strip()]))
                    self.database.database.commit()
                except:
                    pass

    def feel_the_rss_database_database(self):
        with open("rss_files.txt", 'r', encoding='UTF-8') as inf:
            for url in inf:
                try:
                    category = url.strip().split('/')[-1].replace('rss', '').replace('feeds', '').replace('.aspx', '')
                    self.database.cursor.execute("INSERT INTO rss (url, category, bonus) VALUES (%s, %s, %s)",
                                                 (url, category, 0))
                    self.database.database.commit()
                except:
                    pass

    def send_links_to_user(self, users_id):
        try:
            self.database.cursor.execute(F"INSERT INTO user_getted_urls (User_id, sended_urls) VALUES ({users_id}, '')")
        except Exception as e:
            pass
        self.database.cursor.execute(
            F"SELECT sended_urls FROM user_getted_urls "
            F"WHERE User_id = {users_id}"
        )
        news_that_user_got = self.database.cursor.fetchall()
        ids_of_sended_news = [t[0] for t in news_that_user_got]
        ids_of_sended_news_str = ' '.join(ids_of_sended_news)

        self.database.cursor.execute(
            F"SELECT jurusalem_post.url, jurusalem_post.publication_date, jurusalem_post.id, rss.category, jurusalem_post.rss_row "
            F"FROM jurusalem_post INNER JOIN rss ON jurusalem_post.rss_row = rss.id"
            F" WHERE LOCATE(jurusalem_post.id, '{ids_of_sended_news_str}') = 0"
            F" ORDER BY ADDTIME(TIMEDIFF(CURRENT_TIMESTAMP(), publication_date), -rss.bonus * 10000);")
        result = self.database.cursor.fetchall()
        for url, date, news_id, topic, row in result:
            self.add_url(users_id, ids_of_sended_news_str, news_id)
            yield [news_id, url, date, topic]

    def add_url(self, users_id, ids_of_sended_news, new_id):
        self.database.cursor.execute(F"UPDATE user_getted_urls"
                                     F" SET sended_urls = '{''.join(ids_of_sended_news) + ' ' + str(new_id)}'"
                                     F" WHERE User_id = {users_id};"
                                     )
        self.database.database.commit()


