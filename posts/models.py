from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Group(models.Model):
    title = models.CharField(
        'Заголовок',
        max_length=200,
        help_text='Дайте название заголовку'
    )
    description = models.TextField(
        'Описание',
        help_text='Придумайте название группы'
    )
    slug = models.SlugField(
        'Ссылка',
        unique=True,
        help_text='Укажите адрес для страницы группы'
    )

    class Meta:
        verbose_name = 'Сообщество'
        verbose_name_plural = 'Сообщества'

    def __str__(self):
        return self.title


class Post(models.Model):
    text = models.TextField(
        "Содержание",
        help_text='Придумай содержание'
    )
    pub_date = models.DateTimeField("Дата публикации", auto_now_add=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="posts",
        verbose_name="имя"
    )
    group = models.ForeignKey(
        Group, on_delete=models.SET_NULL, blank=True, null=True,
        related_name="posts", verbose_name="Группа", help_text='Выбери группу'
    )
    image = models.ImageField(upload_to='posts/', blank=True, null=True)

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'

    def __str__(self):
        return self.text


class Comment(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments')
    text = models.TextField(
        max_length=100,
        verbose_name='Текст комментария',
        help_text='Добавьте комментарий')
    created = models.DateTimeField('date published', auto_now_add=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return self.text[0:15]


class Follow(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name="follower",
        verbose_name='Подписчики'
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name="following",
        verbose_name='Подписки'
    )

    class Meta:
        verbose_name = 'Follower'
        verbose_name_plural = 'Followers'
