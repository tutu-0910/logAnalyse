from django.http import HttpResponse
from django.shortcuts import render

def gitLogStat(request):
    return render(request, 'index.html')
