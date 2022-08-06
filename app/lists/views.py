from django.shortcuts import redirect
from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpRequest

from lists.models import Item


def home_page(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        new_item_text = request.POST.get('item_text')
        Item.objects.create(text=new_item_text)
        return redirect('view_list')

    return render(request, 'lists/home.html')


def view_list(request: HttpRequest) -> HttpResponse:
    context = {
        'items': Item.objects.all(),
    }

    return render(request, 'lists/list.html', context)
