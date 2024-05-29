from django.urls import path

from . import views


app_name = "account"
urlpatterns = [
    path("contact/", views.contact, name="contact"),
    path("register/", views.signup, name="register"),
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"),
    path("account/<uuid:pk>", views.own_account, name="own_account"),
    path("account/<uuid:pk>/edit/", views.edit_account, name="edit_account"),
]
