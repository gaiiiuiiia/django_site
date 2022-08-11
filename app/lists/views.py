from django.core.exceptions import ValidationError
from django.shortcuts import redirect
from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpRequest

from lists.models import Item, List


def home_page(request: HttpRequest) -> HttpResponse:
    return render(request, 'lists/home.html')


def view_list(request: HttpRequest, list_id: int) -> HttpResponse:
    list_ = List.objects.get(id=list_id)
    context = {
        'list': list_,
    }

    return render(request, 'lists/list.html', context)


def new_list(request: HttpRequest) -> HttpResponse:
    list_ = List.objects.create()
    text = request.POST.get('item_text')
    item = Item.objects.create(text=text, list=list_)
    try:
        item.full_clean()
    except ValidationError:
        list_.delete()
        item.delete()
        error = "You can`t have empty list item"
        return render(request, 'lists/home.html', {'error': error})

    item.save()

    return redirect('lists.view', list_id=list_.id)


def add_list(request: HttpRequest, list_id: int) -> HttpResponse:
    list_ = List.objects.get(id=list_id)
    Item.objects.create(text=request.POST.get('item_text'), list=list_)

    return redirect('lists.view', list_id=list_.id)
