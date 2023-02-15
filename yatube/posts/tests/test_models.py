from django.test import TestCase, Client

from posts.models import Group, Post, User, Comment, Follow ,LONG_TEXT
from posts.tests import const


class PostModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username=const.USERNAME)
        cls.author = User.objects.create_user(username=const.OTHER_USER)
        cls.group = Group.objects.create(
            title=const.GROUP1_TITLE,
            slug=const.GROUP1_SLUG,
            description=const.GROUP1_DESCRIPTION,
        )
        cls.post = Post.objects.create(
            author=cls.user,
            text=const.TEXT,
        )
        cls.comment = Comment.objects.create(
            author=cls.user,
            text=const.TEXT,
            post=cls.post
        )
        cls.follow = Follow.objects.create(
            user=cls.user,
            author=cls.author)
        
        
    def test_models_have_correct_object_names(self):
        """Проверка: что у моделей корректно работает __str__, title"""
        fields_posts_group = {
            self.post.text[:LONG_TEXT]: str(self.post),
            self.group.title: str(self.group),
            self.comment.text: str(self.comment),
            const.FOLLOW_STR: str(self.follow)
        }
        for key, value in fields_posts_group.items():
            with self.subTest(value=value):
                self.assertEqual(key, value)
