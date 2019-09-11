import requests
from bs4 import BeautifulSoup

from django.db import models

class News(models.Model):

    PARSE_URL = 'https://news.ycombinator.com/'

    title = models.CharField(max_length=2048)
    url = models.CharField(max_length=2048)
    created = models.DateTimeField(auto_now_add=True)

    @classmethod
    def get_html(cls, parse_url=None):
        """
        Get HTML page with news.
        Return None in case of any trasport or server response error.
        """
        if not parse_url:
            parse_url = cls.PARSE_URL
        try:
            r = requests.get(parse_url)
            if r.status_code == 200:
                res = r.text
            else:
                print('Response is not OK:', r.status_code, r.text)
                res = None
        except requests.exceptions.RequestException as e:
            print (str(e))
            res = None
        return res

    @classmethod
    def parse_html(cls, html):
        """
        Parse HTML to list of dicts.
        """
        news_list = []
        soup = BeautifulSoup(html, 'html.parser')
        for a in soup.find_all("a", class_="storylink"):
            url = a.attrs['href']
            # self-hosted urls like "item?id=20927552"
            if not 'http' in url:
                url = self.PARSE_URL + url
            title = a.text
            news_list.append({'url': url, 'title': title})
        return news_list

    @classmethod
    def insert_to_db(cls, news_list):
        """
        Insert news to db from list.
        """
        for item in news_list:
            n, _c = cls.objects.get_or_create(title=item['title'], url=item['url'])

    @classmethod
    def process(cls):
        """
        Model method for calling from async task.
        """
        html = cls.get_html()
        if html:
            news_list = cls.parse_html(html)
            cls.insert_to_db(news_list)
        else:
            print('No HTML returned.')
            pass


