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


    def get_links(self, url):
        root = ET.fromstring(requests.get(url).text)
        for item in root.iter('item'):
            date = datetime.strptime(item.find('pubDate').text.replace(' GMT', ''), '%a, %d %b %Y %H:%M:%S')
            try:
                self.cursor.execute("INSERT INTO jurusalem_post (url, publication_date) VALUES (%s, %s)", (item.find('link').text, date))
                self.database.commit()
            except:
                pass


    def set_sended_to_zero(self):
        self.cursor.execute("UPDATE jurusalem_post sended = 0")

    def send_links_to_user(self):
        self.cursor.execute('SELECT * from jurusalem_post WHERE sended = 0 ORDER BY publication_date DESC;')
        result = self.cursor.fetchall()
        for id, url, date, sended in result:
            yield [id, url]

    def update_sended(self, id):
        self.cursor.execute(F"UPDATE jurusalem_post SET sended = true WHERE ID = {id};",)
        self.database.commit()

# 0.6857387000000001
