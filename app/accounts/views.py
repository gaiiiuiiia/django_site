import os

import django.contrib.auth.views as django_views
from django.contrib import auth, messages
from django.core.mail import send_mail
from django.http import HttpResponse, HttpRequest
from django.shortcuts import redirect
from django.urls import reverse

from accounts.models import Token
from lib.helper_functions import url_with_querystring


def send_login_email(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        email = request.POST.get('email')
        token = Token.objects.create(email=email)
        url = request.build_absolute_uri(url_with_querystring(reverse('accounts.login'), token=token.uid))
        send_mail_counts = send_mail(
            'Your login link',
            f'Use this link to login on dj-first.my\n\n{url}',
            os.environ.get('EMAIL_HOST_USER'),
            [email]
        )
        messages.add_message(request, messages.SUCCESS, 'Mail successfully send') if send_mail_counts \
            else messages.add_message(request, messages.WARNING, 'Email was not send')

    return redirect(reverse('home'))


def login(request: HttpRequest) -> HttpResponse:
    user = auth.authenticate(uid=request.GET.get('token'))
    if user:
        auth.login(request, user)
    return redirect(reverse('home'))


def logout(request: HttpRequest) -> HttpResponse:
    django_views.auth_logout(request)
    return redirect(reverse('home'))
