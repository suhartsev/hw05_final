from django.test import Client, TestCase
from django.urls import reverse


class PostsViewsTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.guest_client = Client()

    def test_author_page_uses_correct_template(self):
        """Проверка:  namespace:name в приложении users"""
        templates_pages_names = {
            'users/signup.html': reverse('users:signup'),
            'users/logged_out.html': reverse('users:logout'),
            'users/login.html': reverse('users:login'),
            'users/password_reset_form.html': reverse(
                'users:password_reset_form'
            ),
            'users/password_reset_done.html': reverse(
                'users:password_reset_done'
            ),
            'users/password_reset_complete.html': reverse(
                'users:password_reset_complete'
            )
        }
        for template, reverse_name in templates_pages_names.items():
            with self.subTest(reverse_name=reverse_name):
                response = self.guest_client.get(reverse_name)
                self.assertTemplateUsed(response, template)
