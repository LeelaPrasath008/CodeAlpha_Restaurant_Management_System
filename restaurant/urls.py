from django.urls import path
from . import views

urlpatterns = [
    path('menu/', views.menu_view, name='menu'),
    path('tables/', views.table_list, name='table-list'),
    path('reservation/', views.create_reservation, name='create-reservation'),
    path('reservation/success/', views.reservation_success, name='reservation-success'),
    path('', views.home, name='home'),
    path('orders/', views.create_order, name='create-order'),
    path('orders/success/', views.order_success, name='order-success'),
    path('orders/history/', views.order_list, name='order-list'),
    path('orders/<int:order_id>/status/', views.update_order_status, name='update-order-status'),
]