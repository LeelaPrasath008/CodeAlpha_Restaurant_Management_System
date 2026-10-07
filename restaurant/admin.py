from django.contrib import admin
from restaurant.models import MenuItem, OrderItem, RestaurantTable, Reservation, Order

@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'stock_quantity')
    search_fields = ('name', 'category')

@admin.register(RestaurantTable)
class RestaurantTableAdmin(admin.ModelAdmin):
    list_display = ('table_number', 'capacity', 'is_available')
    list_filter = ('is_available',)

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('customer_name', 'phone_number', 'email', 'table', 'reservation_date', 'status')
    list_filter = ('status',)
    search_fields = ('customer_name', 'phone_number', 'email')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('customer_name', 'table', 'total_amount', 'order_status','order_time')
    list_filter = ('order_status',)
    search_fields = ('customer_name',)

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'menu_item', 'quantity', 'price_at_order_time')