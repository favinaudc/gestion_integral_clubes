from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from .models import Usuario, Perfil, PerfilClub

# ==========================================
# INLINES
# ==========================================
class PerfilInline(admin.StackedInline):
    """Permite editar el Perfil desde la pantalla del Usuario"""
    model = Perfil
    can_delete = False
    verbose_name_plural = 'Perfil del Usuario'
    fk_name = 'usuario'

class PerfilClubInline(admin.TabularInline):
    """Permite vincular Clubes y Roles desde la pantalla del Perfil"""
    model = PerfilClub
    extra = 1  # Fila extra vacía para agregar rápidamente


# ==========================================
# ADMIN CLASSES
# ==========================================
@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    # Campos a mostrar en la lista del panel
    list_display = ('cuit_cuil', 'email', 'grupo_activo', 'is_active', 'is_staff')
    list_filter = ('is_active', 'is_staff', 'is_superuser', 'grupo_activo')
    search_fields = ('cuit_cuil', 'email')
    ordering = ('cuit_cuil',)
    
    # Acoplamos el Perfil al formulario del Usuario
    inlines = (PerfilInline,)
    
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
    readonly_fields = ('last_login',)


@admin.register(Perfil)
class PerfilAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'apellido', 'usuario', 'fecha_nacimiento')
    search_fields = ('nombre', 'apellido', 'usuario__cuit_cuil')
    list_filter = ('club',)
    
    # Acoplamos la tabla intermedia para gestionar asociaciones
    inlines = [PerfilClubInline]


@admin.register(PerfilClub)
class PerfilClubAdmin(admin.ModelAdmin):
    list_display = ('perfil', 'club', 'grupo_rol', 'fecha_asociacion')
    list_filter = ('club', 'grupo_rol', 'fecha_asociacion')
    search_fields = ('perfil__nombre', 'perfil__apellido', 'perfil__usuario__cuit_cuil', 'club__nombre')
    autocomplete_fields = () # Aquí puedes agregar 'perfil' y 'club' si usas search_fields en sus respectivos admins