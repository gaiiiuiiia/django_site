from django.urls import path
import lists.views as views


urlpatterns = [
    path('unique_list/', views.view_list, name='lists.view_list'),
    path('new', views.new_list, name='lists.new_list'),
]
