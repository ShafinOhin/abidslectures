from django.urls import path
from . import views


urlpatterns = [
    path('', views.explore, name = 'explore'),
    path('explore', views.explore, name = 'explore'),
    path('pricing', views.pricing, name = 'pricing'),
    path('get_detailed_pricing', views.get_detailed_pricing, name = 'get_detailed_pricing'),
    path('<slug:course_slug>', views.course_details, name = 'course_details'),
]