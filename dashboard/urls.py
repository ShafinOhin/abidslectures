from django.urls import path
from . import views


urlpatterns = [
    path('', views.dashboard_root, name = 'dashboard'),
    path('path/', views.dashboard_root, name = 'dashboard'),
    path('path/<slug:course_slug>/', views.dashboard_course, name = 'dashboard'),
    path('path/<slug:course_slug>/<slug:unit_slug>/', views.dashboard_unit, name = 'dashboard'),
    path('path/<slug:course_slug>/<slug:unit_slug>/<slug:chapter_slug>/', views.dashboard_chapter, name = 'dashboard'),
    path('path/<slug:course_slug>/<slug:unit_slug>/<slug:chapter_slug>/<slug:video_slug>/', views.dashboard_video, name = 'dashboard'),
    path('action/comment/', views.comment, name = 'comment'),
    path('action/reply/', views.reply, name = 'reply'),
    path('action/like/', views.like, name = 'like'),
    path('action/dislike/', views.dislike, name = 'dislike'),
    path('action/addWatchLater/', views.addWatchLater, name = 'add_watch_later'),
    path('action/removeWatchLater/', views.removeWatchLater, name = 'remove_watch_later'),
]