import re
from datetime import datetime
from django.http import HttpResponse
from django.shortcuts import render

def home(request):
    return render(request, "wfh/home.html")

def about(request):
    return render(request, "wfh/about.html")

def contact(request):
    return render(request, "wfh/contact.html")


def hello_there(request, name):
    return render(
        request,
        'wfh/hello_there.html',
        {
            'name': name,
            'date': datetime.now()
        }
    )