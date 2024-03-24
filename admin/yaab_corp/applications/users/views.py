from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth.models import Group
from django.urls import reverse_lazy,reverse
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from allauth.account.views import SignupView
import base64
from django.core.files.base import ContentFile
from PIL import Image
from io import BytesIO
from django.http import JsonResponse,HttpResponse,HttpResponseRedirect
from django.core.mail import send_mail,BadHeaderError
import os
from django.conf import settings
from django.views.generic import View,TemplateView,ListView,UpdateView,CreateView,DeleteView
from applications.dashboard.models import ProductoCreditoGrupal,Simulador
from applications.dashboard.forms import SimuladorForm
from .mixins import ValidarPermisosMixin
from .models import User,Ubicacion,CorreosCreditoGrupal,GrupoCreditoPersonal
from .forms import UserCreationForm,UserChangeForm,CorreoGrupoCredito,FormularioGRupoCreditoPersona
import apimarket
import uuid


import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
# Create your views here.

class RegistrarUsuario(CreateView):
    model = User
    template_name = 'users/register.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    
    def form_valid(self, form):
        # Obtenemos los datos del formulario
        email = form.cleaned_data['email']
        password = form.cleaned_data['password1']  # Obtenemos la contraseña

        # Creamos una instancia del modelo de usuario pero no la guardamos aún
        user = form.save(commit=False)
        # Usamos make_password para cifrar la contraseña antes de guardarla
        user.password = make_password(password)
        user.save()
        return super().form_valid(form)
    
    
def guardar_ubicacion(request):
    if request.method == 'POST':
        latitud = request.POST.get('latitud')  # Obtén estos valores del request POST
        longitud = request.POST.get('longitud')

        # Aquí puedes guardar la ubicación en la base de datos o realizar acciones necesarias
        
        Ubicacion.objects.create(latitud=latitud, longitud=longitud)
        
        return JsonResponse({'mensaje': 'Ubicación recibida correctamente.'})
    else:
        return JsonResponse({'mensaje': 'Solicitud no válida.'}, status=400)
    
class EditarUsuario(UpdateView):
    model = User
    template_name = 'users/editar-usuario.html'
    form_class = UserChangeForm
    success_url = reverse_lazy('user_app:lista_usuarios')
    
    
    
class EliminarUsuarios(DeleteView):
    model = User
    template_name = 'users/eliminar-usuario.html'
    success_url = reverse_lazy('user_app:lista_usuarios')
    
class ListaUsuarios(ListView):
    template_name = 'users/listar-usuarios.html'
    context_object_name = 'lista'

    def get_queryset(self):
        listar = User.objects.all()
        return listar
    
    
class SolicitudCheck(View):
    def post(self,request,user_id):
        try:
            user= User.objects.get(pk=user_id)
            user.solicitud = True
            user.save()
            return JsonResponse({'message': 'Solicitud marcada como true'})
        
        except User.DoesNotExist:
            return JsonResponse({'message': 'Solicitud no encontrada'}, status=404)
        
class ClientesAll(ListView):
    template_name = 'users/clientes.html'
    context_object_name = 'clientes'
    
    def get_queryset(self):
        
        cliente = User.objects.filter(solicitud=True)
            
        return cliente
        
        
# def crear_o_vincular_grupos_credito(correos, correos_credito):
#     for correo in correos:
#         grupo_credito_existente = GrupoCreditoPersonal.objects.filter(email=correo).first()

#         if grupo_credito_existente:
#             # Si existe, vincular este CorreosCreditoGrupal al GrupoCreditoPersonal existente
#             grupo_credito_existente.correos_credito = correos_credito
#             grupo_credito_existente.save()
#         else:
#             # Si no existe, crear un nuevo GrupoCreditoPersonal y vincularlo
#             nuevo_grupo_credito = GrupoCreditoPersonal(email=correo, correos_credito=correos_credito)
#             nuevo_grupo_credito.save()
    
class GrupalCredito(SignupView):
    
    template_name = 'users/credito-grupal.html'
    
    def get(self, request, *args, **kwargs):
        signup_form = self.get_form()
        correo_form = CorreoGrupoCredito()
        return render(request, self.template_name, {'signup_form': signup_form, 'correo_form': correo_form})
    
