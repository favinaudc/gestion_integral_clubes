import secrets
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from django.urls import reverse_lazy
from django.db.models import Q
from apps.clubes.models import Club
from django.views.generic import CreateView, ListView, UpdateView, DeleteView, DetailView
from django.core.mail import send_mail
from django.contrib.auth.models import Group
from apps.customauth.forms import NuevoPerfilForm, NuevoUsuarioForm, UsuarioExistenteForm
from apps.customauth.models import PerfilClub, Usuario
from ..mixins import SharedFormMixin
from apps.customauth.mixins import ValidarRolClubMixin
from ..forms import ClubForm

class ClubCreateView(SharedFormMixin, CreateView):
    model = Club
    form_class = ClubForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Crear nuevo club'
        context['url_volver'] = 'clubes:listar_clubes'
        return context

    def get_success_url(self): #pone el pk en la url .
        print("self.object.pk", self.object.pk)
        return reverse_lazy('clubes:detalles_club', kwargs={'pk': self.object.pk})

class ClubDetailView(DetailView):
    model = Club
    template_name = 'clubes/club/club_detail.html'
    context_object_name = 'club'  # Nombre del contexto para acceder al club en la plantilla

    def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            context['url_volver'] = 'clubes:listar_clubes'  # URL para el botón de volver
            return context
    

class ClubListView(ListView):
    model = Club
    template_name = 'clubes/club/club_list.html'
    context_object_name = 'clubes'  # Nombre del contexto para acceder a los clubes en la plantilla  

    def get_queryset(self):
        queryset = super().get_queryset()
        
        q = self.request.GET.get('q')
        fecha_desde = self.request.GET.get('fecha_desde')
        fecha_hasta = self.request.GET.get('fecha_hasta')

        # Filtro de texto (búsqueda en múltiples campos con OR)
        if q:
            queryset = queryset.filter(
                Q(nombre__icontains=q) |
                Q(direccion__icontains=q) |
                Q(email__icontains=q)
            )
        
        # Filtros de fecha de fundación (Rango)
        if fecha_desde:
            queryset = queryset.filter(fecha_fundacion__gte=fecha_desde)
            
        if fecha_hasta:
            queryset = queryset.filter(fecha_fundacion__lte=fecha_hasta)
            
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['q'] = self.request.GET.get('q', '')
        context['fecha_desde'] = self.request.GET.get('fecha_desde', '')
        context['fecha_hasta'] = self.request.GET.get('fecha_hasta', '')
        return context

class ClubUpdateView(SharedFormMixin, UpdateView):
    model = Club
    form_class = ClubForm
    # template_name = 'clubes/club_form.html'  # Plantilla para el formulario de edición
    success_url = reverse_lazy('clubes:listar_clubes')  # Redirige a la lista de clubes después de editar un club

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = f'Editar club {self.object}'
        context['url_volver'] = 'clubes:listar_clubes'
        return context

class ClubDeleteView(DeleteView):
    model = Club
    template_name = 'clubes/club_confirm_delete.html'  # Plantilla por defecto que busca Django
    success_url = reverse_lazy('clubes:listar_clubes')  # Redirige a la lista después de eliminar un club


class GestionarClubView(ValidarRolClubMixin, View): 
    rol_requerido = ['CLUB_ADMIN']
    template_name = 'clubes/club/club_gestion.html'

    def dispatch(self, request, *args, **kwargs):
        club_id = kwargs.get('pk')
        club = Club.objects.filter(id=club_id).first()
        if not club:
            messages.error(request, "El club no existe.")
            return redirect('clubes:listar_clubes')
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        club_id = kwargs.get('pk')
        club = Club.objects.filter(id=club_id).first()
        context = {'club': club}
        return render(request, self.template_name, context)

def asociar_usuario_club(request, pk):
    club = get_object_or_404(Club, id=pk)
    form_existente = UsuarioExistenteForm()
    form_usuario = NuevoUsuarioForm()
    form_perfil = NuevoPerfilForm()

    if request.method == 'POST':
        action_type = request.POST.get('action_type')

        if action_type == 'existente':
            form_existente = UsuarioExistenteForm(request.POST)
            if form_existente.is_valid():
                usuario_cleanned = form_existente.cleaned_data['usuario']
                usuario = get_object_or_404(Usuario, cuit_cuil=usuario_cleanned.cuit_cuil)
                       
                grupo_admin = get_object_or_404(Group, name='CLUB_ADMIN')
                usuario.groups.add(grupo_admin)  # Asignar el grupo al usuario

                PerfilClub.objects.create(
                    perfil=usuario.perfil,  # Asumiendo que el usuario tiene un perfil asociado
                    club=club,
                    grupo_rol=grupo_admin
                )
                
                messages.success(request, f"Usuario asociado correctamente al club.")
                return redirect('clubes:listar_clubes') # Cambiar por tu URL

        elif action_type == 'nuevo':
            form_usuario = NuevoUsuarioForm(request.POST)
            form_perfil = NuevoPerfilForm(request.POST)
            
            # Validamos ambos formularios a la vez
            if form_usuario.is_valid() and form_perfil.is_valid():
                password_aleatoria = secrets.token_urlsafe(8)            
                
                # Crear el Usuario
                nuevo_usuario = form_usuario.save(commit=False)
                nuevo_usuario.set_password(password_aleatoria)
                nuevo_usuario.save()
                
                grupo_admin = get_object_or_404(Group, name='CLUB_ADMIN')
                nuevo_usuario.groups.add(grupo_admin)
                grupo_usuario = get_object_or_404(Group, name='USUARIO')
                nuevo_usuario.groups.remove(grupo_usuario)
                
                
                # Crear el Perfil y vincularlo al Usuario recién creado
                nuevo_perfil = form_perfil.save(commit=False)
                nuevo_perfil.usuario = nuevo_usuario
                nuevo_perfil.save()

                PerfilClub.objects.create(
                    perfil=nuevo_perfil,
                    club=club,
                    grupo_rol=grupo_admin
                )
                
                # Enviar correo con credenciales
                send_mail(
                    subject=f'Bienvenido al {club.nombre}',
                    message=f'Hola {nuevo_perfil.nombre},\n\nTu cuenta administrativa ha sido creada.\n\nUsuario (CUIT/CUIL): {nuevo_usuario.cuit_cuil}\nContraseña temporal: {password_aleatoria}\n\nPor favor, cámbiala al iniciar sesión.',
                    from_email='noreply@tuclub.com',
                    recipient_list=[nuevo_usuario.email],
                    fail_silently=False,
                )

                print(f"Correo enviado a {nuevo_usuario.email} con contraseña temporal: {password_aleatoria} - Para el usuario: {nuevo_usuario.cuit_cuil}")
                messages.success(request, "Usuario creado, perfil completado y notificado por email.")
                return redirect('clubes:listar_clubes')

    context = {
        'club': club,
        'form_existente': form_existente,
        'form_usuario': form_usuario,
        'form_perfil': form_perfil,
    }
    return render(request, 'clubes/club/crear_usuario_gestion.html', context)
