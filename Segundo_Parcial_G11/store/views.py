from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse, HttpResponse, Http404
from django.contrib.auth import get_user_model, authenticate, login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.csrf import csrf_exempt
from django.db import connection
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import AuthenticationForm
from .forms import CustomUserCreationForm
from .models import Cart, CartItem, Product, CustomUser, Product, Order, OrderItem, RecoveryRequest
import json



def Tienda(request):
    return render(request,'store.html')

def cart(request):
    context = {}
    return render(request,'cart.html')

def checkout(request):
    context = {}
    return render(request,'checkout.html')

def tommy1(request):
    context = {}
    return render(request,'tommy1.html')
def tommy2(request):
    return render(request,'tommy2.html')
def tommy3(request):
    return render(request,'tommy3.html')

def boss1(request):
    context = {}
    return render(request,'boss1.html')
def boss2(request):
    return render(request,'boss2.html')
def boss3(request):
    return render(request,'boss3.html')

def lauren1(request):
    context = {}
    return render(request,'lauren1.html')
def lauren2(request):
    return render(request,'lauren2.html')
def lauren3(request):
    return render(request,'lauren3.html')

def login(request):
    return render(request,'login.html')

def logout(request):
    return render(request,'logout.html')

def adios(request):
    return render(request,'adios.html')
def gracias(request):
    return render(request,'gracias.html')
def empleado(request):
    return render(request,'empleado.html')
def recovery(request):
    return render(request,'recovery.html')

def register(request):
    return render(request,'register.html')
#---------------------------------------------------------------------------------------------------
def enviar_correo(request, user_id):
    User = get_user_model()  # Obtén el modelo de usuario personalizado
    usuario = get_object_or_404(User, id=user_id)  # Obtén el usuario por su ID

    email_destinatario = usuario.email
    asunto = 'Bienvenido a nuestra tienda'
    mensaje = 'Gracias por registrarte. ¡Esperamos que disfrutes tu experiencia!'

    try:
        send_mail(  # Asegúrate de tener correctamente configurado el envío de correos
            asunto,
            mensaje,
            settings.EMAIL_HOST_USER,
            [email_destinatario],
            fail_silently=False,
        )
        messages.success(request, 'Correo de bienvenida enviado exitosamente.')
    except Exception as e:
        messages.error(request, f'Error al enviar el correo: {e}')

    return redirect('thank')  # Redirige a la página 'thank.html'
#---------------------------------------------------------------------------------------------------
class CustomLogoutView(LogoutView):
    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        return redirect('adios')
#---------------------------------------------------------------------------------------------------
class CustomLoginView(LoginView):
    template_name = 'login.html'

    def form_valid(self, form):
        user = form.get_user()  # Obtener el usuario autenticado
        user.login_attempts = 0  # Reiniciar el contador de intentos
        user.save()

        remember_me = self.request.POST.get('remember_me')
        if not remember_me:
            self.request.session.set_expiry(0)
        else:
            self.request.session.set_expiry(1209600)

        return super().form_valid(form)

    def form_invalid(self, form):
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')

        # Verifica si el usuario existe
        user = authenticate(username=username, password=password)

        if not username:  # Campo de usuario vacío
            messages.error(self.request, "Por favor, introduce un nombre de usuario.")
        elif not password:  # Campo de contraseña vacío
            messages.error(self.request, "Por favor, introduce una contraseña.")
        elif user is None:  # El usuario no existe o la contraseña es incorrecta
            if not self.get_user_exists(username):  # Usuario no encontrado
                messages.error(self.request, "El usuario no existe.")
            else:  # Si el usuario existe pero la contraseña es incorrecta
                existing_user = CustomUser.objects.get(username=username)
                
                # Incrementar los intentos de inicio de sesión
                existing_user.login_attempts += 1
                
                if existing_user.login_attempts >= 3:
                    existing_user.is_locked = True
                    messages.error(self.request, "Tu cuenta ha sido bloqueada después de 3 intentos fallidos.")
                existing_user.save()

                messages.error(self.request, "Contraseña incorrecta.")
        else:  # Otros errores generales
            messages.error(self.request, "Error desconocido. Por favor, intenta nuevamente.")

        return self.render_to_response(self.get_context_data(form=form))

    def get_user_exists(self, username):
        """
        Comprueba si el usuario existe sin verificar la contraseña.
        """
        try:
            CustomUser.objects.get(username=username)  # Usa el modelo de usuario personalizado
            return True
        except CustomUser.DoesNotExist:
            return False
#---------------------------------------------------------------------------------------------------
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Tu cuenta ha sido creada exitosamente.')
            return redirect('login')
        else:
            messages.error(request, 'Error al registrar el usuario. Verifica los datos e intenta de nuevo.')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'register.html', {'form': form})
