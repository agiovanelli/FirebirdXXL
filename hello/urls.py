from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path('veicolo/', views.veicolo, name="veicolo"),
    path('targa/', views.targa, name="targa"),
    path('revisione/', views.revisione, name="revisione"),
    path('aggiungi/', views.aggiungi, name="aggiungi"),
    path('filtra_targhe/', views.filtra_targhe, name='filtra_targhe'),
    path('filtra_veicoli/', views.filtra_veicoli, name='filtra_veicoli'),
    path('filtra_revisioni/', views.filtra_revisioni, name='filtra_revisioni')
]