from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class MyUser(AbstractUser):
    avatar = models.FileField(blank=True, null=True)
    cover_image = models.FileField(blank=True, null=True)
    birthday = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=100, blank=True, null=True)
    address = models.CharField(max_length=100, blank=True, null=True)
    intro = models.CharField(max_length=1000, blank=True, null=True)


class Follower(models.Model):
    f_id = models.AutoField(primary_key=True)
    main_user = models.ForeignKey(MyUser(id), related_name='main_user', on_delete=models.CASCADE, null=False)
    followres = models.ForeignKey(MyUser(id), related_name='followres', on_delete=models.CASCADE, null=False)
    created_at = models.DateTimeField(auto_now_add=True)


class Conversation(models.Model):
    c_id = models.AutoField(primary_key=True)
    user_1 = models.ForeignKey(MyUser(id), related_name='user_1', on_delete=models.CASCADE, null=False)
    user_2 = models.ForeignKey(MyUser(id), related_name='user_2', on_delete=models.CASCADE, null=False)
    created_at = models.DateTimeField(auto_now_add=True)


class Message(models.Model):
    m_id = models.AutoField(primary_key=True)
    from_user = models.ForeignKey(MyUser(id), on_delete=models.CASCADE, null=False)
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, null=False)
    content = models.TextField(null=False)
    created_at = models.DateTimeField(auto_now_add=True)
