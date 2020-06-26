

from django.contrib import admin
from django.urls import path, include
from . import views
from pixels import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


SITE_ROOT = static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns = [
    path('', views.home, name="home"),
    path('test/<str:param>', views.Test.as_view(), name="test"),
    path('login/', views.Login.as_view(), name="login"),
    path('signup/', views.Signup.as_view(), name="signup"),
    path('logout/', views.logout_view, name="logout"),
    path('profile/<int:user_id>-<str:slug>/', views.profile, name="profile"),
    path("profile/<int:user_id>-<str:slug>/followers/", views.profile_follower, name="profile_follower"),
    path("profile/<int:user_id>-<str:slug>/following/", views.profile_following, name="profile_following"),
    path("profile/<int:user_id>-<str:slug>/favorites/", views.profile_favorite, name="profile_favorite"),
    path("profile/<int:user_id>-<str:slug>/stats/", views.profile_stats, name="profile_stat"),
    path("profile/<int:user_id>-<str:slug>/edit/", views.profile_edit, name="profile_edit"),
    path('upload/', views.upload, name="upload"),
    path('photo/<int:photo_id>/', views.photo_detail, name="photo_detail"),
    path('discover/', views.discover, name="discover"),
    path('search/sorted/<str:sort_by>', views.search_sorted, name="search_sorted"),
    path('search/<str:keyword>/', views.search, name="search"),
    path("update-like/", views.update_like, name="update_like"),
    path("update-favorite/", views.update_favorite, name="update_favorite"),
    path("make-comment", views.make_comment, name="make_comment"),
    path("make-follow", views.make_follow, name="make_follow"),

    # API list
    path("photo-download/<int:photo_id>/<int:width>-<int:height>/", views.photo_download, name="photo_download"),

    # Footer static pages
    path("about/", views.about, name="about")
]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += SITE_ROOT