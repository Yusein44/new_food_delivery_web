from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Restaurant, Product, Order, ContactMessage


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

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

    comment = forms.CharField(
        required=False,
        label="Коментар към поръчката (по избор)",
        widget=forms.Textarea(attrs={'rows': 3, 'placeholder': 'Вашето мнение е важно за нас ! :)'})
    )

class ContactForm(forms.Form):
    name = forms.CharField(label='Име', max_length=100)
    email = forms.EmailField(label='Имейл')
    message = forms.CharField(label='Съобщение', widget=forms.Textarea)