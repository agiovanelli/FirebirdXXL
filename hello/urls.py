from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path('veicolo/', views.veicolo, name="veicolo"),
    path('targa/', views.targa, name="targa"),
    path('revisione/', views.revisione, name="revisione"),
    path('aggiungi/', views.aggiungi, name="aggiungi"),
]