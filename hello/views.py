from django.shortcuts import render
from .models import Veicolo, Targa, Revisione

def home(request):
    return render(request,'hello/home.html')

def veicolo(request):
    veicoli = Veicolo.objects.all()
    return render(request,'hello/veicolo.html' ,{'veicoli': veicoli})

def targa(request):
    targhe = Targa.objects.all()
    return render(request,'hello/targa.html' ,{'targhe': targhe})

def revisione(request):
    revisioni = Revisione.objects.all()
    return render(request,'hello/revisione.html' ,{'revisioni': revisioni})

def aggiungi(request):
    return render(request, 'hello/aggiungi.html')

