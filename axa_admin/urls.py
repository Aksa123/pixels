"""pixels URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from . import views


urlpatterns = [
    path('test/', views.admin_test, name='admin_test'),
    path('', views.AdminHome.as_view(), name="admin_home"),
    path('photo/list/', views.AdminPhotoList.as_view(), name="admin_photo_list"),
    path('photo/<int:pk>/', views.AdminPhotoDetail.as_view(), name="admin_photo_detail"),
    path('photo/create/', views.AdminPhotoCreate.as_view(), name="admin_photo_create"),
    path('photo/<int:pk>/delete/', views.AdminPhotoDelete.as_view(), name="admin_photo_delete"),
    path('user/list/', views.AdminUserList.as_view(), name="admin_user_list"),
    path('user/<int:pk>/', views.AdminUserDetail.as_view(), name="admin_user_detail"),
    path('user/<int:pk>/delete/', views.AdminUserDelete.as_view(), name="admin_user_delete"),
    path('tag/list/', views.AdminTagList.as_view(), name="admin_tag_list"),
    path('tag/<int:pk>/', views.AdminTagDetail.as_view(), name="admin_tag_detail"),
    path('tag/create/', views.AdminTagCreate.as_view(), name="admin_tag_create"),
    path('tag/<int:pk>/delete/', views.AdminTagDelete.as_view(), name="admin_tag_delete"),

    path('report/<str:table_data>/daily/', views.admin_report_daily, name="admin_report_daily"),
    path('report/<str:table_data>/monthly/', views.admin_report_monthly, name="admin_report_monthly"),

]


