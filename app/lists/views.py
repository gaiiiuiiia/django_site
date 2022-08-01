from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpRequest


def home_page(request: HttpRequest) -> HttpResponse:
    return render(request, 'lists/home.html')
