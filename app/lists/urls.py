from django.urls import path
import lists.views as views


urlpatterns = [
    path('<int:list_id>/', views.view_list, name='lists.view'),
    path('<int:list_id>/add', views.add_list, name='lists.add'),
    path('new', views.new_list, name='lists.new'),
]
