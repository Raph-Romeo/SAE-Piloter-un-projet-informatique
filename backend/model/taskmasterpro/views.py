from django.shortcuts import render
# Create your views here.
from django.http import HttpResponse

def page_vide(request):
    return render(request,'page_vide.html')
