from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.entries, name="entries"),
    path("crearMD/", views.crearMD, name="create"),
    path("randomMD/", views.randomMD, name="random"),
    path("search/", views.search, name="search" ),
    path("edit/<str:title>", views.edit, name= "edit")

]
