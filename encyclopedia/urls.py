from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.entry, name="entry"),
    path("search", views.search, name="search"),
    path("newForm", views.newForm, name="newForm"),
    path("wiki/<str:title>/edit", views.editPage, name="edit"),
    path("random_seite", views.random_seite, name="random_seite"),


]
