from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.utils.dateparse import parse_date
from django.contrib import messages
from .models import Veicolo, Targa, Revisione, TargaAttiva, TargaRestituita
import datetime
from datetime import date, datetime
from django.db import transaction
from django.views.decorators.csrf import csrf_exempt    

def home(request):
    return render(request,'hello/home.html')

def veicolo(request):
    veicoli = Veicolo.objects.all().order_by('numero_telaio')
    return render(request,'hello/veicolo.html' ,{'veicoli': veicoli})

def targa(request):
    targhe = Targa.objects.all().order_by('targa')
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

        targhe = Targa.objects.all().order_by('targa')

        if targa_query:
            targhe = targhe.filter(targa__icontains=targa_query)
        if data_emissione_query:
            try:
                # Prova a convertire la data di emissione al formato del database
                data_emissione_query = datetime.strptime(data_emissione_query, '%Y-%m-%d').date()
                targhe = targhe.filter(data_emissione=data_emissione_query)
            except ValueError:
                pass  # Ignora il filtro se la data non è valida
        if stato_query:
            if stato_query == 'Attiva':
                targhe = targhe.filter(targaattiva__isnull=False)
            elif stato_query == 'Restituita':
                targhe = targhe.filter(targarestituita__isnull=False)
        if data_restituzione_query:
            try:
             # Prova a convertire la data di restituzione al formato del database
                data_restituzione_query = datetime.strptime(data_restituzione_query, '%Y-%m-%d').date()
                targhe = targhe.filter(targarestituita__data_restituzione=data_restituzione_query)
            except ValueError:
                pass  # Ignora il filtro se la data non è valida

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

        veicoli = Veicolo.objects.all().order_by('numero_telaio')

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
    revisioni = Revisione.objects.all().order_by('targa')
    return render(request,'hello/revisione.html' ,{'revisioni': revisioni})

