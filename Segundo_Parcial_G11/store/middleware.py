class CartMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Verificar si el carrito existe en la sesión del usuario
        if 'cart' not in request.session:
            request.session['cart'] = {}
        response = self.get_response(request)
        return response
