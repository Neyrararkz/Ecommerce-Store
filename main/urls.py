from django.urls import path
from . import views
from django.contrib.auth import views as auth_view

urlpatterns = [
    path('', views.ProductListView.as_view(), name='main'),
    path('test/', views.TestTemplateView.as_view()),
    path('<int:pk>/<slug:slug>/', views.product_detail, name='product_detail'),
    path('cart/<int:product_id>', views.add_cart, name='add_cart'),
    path('cart/minus/<int:product_id>', views.minus_cart, name='minus_cart'),
    path('cart/remove/<int:product_id>', views.remove_cart, name='remove_cart'),
    path('cart/', views.detail_cart, name='cart_detail'),
    path('users/register/', views.register, name='register'),
    path('users/login/', auth_view.LoginView.as_view(template_name="main/login.html"), name='login'),
    path('accounts/profile/', views.accounts_profile, name='account_profile'),
    path('users/logout/', auth_view.LogoutView.as_view(), name='logout')
]
