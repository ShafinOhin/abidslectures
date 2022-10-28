"""abidlectures URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static

from abidlectures import settings
from . import views


urlpatterns = [
    # path('admin/', include('admin_honeypot.urls', namespace = 'admin_honeypot')),
    path('admin/', admin.site.urls),
    path('', views.home, name = 'home'),
    path('accounts/', include('accounts.urls')),
    path('course/', include('course.urls')),
    path('about/', views.about, name = 'about'),
    path('dashboard/', include('dashboard.urls')),
    path('payment/', include('payment.urls')),
    path('manager/', include('manager.urls')),
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
