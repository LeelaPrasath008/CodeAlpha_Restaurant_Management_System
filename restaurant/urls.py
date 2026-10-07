from django.urls import path
from . import views

urlpatterns = [
    path('menu/', views.menu_view, name='menu'),
    path('tables/', views.table_list, name='table-list'),
    path('reservation/', views.create_reservation, name='create-reservation'),
    path('reservation/success/', views.reservation_success, name='reservation-success'),
]