import tempfile
from http import HTTPStatus

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase
from django.urls import reverse

from posts.forms import PostForm
from posts.models import Group, Post, User
from yatube import settings


class PostFormTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        settings.MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)
        cls.form = PostForm()
        cls.user = User.objects.create_user(username='ivan')
        cls.authorized_client = Client()
        cls.authorized_client.force_login(cls.user)

        cls.group = Group.objects.create(
            title='Тестовый заголовок',
            description='Описание',
            slug='test-slug'
        )

        cls.post = Post.objects.create(
            text='Тестовый текст',
            group=cls.group,
            author=cls.user
        )

    def test_create_post(self):
        """Валидная форма создает запись в Post."""
        form_data = {
            'text': 'Тестовый текст',
            'group': self.group.id
        }
        response = self.authorized_client.post(
            reverse('new_post'),
            data=form_data,
            follow=True
        )
        self.assertEqual(Post.objects.count(), 2)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(Post.objects.first().text, form_data['text'])
        self.assertEqual(Group.objects.first().title, self.group.title)

    def test_edit_post(self):
        """ при редактировании поста через форму на странице
        /<username>/<post_id>/edit/ изменяется
         соответствующая запись в базе данных"""
        form_data = {
            'text': 'Тестовый текст',
            'group': self.group.id
        }
        self.authorized_client.post(
            reverse('new_post'),
            data=form_data,
            follow=True
        )
        form_data_edit = {
            'text': 'Тестовый текст',
        }
        response = self.authorized_client.post(
            reverse('post_edit', kwargs={
                'username': self.post.author.username,
                'post_id': self.post.id}),
            data=form_data_edit,
            follow=True
        )

        self.assertRedirects(response, reverse('post', kwargs={
            'username': self.post.author.username, 'post_id': self.post.id}))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(Post.objects.first().text, form_data['text'])

    def test_create_post_with_image(self):
        """Валидная форма создает запись в Post with image."""
        tasks_count = Post.objects.count()
        small_gif = (
            b'\x47\x49\x46\x38\x39\x61\x02\x00'
            b'\x01\x00\x80\x00\x00\x00\x00\x00'
            b'\xFF\xFF\xFF\x21\xF9\x04\x00\x00'
            b'\x00\x00\x00\x2C\x00\x00\x00\x00'
            b'\x02\x00\x01\x00\x00\x02\x02\x0C'
            b'\x0A\x00\x3B'
        )
        uploaded = SimpleUploadedFile(
            name='small.gif',
            content=small_gif,
            content_type='image/gif'
        )
        form_data = {'group': self.group.id,
                     'text': 'test_text',
                     'image': uploaded,
                     }
        response = self.authorized_client.post(
            reverse('new_post'),
            data=form_data,
            follow=True
        )
        self.assertRedirects(response, reverse('index'))
        self.assertEqual(Post.objects.count(), tasks_count + 1)
        self.assertTrue(Post.objects.filter(
            group=self.group).exists())
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(Post.objects.first().image)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(
            Post.objects.filter(
                author=self.post.id,
                text='test_text',
                group=self.group.id,
                image='posts/small.gif'
            ).exists(),
        )
