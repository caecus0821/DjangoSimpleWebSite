"""va_website URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.conf import settings
from website import views

urlpatterns = [
    path('admin/', admin.site.urls),

    #Auth
    path('signup/', views.signupuser, name='signupuser'),
    path('logout/', views.logoutuser, name='logoutuser'),
    path('login/', views.loginuser, name='loginuser'),



    path('current/', views.orderpage, name='orderpage'),
    path('create/', views.createorder, name='createorder'),
    path('', views.home, name='home'),
    path('website/<int:order_pk>', views.vieworder, name='vieworder'),
    path('website/<int:order_pk>/complete', views.completeorder, name='completeorder'),
    path('website/<int:order_pk>/delete', views.deleteorder, name='deleteorder'),
    path('completed/', views.completedorders, name='completedorders'),
]

urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
