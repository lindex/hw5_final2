from django.core.cache import cache
from django.test import TestCase, Client
from django.urls import reverse

from posts.models import User, Group, Post


class PostsPagesTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='test_username')
        cls.guest_client = Client()
        cls.group = Group.objects.create(
            title='test-group',
            slug='test-slug',
            description='Описание тестовой группы',
        )

    def test_cache(self):
        """Тестирование кеширования гл. страницы"""
        response_first = self.guest_client.get(
            reverse('index'))
        uncached_post = Post.objects.create(
            text='Некешированный пост',
            group=self.group,
            author=self.user)
        self.assertNotContains(response_first, uncached_post.text)
        cache.clear()
        response_second = self.guest_client.get(
            reverse('index'))
        self.assertContains(response_second, uncached_post.text)
