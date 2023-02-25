from bs4 import BeautifulSoup
import requests
import time


def g(func):
    def inner(*args, **kwargs):
        start = time.perf_counter()
        res = func(*args, **kwargs)
        print(func.__name__, time.perf_counter() - start)
        return res

    return inner


# class “one-row”


class parsing_part:
    def __init__(self):
        self.urls_list = []

    @staticmethod
    def remove_link_tag(line):
        line = line.replace("link", '')
        line = line.replace("<", '')
        line = line.replace(">", '')
        return line.strip()

    @g
    def get_links(self, url, page_type="home page"):
        rec = requests.get(url)
        self.urls_list = [(self.remove_link_tag(tag), page_type) for tag in rec.text.strip().split('\n') if
                          'link' in tag and len(self.remove_link_tag(tag).split()) == 1]

    def database_sending(self):
        print(self.urls_list)
#0.6857387000000001