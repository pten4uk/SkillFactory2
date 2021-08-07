from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum


class Author(models.Model):
    polzovatel = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    def update_rating(self):
        postRat = self.post_set.aggregate(postRating=Sum('rating'))
        pRat = 0
        pRat += postRat.get('postRating')

        commentRat = self.polzovatel.comment_set.aggregate(commentRating=Sum('rating'))
        cRat = 0
        cRat += commentRat.get('commentRating')

        self.rating = pRat*3 + cRat
        self.save()


class Category(models.Model):
    name = models.CharField(max_length=32, unique=True)


class Post(models.Model):
    article = 'A'
    news = 'N'
    CLASSES = [
        (article, 'Статья'),
        (news, 'Новость')
    ]
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    _class = models.CharField(max_length=1, choices=CLASSES)
    datetime = models.DateTimeField(auto_now_add=True)
    category = models.ManyToManyField(Category, through='PostCategory')
    head = models.CharField(max_length=256)
    text = models.TextField()
    rating = models.SmallIntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return self.text[:124] + '...'


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    datetime = models.DateTimeField(auto_now_add=True)
    rating = models.SmallIntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()