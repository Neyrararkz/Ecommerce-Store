from django.forms import ModelForm
from .models import Order

class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = ['user_name', 'phone_number', 'address', 'email', 'comment', 'delivery_method']