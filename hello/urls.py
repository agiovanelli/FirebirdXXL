from django.urls import path
from hello import views

urlpatterns = [
    path("", views.home, name="home"),
    path("", views.veicolo, name="veicolo"),
    path("", views.targa, name="targa"),
    path("", views.revisione, name="revisione"),
    path("", views.aggiungi, name="aggiungi"),
]