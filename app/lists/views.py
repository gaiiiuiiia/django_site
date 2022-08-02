from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpRequest


def home_page(request: HttpRequest) -> HttpResponse:
    context = {
        'new_item_text': request.POST.get('item_text'),
    }

    return render(request, 'lists/home.html', context)
