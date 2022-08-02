from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpRequest

from lists.models import Item


def home_page(request: HttpRequest) -> HttpResponse:

    new_item_text = ''
    if request.method == 'POST':
        new_item_text = request.POST.get('item_text')
        Item.objects.create(text=new_item_text)

    context = {
        'new_item_text': new_item_text,
    }

    return render(request, 'lists/home.html', context)
