"""project URL Configuration

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
from django.conf import settings
from django.contrib import admin
from django.urls import include, path 
from django.http import HttpResponse

from .views import (
    main_spa, 
    display_hobbies, 
    add_hobby, 
    delete_hobby,
    signup, 
    login_view, 
    logout_view,
    get_all_users,
    csrf_token_view,
    profile_page,
    update_password,
    send_friend_request,
    get_similar_users,
)

urlpatterns = [
    path('', main_spa, name="home"),
    path('csrf-token/', csrf_token_view, name="csrf_token"),
    path('hobbies/', display_hobbies, name='display-hobbies'),
    path('hobbies/add/', add_hobby, name='add-hobby'),
    path('hobbies/delete/<int:hobby_id>/', delete_hobby, name='delete-hobby'),
    path ('login/',login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path("signup/",signup, name="signup"),
    path ("accounts/", include ("django.contrib.auth.urls")),
    path("users/", get_all_users, name="get_all_users"),
    path('profile/<str:username>/', profile_page, name='profile-page'),
    path('profile/<str:username>/password/', update_password, name='update-password'),
    path('send-friend-request/', send_friend_request, name="send_friend_request"),
    path('similar_users/<int:user_id>/', get_similar_users, name='get_similar_users'),
]
  
