from django.urls import path
from . import views

from .views import (
    ClientDashboardView,
    EmployeeDashboardView,
    ProductCreateView,
    ProductUpdateView,
    ProductDeleteView,
)

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('register/', views.register, name='register'),
    path('add-restaurant/', views.add_restaurant, name='add_restaurant'),
    path('edit-restaurant/<int:pk>/', views.edit_restaurant, name='edit_restaurant'),
    path('delete-restaurant/<int:pk>/', views.delete_restaurant, name='delete_restaurant'),
    path('add-product/', ProductCreateView.as_view(), name='add_product'),
    path('edit-product/<int:pk>/', ProductUpdateView.as_view(), name='edit_product'),
    path('delete-product/<int:pk>/', ProductDeleteView.as_view(), name='delete_product'),
    path('view-products/', views.view_products, name='view_products'),
    path('client-dashboard/', ClientDashboardView.as_view(), name='client_dashboard'),
    path('employee-dashboard/', EmployeeDashboardView.as_view(), name='employee_dashboard'),
    path('delivery-person-dashboard/', views.delivery_person_dashboard, name='delivery_person_dashboard'),
    path('delivery-dashboard/', views.delivery_dashboard, name='delivery_dashboard'),
    path('add-to-cart/<int:pk>/', views.add_to_cart, name='add_to_cart'),
    path('view-cart/', views.view_cart, name='view_cart'),
    path('remove-from-cart/<int:pk>/', views.remove_from_cart, name='remove_from_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('track-orders/', views.track_orders, name='track_orders'),
    path('accept-delivery/<int:pk>/', views.accept_delivery, name='accept_delivery'),
    path('mark-as-delivered/<int:pk>/', views.mark_as_delivered, name='mark_as_delivered'),
]
