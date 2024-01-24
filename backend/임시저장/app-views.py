#app-view.py
from django.shortcuts import render#기존
from django.http import HttpResponse #Response 전달해주는 모듈

# Create your views here.
def main(request):
    context={}
    return render(request, 'main.html', context)


def listing(request):
    context = {}
    return render(request, 'listing.html', context)


def searching(request):
    context = {}
    return render(request, 'searching.html', context)
