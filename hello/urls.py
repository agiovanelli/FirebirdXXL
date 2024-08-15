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
    path('filtra_revisioni/', views.filtra_revisioni, name='filtra_revisioni'),
    path('aggiungi/veicolo/', views.aggiungi_veicolo, name='aggiungi_veicolo'),
    path('aggiungi_targa/', views.aggiungi_targa, name='aggiungi_targa'),
    path('aggiungi_revisione/', views.aggiungi_revisione, name='aggiungi_revisione'),
    path('modifica_veicolo/', views.modifica_veicolo, name='modifica_veicolo'),
    path('elimina_veicolo/', views.elimina_veicolo, name='elimina_veicolo'),
    path('modifica_targa/', views.modifica_targa, name='modifica_targa'),
    path('elimina_targa/', views.elimina_targa, name='elimina_targa'),
    path('modifica_revisione/', views.modifica_revisione, name='modifica_revisione'),
    path('elimina_revisione/', views.elimina_revisione, name='elimina_revisione')
]