from django.contrib import admin
from .models import (
    User, Client, Employee, DeliveryPerson,
    Category, Restaurant, Product, Order, OrderItem, Delivery
)

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'is_client', 'is_employee', 'is_delivery_person', 'is_staff')
    list_filter = ('is_client', 'is_employee', 'is_delivery_person', 'is_staff')
    search_fields = ('username',)
    ordering = ('username',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'restaurant')
    list_filter = ('category', 'restaurant')
    search_fields = ('name',)
    ordering = ('name',)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'client', 'status', 'total_price', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('client__user__username',)
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'total_price')


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('user', 'address')
    search_fields = ('user__username', 'address')

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('user', 'department')
    search_fields = ('user__username', 'department')


@admin.register(DeliveryPerson)
class DeliveryPersonAdmin(admin.ModelAdmin):
    list_display = ('user', 'vehicle_type')
    search_fields = ('user__username', 'vehicle_type')

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ('name', 'address')
    search_fields = ('name', 'address')

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity', 'price')
    search_fields = ('order__id', 'product__name')

@admin.register(Delivery)
class DeliveryAdmin(admin.ModelAdmin):
    list_display = ('order', 'delivery_person', 'delivery_address', 'delivery_time')
    search_fields = ('order__id', 'delivery_person__username', 'delivery_address')
