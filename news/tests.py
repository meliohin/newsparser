from bs4 import BeautifulSoup

from django.test import TestCase
from django.urls import path, reverse

from rest_framework.test import APITestCase, URLPatternsTestCase

from news.models import News
from news.views import NewsList

from newsparser.urls import urlpatterns as project_urlpatterns 

class NewsModelTestCase(TestCase):

    def setUp(self):
        News.objects.create(title="n1", url="http://u1.ru/")
        News.objects.create(title="n2", url="http://u2.ru/")
        News.objects.create(title="n3", url="http://u3.ru/")

    def test_get_html(self):
        html = News.get_html()
        is_html = bool(BeautifulSoup(html, "html.parser").find())
        self.assertTrue(is_html)

    def test_parse_html(self):
        test_result = True
        html = """
            <html>
                <a class="storylink" href ="http://url1.ru/">news1</a>
                <a class="storylink" href ="http://url2.ru/">news2</a>
                <a class="storylink" href ="http://url3.ru/">news3</a>
            </html>
        """
        l = News.parse_html(html)
        if not (l[0]['url'] == 'http://url1.ru/' and
                l[0]['title'] == 'news1' and
                l[1]['url'] == 'http://url2.ru/' and
                l[1]['title'] == 'news2' and
                l[2]['url'] == 'http://url3.ru/' and
                l[2]['title'] == 'news3'
            ):
            test_result = False
        self.assertTrue(test_result)

    def test_insert_to_db(self):
        l = [
                {'url': 'http://url1.ru/', 'title': 'news1'},
                {'url': 'http://url2.ru/', 'title': 'news2'},
                {'url': 'http://url3.ru/', 'title': 'news3'},
            ]
        News.insert_to_db(l)
        count = News.objects.filter(title__contains='news').count()
        self.assertEqual(count, 3)

    def test_process(self):
        News.objects.all().delete()
        News.process()
        count = News.objects.all().count() - 3
        self.assertTrue(count > 0)


class GetPostsTestCase(APITestCase, URLPatternsTestCase):
    urlpatterns = project_urlpatterns
    url = reverse('posts')

    def setUp(self):
        News.objects.create(title="n1", url="http://u1.ru/")
        News.objects.create(title="n2", url="http://u2.ru/")
        News.objects.create(title="n3", url="http://u3.ru/")

    def test_api_common(self):
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 3)

    def test_api_ordering_id(self):
        response = self.client.get(self.url, format='json', data={'ordering': '-id'})
        self.assertEqual(response.data[0]['id'], 3)

    def test_api_ordering_title(self):
        response = self.client.get(self.url, format='json', data={'ordering': '-title'})
        self.assertEqual(response.data[0]['title'], 'n3')

    def test_api_ordering_url(self):
        response = self.client.get(self.url, format='json', data={'ordering': '-url'})
        self.assertEqual(response.data[0]['url'], "http://u3.ru/")