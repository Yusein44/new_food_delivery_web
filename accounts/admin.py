from django.contrib import admin
from .models import (
    User, Client, Employee, DeliveryPerson,
    Category, Restaurant, Product, Order, OrderItem, Delivery
)

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'is_client', 'is_employee', 'is_delivery_person', 'is_staff')
    list_filter = ('is_client', 'is_employee', 'is_delivery_person')
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
    list_filter = ('status',)
    search_fields = ('client__user__username',)
    ordering = ('-created_at',)


admin.site.register(Client)
admin.site.register(Employee)
admin.site.register(DeliveryPerson)
admin.site.register(Category)
admin.site.register(Restaurant)
admin.site.register(OrderItem)
admin.site.register(Delivery)
