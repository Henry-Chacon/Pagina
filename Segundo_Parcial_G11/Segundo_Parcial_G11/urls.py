from django.contrib import admin
from django.urls import path, include
from django.conf.urls import handler404, handler500
from django.shortcuts import render
from store import views
from store.views import update_cart_sum
from store.views import checkout
from store.views import empleado
from store.views import download_order
from store.views import delete_order


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.Tienda, name='Tienda'),
    path('checkout/', views.checkout, name='checkout'),

    path('tommy1/', views.tommy1, name='tommy1'),
    path('tommy2/', views.tommy2, name='tommy2'),
    path('tommy3/', views.tommy3, name='tommy3'),

    path('boss1/', views.boss1, name='boss1'),
    path('boss2/', views.boss2, name='boss2'),
    path('boss3/', views.boss3, name='boss3'),

    path('lauren1/', views.lauren1, name='lauren1'),
    path('lauren2/', views.lauren2, name='lauren2'),
    path('lauren3/', views.lauren3, name='lauren3'),

    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('login/', views.login, name='login'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),
    path('adios/', views.adios, name='adios'),
    path('gracias/', views.gracias, name='gracias'),
    path('register/', views.register, name='register'),
    path('empleado/', views.empleado, name='empleado'),

    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('update-cart-sum/<int:product_id>/', views.update_cart_sum, name='update_cart_sum'),
    path('update-cart-res/<int:product_id>/', views.update_cart_res, name='update_cart_res'),
    path('remove_from_cart/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),

    path('download/', views.download, name='download'),
    path('cart/', views.cart_view, name='cart_view'),
    path('clear-cart/', views.clear_cart, name='clear_cart'),
    path('enviar_correo/<int:user_id>/', views.enviar_correo, name='enviar_correo'),
    path('download_order/<int:order_id>/', download_order, name='download_order'),
    path('delete_order/<int:order_id>/', delete_order, name='delete_order'),

    path('captcha/', include('captcha.urls')),
    path('recovery/', views.recovery_request, name='recovery'),
    #path('recovery/', views.recovery_request, name='load_recovery'),
    #path('recovery/', views.view_recovery, name='view_recovery'),
    path('recovery/download/<int:request_id>/', views.download_recovery, name='download_recovery'),
    path('recovery/delete/<int:request_id>/', views.delete_recovery, name='delete_recovery'),

]
