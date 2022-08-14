from django.core.exceptions import ValidationError
from django.shortcuts import redirect
from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpRequest

from lists.forms import ItemForm
from lists.models import Item, List


def home_page(request: HttpRequest) -> HttpResponse:
    form = ItemForm()
    return render(request, 'lists/home.html', {
        'form': form,
    })


def view_list(request: HttpRequest, list_id: int) -> HttpResponse:
    list_ = List.objects.get(id=list_id)
    error = None
    if request.method == 'POST':
        item = Item.objects.create(
            text=request.POST.get('text', ''),
            list=list_
        )
        try:
            item.full_clean()
            item.save()
            return redirect(list_)
        except ValidationError:
            item.delete()
            error = 'You can`t have empty list item'

    return render(request, 'lists/list.html', {
        'list': list_,
        'error': error,
    })


def new_list(request: HttpRequest) -> HttpResponse:
    list_ = List.objects.create()
    text = request.POST.get('text')
    item = Item.objects.create(text=text, list=list_)
    try:
        item.full_clean()
    except ValidationError:
        list_.delete()
        item.delete()
        error = "You can`t have empty list item"
        return render(request, 'lists/home.html', {'error': error})

    item.save()

    return redirect(list_)
