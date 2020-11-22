from django.urls import path

from . import views

app_name = 'wiki'
urlpatterns = [
    path("random/", views.random, name="random"),
    path("save_edit/<str:entry>", views.save_edit, name="save_edit"),
    path("edit/<str:entry>/", views.edit, name="edit"),
    path("new/", views.new, name="new"),
    path("wiki/<str:entry>", views.entry, name="entry"),
    path("search/", views.search, name="search"),
    path("", views.index, name="index")
]
