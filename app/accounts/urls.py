from django.urls import path
import accounts.views as views

urlpatterns = [
    path('send_login_email', views.send_login_email, name='accounts.send_login_email'),
    path('login', views.login, name='accounts.login'),
    path('logout', views.logout, name='accounts.logout'),
]
