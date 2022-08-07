from django.shortcuts import redirect
from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpRequest

from lists.models import Item, List


def home_page(request: HttpRequest) -> HttpResponse:
    return render(request, 'lists/home.html')


def view_list(request: HttpRequest) -> HttpResponse:
    context = {
        'items': Item.objects.all(),
    }

    return render(request, 'lists/list.html', context)


def new_list(request: HttpRequest) -> HttpResponse:
    list_ = List.objects.create()
    text = request.POST.get('item_text')
    Item.objects.create(text=text, list = list_)

    return redirect('lists.view_list')
