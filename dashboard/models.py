from pyexpat import model
from django.db import models
from accounts.models import Account

from course.models import Course, Video

# Create your models here.

# class LastWatched(models.Model):
#     course = models.ForeignKey(Course, on_delete = models.CASCADE)
#     user = models.ForeignKey(Account, on_delete = models.CASCADE)
#     last_video = models.ForeignKey(Video, on_delete = models.SET_NULL, blank = true, null = T)


class Like(models.Model):
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    user = models.ForeignKey(Account, on_delete=models.CASCADE)

class Dislike(models.Model):
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    user = models.ForeignKey(Account, on_delete=models.CASCADE)

class Watchlater(models.Model):
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    user = models.ForeignKey(Account, on_delete=models.CASCADE)

class Comment(models.Model):
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    comment_content = models.TextField(max_length = 300, blank=True, null=True)
    comment_date = models.DateField(auto_now_add=True)

class Reply(models.Model):
    reply_to = models.ForeignKey(Comment, on_delete=models.CASCADE)
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    reply_content = models.TextField(max_length = 300, blank = True, null = True)
    reply_date = models.DateField(auto_now_add=True)
