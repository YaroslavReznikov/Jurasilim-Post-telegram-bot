import requests
import xml.etree.ElementTree as ET
from datetime import datetime
from setup import password, database_name, host, user
import mysql.connector


class DatabaseConnector:
    connect = None

    def __new__(cls, *args, **kwargs):
        if not cls.connect:
            cls.connect = object.__new__(cls)
        return cls.connect

    def __init__(self):
        self.database = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database_name,
        )
        self.cursor = self.database.cursor(buffered=True)
        self.cursor.execute("SELECT id, url FROM channels "
                            "ORDER BY id;")
        self.channels_ids = {url.strip(): number for number, url in self.cursor.fetchall()}
        self.channels_urls = list(self.channels_ids.keys())
        self.cursor.execute(F"SET SESSION connect_timeout = {10}")
        self.cursor.execute(F"SET SESSION wait_timeout = {10}")
        self.cursor.execute(F"SET SESSION interactive_timeout = {10}")

    @property
    def cursor(self):
        return self.__cursor

    @cursor.setter
    def cursor(self, new):
        self.__cursor = new

    @property
    def channels_ids(self):
        return self.__channels_ids

    @channels_ids.setter
    def channels_ids(self, new):
        self.__channels_ids = new

    @property
    def database(self):
        return self.__database

    @database.setter
    def database(self, new):
        self.__database = new

    @property
    def channels_urls(self):
        return self.__channels_urls

    @channels_urls.setter
    def channels_urls(self, new):
        self.__channels_urls = new

    def __del__(self):
        self.database.commit()
        self.database.close()


class ParsingPart:
    def __init__(self):
        self.database = DatabaseConnector()

    def get_links(self):
        for url in self.database.channels_urls:
            if url.strip() == '':
                break
            root = ET.fromstring(requests.get(url.strip()).text)
            for item in root.iter('item'):
                date = datetime.strptime(item.find('pubDate').text.replace(' GMT', ''), '%a, %d %b %Y %H:%M:%S')
                self.database.cursor.execute(
                    "INSERT IGNORE INTO news (url, publication_datetime, channels_id) VALUES (%s, %s, %s)",
                    (item.find('link').text, date, self.database.channels_ids[url.strip()]))
                self.database.database.commit()

    def fill_the_channels_database_with_basic_news(self):
        with open("rss_files.txt", 'r', encoding='UTF-8') as inf:
            for url in inf:
                category = url.strip().split('/')[-1].replace('rss', '').replace('feeds', '').replace('.aspx',
                                                                                                      '').replace(
                    '.html', '').replace(
                    'xml', '')
                self.database.cursor.execute("INSERT IGNORE INTO channels (url, category) VALUES (%s, %s,)",
                                             (url, category))
                self.database.database.commit()

    def first_time_using(self, users_id):
        for i in range(1, 41):
            self.database.cursor.execute(
                f"INSERT IGNORE INTO channel (telegram_id, wanted_news, adding_datetime, bonus) "
                f"VALUES ({users_id}, {i}, '{datetime.today()}', 0);"

            )
            self.database.database.commit()

    def find_links_for_user(self, users_id, user_wanted_amount_of_news):
        self.first_time_using(users_id)
        self.database.cursor.execute(
            f"SELECT news.url, news.publication_datetime, news.id, news.channels_id, "
            f"(SELECT category FROM channels WHERE id = news.channels_id) AS category "
            f"FROM news "
            f"INNER JOIN channel ON channel.wanted_news = news.channels_id "
            f"LEFT JOIN user_got_urls ON user_got_urls.telegram_id = {users_id} "
            f"AND user_got_urls.sent_urls = news.id "
            f"WHERE user_got_urls.sent_urls IS NULL "
            f"ORDER BY ADDTIME(TIMEDIFF(CURRENT_TIMESTAMP(), publication_datetime), -(channel.bonus * 10000)) "
            f"LIMIT {user_wanted_amount_of_news};")
        result = self.database.cursor.fetchall()
        return result

    def add_url(self, users_id, new_id):
        self.database.cursor.execute(F"INSERT INTO user_got_urls (telegram_id, sent_urls, getting_datetime)"
                                     F" VALUES ({users_id}, {new_id}, '{datetime.today()}');")
        self.database.database.commit()

    @staticmethod
    def url_check(rss_url):
        try:
            requests.get(rss_url)
        except:
            raise "Something wrong with given url"

    def get_row_of_url_in_news(self, rss_url):
        self.url_check(rss_url)
        self.database.cursor.execute(F"SELECT id FROM channels"
                                     F" WHERE url = '{rss_url}'"
                                     F" LIMIT 1;")
        return self.database.cursor.fetchall()[0]

    def insert_into_channels(self, rss_url):
        category = rss_url.strip().split('/')[-1].replace('rss', '').replace('feeds', '').replace('.aspx', '').replace(
            '.html', '').replace('xml', '')
        self.database.cursor.execute(F"INSERT IGNORE  INTO channels (url, category) "
                                     F"VALUES ('{rss_url}', '{category}');")
        self.database.database.commit()

    def add_new_source(self, rss_url, users_id, prio):
        self.url_check(rss_url)
        self.insert_into_channels(rss_url)
        row = self.get_row_of_url_in_news(rss_url)
        self.database.cursor.execute(f"INSERT IGNORE INTO channel (telegram_id, wanted_news, adding_datetime, bonus)"
                                     F" VALUES ({users_id}, '{row[0]}', '{datetime.today()}', {prio});")
        self.database.database.commit()
