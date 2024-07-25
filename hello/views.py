from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.utils.dateparse import parse_date
from django.contrib import messages
from .models import Veicolo, Targa, Revisione
import datetime


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
        data_restituzione_query = request.GET.get('data_restituzione', '')

        targhe = Targa.objects.all()

        if targa_query:
            targhe = targhe.filter(targa__icontains=targa_query)
        if data_emissione_query:
            targhe = targhe.filter(data_emissione=data_emissione_query)
        if stato_query == '1':  # Attiva
            targhe = targhe.filter(targaattiva__isnull=False)
        elif stato_query == '0':  # Restituita
            targhe = targhe.filter(targarestituita__isnull=False)
            if data_restituzione_query:
                targhe = targhe.filter(targarestituita__data_restituzione=data_restituzione_query)

        targhe_dettagli = []

        for t in targhe:
            targa_info = {
                'targa': t.targa,
                'data_emissione': t.data_emissione,
                'stato': 'Attiva' if hasattr(t, 'targaattiva') else 'Restituita',
                'numero_telaio': t.targaattiva.numero_telaio_id if hasattr(t, 'targaattiva') else None,
                'data_restituzione': t.targarestituita.data_restituzione if hasattr(t, 'targarestituita') else None
            }
            targhe_dettagli.append(targa_info)

        return JsonResponse({'targhe': targhe_dettagli})
    return JsonResponse({'error': 'Invalid request method'}, status=400)

def filtra_veicoli(request):
    if request.method == "GET":
        numero_telaio_query = request.GET.get('numero_telaio', '')
        marca_query = request.GET.get('marca', '')
        modello_query = request.GET.get('modello', '')
        data_produzione_query = request.GET.get('data_produzione', '')

        veicoli = Veicolo.objects.all()

        if numero_telaio_query:
            veicoli = veicoli.filter(numero_telaio__icontains=numero_telaio_query)
        if marca_query:
            veicoli = veicoli.filter(marca__icontains = marca_query)
        if modello_query:  
            veicoli = veicoli.filter(modello__icontains=modello_query)
        if data_produzione_query:
                veicoli = veicoli.filter(data_produzione=data_produzione_query)
        veicoli_dettagli = []
        for veicolo in veicoli:
            veicolo_info = {
                'numero_telaio': veicolo.numero_telaio,
                'marca': veicolo.marca,
                'modello': veicolo.modello,
                'data_produzione': veicolo.data_produzione,
            }
            veicoli_dettagli.append(veicolo_info)
        return JsonResponse({'veicoli': veicoli_dettagli})
    return JsonResponse({'error': 'Invalid request method'}, status=400)
    
def revisione(request):
    revisioni = Revisione.objects.all()
    return render(request,'hello/revisione.html' ,{'revisioni': revisioni})

def filtra_revisioni(request):
    if request.method == "GET":
        targa_query = request.GET.get('targa', '')
        data_revisione_query = request.GET.get('data_revisione', '')
        stato_query = request.GET.get('stato', '')
        #data_produzione_query = request.GET.get('data_produzione', '')

        revisioni = Revisione.objects.all()

        if targa_query:
            revisioni = revisioni.filter(targa__targa__icontains=targa_query)
        if data_revisione_query:
            revisioni = revisioni.filter(revisione__data_revisione = data_revisione_query)

        revisioni_dettagli = []
        for rev in revisioni:
            revisione_info = {
                'targa': rev.targa.targa,
                'numero_revisione': rev.numero_revisione,
                'data_revisione': rev.data_revisione,
                'stato': rev.stato,
                'motivazione': rev.motivazione
            }
            revisioni_dettagli.append(revisione_info)
        return JsonResponse({'revisioni': revisioni_dettagli})
    return JsonResponse({'error': 'Invalid request method'}, status=400)

def aggiungi(request):
    return render(request, 'hello/aggiungi.html')

def aggiungi_veicolo(request):
    if request.method == 'POST':
        numero_telaio = request.POST.get('numTelaio')
        marca = request.POST.get('marca')
        modello = request.POST.get('modello')
        data_produzione = request.POST.get('dataProd')

    
        # Controllo sul numero di telaio
        if len(numero_telaio) != 17 or not numero_telaio.isalnum():
            messages.error(request, "Il numero di telaio deve essere composto da 17 caratteri alfanumerici.")
            return redirect('aggiungi')

        # Controllo sulla data di produzione
        if data_produzione > str(datetime.date.today()):
            messages.error(request, "La data di produzione non può essere successiva alla data odierna.")
            return redirect('aggiungi')

        # Creazione del veicolo
        try:
            veicolo = Veicolo(numero_telaio=numero_telaio, marca=marca, modello=modello, data_produzione=data_produzione)
            veicolo.save()
            messages.success(request, "Veicolo aggiunto con successo!")
        except Exception as e:
            messages.error(request, f"Errore durante l'aggiunta del veicolo: {e}")
        
        return redirect('aggiungi')
    return render(request, 'hello/aggiungi.html')

def aggiungi_targa(request):
    if request.method == 'POST':
        targa = request.POST.get('targa')
        data_emissione = request.POST.get('dataEm')
        numero_telaio = request.POST.get('telaio')

        # Controlli e creazione della targa
        try:
            nuova_targa = Targa(targa=targa, data_emissione=data_emissione, numero_telaio=numero_telaio)
            nuova_targa.save()
            messages.success(request, "Targa aggiunta con successo!")
        except Exception as e:
            messages.error(request, f"Errore durante l'aggiunta della targa: {e}")
        
        return redirect('aggiungi')
    return render(request, 'hello/aggiungi.html')

def aggiungi_revisione(request):
    if request.method == 'POST':
        targa = request.POST.get('targa1')
        data_ultima_revisione = request.POST.get('dataRev')
        stato = request.POST.get('mostra_div')
        menu = request.POST.get('menu')

        # Controlli e creazione della revisione
        try:
            revisione = Revisione(targa=targa, data_ultima_revisione=data_ultima_revisione, stato=stato, menu=menu)
            revisione.save()
            messages.success(request, "Revisione aggiunta con successo!")
        except Exception as e:
            messages.error(request, f"Errore durante l'aggiunta della revisione: {e}")
        
        return redirect('aggiungi')
    return render(request, 'hello/aggiungi.html')
