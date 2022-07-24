from django.urls import path
from . import views


urlpatterns = [
    path('<slug:course_slug>', views.course_dashboard, name = 'course_dashboard'),
]