from django.shortcuts import render
from .models import Veicolo, Targa, Revisione

def home(request):
    return render(request,'hello/home.html')

def veicolo(request):
    veicoli = Veicolo.objects.all()
    return render(request,'hello/veicolo.html' ,{'veicoli': veicoli})

def targa(request):
    targhe = Targa.objects.all()
    targhe_dettagli = []

    for t in targhe:
        targa_info= {
            'targa': t.targa,
            'data_emissione' : t.data_emissione,
            'stato': 'Attiva' if hasattr(t,'targaattiva') else 'Restituita',
            'numero_telaio': t.targaattiva.veicolo.nummero_telaio if hasattr (t, 'targaattiva') else None,
            'data_restituzione': t.targarestituita.data_restituzione if hasattr(t, 'targarestituita') else None
        }
        targhe_dettagli.append(targa_info)
    return render(request,'hello/targa.html' ,{'targhe_dettagli': targhe_dettagli})

def revisione(request):
    revisioni = Revisione.objects.all()
    return render(request,'hello/revisione.html' ,{'revisioni': revisioni})

def aggiungi(request):
    return render(request, 'hello/aggiungi.html')

