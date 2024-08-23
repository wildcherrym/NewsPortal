from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from django.db.models.functions import Coalesce


class Author(models.Model):
    user_auth = models.OneToOneField(User, on_delete = models.CASCADE)
    rating = models.IntegerField(default=0)

    def updating_rating(self):
        prat = Post.objects.filter(author=self).aggregate(pr=Coalesce(Sum('rating'),0))['pr']
        crat = Comment.objects.filter(user_cm = self.user_auth).aggregate(cr=Coalesce(Sum('rating'),0))['cr']
        pcrat = Comment.objects.filter(post_sm__author=self).aggregate(pcr=Coalesce(Sum('rating'),0))['pcr']
        self.rating = prat*3+crat+pcrat
        self.save()





class Category(models.Model):
    name_cat = models.CharField(max_length = 64, unique=True)


news = 'NW'
article = "AR"
cat_choice = (
    (news, 'Новость'),
    (article, 'Статья'),
)


class Post(models.Model):
    author = models.ForeignKey(Author, on_delete = models.CASCADE)
    choice_cat = models.CharField(max_length = 2, choices = cat_choice,
                            default = news)
    date_in_st = models.DateTimeField(auto_now_add = True)
    post_cat = models.ManyToManyField(Category, through = 'PostCategory')
    article = models.CharField(max_length = 128)
    text_st = models.TextField()
    rating = models.IntegerField(default = 0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return self.text_st[:123]+'...'

class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete = models.CASCADE)
    category = models.ForeignKey(Category, on_delete = models.CASCADE)

class Comment(models.Model):
    post_sm = models.ForeignKey(Post, on_delete = models.CASCADE)
    user_cm = models.ForeignKey(User, on_delete = models.CASCADE)
    text_cm = models.TextField()
    date_in_cm = models.DateTimeField(auto_now_add = True)
    rating = models.IntegerField(default = 0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()