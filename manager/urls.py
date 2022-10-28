from django.urls import path
from . import views


urlpatterns = [
    path('', views.manager_dashboard, name = 'manager_dashboard'),
    path('approve_trans/', views.approve_trans, name = 'approve_trans'),
    path('refresh_order/', views.refresh_order, name = 'refresh_order'),
]