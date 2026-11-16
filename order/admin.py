from django.contrib import admin
from .models import Order, OrderItem

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user_name', 'phone_number', 'delivery_method', 'status']
    list_filter = ['status', 'delivery_method']
    list_editable = ['status']
    search_fields = ['user_name', 'phone_number']
    
admin.site.register(OrderItem)