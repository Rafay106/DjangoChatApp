from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class UserModel(AbstractUser):
    name = models.CharField(max_length = 90)
    email = models.EmailField(unique = True)
    about = models.TextField(blank = True, null = True)
    avatar = models.ImageField(null=True, default="avatar.svg")

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

class TopicModel(models.Model):
    name = models.CharField(max_length = 100)

    def __str__(self):
        return self.name

class RoomModel(models.Model):
    host         = models.ForeignKey(UserModel, on_delete = models.SET_NULL, null = True)
    topic        = models.ForeignKey(TopicModel, on_delete = models.SET_NULL, null = True)
    name         = models.CharField(max_length = 150)
    description  = models.TextField(null = True, blank = True)
    participants = models.ManyToManyField(UserModel, related_name = 'participants', blank = True)
    updated      = models.DateTimeField(auto_now = True)
    created      = models.DateTimeField(auto_now_add = True)

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.name

    
class MessageModel(models.Model):
    user    = models.ForeignKey(UserModel, on_delete = models.CASCADE)
    room    = models.ForeignKey(RoomModel, on_delete = models.CASCADE)
    body    = models.TextField()
    updated = models.DateTimeField(auto_now = True)
    created = models.DateTimeField(auto_now_add = True)

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return f'{self.body[0:30]}'

