from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib import messages
from .models import *
from .forms import CustomUserCreationForm, CheckoutForm
from django.shortcuts import render, get_object_or_404, redirect
from .forms import RestaurantForm, ProductForm
from .models import Restaurant, Product
from .forms import OrderForm

from django.views.generic import TemplateView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy

# Create your views here.

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            role = form.cleaned_data.get('role')
            if role == 'client':
                user.is_client = True
            elif role == 'employee':
                user.is_employee = True
            elif role == 'delivery_person':
                user.is_delivery_person = True
            user.save()
            if user.is_client:
                Client.objects.create(user=user, address='Default Address')
            messages.success(request, f'Акаунтът за {user.username} е създаден успешно!')
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})

def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            if user.is_client:
                return redirect('client_dashboard')
            elif user.is_employee:
                return redirect('employee_dashboard')
            elif user.is_delivery_person:
                return redirect('delivery_person_dashboard')
            else:
                return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})

def logout(request):
    auth_logout(request)
    messages.success(request, 'Успешно излязохте.')
    return redirect('login')

def home(request):
    return render(request, 'accounts/home.html')

@login_required
def add_restaurant(request):
    if not request.user.is_employee:
        return redirect('home')
    if request.method == 'POST':
        form = RestaurantForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('employee_dashboard')
    else:
        form = RestaurantForm()
    return render(request, 'accounts/add_restaurant.html', {'form': form})


class ProductCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'accounts/add_product.html'
    success_url = reverse_lazy('employee_dashboard')

    def test_func(self):
        return self.request.user.is_employee


class ClientDashboardView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = 'accounts/client_dashboard.html'

    def test_func(self):
        return self.request.user.is_client


class EmployeeDashboardView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = 'accounts/employee_dashboard.html'

    def test_func(self):
        return self.request.user.is_employee

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['restaurants'] = Restaurant.objects.all()
        context['products'] = Product.objects.all()
        return context

def delivery_person_dashboard(request):
    return render(request, 'accounts/delivery_person_dashboard.html')

@login_required
def edit_restaurant(request, pk):
    if not request.user.is_employee:
        return redirect('home')
    restaurant = get_object_or_404(Restaurant, pk=pk)
    if request.method == 'POST':
        form = RestaurantForm(request.POST, instance=restaurant)
        if form.is_valid():
            form.save()
            return redirect('employee_dashboard')
    else:
        form = RestaurantForm(instance=restaurant)
    return render(request, 'accounts/edit_restaurant.html', {'form': form})

@login_required
def delete_restaurant(request, pk):
    if not request.user.is_employee:
        return redirect('home')
    restaurant = get_object_or_404(Restaurant, pk=pk)
    if request.method == 'POST':
        restaurant.delete()
        return redirect('employee_dashboard')
    return render(request, 'accounts/delete_restaurant.html', {'restaurant': restaurant})


class ProductUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'accounts/edit_product.html'
    success_url = reverse_lazy('employee_dashboard')

    def test_func(self):
        return self.request.user.is_employee


class ProductDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Product
    template_name = 'accounts/delete_product.html'
    success_url = reverse_lazy('employee_dashboard')

    def test_func(self):
        return self.request.user.is_employee

@login_required
def view_products(request):
    if not request.user.is_client:
        return redirect('home')

    category = request.GET.get('category')
    if category:
        products = Product.objects.filter(category=category)
    else:
        products = Product.objects.all()

    categories = Product.CATEGORY_CHOICES

    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        quantity = int(request.POST.get('quantity', 1))
        product = get_object_or_404(Product, pk=product_id)

        cart_item, created = CartItem.objects.get_or_create(user=request.user, product=product)
        if created:
            cart_item.quantity = quantity
        else:
            cart_item.quantity += quantity
        cart_item.save()

        return redirect('view_products')

    return render(request, 'accounts/view_products.html', {'products': products, 'categories': categories})


