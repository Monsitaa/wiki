from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.entries, name="entries"),
    path("crearMD/", views.crearMD, name="crearMD"),
    path("randomMD/", views.randomMD, name="randomMD"),
    path("search/", views.search, name="search" )

]
