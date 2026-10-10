import json
from django.contrib import messages
from django.db import transaction
from django.shortcuts import render, redirect, get_object_or_404
from .forms import ReservationForm
from .models import MenuItem, RestaurantTable, Reservation, Order, OrderItem

def menu_view(request):
    menu_items = MenuItem.objects.all()
    return render(request, "restaurant/menu_list.html", {
        "menu_items": menu_items
    })


def table_list(request):
    tables = RestaurantTable.objects.all()
    return render(request, "restaurant/table_list.html", {
        "tables": tables
    })


def create_reservation(request):
    if request.method == "POST":
        form = ReservationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("reservation-success")
    else:
        form = ReservationForm()

    return render(request, "restaurant/reservation_form.html", {
        "form": form
    })


def reservation_success(request):
    return render(request, "restaurant/reservation_success.html")


def home(request):
    menu_items = MenuItem.objects.count()
    tables = RestaurantTable.objects.count()
    reservations = Reservation.objects.count()
    orders = Order.objects.count()

    return render(request, "restaurant/home.html", {
        "menuItems": menu_items,
        "tables": tables,
        "reservations": reservations,
        "orders": orders
    })


def create_order(request):
    tables = RestaurantTable.objects.all()
    menu_items = MenuItem.objects.all()

    if request.method == "POST":
        customer_name = request.POST.get("customer_name", "").strip()
        table_id = request.POST.get("table")
        items_json = request.POST.get("order_items", "")

        if not customer_name or not table_id:
            return render(request, "restaurant/order_form.html", {
                "tables": tables,
                "menu_items": menu_items,
                "error": "Enter the customer name and select a table."
            })

        try:
            items = json.loads(items_json)

            if not isinstance(items, list) or not items:
                raise ValueError

            quantities = {}

            for item in items:
                if not isinstance(item, dict):
                    raise ValueError

                item_id = int(item["menu_item"])
                quantity = int(item["quantity"])

                if item_id <= 0 or quantity <= 0:
                    raise ValueError

                quantities[item_id] = quantities.get(item_id, 0) + quantity

        except (ValueError, TypeError, KeyError, json.JSONDecodeError):
            return render(request, "restaurant/order_form.html", {
                "tables": tables,
                "menu_items": menu_items,
                "error": "Invalid order. Please select items and quantities again."
            })

        try:
            with transaction.atomic():
                table = RestaurantTable.objects.get(pk=table_id)
                selected_items = []

                for item_id, quantity in quantities.items():
                    menu_item = MenuItem.objects.select_for_update().get(
                        pk=item_id
                    )

                    if quantity > menu_item.stock_quantity:
                        raise ValueError(
                            f"Only {menu_item.stock_quantity} units of "
                            f"{menu_item.name} are available."
                        )

                    selected_items.append((menu_item, quantity))

                order = Order.objects.create(
                    customer_name=customer_name,
                    table=table
                )

                for menu_item, quantity in selected_items:
                    OrderItem.objects.create(
                        order=order,
                        menu_item=menu_item,
                        quantity=quantity,
                        price_at_order_time=menu_item.price
                    )

                    menu_item.stock_quantity -= quantity
                    menu_item.save(update_fields=["stock_quantity"])

        except RestaurantTable.DoesNotExist:
            return render(request, "restaurant/order_form.html", {
                "tables": tables,
                "menu_items": menu_items,
                "error": "The selected table does not exist."
            })

        except MenuItem.DoesNotExist:
            return render(request, "restaurant/order_form.html", {
                "tables": tables,
                "menu_items": menu_items,
                "error": "One of the selected menu items no longer exists."
            })

        except ValueError as exc:
            return render(request, "restaurant/order_form.html", {
                "tables": tables,
                "menu_items": menu_items,
                "error": str(exc)
            })

        return redirect("order-success")

    return render(request, "restaurant/order_form.html", {
        "tables": tables,
        "menu_items": menu_items
    })


def order_list(request):
    orders = Order.objects.prefetch_related(
        "items__menu_item"
    ).select_related("table").order_by("-order_time")

    return render(request, "restaurant/order_list.html", {
        "orders": orders
    })


def order_success(request):
    return render(request, "restaurant/order_success.html")


@transaction.atomic
def update_order_status(request, order_id):
    if request.method != "POST":
        return redirect("order-list")

    order = get_object_or_404(
        Order.objects.select_for_update(),
        id=order_id
    )

    new_status = request.POST.get("order_status")

    valid_statuses = [
        "Pending",
        "In Progress",
        "Completed",
        "Cancelled",
    ]

    if new_status not in valid_statuses:
        messages.error(request, "Invalid order status.")
        return redirect("order-list")

    if order.order_status == "Cancelled":
        if new_status != "Cancelled":
            messages.error(
                request,
                "Cancelled orders cannot be reactivated. Create a new order instead."
            )
        else:
            messages.info(request, "This order is already cancelled.")

        return redirect("order-list")

    if new_status == "Cancelled":
        order_items = list(
            order.items.select_related("menu_item").all()
        )

        for order_item in order_items:
            menu_item = MenuItem.objects.select_for_update().get(
                pk=order_item.menu_item_id
            )

            menu_item.stock_quantity += order_item.quantity
            menu_item.save(update_fields=["stock_quantity"])

    order.order_status = new_status
    order.save(update_fields=["order_status"])

    messages.success(
        request,
        f"Order #{order.id} status updated to {new_status}."
    )

    return redirect("order-list")

