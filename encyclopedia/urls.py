from django.urls import path

from . import views

urlpatterns = [
    path("wiki", views.wiki, name="wiki"),
    path("", views.index, name="index")
]
