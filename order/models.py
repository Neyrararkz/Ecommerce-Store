from django.db import models
from main.models import Product
from django.conf import settings

class Order(models.Model):
    STATUS_CHOICES = [
        ("new", "Новый"),
        ("processing", "В обработке"),
        ("completed", "Завершенный")
    ]
    DELIVERY_CHOICES = [
        ("pickup", "Самовывоз"),
        ("delivery", "Доставка")
    ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    user_name = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=30)
    address = models.CharField(max_length=100)
    email = models.EmailField(blank=True)
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default="new")
    delivery_method = models.CharField(choices=DELIVERY_CHOICES, default="pickup")

    def __str__(self):
        return f"Заказ №{self.id} — {self.user_name}"
    
    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.product.name} — {self.quantity}шт."
    
    class Meta:
        verbose_name = "Позиция закакза"
        verbose_name_plural = "Позиции заказа"