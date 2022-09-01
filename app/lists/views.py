from django.shortcuts import redirect
from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpRequest

from accounts.models import User
from lists.forms import ItemForm, ExistingListItemForm, NewListForm
from lists.models import List


def home_page(request: HttpRequest) -> HttpResponse:
    form = ItemForm()
    return render(request, 'lists/home.html', {
        'form': form,
    })


def view_list(request: HttpRequest, list_id: int) -> HttpResponse:
    list_ = List.objects.get(id=list_id)
    form = ExistingListItemForm(list_)
    if request.method == 'POST':
        form = ExistingListItemForm(list_, request.POST)
        if form.is_valid():
            form.save_for_list(list_)
            return redirect(list_)

    return render(request, 'lists/list.html', {
        'list': list_,
        'form': form,
    })


def new_list(request: HttpRequest) -> HttpResponse:
    form = ItemForm(data=request.POST)
    if form.is_valid():
        list_ = List()
        list_.owner = request.user
        list_.save()
        form.save_for_list(list_)
        return redirect(list_)

    return render(request, 'lists/home.html', {
        'form': form,
    })


def new_list2(request: HttpRequest) -> HttpResponse:
    form = NewListForm(data=request.POST)
    form.save(owner=request.user)


def user_list(request: HttpRequest, email: str) -> HttpResponse:
    return render(request, 'lists/user_list.html', {
        'owner': User.objects.get(email=email)
    })
