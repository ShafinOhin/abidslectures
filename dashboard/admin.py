from django.contrib import admin

# Register your models here.
from .models import Comment, Reply, Like, Dislike, Watchlater

admin.site.register(Comment)
admin.site.register(Reply)
admin.site.register(Like)
admin.site.register(Dislike)
admin.site.register(Watchlater)