#---------------------------------------------------------------------------------------------------
def cart_view(request):
    cart = request.session.get('cart', {})
    cart_items = []
    total_price = 0

    for product_id, quantity in cart.items():
        product = get_object_or_404(Product, id=product_id)
        total_item_price = product.price * quantity
        total_price += total_item_price

        cart_items.append({
            'product': product,
            'quantity': quantity,
            'get_total_price': total_item_price
        })

    context = {
        'cart_items': cart_items,
        'total_price': total_price
    }

    return render(request, 'cart.html', context)
#---------------------------------------------------------------------------------------------------
def clear_cart(request):
    request.session['cart'] = {}
    return redirect('cart_view')
#---------------------------------------------------------------------------------------------------
def cart_detail(request):
    cart = Cart.objects.get(user=request.user)
    return render(request, 'cart/cart_detail.html', {'cart': cart})
#---------------------------------------------------------------------------------------------------
def store_view(request):
    products = Product.objects.all()
    context = {
        'products': products
    }
    return render(request, 'store.html', context)
#---------------------------------------------------------------------------------------------------
def update_cart_sum(request, product_id):
    try:
        product = get_object_or_404(Product, id=product_id)
        cart = request.session.get('cart', {})

        if cart[str(product_id)] < 10:  # Limitar a un máximo de 10
            cart[str(product_id)] += 1
            request.session['cart'] = cart
            messages.success(request, f'El producto {product.name} ha sido agregado al carrito.')
        else:
            messages.info(request, f'Límite de productos alcanzados')
    except Product.DoesNotExist:
        messages.error(request, 'Error: el producto no existe.')
    except Exception as e:
        messages.error(request, 'Ha ocurrido un error al agregar el producto al carrito.')

    request.session['cart'] = cart

    return redirect('cart_view')
#---------------------------------------------------------------------------------------------------
def update_cart_res(request, product_id):
    try:
        product = get_object_or_404(Product, id=product_id)
        cart = request.session.get('cart', {})

        if cart[str(product_id)] > 0:  # Limitar a un máximo de 10
            cart[str(product_id)] -= 1
            request.session['cart'] = cart
            messages.success(request, f'El producto {product.name} ha sido removido del carrito.')
        elif cart[str(product_id)] == 0:
            cart = [item for item in cart if item['product_id'] != product_id]
    except Product.DoesNotExist:
        messages.error(request, 'Error: el producto no existe.')
    except Exception as e:
        messages.error(request, 'Ha ocurrido un error al agregar el producto al carrito.')

    request.session['cart'] = cart

    return redirect('cart_view')