def filtra_revisioni(request):
    if request.method == "GET":
        # Ottieni i parametri di filtro dalla richiesta
        targa = request.GET.get('targa', '')
        data_revisione = request.GET.get('data_revisione', '')
        stato = request.GET.get('stato', '')
        motivazione = request.GET.get('motivazione', '')

        # Filtro base senza condizioni (se non specificato)
        revisioni = Revisione.objects.all().order_by('targa__targa', 'numero_revisione')

        # Applica i filtri solo se i parametri sono specificati
        if targa:
            revisioni = revisioni.filter(targa__targa__icontains=targa)
        if data_revisione:
            revisioni = revisioni.filter(data_revisione=data_revisione)
        if stato:
            revisioni = revisioni.filter(stato=stato)
        if motivazione and motivazione != "NULL":  # Assicurati di gestire l'opzione "NULL" del menu
            revisioni = revisioni.filter(motivazione=motivazione)

        # Costruzione della lista dei dettagli delle revisioni
        revisioni_dettagli = []
        for rev in revisioni:
            revisione_info = {
                'targa': rev.targa.targa,
                'numero_revisione': rev.numero_revisione,
                'data_revisione': rev.data_revisione.strftime('%d/%m/%Y') if rev.data_revisione else '',
                'stato': rev.stato,
                'motivazione': rev.motivazione if rev.motivazione else ''
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
            return redirect('veicolo')

        # Controllo sulla data di produzione
        if data_produzione > str(date.today()):
            messages.error(request, "La data di produzione non può essere successiva alla data odierna.")
            return redirect('veicolo')

        # Creazione del veicolo
        try:
            veicolo = Veicolo(numero_telaio=numero_telaio, marca=marca, modello=modello, data_produzione=data_produzione)
            veicolo.save()
            messages.success(request, "Veicolo aggiunto con successo!")
        except Exception as e:
            messages.error(request, f"Errore durante l'aggiunta del veicolo: {e}")
        
        return redirect('veicolo')
    return render(request, 'hello/veicolo.html')

def aggiungi_targa(request):
    if request.method == 'POST':
        targa = request.POST.get('targa')
        data_emissione = request.POST.get('dataEm')
        numero_telaio = request.POST.get('telaio')

        targa = targa.upper()

        # Controlli sulla targa
        if not targa or len(targa) != 7 or not targa[:2].isalpha() or not targa[2:5].isdigit() or not targa[5:].isalpha():
            messages.error(request, "La targa deve essere composta da 2 lettere, 3 numeri e 2 lettere.")
            return redirect('targa')

        prima_lettera = targa[0].upper()
        if prima_lettera not in 'ABCDEFG':
            messages.error(request, "La prima lettera della targa deve essere compresa tra A e G.")
            return redirect('targa')

        try:
            data_emissione = datetime.strptime(data_emissione, '%Y-%m-%d')
        except ValueError:
            messages.error(request, "Data di emissione non valida.")
            return redirect('targa')

        # Controlli sulla prima lettera e la data di emissione
        if prima_lettera == 'A' and not (datetime(1994, 1, 1) <= data_emissione <= datetime(1997, 12, 31)):
            messages.error(request, "La data di emissione per la lettera A deve essere tra 01/01/1994 e 31/12/1997.")
            return redirect('targa')
        if prima_lettera == 'B' and not (datetime(1998, 1, 1) <= data_emissione <= datetime(2001, 12, 31)):
            messages.error(request, "La data di emissione per la lettera B deve essere tra 01/01/1998 e 31/12/2001.")
            return redirect('targa')
        if prima_lettera == 'C' and not (datetime(2002, 1, 1) <= data_emissione <= datetime(2005, 12, 31)):
            messages.error(request, "La data di emissione per la lettera C deve essere tra 01/01/2002 e 31/12/2005.")
            return redirect('targa')
        if prima_lettera == 'D' and not (datetime(2006, 1, 1) <= data_emissione <= datetime(2009, 12, 31)):
            messages.error(request, "La data di emissione per la lettera D deve essere tra 01/01/2006 e 31/12/2009.")
            return redirect('targa')
        if prima_lettera == 'E' and not (datetime(2010, 1, 1) <= data_emissione <= datetime(2014, 12, 31)):
            messages.error(request, "La data di emissione per la lettera E deve essere tra 01/01/2010 e 31/12/2014.")
            return redirect('targa')
        if prima_lettera == 'F' and not (datetime(2015, 1, 1) <= data_emissione <= datetime(2018, 12, 31)):
            messages.error(request, "La data di emissione per la lettera F deve essere tra 01/01/2015 e 31/12/2018.")
            return redirect('targa')
        if prima_lettera == 'G' and data_emissione < datetime(2019, 1, 1):
            messages.error(request, "La data di emissione per la lettera G deve essere dal 01/01/2019 in poi.")
            return redirect('targa')

        # Verifica che il numero di telaio esista e che non abbia già una targa assegnata
        try:
            veicolo = Veicolo.objects.get(numero_telaio=numero_telaio)
        except Veicolo.DoesNotExist:
            messages.error(request, "Il numero di telaio inserito non esiste.")
            return redirect('targa')

        if TargaAttiva.objects.filter(numero_telaio=numero_telaio).exists():
            messages.error(request, "Il veicolo ha già una targa assegnata.")
            return redirect('targa')

        # Verifica che la data di emissione non sia antecedente alla data di produzione del veicolo
        dp = veicolo.data_produzione.strftime('%Y-%m-%d')
        data_produzione = datetime.strptime(dp, '%Y-%m-%d')
        if data_emissione < data_produzione:
            messages.error(request, "La data di emissione della targa non può essere antecedente alla data di produzione del veicolo.")
            return redirect('targa')

        # Creazione della targa
        try:    
            nuova_targa = Targa(targa=targa, data_emissione=data_emissione)
            nuova_targa.save()
            nuova_targa_attiva = TargaAttiva(targa_id=targa, numero_telaio_id=numero_telaio)
            nuova_targa_attiva.save()
            messages.success(request, "Targa aggiunta con successo!")
        except Exception as e:
            messages.error(request, f"Errore durante l'aggiunta della targa: {e}")

        return redirect('targa')
    return render(request, 'hello/targa.html')


def aggiungi_revisione(request):
    if request.method == 'POST':
        targa_input = request.POST.get('targa1')
        data_ultima_revisione = request.POST.get('dataRev')
        stato = request.POST.get('mostra_div')
        menu = request.POST.get('menu')

        # Controllo che la targa esista
        try:
            targa = Targa.objects.get(targa=targa_input)
        except Targa.DoesNotExist:
            messages.error(request, "La targa non esiste.")
            return redirect('revisione')

        # Conversione della data
        try:
            data_ultima_revisione_dt = datetime.strptime(data_ultima_revisione, "%Y-%m-%d").date()
        except ValueError:
            messages.error(request, "La data dell'ultima revisione non è valida.")
            return redirect('revisione')

        # Controllo che la data dell'ultima revisione non sia nel futuro
        if data_ultima_revisione_dt > datetime.now().date():
            messages.error(request, "La data dell'ultima revisione non può essere nel futuro.")
            return redirect('revisione')

        # Controllo che la data dell'ultima revisione non sia antecedente alla data della revisione precedente
        ultime_revisioni = Revisione.objects.filter(targa=targa).order_by("-numero_revisione")
        if ultime_revisioni.exists():
            ultima_revisione = ultime_revisioni.first()
            if data_ultima_revisione_dt <= ultima_revisione.data_revisione:
                messages.error(request, "La data dell'ultima revisione non può essere antecedente alla revisione precedente.")
                return redirect('revisione')

        # Determinazione del numero di revisione
        try:
            numero_revisione = 1
            if ultime_revisioni.exists():
                numero_revisione = ultime_revisioni.first().numero_revisione + 1  # Conversione in intero

            # Conversione dello stato
            stato_db = "positivo" if stato == 'true' else "negativo"

            # Se la revisione non è superata, la motivazione non può essere vuota
            if stato == 'false' and (not menu or menu == ""):
                messages.error(request, "Se la revisione non è superata, deve essere fornita una motivazione.")
                return redirect('revisione')

            revisione = Revisione(
                targa=targa,
                data_revisione=data_ultima_revisione_dt,
                stato=stato_db,
                motivazione=menu if stato_db == "negativo" else None,
                numero_revisione=numero_revisione
            )
            revisione.save()
            messages.success(request, "Revisione aggiunta con successo!")
        except Exception as e:
            messages.error(request, f"Errore durante l'aggiunta della revisione: {str(e)}")

        return redirect('revisione')
    return render(request, 'hello/revisione.html')

@csrf_exempt
def modifica_veicolo(request):
    if request.method == 'POST':
        numero_telaio_old = request.POST.get('numero_telaio_old')
        numero_telaio_new = request.POST.get('numero_telaio')
        marca = request.POST.get('marca')
        modello = request.POST.get('modello')
        data_produzione = request.POST.get('data_produzione')

        # Convertire la data dal formato YYYY-MM-DD a un formato compatibile
        try:
            data_produzione_dt = datetime.strptime(data_produzione, '%Y-%m-%d')
            data_produzione_formattata = data_produzione_dt.strftime('%Y-%m-%d')
        except ValueError:
            return JsonResponse({'success': False, 'message': 'Formato della data di produzione non valido.'})

        # Controllo lunghezza numero_telaio
        if len(numero_telaio_new) != 17:
            return JsonResponse({'success': False, 'message': 'Il numero di telaio deve avere 17 caratteri.'})

        # Controllo data di produzione
        data_min = datetime(1994, 1, 1)
        data_max = datetime.now()

        if data_produzione_dt < data_min or data_produzione_dt > data_max:
            return JsonResponse({'success': False, 'message': 'La data di produzione deve essere tra 01-01-1994 e la data odierna.'})

        # Controllo data di produzione con data di emissione della targa
        try:
            targa_attiva = TargaAttiva.objects.get(numero_telaio_id=numero_telaio_old)
            if data_produzione_dt > targa_attiva.data_emissione:
                return JsonResponse({'success': False, 'message': 'La data di produzione non può essere successiva alla data di emissione della targa.'})
        except TargaAttiva.DoesNotExist:
            # Se non viene trovata una targa attiva, non mostrare errore e continua l'operazione
            pass

        # Verifica se il numero di telaio nuovo esiste già
        if numero_telaio_old != numero_telaio_new:
            if Veicolo.objects.filter(numero_telaio=numero_telaio_new).exists():
                return JsonResponse({'success': False, 'message': 'Numero di telaio nuovo già esistente.'})

        try:
            with transaction.atomic():
                # Ottieni il veicolo esistente
                veicolo_esistente = get_object_or_404(Veicolo, numero_telaio=numero_telaio_old)

                # Elimina il veicolo esistente
                veicolo_esistente.delete()
                
                # Aggiorna il veicolo con la nuova PK
                veicolo_nuovo = Veicolo(
                    numero_telaio=numero_telaio_new,
                    marca=marca,
                    modello=modello,
                    data_produzione=data_produzione_formattata
                )
                veicolo_nuovo.save()

                # Aggiorna la targa attiva se esiste
                try:
                    targa_attiva = TargaAttiva.objects.get(numero_telaio_id=numero_telaio_old)
                    targa_attiva.numero_telaio_id = numero_telaio_new
                    targa_attiva.save()
                except TargaAttiva.DoesNotExist:
                    pass

                # Aggiorna la targa restituita se esiste
                try:
                    targa_restituita = TargaRestituita.objects.get(numero_telaio_id=numero_telaio_old)
                    targa_restituita.numero_telaio_id = numero_telaio_new
                    targa_restituita.save()
                except TargaRestituita.DoesNotExist:
                    pass

            return JsonResponse({'success': True, 'message': 'Veicolo modificato con successo.'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': f'Errore nella modifica del veicolo: {e}'})
    else:
        return JsonResponse({'success': False, 'message': 'Metodo non consentito.'})
    
@csrf_exempt
def elimina_veicolo(request):
    if request.method == 'POST':
        numero_telaio = request.POST.get('numero_telaio')

        try:
            veicolo = get_object_or_404(Veicolo, numero_telaio=numero_telaio)
            veicolo.delete()
            messages.success(request, 'Veicolo eliminato con successo.')
            response = {'success': True}
        except Exception as e:
            messages.error(request, f'Errore nell\'eliminazione del veicolo: {e}')
            response = {'success': False, 'message': str(e)}
        
        return JsonResponse(response)
    else:
        return JsonResponse({'success': False, 'message': 'Metodo non consentito.'})


def modifica_targa(request):
    if request.method == 'POST':
        targa = request.POST.get('targa')
        nuovo_targa = request.POST.get('nuovo_targa')
        data_emissione_str = request.POST.get('data_emissione')
        stato = request.POST.get('stato')
        numero_telaio = request.POST.get('numero_telaio')
        data_restituzione_str = request.POST.get('data_restituzione')

        # Converti le stringhe delle date in oggetti datetime
        try:
            data_emissione = datetime.strptime(data_emissione_str, "%d-%m-%Y").date()
        except ValueError:
            return JsonResponse({'success': False, 'message': 'Data di emissione non valida'})

        data_restituzione = None
        if data_restituzione_str:
            try:
                data_restituzione = datetime.strptime(data_restituzione_str, "%d-%m-%Y").date()
            except ValueError:
                return JsonResponse({'success': False, 'message': 'Data di restituzione non valida'})

        # Controlli sulle date
        if not (datetime(1994, 1, 1).date() <= data_emissione <= datetime.now().date()):
            return JsonResponse({'success': False, 'message': 'Data di emissione non valida'})

        if data_restituzione and not (data_emissione <= data_restituzione <= datetime.now().date()):
            return JsonResponse({'success': False, 'message': 'Data di restituzione non valida'})

        # Controlli sul collegamento tra prima lettera della targa e data di emissione
        lettera_iniziale = nuovo_targa[0].upper()
        date_ranges = {
            'A': (datetime(1994, 1, 1).date(), datetime(1997, 12, 31).date()),
            'B': (datetime(1998, 1, 1).date(), datetime(2001, 12, 31).date()),
            'C': (datetime(2002, 1, 1).date(), datetime(2005, 12, 31).date()),
            'D': (datetime(2006, 1, 1).date(), datetime(2009, 12, 31).date()),
            'E': (datetime(2010, 1, 1).date(), datetime(2014, 12, 31).date()),
            'F': (datetime(2015, 1, 1).date(), datetime(2018, 12, 31).date()),
            'G': (datetime(2019, 1, 1).date(), datetime.now().date()),
        }

        if lettera_iniziale not in date_ranges or not (date_ranges[lettera_iniziale][0] <= data_emissione <= date_ranges[lettera_iniziale][1]):
            return JsonResponse({'success': False, 'message': f'Data di emissione non valida per la targa che inizia con {lettera_iniziale}'})

        # Ottieni il veicolo
        veicolo = get_object_or_404(Veicolo, numero_telaio=numero_telaio)
        if data_emissione < veicolo.data_produzione:
            return JsonResponse({'success': False, 'message': 'Data di emissione non può essere minore della data di produzione del veicolo'})
        if data_restituzione and data_restituzione < data_emissione:
            return JsonResponse({'success': False, 'message': 'Data di restituzione non può essere minore della data di emissione'})
        if data_restituzione and data_restituzione < veicolo.data_produzione:
            return JsonResponse({'success': False, 'message': 'Data di restituzione non può essere minore della data di produzione del veicolo'})

        # Controlli sullo stato
        if stato == 'Attiva' and data_restituzione:
            return JsonResponse({'success': False, 'message': 'Una targa attiva non può avere una data di restituzione'})
        if stato == 'Restituita' and not data_restituzione:
            return JsonResponse({'success': False, 'message': 'Una targa restituita deve avere una data di restituzione'})

        # Aggiorna la targa
        try:
            with transaction.atomic():
                # Ottieni la targa esistente
                targa_esistente = get_object_or_404(Targa, targa=targa)

                # Crea la nuova targa
                targa_nuova = Targa(
                    targa=nuovo_targa,
                    data_emissione=data_emissione
                )
                targa_nuova.save()

                # Aggiorna la targa attiva o restituita se esiste
                if TargaAttiva.objects.filter(targa=targa_esistente).exists():
                    if stato == 'Attiva':
                        TargaAttiva.objects.filter(targa=targa_esistente).delete()
                        TargaAttiva.objects.create(targa=targa_nuova, numero_telaio=veicolo)
                    else:
                        TargaAttiva.objects.filter(targa=targa_esistente).delete()
                        TargaRestituita.objects.create(targa=targa_nuova, numero_telaio=veicolo, data_restituzione=data_restituzione)
                elif TargaRestituita.objects.filter(targa=targa_esistente).exists():
                    TargaRestituita.objects.filter(targa=targa_esistente).delete()
                    TargaRestituita.objects.create(targa=targa_nuova, numero_telaio=veicolo, data_restituzione=data_restituzione)

                # Elimina la targa esistente
                

            return JsonResponse({'success': True, 'message': 'Targa modificata con successo.'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': f'Errore nella modifica della targa: {e}'})
    else:
        return JsonResponse({'success': False, 'message': 'Metodo non consentito.'})


def elimina_targa(request):
    if request.method == 'POST':
        targa = request.POST.get('targa')
        targa_obj = get_object_or_404(Targa, targa=targa)
        
        try:
            TargaAttiva.objects.filter(targa=targa).delete()
            TargaRestituita.objects.filter(targa=targa).delete()
            targa_obj.delete()
            return JsonResponse({'status': 'success', 'message': 'Targa eliminata con successo.'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': f'Errore nell\'eliminazione della targa: {e}'})

    return JsonResponse({'status': 'error', 'message': 'Metodo non consentito.'})


@csrf_exempt
def modifica_revisione(request):
    if request.method == 'POST':
        try:
            # Recupera i dati dalla richiesta POST
            targa_str = request.POST.get('targa')
            print(f"Targa: {targa_str}")
            numero_revisione = request.POST.get('numero_revisione')
            print(f"Numero Revisione: {numero_revisione}")
            data_revisione = request.POST.get('data_revisione')
            print(f"Data Revisione: {data_revisione}")
            stato = request.POST.get('stato')
            print(f"Stato: {stato}")
            motivazione = request.POST.get('motivazione')
            print(f"Motivazione: {motivazione}")

            # Verifica che tutti i parametri siano presenti
            if not targa_str or not numero_revisione or not data_revisione:
                raise ValueError("Tutti i parametri devono essere forniti.")

            # Converti la data se necessario
            try:
                data_revisione = datetime.strptime(data_revisione, '%Y-%m-%d').date()
            except ValueError:
                raise ValueError("Formato della data non valido. Usa YYYY-MM-DD.")

            # Recupera l'istanza della Targa
            targa = get_object_or_404(Targa, targa=targa_str)

            # Recupera la revisione da aggiornare
            revisione = get_object_or_404(Revisione, targa=targa, numero_revisione=numero_revisione)
            revisione_id = revisione.id

            print(f"Revisione trovata: ID {revisione_id}")

            # Validazione: se lo stato è positivo, la motivazione deve essere vuota
            if stato == 'positivo' and motivazione:
                messages.error(request, "Non è possibile specificare una motivazione se lo stato è positivo.")
                return JsonResponse({'success': False, 'error': 'La motivazione non deve essere specificata se lo stato è positivo.'})

            # Validazione: se lo stato è negativo, la motivazione è obbligatoria
            if stato == 'negativo' and not motivazione:
                messages.error(request, "È necessario specificare una motivazione se lo stato è negativo.")
                return JsonResponse({'success': False, 'error': 'La motivazione è obbligatoria se lo stato è negativo.'})

            # Verifica che la revisione attuale non sia incoerente con le revisioni precedenti
            revisione_precedente = Revisione.objects.filter(
                targa=targa,
                numero_revisione__lt=numero_revisione
            ).order_by('-numero_revisione').first()

            if revisione_precedente:
                print(f"Revisione precedente trovata: ID {revisione_precedente.id}, Numero Revisione: {revisione_precedente.numero_revisione}")
                if data_revisione < revisione_precedente.data_revisione:
                    messages.error(request, "La data della revisione non può essere precedente alla revisione precedente.")
                    return JsonResponse({'success': False, 'error': 'Data revisione non valida.'})

            # Verifica che la revisione attuale non sia incoerente con le revisioni successive
            revisione_successiva = Revisione.objects.filter(
                targa=targa,
                numero_revisione__gt=numero_revisione
            ).order_by('numero_revisione').first()

            if revisione_successiva:
                print(f"Revisione successiva trovata: ID {revisione_successiva.id}, Numero Revisione: {revisione_successiva.numero_revisione}")
                if data_revisione > revisione_successiva.data_revisione:
                    messages.error(request, "La data della revisione non può essere successiva alla revisione successiva.")
                    return JsonResponse({'success': False, 'error': 'Data revisione non valida.'})

            # Aggiorna i campi della revisione
            revisione.data_revisione = data_revisione
            revisione.stato = stato
            revisione.motivazione = motivazione if stato == 'negativo' else ''

            # Salva le modifiche nel database
            revisione.save()

            # Aggiungi un messaggio di successo
            messages.success(request, "Revisione aggiornata con successo.")
            return JsonResponse({'success': True})

        except Exception as e:
            print(f"Errore durante l'aggiornamento della revisione: {str(e)}")
            messages.error(request, "Si è verificato un errore durante l'aggiornamento della revisione.")
            return JsonResponse({'success': False, 'error': str(e)})

    # Se il metodo non è POST, aggiungi un messaggio di errore
    messages.error(request, "Metodo non valido.")
    return JsonResponse({'success': False, 'error': 'Metodo non valido'})




def elimina_revisione(request):
    print("Funzione elimina_revisione chiamata")
    if request.method == 'POST':
        try:
            # Recupera i parametri targa e numero revisione dal POST
            targa = request.POST.get('targa')
            numero_revisione = int(request.POST.get('numero_revisione'))

            print(f"Ricevuto: targa={targa}, numero_revisione={numero_revisione}")

            # Usa una transazione per assicurarti che tutte le operazioni siano atomiche
            with transaction.atomic():
                # Cerca la revisione da eliminare usando targa e numero revisione
                revisione = get_object_or_404(Revisione, targa=targa, numero_revisione=numero_revisione)

                # Elimina la revisione
                revisione.delete()

                # Aggiorna il numero di revisione per le revisioni successive
                revisioni_successive = Revisione.objects.filter(targa=targa, numero_revisione__gt=numero_revisione)
                for rev in revisioni_successive:
                    rev.numero_revisione -= 1
                    rev.save()

            # Risposta di successo
            return JsonResponse({'success': True})

        except Exception as e:
            # In caso di errore, restituisci una risposta di errore
            return JsonResponse({'success': False, 'error': str(e)})

    # Se il metodo non è POST, restituisci un errore
    return JsonResponse({'success': False, 'error': 'Metodo non valido'})