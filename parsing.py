import requests
import time
import xml.etree.ElementTree as ET
from datetime import datetime
from setup import password, database_name, host, user
import mysql.connector


def g(func):
    def inner(*args, **kwargs):
        start = time.perf_counter()
        res = func(*args, **kwargs)
        print(func.__name__, time.perf_counter() - start)
        return res

    return inner


class parsing_part:
    def __init__(self):
        self.database = mysql.connector.connect(
            host='localhost',
            user='root',
            password='yaros5lav',
            database='first_project',
        )
        self.cursor = self.database.cursor(buffered=True)
        self.cursor.execute("SELECT url FROM rss")
        self.rss_urls = list(map(lambda x: x[0].strip(), self.cursor.fetchall()))[1:]
        self.rss_id = {url: number + 1 for number, url in (enumerate(self.rss_urls))}

    @g
    def get_links(self):
        for url in self.rss_urls:
            if url == '':
                break
            print(url)
            root = ET.fromstring(requests.get(url).text)
            for item in root.iter('item'):
                date = datetime.strptime(item.find('pubDate').text.replace(' GMT', ''), '%a, %d %b %Y %H:%M:%S')
                try:
                    self.cursor.execute(
                        "INSERT INTO jurusalem_post (url, publication_date, rss_row) VALUES (%s, %s, %s)",
                        (item.find('link').text, date, self.rss_id[url]))
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
            "SELECT jurusalem_post.url, jurusalem_post.publication_date, jurusalem_post.id, rss.category FROM "
            "jurusalem_post INNER JOIN rss "
            "ON jurusalem_post.rss_row = rss.id"
            " ORDER BY DATEDIFF(CURRENT_TIMESTAMP(), publication_date) + HOUR(TIMEDIFF(CURRENT_TIMESTAMP(), publication_date)) - rss.bonus;")
        result = self.cursor.fetchall()
        for id, url, date, topic in result:
            yield [id, url, date, topic]

    def update_sended(self, id):
        self.cursor.execute(F"UPDATE jurusalem_post SET sended = true WHERE ID = {id};", )
        self.database.commit()

# 0.6857387000000001
