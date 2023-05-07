import django
from django import forms
from store.models import Product,Order

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'address', 'zipcode', 'city']