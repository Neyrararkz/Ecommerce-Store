from django.shortcuts import render, get_object_or_404, redirect
from .models import Category, Product
from django.views.generic import TemplateView, ListView
from django.db.models import Q  
from django.views.decorators.http import require_POST
from decimal import Decimal 
from django.contrib.auth.forms import UserCreationForm

class TestTemplateView(TemplateView):
    template_name = "main/test.html"

def index(request):
    category = request.GET.get('category', 'all')
    products = Product.objects.filter(available=True)
    categories = Category.objects.all()

    if category != "all":
        # ct = get_object_or_404(Category, slug=category)
        products = products.filter(category__slug=category)

    context = {
        "products": products,
        "categories": categories,
        "category_select": category,
    }
    return render(request, 'main/index.html', context)


class ProductListView(ListView):
    model = Product
    template_name = "main/index.html"
    context_object_name = "products"
    extra_context = {"title": "Главная страница"}

    def get_queryset(self):
        self.category = self.request.GET.get("category", "all")
        self.searchText = self.request.GET.get("text", "").strip()
        products = Product.objects.filter(available=True)
        if (self.category != "all"):
            products = products.filter(category__slug=self.category)
        if (self.searchText != ""):
            products = products.filter(Q(name__icontains=self.searchText) | Q(description__icontains=self.searchText))
        
        return products

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Главная страница"
        context["categories"] = Category.objects.all()
        context["category_select"] = self.category
        context["search_text"] = self.searchText
        print(context)
        return context
        

def product_detail(request, pk, slug):
    product = get_object_or_404(Product, pk=pk, slug=slug)
    context = {
        "product": product
    }
    return render(request, "main/product_detail.html", context)

@require_POST
def add_cart(request, product_id):
    cart = request.session.get("cart", {})
    product_id = str(product_id)

    if product_id in cart:
        cart[product_id] += 1
    else:
        cart[product_id] = 1

    request.session["cart"] = cart
    return redirect('cart_detail')

def minus_cart(request, product_id):
    cart = request.session.get("cart", {})
    product_id = str(product_id)

    if cart[product_id] > 1:
        cart[product_id] -= 1
    

    request.session["cart"] = cart
    return redirect('cart_detail')

def remove_cart(request, product_id):
    cart = request.session.get("cart", {})
    product_id = str(product_id)
    cart.pop(str(product_id))
    request.session["cart"] = cart
    return redirect('cart_detail')
    
def detail_cart(request):
    cart = request.session.get("cart", {})

    products = Product.objects.filter(id__in=cart.keys())

    items = []
    total_price = Decimal("0.00")
    total_quantity = 0

    for product in products:
        quantity = cart[str(product.id)]
        item_total = product.price * quantity

        items.append({
            "product": product,
            "quantity": quantity,
            "item_total": item_total
        })
        total_price += item_total
        total_quantity += quantity

    context = {
        "total_price": total_price,
        "total_quantity": total_quantity,
        "items": items
    }

    return render(request, 'main/cart_detail.html', context)


def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()

    context = {
        "form": form
    }
    return render(request, 'main/register.html', context)

def accounts_profile(request):
    context = {
        "user": request.user
    }
    return render(request, 'main/account_profile.html', context)