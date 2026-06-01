# 🍔 Online Food Delivery - Django Web App

Online Food Delivery is a robust, backend-driven web application built with Python and Django. It provides a complete platform for browsing restaurant menus, managing a shopping cart, and processing food orders.

## Getting Started

To get a local copy up and running, follow these simple steps. The project runs entirely on a Django server.

### Prerequisites & Installation

1. Clone the repository:
```bash
   git clone [https://github.com/Yusein44/new_food_delivery_web.git](https://github.com/Yusein44/new_food_delivery_web.git)
2.Navigate to the project directory: cd new_food_delivery_web
3.Create and activate a virtual environment:
  python -m venv venv
     # On Windows: venv\Scripts\activate
     # On macOS/Linux: source venv/bin/activate
4.Install the required dependencies: pip install -r requirements.txt
5.Apply database migrations to set up the SQLite/PostgreSQL database: python manage.py migrate
6.Start the development server: python manage.py runserver
7.Open the link shown in the terminal (usually http://127.0.0.1:8000/).

Technologies Used
Framework: Django (Python)

Architecture: MVT (Model-View-Template)

Database: SQLite (Development) / PostgreSQL (Production ready)

Frontend/Styling: HTML5, CSS (Django Templates)

Authentication: Django Built-in Authentication System

Features
Public Part (Accessible to everyone)
Home Page: Welcoming interface with an overview of the platform.

Menu Catalog: Displays all available food items categorized for easy browsing.

Details Page: View specific details, ingredients, and prices for individual menu items.

Authentication: User registration and login forms with validation.

Private Part (Available for Registered Users)
Shopping Cart: Users can dynamically add, update quantities, or remove items before checkout.

Order Processing: Secure checkout system that calculates total prices and finalizes orders.

Order History / Profile: Users can view their past and current orders.

Route Protection:

Unauthenticated users are redirected to the Login page when trying to access the cart or checkout.

Logged-in users are restricted from accessing generic Login/Register pages.

Project Architecture
The project follows the standard Django MVT architecture with separation of concerns:

models.py: Database schema and business logic (e.g., Order, MenuItem, Cart, User models).

views.py: Request handling, querying the database, and returning the appropriate templates.

urls.py: URL routing mapping web addresses to specific views.

templates/: HTML files utilizing Django Template Language (DTL) for dynamic rendering.

static/: CSS, JavaScript, and image assets.

admin.py: Configuration for the built-in Django Admin interface to manage the store's inventory.

Security & Validation
CSRF Protection: Cross-Site Request Forgery tokens implemented in all forms modifying data.

Route Guards: @login_required decorators and LoginRequiredMixin used to protect private views (Cart, Checkout).

Owner Validation: Users can only view and process their own shopping carts and order histories.

Form Validation: Django Forms used to ensure clean and valid data submission for user registration and orders.

Secure Password Hashing: Handled automatically by Django's robust authentication backend.
