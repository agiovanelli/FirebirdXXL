from django.shortcuts import render
from django.http import JsonResponse
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
            'numero_telaio': t.targaattiva.numero_telaio if hasattr (t, 'targaattiva') else None,
            'data_restituzione': t.targarestituita.data_restituzione if hasattr(t, 'targarestituita') else None
        }
        targhe_dettagli.append(targa_info)
    return render(request,'hello/targa.html' ,{'targhe_dettagli': targhe_dettagli})

def filtra_targhe(request):
    if request.method == "GET":
        targa_query = request.GET.get('targa', '')
        data_emissione_query = request.GET.get('data_emissione', '')
        stato_query = request.GET.get('stato', '')

        targhe = Targa.objects.all()

        if targa_query:
            targhe = targhe.filter(targa__icontains=targa_query)
        if data_emissione_query:
            targhe = targhe.filter(data_emissione=data_emissione_query)
        if stato_query == '1':  # Attiva
            targhe = targhe.filter(targaattiva__isnull=False)
        elif stato_query == '0':  # Restituita
            targhe = targhe.filter(targarestituita__isnull=False)

        targhe_dettagli = []

        for t in targhe:
            targa_info = {
                'targa': t.targa,
                'data_emissione': t.data_emissione,
                'stato': 'Attiva' if hasattr(t, 'targaattiva') else 'Restituita',
                'numero_telaio': t.targaattiva.veicolo.numero_telaio if hasattr(t, 'targaattiva') else None,
                'data_restituzione': t.targarestituita.data_restituzione if hasattr(t, 'targarestituita') else None
            }
            targhe_dettagli.append(targa_info)

        return JsonResponse({'targhe': targhe_dettagli})
    
def revisione(request):
    revisioni = Revisione.objects.all()
    return render(request,'hello/revisione.html' ,{'revisioni': revisioni})

def aggiungi(request):
    return render(request, 'hello/aggiungi.html')

