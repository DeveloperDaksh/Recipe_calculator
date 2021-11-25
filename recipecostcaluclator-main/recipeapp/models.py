from django.contrib.auth.models import AbstractUser
from django.db import models


class UserModel(AbstractUser):
    timezone = models.CharField(max_length=50, blank=True)

    class Meta:
        db_table = 'auth_user'


class FeedBack(models.Model):
    user = models.CharField(max_length=225)
    feeling = models.CharField(max_length=225)
    suggestion = models.TextField(blank=True, null=True)
