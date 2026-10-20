from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from .models import Usuario

@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    # Campos a mostrar en la lista del panel
    list_display = ('cuit_cuil', 'email', 'grupo_activo', 'is_active', 'is_staff')
    
    # Filtros laterales
    list_filter = ('is_active', 'is_staff', 'is_superuser', 'grupo_activo')
    
    # Barra de búsqueda (busca por CUIT/CUIL y Email)
    search_fields = ('cuit_cuil', 'email')
    
    # Ordenamiento por defecto
    ordering = ('cuit_cuil',)
    
    # Configuración de los campos al EDITAR un usuario existente
    fieldsets = (
        (None, {'fields': ('cuit_cuil', 'password')}),
        (_('Información de Contacto'), {'fields': ('email',)}),
        (_('Permisos y Grupos'), {
            'fields': (
                'is_active', 
                'is_staff', 
                'is_superuser', 
                'grupo_activo', 
                'groups', 
                'user_permissions'
            ),
        }),
        (_('Fechas Importantes'), {'fields': ('last_login',)}),
    )

    # Configuración de los campos al CREAR un nuevo usuario desde el admin
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('cuit_cuil', 'email', 'grupo_activo', 'is_staff', 'is_active'),
        }),
    )
    
    # Opcional: mostrar las propiedades como campos de solo lectura si querés verlas en el admin
    readonly_fields = ('last_login',)