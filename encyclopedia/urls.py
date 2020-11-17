from django.urls import path

from . import views

app_name = 'wiki'
urlpatterns = [
    path("new/", views.new, name = "new"),
    path("wiki/<str:entry>", views.entry, name="entry"),
    path("search/", views.search, name="search"),
    path("", views.index, name="index")
]
