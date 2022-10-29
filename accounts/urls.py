from django.urls import path
from . import views


urlpatterns = [
    path('register/', views.register, name = 'register'),
    path('login/', views.login, name = 'login'),
    path('logout/', views.logout, name = 'logout'),
    path('activate/<uidb64>/<token>/', views.activate, name = 'activate'),
    path('resetpassword_validate/<uidb64>/<token>/', views.resetpassword_validate, name = 'resetpassword_validate'),
    path('', views.profile, name = 'profile'),
    path('profile/', views.profile, name = 'profile'),
    path('forgotpassword', views.forgotpassword, name = 'forgotpassword'),
    path('resetpassword', views.resetpassword, name = 'resetpassword'),
    path('changepassword',views.changepassword, name = 'changepassword'),
    path('bug_solver',views.bug_solver, name = 'bug_solver'),
]