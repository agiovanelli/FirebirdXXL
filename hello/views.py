from django.shortcuts import render

def home(request):
    return render(request,'hello/home.html')

def veicolo(request):
    return render(request,'hello/veicolo.html')

def targa(request):
    return render(request,'hello/targa.html')

def revisione(request):
    return render(request,'hello/revisione.html')

def aggiungi(request):
    mostra_div = False

    if request.method == 'POST':
        if 'mostra_div' in request.POST and request.POST['mostra_div'] == 'true':
            mostra_div = True
    
    context = {
        'mostra_div': mostra_div
    }

    return render(request, 'hello/aggiungi.html', context)

