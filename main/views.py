from django.shortcuts import render, get_object_or_404, redirect
from .models import Category, Product, Review
from django.views.generic import TemplateView, ListView
from django.db.models import Q  
from django.views.decorators.http import require_POST
from decimal import Decimal 
from django.contrib.auth.forms import UserCreationForm
from .forms import ReviewForm
from django.core.paginator import Paginator

class TestTemplateView(TemplateView):
    template_name = "main/test.html"

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
        self.sort_price = self.request.GET.get("sort_price", "")
        self.sort_name = self.request.GET.get("sort_name", "")
        ordering = {
            "price_asc": "price",
            "price_desc": "-price",
            "name_asc": "name",
            "name_desc": "-name"
        }
        selected_option_price = ordering.get(self.sort_price, "id")    
        selected_option_name = ordering.get(self.sort_name, "id")
        if selected_option_price != "id" or selected_option_name != "id":
            if selected_option_price != "id" and selected_option_name != "id":
                products = products.order_by(selected_option_price, selected_option_name, "id")
            elif selected_option_price != "id" and selected_option_name == "id":
                products = products.order_by(selected_option_price, "id")
            elif selected_option_price == "id" and selected_option_name != "id":
                products = products.order_by(selected_option_name, "id")
        else:
            products = products.order_by("id")      

        self.per_page = self.request.GET.get("per_page", "6")

        self.products_paginator = Paginator(products, self.per_page)
        self.page_number = self.request.GET.get("page", "")
        self.page = self.products_paginator.get_page(self.page_number)

        self.start_index = self.page.start_index
        self.end_index = self.page.end_index
        self.count = self.products_paginator.count
        return products

    def get_context_data(self, **kwargs):
        

        context = super().get_context_data(**kwargs)
        context["title"] = "Главная страница"
        context["categories"] = Category.objects.all()
        context["category_select"] = self.category
        context["search_text"] = self.searchText
        context["reviews"] = Review.objects.all()
        context["sort_price_selected"] = self.sort_price
        context["sort_name_selected"] = self.sort_name
        context["per_page_selected"] = self.per_page
        context["products_paginator"] = self.products_paginator
        context["page_number"] = self.page_number
        context["page"] = self.page
        context["start_index"] = self.start_index
        context["end_index"] = self.end_index
        context["count"] = self.count
        print(self.products_paginator.object_list)        
        print(self.products_paginator.get_page(1).object_list)

        params = self.request.GET.copy()
        params.pop("page", None) 
        params = params.urlencode()
        context["params"] = params

        return context
        

def product_detail(request, pk, slug):
    product = get_object_or_404(Product, pk=pk, slug=slug)
    reviews = Review.objects.filter(product=product)
    error = ''

    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            form.save()
        else:
            error = "Некорректная форма"
    else:
        form = ReviewForm()

    context = {
        "product": product,
        "reviews": reviews,
        "form": form,
        "error": error
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