from django.shortcuts import render, redirect, get_object_or_404
from .models import Order, OrderItem
from main.models import Product
from .forms import OrderForm
from decimal import Decimal 

def create_order(request):
    cart = request.session.get("cart", {})
    error = ''
    if not cart:
        return redirect('main')
    products = [get_object_or_404(Product, id=product_id) for product_id in cart]     
    items = []
    total_price = Decimal("0.00")
    total_quantity = 0
    for product in products:
            item_total = product.price * cart[str(product.id)]
            items.append({
                "product": product,
                "quantity": cart[str(product.id)],
                "item_total": item_total
            })
            total_price += item_total
            total_quantity += cart[str(product.id)]
    
    if request.method == "POST":
           
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save()

            for product in products:
                OrderItem.objects.create(
                    order=order,
                    product=product,
                    price=product.price,
                    quantity=cart[str(product.id)]
                )

            del request.session["cart"]
            return redirect('/')
        else:
            error = "данные какашко"
    else:
        form = OrderForm()

    context = {
        "form": form,
        "error": error,
        "total_price": total_price,
        "total_quantity": total_quantity,
        "items": items
    }
    return render(request, 'order/create_order.html', context)