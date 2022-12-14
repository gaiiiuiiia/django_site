from django.urls import path
import lists.views as views


urlpatterns = [
    path('<int:list_id>/', views.view_list, name='lists.view'),
    path('new', views.new_list, name='lists.new'),
    path('user/<str:email>', views.user_list, name='lists.user_list'),
]
