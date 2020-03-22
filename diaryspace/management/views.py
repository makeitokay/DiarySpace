from django.http import HttpResponse
from django.shortcuts import render


def management_home_view(request):
    return HttpResponse("Hello, world!")