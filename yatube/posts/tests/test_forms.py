import shutil

from unittest import TestCase

from http import HTTPStatus

from django.test import Client, TestCase, override_settings
from django.urls import reverse
from django import forms

from posts.forms import PostForm
from posts.models import Group, Post, User
from posts.tests import const


@override_settings(MEDIA_ROOT=const.TEMP_MEDIA_ROOT)
class PostCreateFormTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.form = PostForm()
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
        cls.POST_EDIT = reverse(
            const.URL_POST_EDIT,
            kwargs={'post_id': cls.post.pk}
        )

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(const.TEMP_MEDIA_ROOT, ignore_errors=True)

    def setUp(self):
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_create_post(self):
        """Проверка: валидная форма создает запись в Post."""
        posts_count = Post.objects.count()
        form_data = {
            'group': self.group.pk,
            'text': const.TEXT,
            'image': self.post.image
        }
        response = self.authorized_client.post(
            const.URL_POST_CREATE_REV,
            data=form_data,
            follow=True
        )
        self.assertEqual(Post.objects.count(), posts_count + 1)
        self.assertRedirects(response, const.URL_PROFILE_REV)
        self.assertTrue(
            Post.objects.filter(
                text=form_data['text'],
                group=form_data['group'],
                author=self.user,
                image=const.URL_GIF
            ).exists()
        )

    def test_create_post_form(self):
        """Проверка: Создаётся ли новая запись в базе данных, создавая пост"""
        post_count = Post.objects.count()
        form_data = {
            'text': const.TEXT,
            'group': self.group.id
        }
        response = self.authorized_client.post(
            const.URL_POST_CREATE_REV,
            data=form_data,
            follow=True
        )
        post = Post.objects.first()
        self.assertRedirects(
            response, const.URL_PROFILE_REV
        )
        self.assertEqual(Post.objects.count(), post_count + 1)
        self.assertEqual(post.text, form_data['text'])
        self.assertEqual(post.group.id, form_data['group'])
        self.assertEqual(post.author, self.user)

    def test_post_create_page_show_correct_context(self):
        """Проверка: Форма создания поста - post_create."""
        response = self.authorized_client.get(const.URL_POST_CREATE_REV)
        form_fields = {
            'text': forms.fields.CharField,
            'group': forms.models.ModelChoiceField,
        }
        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context['form'].fields[value]
                self.assertIsInstance(form_field, expected)

    def test_edit_show_correct_context(self):
        """Проверка: форма редактирования поста, отфильтрованного по id."""
        response = self.authorized_client.get(self.POST_EDIT)
        form_fields = {
            'text': forms.fields.CharField,
            'group': forms.models.ModelChoiceField,
        }
        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context['form'].fields[value]
                self.assertIsInstance(form_field, expected)

    def test_edit_post_form(self):
        """Проверка: происходит ли изменение поста с post_id в базе данных"""
        post_count = Post.objects.count()
        form_data = {
            'text': const.TEXT,
            'group': self.group2.id
        }
        response = self.authorized_client.post(
            self.POST_EDIT,
            data=form_data,
            follow=True
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(Post.objects.count(), post_count)
        self.assertEqual(self.post.text, form_data['text'])
