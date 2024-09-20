from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import ListView

#from .models import UsbStor


def index(request):
    html_resp = """<html>
    <body>
        <dl>
            <dt><a href="usbstor">UsbStor</a></dt>
            <dd>Зареєстровані зовнішні носії інформації</dd>
            <dt><a href="host">Host</a></dt>
            <dd>Обліковані АС, АРМ, ПЕОМ</dd>
            <dt><a href="/static/AsCheck.ps1">Windows AS data collector</a></dt>
            <dd>Скрипт збирання інформації АС, АРМ, ПЕОМ</dd>
        </dl>
    </body>
</html>
"""
    return HttpResponse(html_resp)

#class UsbStorView(ListView):
#    model = UsbStor