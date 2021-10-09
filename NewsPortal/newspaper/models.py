from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
from django.db.models import Sum


class CustomUser(AbstractUser):
    subscribe_category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True, blank=True)


User = get_user_model()


class Author(models.Model):
    user = models.OneToOneField(User, verbose_name='Пользователь', on_delete=models.CASCADE)
    rating = models.IntegerField('Рейтинг', default=0)

    def update_rating(self):
        postRat = self.post_set.aggregate(postRating=Sum('rating'))
        pRat = 0
        pRat += postRat.get('postRating')

        commentRat = self.user.comment_set.aggregate(commentRating=Sum('rating'))
        cRat = 0
        cRat += commentRat.get('commentRating')

        self.rating = pRat*3 + cRat
        self.save()

    def __str__(self):
        return f'{self.user.username}'


class Category(models.Model):
    name = models.CharField('Название', max_length=32, unique=True)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Post(models.Model):
    article = 'A'
    news = 'N'

    CLASSES = [
        (article, 'Статья'),
        (news, 'Новость')
    ]

    author = models.ForeignKey(Author, verbose_name='Автор', on_delete=models.CASCADE)
    type = models.CharField('Тип', max_length=1, choices=CLASSES)
    datetime = models.DateTimeField('Дата', auto_now_add=True)
    category = models.ManyToManyField(Category, verbose_name='Категория', through='PostCategory')
    head = models.CharField('Заголовок', max_length=256)
    text = models.TextField('Текст')
    rating = models.SmallIntegerField('Рейтинг', default=0)

    def __str__(self):
        return f'{self.head}'

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return self.text[:124] + '...'

    def get_absolute_url(self):
        return '/news/'

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    post = models.ForeignKey(Post, verbose_name='Пост', on_delete=models.CASCADE)
    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE)
    text = models.TextField('Текст')
    datetime = models.DateTimeField('Дата', auto_now_add=True)
    rating = models.SmallIntegerField('Рейтинг', default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()