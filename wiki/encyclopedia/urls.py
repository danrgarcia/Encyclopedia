from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/search", views.search, name="search"),
    path("wiki/newpage", views.newpage, name="newpage"),
    path("wiki/random", views.random, name="random"),
    path("wiki/edit/<str:title>", views.edit, name="edit"),
    path("wiki/<str:title>", views.title, name="title")
]