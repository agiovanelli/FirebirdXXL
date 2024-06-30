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
    return render(request,'hello/aggiungi.html')
