from http import HTTPStatus

from django.test import Client, TestCase
from django.urls import reverse

from posts.models import Group, Post, User
from posts.tests import const


class PostURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.author_post = User.objects.create_user(
            username=const.USERNAME
        )
        cls.other_user = User.objects.create_user(
            username=const.OTHER_USER
        )
        cls.group = Group.objects.create(
            title=const.GROUP1_TITLE,
            slug=const.GROUP1_SLUG,
            description=const.GROUP1_DESCRIPTION,
        )
        cls.post = Post.objects.create(
            text=const.TEXT,
            author=cls.author_post,
            group=cls.group
        )
        cls.POST_DETAIL = reverse(
            const.URL_POST_DETAIL,
            kwargs={'post_id': cls.post.id}
        )
        cls.POST_EDIT = reverse(
            const.URL_POST_EDIT,
            kwargs={'post_id': cls.post.id}
        )
        cls.GROUP_LIST = reverse(
            const.URL_GROUP_LIST,
            kwargs={'slug': cls.group.slug}
        )

    def setUp(self):
        self.guest = Client()
        self.author = Client()
        self.author.force_login(self.author_post)
        self.other = Client()
        self.other.force_login(self.other_user)

    def test_urls_exists_at_desired_location_client(self):
        """Проверка: доступа страниц для Автор, Гость, Пользователь"""
        url_code = [
            (
                const.URL_INDEX_HOME,
                HTTPStatus.OK,
                HTTPStatus.OK,
                HTTPStatus.OK
            ),
            (
                self.GROUP_LIST,
                HTTPStatus.OK,
                HTTPStatus.OK,
                HTTPStatus.OK
            ),
            (
                const.URL_PROFILE_REV,
                HTTPStatus.OK,
                HTTPStatus.OK,
                HTTPStatus.OK
            ),
            (
                self.POST_DETAIL,
                HTTPStatus.OK,
                HTTPStatus.OK,
                HTTPStatus.OK
            ),
            (
                const.URL_POST_CREATE_REV,
                HTTPStatus.OK,
                HTTPStatus.OK,
                HTTPStatus.FOUND
            ),
            (
                self.POST_EDIT,
                HTTPStatus.OK,
                HTTPStatus.FOUND,
                HTTPStatus.FOUND
            ),
            (
                const.URL_UNEXISTRING,
                HTTPStatus.NOT_FOUND,
                HTTPStatus.NOT_FOUND,
                HTTPStatus.NOT_FOUND
            ),
            (
                const.URL_FOLLOW,
                HTTPStatus.OK,
                HTTPStatus.OK,
                HTTPStatus.FOUND
            )
        ]
        for urls, auth_cond, other_cond, guest_cond in url_code:
            for client, cond in [
                (self.author, auth_cond),
                (self.other, other_cond),
                (self.guest, guest_cond),
            ]:
                with self.subTest(urls=urls):
                    self.assertEqual(client.get(urls).status_code, cond)
