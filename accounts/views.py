from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib import messages
from django.views.generic import TemplateView, CreateView, UpdateView, DeleteView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy

from django.core.paginator import Paginator
from rest_framework.generics import ListAPIView
from .serializers import ProductSerializer, OrderSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import (
    Client, CartItem, Order, OrderItem,
    Product, Restaurant
)
from .forms import (
    CustomUserCreationForm, RestaurantForm,
    ProductForm, OrderForm, CheckoutForm, ContactForm
)


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_client = True
            user.save()

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


class ProductCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'accounts/add_product.html'
    success_url = reverse_lazy('employee_dashboard')

    def test_func(self):
        return self.request.user.is_employee


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
    search_query = request.GET.get('search', '')


    product_list = Product.objects.all()

    if category:
        product_list = product_list.filter(category=category)

    if search_query:
        product_list = product_list.filter(name__icontains=search_query)

    paginator = Paginator(product_list, 5)
    page_number = request.GET.get('page')
    products = paginator.get_page(page_number)

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

    return render(request, 'accounts/view_products.html', {
        'products': products,
        'categories': categories,
        'search_query': search_query,
    })


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
        context['orders'] = Order.objects.all().order_by('-created_at')
        return context


def delivery_person_dashboard(request):
    return render(request, 'accounts/delivery_person_dashboard.html')

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
            comment = form.cleaned_data['comment']

            order = Order.objects.create(
                client = client,
                total_price = sum(item.product.price * item.quantity for item in cart_items),
                status = 'pending',
                address = address,
                phone_number = phone_number,
                comment=comment
            )
            for item in cart_items:
                OrderItem.objects.create(
                    order = order,
                    product = item.product,
                    quantity = item.quantity,
                    price = item.product.price * item.quantity
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


class AboutView(TemplateView):
    template_name = 'accounts/about.html'


class ContactView(LoginRequiredMixin, FormView):
    template_name = 'accounts/contact.html'
    form_class = ContactForm
    success_url = '/contact/?success=1'
    login_url = 'login'

    def form_valid(self, form):
        return super().form_valid(form)


@login_required
def user_profile(request):
    context = {
        'user': request.user,
    }
    if request.user.is_client:
        context['client'] = request.user.client

    return render(request, 'accounts/profile.html', context)


class FAQView(TemplateView):
    template_name = 'accounts/faq.html'


class ProductListAPI(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class OrderListAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        orders = Order.objects.filter(client__user=request.user)
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)