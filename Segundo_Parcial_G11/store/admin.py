from django.contrib import admin
from django.contrib.auth.models import User, Group, Permission
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from .models import CustomUser, Cart, CartItem, Product

@admin.register(CustomUser)
class CustomUserAdmin(BaseUserAdmin):
    list_display = ('username', 'name', 'email', 'phone_number', 'is_employee', 'is_staff', 'is_active', 'direccion', 'is_locked', 'login_attempts', 'last_login')  # Campos a mostrar en la lista
    search_fields = ('username', 'name', 'email')  # Campos que se pueden buscar
    list_filter = ('is_employee', 'is_staff', 'is_active')  # Filtros en la lista

    fieldsets = (
        (None, {'fields': ('username', 'password')}),  # Dejar contraseña en lectura
        (_('Personal info'), {'fields': ('name', 'email', 'phone_number', 'direccion')}),
        (_('Permissions'), {'fields': ('is_employee', 'is_active', 'is_superuser', 'is_staff', 'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'name', 'email', 'phone_number', 'is_employee', 'is_staff', 'is_active', 'direccion', 'is_superuser'),
        }),
    )

    def save_model(self, request, obj, form, change):
        if change:
            # Si el usuario está siendo editado, no cambiar la contraseña a menos que explícitamente lo hagan
            password = form.cleaned_data.get('password1')
            if password:
                obj.set_password(password)  # Cambiar la contraseña de forma segura
        else:
            # Si es un nuevo usuario, establecer la contraseña
            password = form.cleaned_data.get('password1')
            if password:
                obj.set_password(password)

        super().save_model(request, obj, form, change)

    def get_form(self, request, obj=None, **kwargs):
        # No permitir la edición de la contraseña a menos que sea necesario
        form = super().get_form(request, obj, **kwargs)
        if obj:  # Si es una edición
            form.base_fields['password'].widget.attrs['readonly'] = True  # Establecer como solo lectura en edición
        return form



@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'stock', 'created_at', 'updated_at')  # Campos a mostrar en la lista
    search_fields = ('name',)  # Campos que se pueden buscar



def create_employee_group():
    employee_group, created = Group.objects.get_or_create(name='Empleados')
    content_type = ContentType.objects.get_for_model(Product)
    
    # Asigna permisos relacionados con los productos
    permissions = Permission.objects.filter(content_type=content_type)
    for permission in permissions:
        employee_group.permissions.add(permission)

    return employee_group