from django.urls import path
from . import views

urlpatterns = [
    path("", views.homePage, name="index"),
    path("register/", views.register, name="register"),
    path("login/", views.loginClient, name="login"),
    path("logout/", views.logoutClient, name="logout"),
]