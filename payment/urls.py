from django.urls import path
from . import views


urlpatterns = [
    path('', views.payment, name = 'payment'),
    path('authorize/', views.authorize_payment, name='authorize'),
    path('payment_details/<slug:payment_id>/', views.user_payment_details, name = 'payment_details')
]