def correo_grupo_credito(request):
    
    if request.method == 'POST':
        
        nombres = request.POST.get('names_grupal')
        apellidos = request.POST.get('surnames_grupal')
        curp = request.POST.get('curp_texto_grupal')
        rfc = request.POST.get('rfc_grupal')
        celular = request.POST.get('celular_coordinador')  
        correo_coordinador = request.POST.get('correo_coordinador')
        participantes_id = request.POST.get('participantes_numero')  
        try:
           
            participantes = ProductoCreditoGrupal.objects.get(pk=participantes_id)
        except ProductoCreditoGrupal.DoesNotExist:
            participantes = None
            
        monto = request.POST.get('monto_vacantes')
        correos_electronicos = []
        
        for key, value in request.POST.items():
            if key.startswith('email_'):
                # Agregar los valores de los campos de correo electrónico a la lista
                correos_electronicos.append(value)
        
        if participantes:
            
            # monto_valor =  ProductoCreditoGrupal() 
            
            correo_nuevo = CorreosCreditoGrupal()
            correo_nuevo.guardar_correos(correos_electronicos,nombres,apellidos,curp,rfc,celular,participantes,monto,correo_coordinador)
            
            
            # Crear un nuevo GrupoCreditoPersonal y asignar los valores
            
            enlace_base = 'http://127.0.0.1:8000/users/formulario-credito/?token={}'
        
            for correo_destinatario in correos_electronicos:
                token = uuid.uuid4().hex  # Generar un token único
                
                nuevo_destinatario = GrupoCreditoPersonal(
                    email=correo_destinatario,
                    token=token,
                    correos_credito=correo_nuevo,
                    
                )
                
                if participantes:
                    
                                    
                    monto_valor, creado = ProductoCreditoGrupal.objects.get_or_create(
                        numero_participante=participantes.numero_participante,
                        defaults={'monto_credito': monto}  # Valores adicionales para la creación
                    )
                
                
                    nuevo_destinatario.productocreditogrupal = monto_valor
                    nuevo_destinatario.save()
                
                    enlace_destinatario = enlace_base.format(token) 
                    
                    mensaje = f'Debes de completar el formulario para unirte al crédito. Visita: {enlace_destinatario}'
                    send_mail(
                        'Credito grupal Yaab',
                        mensaje,
                        settings.EMAIL_HOST_USER,  # Email del remitente configurado en settings.py
                        [correo_destinatario],  # Lista de destinatarios
                        fail_silently=False,
                        
                    )
            
    return redirect('landing_app:landing')
   
    
def obtener_monto(request):
    if request.method == 'GET':
        monto_id = request.GET.get('monto_id')
        try:
            monto = ProductoCreditoGrupal.objects.get(id=monto_id)
            interest = monto.monto_credito
            return JsonResponse({'interest': interest})
        except ProductoCreditoGrupal.DoesNotExist:
            return JsonResponse({'interest': None})   


class FormularioCreditoGrupal(UpdateView):
    model = GrupoCreditoPersonal
    template_name = 'users/formulario-credito-grupal.html'
    form_class = FormularioGRupoCreditoPersona
    success_url = reverse_lazy('login')
    
    # def form_valid(self,form):
    #     token = self.request.GET.get('token')
    
    def get_object(self, queryset=None):
        token = self.request.GET.get('token')
        print(f"Token recibido: {token}")
        return get_object_or_404(GrupoCreditoPersonal, token=token)
    
    def form_valid(self, form):
        # Guardar los archivos si están presentes en la solicitud
        if self.request.FILES:
            
            ine_file = self.request.FILES.get('documento_ine_grupal')
            if ine_file:
                form.cleaned_data['documento_ine_grupal'] = ine_file
                
            for field_name, file in self.request.FILES.items():
                setattr(form.instance, field_name, file)
                
                
        signature_data = self.request.POST.get('signature', None)
        if signature_data:
            # Guardar la firma en tu modelo GrupoCreditoPersonal
            
            
            ## ultima actualizacion 
            # Convertir la cadena base64 en una imagen
            format, imgstr = signature_data.split(';base64,')  # Separar el encabezado de los datos base64
            ext = format.split('/')[-1]  # Obtener la extensión del archivo
            signature_img = ContentFile(base64.b64decode(imgstr), name=f'{self.object.token}_signature.{ext}')

            # Guardar la imagen en el campo firma_imagen
            form.instance.firma_imagen = signature_img
            form.instance.firma_digital = signature_data  # Limpiar el campo firma_digital, ya que ahora tienes la imagen
            
            
        
        self.object = form.save()
        token = self.object.token

        return super().form_valid(form)
        # response_data = {'message': 'Datos guardados exitosamente.'}
        # return JsonResponse(response_data)
        #return HttpResponseRedirect(reverse('login') + f'?token={token}')
    
    
    
class ModalBruroCredito(TemplateView):
    template_name = 'users/buro-credito-html.html'
    
class AvisoPrivacidadGrupal(TemplateView):
    template_name = 'users/aviso-privacidad-grupal.html'
 
 
 
# def tu_vista_crear_simulador(request,user_id):
    
#     usuario_actual = User.objects.get(pk=user_id)
    
#     if request.method == 'POST':
        
#         formulario = SimuladorForm(request.POST)
#         if formulario.is_valid():
#             simulador = Simulador.objects.create(
#                 tipo_credito=formulario.cleaned_data['tipo_credito'],
#                 plazo_nombre=formulario.cleaned_data['plazo_nombre'],
#                 term=formulario.cleaned_data['term'],
#                 amount=formulario.cleaned_data['amount'],
#                 interest_rate=formulario.cleaned_data['interest_rate'],
#                 monthly_payment=formulario.cleaned_data['monthly_payment']
#             )
            
#             usuario_actual.simulador = simulador
#             usuario_actual.save()
            
#             return redirect('dashboard_app:index')
        
#     else:
            
#         formulario = SimuladorForm()
#     return render(request,'index.html',{'formulario':formulario})
        
        
            
            