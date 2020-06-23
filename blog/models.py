from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from userData.models import UserData
import datetime

DEFAULT_USER_ID = 0
MAX_POST_LENGTH = 500

class Post(models.Model):
    text = models.CharField(max_length=MAX_POST_LENGTH)
    pub_date = models.DateTimeField('date published')
    author = models.ForeignKey(UserData, on_delete=models.CASCADE)
    likes = models.IntegerField()

    def __str__(self):
        return self.text

    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)


class LikedPosts(models.Model):
    user = models.ForeignKey(UserData, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)