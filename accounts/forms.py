from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Restaurant, Product, Order

class CustomUserCreationForm(UserCreationForm):
    ROLE_CHOICES = [
        ('client', 'Клиент'),
        ('employee', 'Служител'),
        ('delivery_person', 'Доставчик'),
    ]
    role = forms.ChoiceField(choices=ROLE_CHOICES, label='Роля')
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'role']


class RestaurantForm(forms.ModelForm):
    class Meta:
        model = Restaurant
        fields = ['name', 'address']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Име на ресторанта'}),
            'address': forms.TextInput(attrs={'placeholder': 'Адрес'}),
        }

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['restaurant', 'name', 'description', 'price', 'category']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Име на продукта'}),
            'description': forms.Textarea(attrs={'rows': 3}),
            'price': forms.NumberInput(attrs={'min': 0}),
        }

class OrderForm(forms.ModelForm):
    items = forms.ModelMultipleChoiceField(
        queryset=Product.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True,
        label="Изберете продукти"
    )

    class Meta:
        model = Order
        fields = []

class CheckoutForm(forms.Form):
    address = forms.CharField(
        max_length=255,
        required=True,
        label="Адрес за доставка",
        widget=forms.TextInput(attrs={'placeholder': 'ул. Пример 123'})
    )
    phone_number = forms.CharField(
        max_length=20,
        required=True,
        label="Телефонен номер",
        widget=forms.TextInput(attrs={'placeholder': '+359...'})
    )
