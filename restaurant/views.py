from django.shortcuts import redirect, render
from restaurant.forms import ReservationForm
from restaurant.models import MenuItem, RestaurantTable

def menu_view(request):
    menu_items = MenuItem.objects.all()
    return render(
        request, 
        'restaurant/menu_list.html', 
        {'menu_items': menu_items}
    )

def table_list(request):
    tables = RestaurantTable.objects.all()
    return render(
        request,
        'restaurant/table_list.html',
        {'tables': tables}
    )

def create_reservation(request):
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('reservation-success')
    else:
        form = ReservationForm()
    return render(request, 'restaurant/reservation_form.html', {'form': form})

def reservation_success(request):
    return render(request, 'restaurant/reservation_success.html')