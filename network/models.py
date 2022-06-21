from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    username = models.CharField(max_length=500, unique=True)
    email = models.CharField(max_length=500)
    password = models.CharField(max_length=500)

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.CharField(max_length=500)
    likes = models.IntegerField(default=0)

    def serialize(self):
            return {
                "likes":self.likes
            }

    timestamp = models.DateTimeField()

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

class Follow(models.Model):
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name="follower")
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name="following")



