from django.db import models
from django.contrib.auth.models import (AbstractUser, BaseUserManager)

# Create your models here.

class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(
            email=self.normalize_email(email),
        )
        user.is_active = True
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staffuser(self, email, password):
        user = self.create_user(email, password=password)

        user.is_staff = True
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, username, password):
        user = self.create_user(email, password=password)
        
        user.username = username
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class UserModel(AbstractUser):
    first_name = None
    last_name = None
    email = models.EmailField(verbose_name='Email Address', max_length=255, unique = True)
    name = models.CharField(max_length = 90)
    about = models.TextField(blank = True, null = True)
    avatar = models.ImageField(null=True, default="avatar.svg")

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

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
        ordering = ['updated', 'created']

    def __str__(self):
        return f'{self.body[0:30]}'

