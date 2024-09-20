from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import ListView

#from .models import UsbStor


def index(request):
    return HttpResponse('<html><body><dl><dt><a href="usbstor">UsbStor</a></dt><dd>Зареєстровані зовнішні носії інформації</dd></dl></body></html>')

#class UsbStorView(ListView):
#    model = UsbStor