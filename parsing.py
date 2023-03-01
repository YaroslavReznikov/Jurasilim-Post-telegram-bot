import requests
import time
import xml.etree.ElementTree as ET
from datetime import datetime
from setup import password, database_name, host, user
import pymysql


def g(func):
    def inner(*args, **kwargs):
        start = time.perf_counter()
        res = func(*args, **kwargs)
        print(func.__name__, time.perf_counter() - start)
        return res

    return inner



class parsing_part:
    def __init__(self):
        self.urls_list = []
        self.database = pymysql.connect(
            host=host,
            password=password,
            database=database_name,
            user=user,
            port=3306,
            cursorclass=pymysql.cursors.DictCursor
        )

    @g
    def get_links(self, url):
        root = ET.fromstring(requests.get(url).text)
        for item in root.iter('item'):
            date = datetime.strptime(item.find('pubDate').text.replace(' GMT', ''), '%a, %d %b %Y %H:%M:%S')
            self.urls_list.append((item.find('link').text, date))

    def database_sending(self):
        print(self.urls_list)

    def send_links_to_user(self):
        print('does_something_with_database')
# 0.6857387000000001
