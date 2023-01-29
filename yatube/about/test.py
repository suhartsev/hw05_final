from http import HTTPStatus

from django.test import Client, TestCase
from django.urls import reverse


class StaticURLTests(TestCase):
    def setUp(self):
        self.guest_client = Client()

    def test_static_urls_exists_at_desired_location(self):
        """Проверка: Страницы доступны любому пользователю."""
        static_urls = {
            '/': HTTPStatus.OK,
            '/about/author/': HTTPStatus.OK,
            '/about/tech/': HTTPStatus.OK
        }
        for address, response_on_url in static_urls.items():
            with self.subTest(address=address):
                response = self.guest_client.get(address)
                self.assertAlmostEqual(response.status_code, response_on_url)

    def test_static_pages_have_correct_template(self):
        """Проверка: URL-адрес использует соответствующий шаблон."""
        static_templates = {
            '/': 'posts/index.html',
            '/about/author/': 'about/author.html',
            '/about/tech/': 'about/tech.html'
        }
        for address, template in static_templates.items():
            with self.subTest(address=address):
                response = self.guest_client.get(address)
                self.assertTemplateUsed(response, template)


class StaticViewsTests(TestCase):
    def setUp(self):
        self.guest_client = Client()

    def test_author_page_uses_correct_template(self):
        """Проверка: about:author, about:tech в приложении about"""
        templates_pages_names = {
            'about/author.html': reverse('about:author'),
            'about/tech.html': reverse('about:tech')
        }
        for template, reverse_name in templates_pages_names.items():
            with self.subTest(reverse_name=reverse_name):
                response = self.guest_client.get(reverse_name)
                self.assertTemplateUsed(response, template)
