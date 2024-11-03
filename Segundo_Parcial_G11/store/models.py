from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from django.apps import apps
from django.utils.deprecation import MiddlewareMixin
#from store.models import CustomUser, Product

class CustomUser(AbstractUser):
    usname = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=8)
    email = models.CharField(max_length=255)
    direccion = models.CharField(max_length=255, null=True, blank=True)
    is_employee = models.BooleanField(default=False)

    login_attempts = models.IntegerField(default=0)
    is_locked = models.BooleanField(default=False)

    def __str__(self):
        return self.username
    
class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

class CartItem(models.Model):
    cart = models.ForeignKey('Cart', on_delete=models.CASCADE)
    product = models.ForeignKey('store.Product', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def get_total_price(self):
        return self.product.price * self.quantity


class CartMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if 'cart' not in request.session:
            request.session['cart'] = []

    def add_to_cart(self, request, product_id, quantity):
        cart = request.session.get('cart', [])

        product_exists = False
        for item in cart:
            if item['product_id'] == product_id:
                item['quantity'] += quantity
                product_exists = True
                break

        if not product_exists:
            cart.append({'product_id': product_id, 'quantity': quantity})

        request.session['cart'] = cart


    def process_view(self, request, view_func, view_args, view_kwargs):
        if request.method == 'POST' and 'add_to_cart' in request.POST:
            product_id = int(request.POST.get('product_id'))
            quantity = int(request.POST.get('quantity'))
            self.add_to_cart(request, product_id, quantity)

class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True)
    image = models.CharField(max_length=255, blank=True)
    stock = models.IntegerField(default=10)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    

class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    direccion_envio = models.CharField(max_length=255)  # Asegúrate de que este campo exista
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Pedido {self.id} de {self.user.username}'

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    item_total = models.DecimalField(max_digits=10, decimal_places=2)  # Agregar este campo

    def __str__(self):
        return f'{self.quantity} de {self.product.name}'

class RecoveryRequest(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    request_message = models.TextField()
    request_type = models.CharField(max_length=50, default='forgot_password') #borrar si no funciona
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Solicitud de {self.user.username} ({self.request_type}) en {self.submitted_at}'