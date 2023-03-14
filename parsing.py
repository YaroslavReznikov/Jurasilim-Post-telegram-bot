import requests
import xml.etree.ElementTree as ET
from datetime import datetime
from setup import password, database_name, host, user
import mysql.connector


class parsing_part:
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

    def get_links(self):
        for url in self.rss_urls:
            if url.strip() == '':
                break
            root = ET.fromstring(requests.get(url.strip()).text)
            for item in root.iter('item'):
                date = datetime.strptime(item.find('pubDate').text.replace(' GMT', ''), '%a, %d %b %Y %H:%M:%S')
                try:
                    self.cursor.execute(
                        "INSERT INTO jurusalem_post (url, publication_date, rss_row) VALUES (%s, %s, %s)",
                        (item.find('link').text, date, self.rss_id[url.strip()]))
                    self.database.commit()
                except:
                    pass

    def feel_the_rss_database_database(self):
        with open("rss_files.txt", 'r', encoding='UTF-8') as inf:
            for url in inf:
                try:
                    category = url.strip().split('/')[-1].replace('rss', '').replace('feeds', '').replace('.aspx', '')
                    self.cursor.execute("INSERT INTO rss (url, category, bonus) VALUES (%s, %s, %s)",
                                        (url, category, 0))
                    self.database.commit()
                except:
                    pass

    def set_sended_to_zero(self):
        self.cursor.execute("UPDATE jurusalem_post sended = 0")

    def send_links_to_user(self):
        self.cursor.execute(
            "SELECT jurusalem_post.url, jurusalem_post.publication_date, jurusalem_post.id, rss.category, jurusalem_post.rss_row "
            "FROM jurusalem_post INNER JOIN rss ON jurusalem_post.rss_row = rss.id"
            " WHERE sended = 0"
            " ORDER BY ADDTIME(TIMEDIFF(CURRENT_TIMESTAMP(), publication_date), -rss.bonus * 10000);")
        result = self.cursor.fetchall()
        for url, date, id, topic, row in result:
            yield [id, url, date, topic]

    def update_sended(self, id):
        self.cursor.execute(F"UPDATE jurusalem_post SET sended = true WHERE ID = {id};", )
        self.database.commit()
