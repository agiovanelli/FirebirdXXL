import re
from django.utils.timezone import datetime
from django.http import HttpResponse
from django.shortcuts import render

def home(request):
    return HttpResponse("Hello, Django!")

def hello_there(request):
    print(request.build_absolute_uri()) #optional
    return render(
        request,
        'hello/hello_there.html',
        {
            'date': datetime.now()
        }
    )

def home(request):
    return render(
        request,
        'hello/home.html'
    )

    
# Create your views here.
