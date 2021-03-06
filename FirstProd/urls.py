"""FirstProd URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from users import views as userviews
from django.contrib.auth import views as authvievs

from django.conf import settings
from django.conf.urls.static import static

from Blog import views as blviews

#https://webdevblog.ru/razrabotka-na-osnove-testov-django-restful-api/,,,,https://webdevblog.ru/sozdanie-django-api-ispolzuya-django-rest-framework-apiview/


urlpatterns = [
    path('admin/', admin.site.urls),
    path('reg/', userviews.register, name='reg'),
    path('profile/', userviews.profile, name='profile'),
    path('user/', authvievs.LoginView.as_view(template_name = 'users/user.html'), name='user'),
    path('exit/', authvievs.LogoutView.as_view(template_name = 'users/exit.html'), name='exit'),
    path('', include('Blog.urls')),
    path('pass-reset/', authvievs.PasswordResetView.as_view(template_name = 'users/pass-reset.html'),
         name='pass-reset'),
    path('password_reset_confirm/<uidb64>/<token>', authvievs.PasswordResetConfirmView.as_view(template_name = 'users/password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('password-reset/done/',
         authvievs.PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'),
         name='password_reset_done'),
    path('password_reset/complete/',
         authvievs.PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'),
         name='password_reset/complete'),
    path('like/', blviews.like_post, name='like_post' ),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    
]
    
   


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
