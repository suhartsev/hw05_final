import shutil

from django.core.cache import cache
from django.test import Client, TestCase, override_settings
from django.urls import reverse

from posts.models import Follow, Group, Post, User
from posts.tests import const


@override_settings(MEDIA_ROOT=const.TEMP_MEDIA_ROOT)
class PostsViewsTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.guest_client = Client()
        cls.user = User.objects.create_user(username=const.USERNAME)
        cls.group = Group.objects.create(
            title=const.GROUP1_TITLE,
            slug=const.GROUP1_SLUG,
            description=const.GROUP1_DESCRIPTION
        )
        cls.group2 = Group.objects.create(
            title=const.GROUP2_TITLE,
            slug=const.GROUP2_SLUG,
            description=const.GROUP2_DESCRIPTION,
        )
        cls.post = Post.objects.create(
            text=const.TEXT,
            author=cls.user,
            group=cls.group,
            image=const.UPLOADED,
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
        cls.GROUP_LIST_GROUP_2 = reverse(
            const.URL_GROUP_LIST,
            kwargs={'slug': cls.group2.slug}
        )
        cls.ADD_COMMENT = reverse(
            const.URL_ADD_COMMENT,
            kwargs={'post_id': cls.post.pk})

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(const.TEMP_MEDIA_ROOT, ignore_errors=True)

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)
        cache.clear()

    def check_contex(self, context_page):
        """Проверки: контекста картинки, текста, поста, автора"""
        context_page = {
            context_page.text: const.TEXT,
            context_page.author: self.user,
            context_page.group: self.group,
            context_page.image: self.post.image
        }
        for context, expected in context_page.items():
            self.assertEqual(context, expected)

    def test_pages_uses_correct_template(self):
        """Проверка: view-функциях используются правильные html-шаблоны"""
        templates_pages_names = {
            const.URL_INDEX_REV: const.TEMPLATE_INDEX,
            const.URL_POST_CREATE_REV: const.TEMPLATE_POST_CREATE,
            self.GROUP_LIST: const.TEMPLATE_GROUP_LIST,
            const.URL_PROFILE_REV: const.TEMPLATE_PROFILE_REV,
            self.POST_DETAIL: const.TEMPLATE_POST_DETAIL,
            self.POST_EDIT: const.TEMPLATE_POST_EDIT,
            const.URL_FOLLOW: const.TEMPLATE_FOLLOW,
            const.URL_UNEXISTRING: const.TEMPLATE_CORE_404,
            self.ADD_COMMENT: const.TEMPLATE_POST_DETAIL,
            const.URL_FOLLOW: const.TEMPLATE_FOLLOW,
            const.URL_AUTHOR: const.TEMPLATE_AUTHOR,
            const.URL_TECH: const.TEMPLATE_TECH,
        }
        for reverse_name, template in templates_pages_names.items():
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_client.get(
                    reverse_name,
                    follow=True
                )
                self.assertTemplateUsed(response, template)

    def test_profile_page_shows_correct_context(self):
        """Проверка: Шаблон profile сформирован с правильным контекстом."""
        response = self.authorized_client.get(const.URL_PROFILE_REV)
        post = response.context['page_obj'][0]
        self.assertEqual(post, self.post)
        self.check_contex(post)

    def test_index_page_show_correct_context(self):
        """Проверка: Шаблон index сформирован с правильным контекстом."""
        response = self.authorized_client.get(const.URL_INDEX_REV)
        post = response.context['page_obj'][0]
        self.assertIn('page_obj', response.context)
        self.check_contex(post)

    def test_group_list_page_show_correct_context(self):
        """Проверка: Шаблон group_list сформирован с правильным контекстом."""
        response = self.authorized_client.get(self.GROUP_LIST)
        group = response.context['page_obj'][0]
        self.assertIn('page_obj', response.context)
        self.check_contex(group)

    def test_post_detail_list_page_show_correct_context(self):
        """Проверка: Шаблон post_detail сформирован с правильным контекстом."""
        response = self.authorized_client.get(self.POST_DETAIL,)
        post_detail = response.context['post']
        self.check_contex(post_detail)

    def test_post_not_in_other_group(self):
        """Проверка: Созданный пост не появился в другой группе"""
        post = self.post
        response = self.authorized_client.get(self.GROUP_LIST_GROUP_2)
        self.assertNotIn(post, response.context.get('page_obj'))
        group2 = response.context.get('group')
        self.assertNotEqual(group2, self.group)

    def test_cache_index_page(self):
        """"Проверка: Кэш на странице Index"""
        cache.clear()
        response = self.authorized_client.get(const.URL_INDEX_REV)
        cache_response = response.content
        post = Post.objects.get(pk=self.post.id)
        post.delete()
        response = self.authorized_client.get(const.URL_INDEX_REV)
        self.assertEqual(response.content, cache_response)


class PaginatorViewsTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username=const.USERNAME)
        cls.author = User.objects.get(username=const.USERNAME)
        cls.group = Group.objects.create(
            title=const.GROUP1_TITLE,
            slug=const.GROUP1_SLUG,
            description=const.GROUP1_DESCRIPTION,
        )
        cls.GROUP_LIST = reverse(
            const.URL_GROUP_LIST,
            kwargs={'slug': cls.group.slug}
        )
        cls.posts = [
            Post(
                text=f'{const.TEXT} {number_post}',
                author=cls.user,
                group=cls.group,
            )
            for number_post in range(const.TOTAL_POSTS)
        ]
        Post.objects.bulk_create(cls.posts)

    def setUp(self):
        self.authorized = Client()

    def test_page_paginator_obj(self):
        """Проверка: пагинатор на 1, 2 странице index, group_list, profile"""
        templates = [
            (const.URL_INDEX_REV),
            (self.GROUP_LIST),
            (const.URL_PROFILE_REV)
        ]
        count_and_page = [
            (const.ONE_PAGE, const.COUNT_POST_TEN),
            (const.TWO_PAGE, const.COUNT_POST_THREE)
        ]
        for reverse_name in templates:
            for page, count_posts in count_and_page:
                with self.subTest(reverse_name=reverse_name):
                    response = self.authorized.get(
                        reverse_name, {'page': page}
                    )
                    posts = len(response.context['page_obj'])
                    self.assertEqual(posts, count_posts)


class FollowViewsTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username=const.USERNAME)
        cls.another_user = User.objects.create_user(username=const.OTHER_USER)
        cls.post = Post.objects.create(
            text=const.TEXT,
            author=cls.another_user
        )

    def setUp(self):
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)
        self.author_user = Client()
        self.author_user.force_login(self.another_user)

    def test_authorized_client_follow(self):
        """Проверка: Пользователь может пописаться на другого автора"""
        self.authorized_client.get(const.URL_FOLLOW_PROF)
        self.assertTrue(
            Follow.objects.filter(
                user=self.user,
                author=self.another_user).exists()
        )

    def test_authorized_client_unfollow(self):
        """Проверка: Пользователь может отаисаться от автора"""
        Follow.objects.create(
            user=self.user,
            author=self.another_user
        )
        self.authorized_client.get(
            const.URL_UNFOLLOW
        )
        self.assertFalse(
            Follow.objects.filter(
                user=self.user,
                author=self.another_user
            ).exists()
        )

    def test_following_posts_showing_to_followers(self):
        """ Проверка: запись пользователя отображается в ленте тех,
        кто на него подписан."""
        self.authorized_client.get(const.URL_FOLLOW_PROF)
        response = self.authorized_client.get(const.URL_FOLLOW)
        following_post = response.context['page_obj'][0].text
        self.assertEqual(following_post, self.post.text)

    def test_new_post_does_not_appear_for_nonfollowers(self):
        """Проверка: запись пользователя не отображается в ленте тех,
        кто на него не подписан."""
        user_response = self.authorized_client.get(const.URL_FOLLOW)
        user_content = user_response.context['page_obj']
        self.assertNotIn(self.post, user_content)
