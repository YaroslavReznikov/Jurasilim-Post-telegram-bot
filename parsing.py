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
        self.cursor = self.database.cursor()


    def get_links(self, url):
        root = ET.fromstring(requests.get(url).text)
        for item in root.iter('item'):
            date = datetime.strptime(item.find('pubDate').text.replace(' GMT', ''), '%a, %d %b %Y %H:%M:%S')
            try:
                self.cursor.execute("INSERT INTO jurusalem_post (url, publication_date) VALUES (%s, %s)", (item.find('link').text, date))
                self.database.commit()
            except:
                pass


    def send_links_to_user(self):
        print('does_something_with_database')
# 0.6857387000000001
