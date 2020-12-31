from django.db import models

# Create your models here.
from user.models import MyUser


class Post(models.Model):
    post = models.AutoField(primary_key=True)
    user = models.ForeignKey(MyUser(id), on_delete=models.CASCADE, blank=True, null=False)
    content = models.TextField(blank=True, null=True)
    photo = models.FileField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    hashtag = models.CharField(max_length=1000)
    public = models.CharField(max_length=100)
    feeling = models.CharField(max_length=1000, blank=True, null=True)


class Comment(models.Model):
    comment = models.AutoField(primary_key=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, blank=False, null=False)
    user = models.ForeignKey(MyUser(id), on_delete=models.CASCADE, blank=False, null=False)
    content = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)