#---------------------------------------------------------------------------------------------------
@login_required
def download(request):
    from .models import Product
    cart = request.session.get('cart', {})
    
    if not cart:
        return redirect('cart_detail')
        
    user_name = request.user.name if request.user.is_authenticated else "Anónimo"
    user_address = request.user.direccion

    content = f"Carrito de compras de {user_name}\n\n"
    content += f"Dirección de entrega {user_address}\n\n"

    total_general = 0

    for product_id, quantity in cart.items():
        product = Product.objects.get(id=product_id)
        total = product.price * quantity
        content += f"Producto: {product.name}\n"
        content += f"Cantidad: {quantity}\n"
        content += f"Precio unitario: Q{product.price}\n"
        content += f"Total: Q{total}\n\n"
        total_general += total

    content += f"Total general: Q{total_general}"

    order = Order.objects.create(
        user=request.user,
        total_price=total_general,
        direccion_envio=user_address,
    )

    for product_id, quantity in cart.items():
        product = Product.objects.get(id=product_id)
        item_total = product.price * quantity
        OrderItem.objects.create(
            order=order,
            product=product,
            quantity=quantity,
            item_total=item_total,
        )

    response = HttpResponse(content, content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename=detalles de compra.txt'

    request.session['cart'] = {}

    return response
#---------------------------------------------------------------------------------------------------
def is_staff(user):
    return user.is_staff

@user_passes_test(is_staff)
def empleado(request):
    products = Product.objects.all()  # Obtener todos los productos
    orders = Order.objects.all()  # Obtener todos los pedidos
    recovery_request = RecoveryRequest.objects.all()

    User = get_user_model()
    users = User.objects.exclude(is_staff=True, is_superuser=True)

    if request.method == 'POST':
        if 'reset_attempts' in request.POST:  # Verifica si se está intentando restablecer intentos
            user_id = request.POST.get('user_id')
            if user_id:
                user = User.objects.get(id=user_id)
                user.login_attempts = 0  # Restablecer intentos
                user.is_locked = False  # Desbloquear usuario
                user.save()
    
    if request.method == 'POST':
        for product in products:
            stock = request.POST.get(f'stock_{product.id}')
            price = request.POST.get(f'price_{product.id}')
            if stock and price:
                product.stock = int(stock)
                product.price = float(price)
                product.save()
        return redirect('empleado')

    return render(request, 'empleado.html', {'products': products, 'orders': orders, 'users': users, 'recovery_request': recovery_request})
#---------------------------------------------------------------------------------------------------
@login_required
def download_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    user_name = order.user.name
    user_address = order.direccion_envio

    content = f"Pedido de {user_name}\n\n"
    content += f"Dirección de entrega {user_address}\n\n"

    total_general = 0
    total_general = 0

    # Iterar sobre los elementos de la orden
    for item in order.orderitem_set.all():  # Cambiado de items a orderitem_set
        total = item.item_total  # Asegúrate de que item_total se refiere al precio total del item
        content += f"Producto: {item.product.name}\n"
        content += f"Cantidad: {item.quantity}\n"
        content += f"Precio unitario: Q{item.product.price}\n"
        content += f"Total: Q{total}\n\n"
        total_general += total

    content += f"Total general: Q{total_general}"

    response = HttpResponse(content, content_type='text/plain')
    response['Content-Disposition'] = f'attachment; filename=pedido_{order_id}.txt'

    return response
#---------------------------------------------------------------------------------------------------
@login_required
def delete_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order.delete()
    messages.success(request, "Pedido eliminado con éxito.")
    return redirect('empleado')
#---------------------------------------------------------------------------------------------------
@login_required
def reset_login_attempts(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    user.login_attempts = 0
    user.is_locked = False
    user.save()
    messages.success(request, f'Los intentos de inicio de sesión para {user.username} han sido restablecidos.')
    return redirect('empleado')
#---------------------------------------------------------------------------------------------------
def recovery_request(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        request_message = request.POST.get('request_message')
        request_type = request.POST.get('request_type')  # Captura el tipo de solicitud
        
        User = get_user_model()
        try:
            user = User.objects.get(username=username)
            RecoveryRequest.objects.create(
                user=user, 
                request_message=request_message,
                request_type=request_type
            )
            messages.success(request, 'Tu solicitud ha sido enviada con éxito. Nos pondremos en contacto contigo.')
            return redirect('recovery')
        except User.DoesNotExist:
            messages.error(request, 'Usuario no encontrado.')
            return redirect('recovery')

    return render(request, 'recovery.html')
#---------------------------------------------------------------------------------------------------
@login_required
def view_recovery(request):
    requests = RecoveryRequest.objects.all()  # Obtener todas las solicitudes
    return render(request, 'recovery', {'recovery_request': requests})


@login_required
def download_recovery(request, request_id):
    recovery_request = get_object_or_404(RecoveryRequest, id=request_id)
    
    content = f"Solicitud de {recovery_request.user.username}\n\n"
    #content += f"Motivo: {recovery_request.request_type}\n"
    content += f"Mensaje: {recovery_request.request_message}\n"
    content += f"Fecha de solicitud: {recovery_request.submitted_at}\n"
    
    response = HttpResponse(content, content_type='text/plain')
    response['Content-Disposition'] = f'attachment; filename=solicitud_{request_id}.txt'

    return response


@login_required
def delete_recovery(request, request_id):
    recovery_request = get_object_or_404(RecoveryRequest, id=request_id)
    recovery_request.delete()  # Eliminar la solicitud
    return redirect('empleado')  # Redirigir a la lista de solicitudes
#---------------------------------------------------------------------------------------------------
def add_to_cart(request, product_id):
    try:
        product = get_object_or_404(Product, id=product_id)
        cart = request.session.get('cart', {})

        if str(product_id) in cart:
            cart[str(product_id)] += 1 
        else:
            cart[str(product_id)] = 1

        # Guardar el carrito en la sesión
        request.session['cart'] = cart
        messages.success(request, f'El producto {product.name} ha sido agregado al carrito.')
    except Product.DoesNotExist:
        messages.error(request, 'Error: el producto no existe.')
    except Exception as e:
        messages.error(request, 'Ha ocurrido un error al agregar el producto al carrito.')

    return redirect('Tienda')
#---------------------------------------------------------------------------------------------------
def remove_from_cart(request, product_id):
    # Obtener el producto que se quiere eliminar
    product = get_object_or_404(Product, id=product_id)

    # Obtener el carrito de la sesión
    cart = request.session.get('cart', [])

    # Filtrar el carrito para eliminar solo el producto específico
    cart = [item for item in cart if item['product_id'] != product_id]

    # Guardar el carrito actualizado en la sesión
    request.session['cart'] = cart

    # Mensaje de éxito
    messages.success(request, f'El producto {product.name} ha sido removido del carrito.')

    return redirect('cart_view')



