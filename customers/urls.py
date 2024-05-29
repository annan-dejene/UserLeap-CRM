from django.urls import path

from . import views


app_name = "customers"
urlpatterns = [
    path("add/", views.add_records, name="add"),
    path("", views.records, name="customers"),
    path("<int:pk>/", views.record, name="customer"),
    path("<int:pk>/edit/", views.edit, name="edit"),
    path("<int:pk>/delete/", views.delete, name="delete"),
]