@login_required
def delivery_dashboard(request):
    if not request.user.is_delivery_person:
        return redirect('home')

    orders = Order.objects.filter(status__in=['pending', 'shipped']).order_by('-created_at')

    return render(request, 'accounts/delivery_dashboard.html', {'orders': orders})


@login_required
def accept_delivery(request, pk):
    if not request.user.is_delivery_person:
        return redirect('home')

    order = get_object_or_404(Order, pk=pk)
    if order.status == 'pending':
        order.status = 'shipped'
        order.delivery_person = request.user
        order.save()
    return redirect('delivery_dashboard')


@login_required
def create_order(request):
    if not request.user.is_client:
        return redirect('home')

    category = request.GET.get('category')
    if category:
        products = Product.objects.filter(category=category)
    else:
        products = Product.objects.all()

    categories = Product.CATEGORY_CHOICES

    if request.method == 'POST':
        form = OrderForm(request.POST)
        try:
            if form.is_valid():
                order = form.save(commit=False)
                order.client = Client.objects.get(user=request.user)

                total_price = 0
                for item in form.cleaned_data['items']:
                    quantity = int(request.POST.get(f'quantity_{item.id}', 1))
                    price = item.price * quantity
                    total_price += price

                order.total_price = total_price
                order.save()

                for item in form.cleaned_data['items']:
                    quantity = int(request.POST.get(f'quantity_{item.id}', 1))
                    OrderItem.objects.create(
                        order=order,
                        product=item,
                        quantity=quantity,
                        price=item.price * quantity
                    )

                return redirect('checkout', order_id=order.pk)
            else:
                messages.error(request, "Формата не е валидна. Моля, проверете данните.")
        except Exception as e:
            messages.error(request, "Възникна неочаквана грешка при създаване на поръчката.")
    else:
        form = OrderForm()

    return render(request, 'accounts/create_order.html', {
        'form': form,
        'products': products,
        'categories': categories
    })

@login_required
def mark_as_delivered(request, pk):
    if not request.user.is_delivery_person:
        return redirect('home')

    order = get_object_or_404(Order, pk=pk)
    if order.delivery_person == request.user and order.status == 'shipped':
        order.status = 'delivered'
        order.save()
    return redirect('delivery_dashboard')

@login_required
def add_to_cart(request, pk):
    if not request.user.is_client:
        return redirect('home')
    product = get_object_or_404(Product, pk=pk)
    cart_item, created = CartItem.objects.get_or_create(user=request.user, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    return redirect('view_products')
@login_required
def view_cart(request):
    if not request.user.is_client:
        return redirect('home')
    cart_items = CartItem.objects.filter(user=request.user)
    total_price = sum(item.product.price * item.quantity for item in cart_items)
    return render(request, 'accounts/view_cart.html', {'cart_items': cart_items, 'total_price': total_price})

@login_required
def remove_from_cart(request, pk):
    if not request.user.is_client:
        return redirect('home')
    cart_item = get_object_or_404(CartItem, pk=pk, user=request.user)
    cart_item.delete()
    return redirect('view_cart')


@login_required
def checkout(request):
    if not request.user.is_client:
        return redirect('home')

    client = Client.objects.get(user=request.user)
    cart_items = CartItem.objects.filter(user=request.user)

    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            address = form.cleaned_data['address']
            phone_number = form.cleaned_data['phone_number']

            order = Order.objects.create(
                client=client,
                total_price=sum(item.product.price * item.quantity for item in cart_items),
                status='pending',
                address=address,
                phone_number=phone_number
            )
            for item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    quantity=item.quantity,
                    price=item.product.price * item.quantity
                )
            cart_items.delete()
            return redirect('client_dashboard')
    else:
        form = CheckoutForm()
    return render(request, 'accounts/checkout.html', {'form': form})

@login_required
def track_orders(request):
    if not request.user.is_client:
        return redirect('home')
    client = Client.objects.get(user=request.user)
    orders = Order.objects.filter(client=client).order_by('-created_at')
    return render(request, 'accounts/track_orders.html', {'orders': orders})
