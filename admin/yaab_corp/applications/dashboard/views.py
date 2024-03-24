from django.forms import BaseModelForm
from django.contrib import messages
from django.shortcuts import render
from django.contrib.auth.models import Group
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.views import View
from django.views.decorators.http import require_POST,require_GET
from django.db import IntegrityError
from django.http import HttpResponseBadRequest

import base64
from django.core.files.base import ContentFile

from django.views.generic import TemplateView
from django.views.generic import ListView,UpdateView,CreateView,DeleteView
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render,redirect,get_object_or_404

from django.urls import reverse_lazy,reverse
from django.template.loader import get_template
from django.http import FileResponse
from datetime import datetime
import locale

from .models import Productos,Plazo,Simulador,ImageYaab,ProductoCreditoGrupal,Prestamo,SimuladorPrueba,PruebaSimula
from .forms import ProductosForm,PlazoPagoForm,SimuladorForm,FormProductosGrupal,PrestamoForm,SimPruebas,SimuladorPruebaForm,PruebaSimulaForms

from applications.users.models import User,GrupoCreditoPersonal,CorreosCreditoGrupal
from applications.users.mixins import ValidarPermisosMixin
from applications.users.forms import UserChangeForm
from .utils import render_to_pdf,crearMifiel
from mifiel import Document, Client
import apimarket
import uuid
import logging



# Create your views here.from django.views.generic.base import TemplateView
class DashboardView(LoginRequiredMixin,CreateView):
    model = SimuladorPrueba
    template_name="dashboard/index.html"
    form_class = SimPruebas #SimuladorForm
    success_url = reverse_lazy('dashboard_app:index')
    
    def form_valid(self, form):
        # Asignar el usuario logeado al campo usuario_user antes de guardar
        form.instance.usuario_user = self.request.user
        return super().form_valid(form)
    
class GetNombreProductoView(View):
    def get(self, request, prestamo_id, *args, **kwargs):
        prestamo = get_object_or_404(Prestamo, id=prestamo_id)
        nombre_producto = prestamo.nombre_producto
        tipo_prestamo_nombre = prestamo.tipo_prestamo.tipo_credito if prestamo.tipo_prestamo else None
        tipo_periodo = prestamo.tipo_periodo.periodo_credito if prestamo.tipo_periodo else None
        plazo = prestamo.plazo
        interes_ordinario = prestamo.interes_ordinario
        interes_moratorio = prestamo.interes_moratorio
        pago_mensual = prestamo.pago_mensual
        return JsonResponse({'nombre_producto': nombre_producto,'tipo_prestamo':tipo_prestamo_nombre,'tipo_periodo': tipo_periodo,'plazo':plazo,'interes_ordinario':interes_ordinario,'interes_moratorio':interes_moratorio,'pago_mensual':pago_mensual})





##el bueno##
# class DashboardView(CreateView):
#     template_name="dashboard/index.html"
#     form_class = SimuladorForm
#     success_url = reverse_lazy('dashboard_app:index')
    
#     def get_context_data(self, **kwargs):
#         context = super(DashboardView, self).get_context_data(**kwargs)
#         user = self.kwargs.get('pk')
#         #user_id = self.kwargs.get('pk')
#         #user_id = self.kwargs.get('user_id')
#         #print("Valor de user_id:", user_id)
#         context['pk'] = user
#         context['simula'] = Simulador.objects.filter(id=user)
        

#         return context
    
#     def form_valid(self, form):
        
#         # user_id = self.kwargs.get('user_id')
#         # usuario_actual = get_object_or_404(User, pk=user_id)
        
#         tipo_credito = form.cleaned_data['tipo_credito']
#         plazo_nombre = form.cleaned_data['plazo_nombre']
#         amount = form.cleaned_data['amount']
#         interest_rate = form.cleaned_data['interest_rate']
#         term = form.cleaned_data['term']

#         # Realiza el cálculo
#         monthly_interest_rate = (interest_rate / 12) / 100
#         num_payments = term * 12
#         monthly_payment = (amount * monthly_interest_rate) / (1 - (1 + monthly_interest_rate) ** -num_payments) + (amount / 12) 

#         # Guarda los resultados en la base de datos o donde lo necesites
#         # Aquí se asume que hay un modelo Loan para guardar los resultados
        
#         loan = Simulador(amount=amount, tipo_credito = tipo_credito,plazo_nombre=plazo_nombre, interest_rate=interest_rate, term=term, monthly_payment=monthly_payment)
#         loan.save()
        
#         # url_crear_simulador = reverse('crear_simulador', kwargs={'user_id': user_id})
        
#         # # Guarda el simulador asociándolo al usuario actual
#         # simulador = Simulador.objects.create(
#         #     tipo_credito=tipo_credito,
#         #     plazo_nombre=plazo_nombre,
#         #     amount=amount,
#         #     interest_rate=interest_rate,
#         #     term=term,
#         #     monthly_payment=monthly_payment
#         # )
#         # usuario_actual.simulador = simulador
#         # usuario_actual.save()

#         response_data = {'monthly_payment': monthly_payment}
#         return JsonResponse(response_data)

# class DashboardView(LoginRequiredMixin,CreateView):
#     model = SimuladorPrueba
#     template_name="dashboard/index.html"
#     form_class = SimPruebas #SimuladorForm
#     success_url = reverse_lazy('dashboard_app:index')
    
    
#     def form_valid(self, form):
#         # Guarda la instancia de SimuladorPrueba y asocia el simulador al usuario
#         response = super().form_valid(form)
#         self.object.usuario = self.request.user
#         self.object.save()

#         # Puedes agregar un mensaje si lo deseas
#         messages.success(self.request, 'Simulador guardado exitosamente.')

#         return response
    
    
         
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['montos_prestamo'] = Prestamo.objects.values_list('monto', flat=True)
#         context['prestamos'] = Prestamo.objects.select_related('tipo_prestamo').all().order_by('id')
#         context['tabla_prestamos'] = Prestamo.objects.all()
        
#         return context

#checar esto despues
# class GetNombreProductoView(View):
#     def get(self, request, prestamo_id, *args, **kwargs):
#         prestamo = get_object_or_404(Prestamo, id=prestamo_id)
#         nombre_producto = prestamo.nombre_producto
#         tipo_prestamo_nombre = prestamo.tipo_prestamo.tipo_credito if prestamo.tipo_prestamo else None
#         return JsonResponse({'nombre_producto': nombre_producto,'tipo_prestamo':tipo_prestamo_nombre})
    
    
    # def post(self, request, *args, **kwargs):
    #     try:
    #         # Puedes procesar el índice y realizar otras acciones aquí
    #         selected_index = int(request.POST.get('selected_index'))

    #         # Intenta acceder a la instancia de Prestamo según el índice
    #         prestamo_instance = Prestamo.objects.get(id=selected_index)

    #         # Crea una instancia de tu modelo y guárdala
    #         simulador_prueba = SimuladorPrueba(nombre_prestamo=prestamo_instance)
    #         simulador_prueba.save()

    #         return JsonResponse({'success': True})
    #     except Prestamo.DoesNotExist:
    #         # Maneja el caso donde el Prestamo con el índice dado no existe
    #         return JsonResponse({'success': False, 'error': 'Prestamo no encontrado'}, status=404)
    #     except Exception as e:
    #         # Maneja otras excepciones generales
    #         return JsonResponse({'success': False, 'error': str(e)}, status=500)
    
    # def form_valid(self, form):
    #     try:
    #         # Puedes procesar el índice y realizar otras acciones aquí
    #         selected_index = int(self.request.POST.get('selected_index'))

    #         # Intenta acceder a la instancia de Prestamo según el índice
    #         prestamo_instance = Prestamo.objects.get(id=selected_index)

    #         # Crea una instancia de tu modelo y guárdala
    #         simulador_prueba = SimuladorPrueba(nombre_prestamo=prestamo_instance)
    #         simulador_prueba.save()

    #         return JsonResponse({'success': True})
    #     except Prestamo.DoesNotExist:
    #         # Maneja el caso donde el Prestamo con el índice dado no existe
    #         return JsonResponse({'success': False, 'error': 'Prestamo no encontrado'}, status=404)
    #     except Exception as e:
    #         # Maneja otras excepciones generales
    #         return JsonResponse({'success': False, 'error': str(e)}, status=500)
    
    #@staticmethod
    
    
    # def guardar_datos_backend(request):
    #     if request.method == 'POST':
    #         selected_index = request.POST.get('selected_index')
            
    #         # Procesar y guardar los datos según tus necesidades

    #         # Devolver una respuesta (en este caso, solo un mensaje de éxito)
    #         return JsonResponse({'success': True})
    #     else:
    #         # Devolver una respuesta indicando un método no permitido
    #         return JsonResponse({'success': False, 'error': 'Método no permitido'}, status=405)
    
    
    
    # def form_valid(self, form):
    #     if form.is_valid():
    #         nuevo_simulador = form.save(commit=False)
    #         nuevo_simulador.save()
    #         return super().form_valid(form)
    #     else:
    #         print(form.errors)  # Muestra los errores del formulario en la consola
    #         return super().form_invalid(form)
    
    # def form_valid(self, form):
    #     print('Formulario es válido')
        
    #     #tipo_prestamo = Prestamo.objects.first()  
        
    #     #tipo_prestamo = Prestamo.objects.filter(monto=monto_seleccionado).first()
    #     try:
        
    #         tipo_prestamo_id = form.cleaned_data['tipo_prestamo']
    #         #tipo_prestamo = Prestamo.objects.select_related('tipo_prestamo').get(id=tipo_prestamo_id)
    #         tipo_prestamo = Prestamo.objects.get(id=tipo_prestamo_id)
            
    #         #form.instance.tipo_prestamo = tipo_prestamo
    #         form.instance.nombre_prestamo = tipo_prestamo
        
    #         return super().form_valid(form)
    #     except IntegrityError as e:
    #         print(f'Error al guardar: {e}')
    #         return HttpResponseBadRequest('Hubo un problema al intentar crear el SimuladorPrueba. Por favor, inténtalo de nuevo.')
    
    ''' 
    def form_valid(self, form):
        
        # user_id = self.kwargs.get('user_id')
        # usuario_actual = get_object_or_404(User, pk=user_id)
        if self.request.user.is_authenticated:
            usuario_actual = self.request.user
            tipo_credito = form.cleaned_data['tipo_credito']
            plazo_nombre = form.cleaned_data['plazo_nombre']
            amount = form.cleaned_data['amount']
            interest_rate = form.cleaned_data['interest_rate']
            interest_moratorio = form.cleaned_data['interest_moratorio']
            term = form.cleaned_data['term']

            # Realiza el cálculo
            monthly_interest_rate = (interest_rate / 12) / 100
            num_payments = term * 12
            monthly_payment = (amount * monthly_interest_rate) / (1 - (1 + monthly_interest_rate) ** -num_payments) + (amount / 12) 
            
            
            simulador = Simulador.objects.create(
                tipo_credito=tipo_credito,
                plazo_nombre=plazo_nombre,
                amount=amount,
                interest_rate=interest_rate,
                term=term,
                interest_moratorio=interest_moratorio,
                monthly_payment=monthly_payment
            )
            usuario_actual.simulador = simulador
            usuario_actual.save()

        response_data = {'monthly_payment': monthly_payment}
        return JsonResponse(response_data)
    '''

'''
class DashboardView(LoginRequiredMixin,CreateView):
    template_name="dashboard/index.html"
    form_class = SimuladorForm
    success_url = reverse_lazy('dashboard_app:index')
    
    # def get_context_data(self, **kwargs):
    #     context = super(DashboardView, self).get_context_data(**kwargs)
    #     user = self.kwargs.get('pk')
    #     #user_id = self.kwargs.get('pk')
    #     #user_id = self.kwargs.get('user_id')
    #     #print("Valor de user_id:", user_id)
    #     context['pk'] = user
    #     context['simula'] = Simulador.objects.filter(id=user)
        

    #     return context
    
    def form_valid(self, form):
        
        # user_id = self.kwargs.get('user_id')
        # usuario_actual = get_object_or_404(User, pk=user_id)
        if self.request.user.is_authenticated:
            usuario_actual = self.request.user
            tipo_credito = form.cleaned_data['tipo_credito']
            plazo_nombre = form.cleaned_data['plazo_nombre']
            amount = form.cleaned_data['amount']
            interest_rate = form.cleaned_data['interest_rate']
            interest_moratorio = form.cleaned_data['interest_moratorio']
            term = form.cleaned_data['term']

            # Realiza el cálculo
            monthly_interest_rate = (interest_rate / 12) / 100
            num_payments = term * 12
            monthly_payment = (amount * monthly_interest_rate) / (1 - (1 + monthly_interest_rate) ** -num_payments) + (amount / 12) 

            # Guarda los resultados en la base de datos o donde lo necesites
            # Aquí se asume que hay un modelo Loan para guardar los resultados
            
            # loan = Simulador(amount=amount, tipo_credito = tipo_credito,plazo_nombre=plazo_nombre, interest_rate=interest_rate, term=term, monthly_payment=monthly_payment)
            # loan.save()
        
        # url_crear_simulador = reverse('crear_simulador', kwargs={'user_id': user_id})
        
            # Guarda el simulador asociándolo al usuario actual
            simulador = Simulador.objects.create(
                tipo_credito=tipo_credito,
                plazo_nombre=plazo_nombre,
                amount=amount,
                interest_rate=interest_rate,
                term=term,
                interest_moratorio=interest_moratorio,
                monthly_payment=monthly_payment
            )
            usuario_actual.simulador = simulador
            usuario_actual.save()

        response_data = {'monthly_payment': monthly_payment}
        return JsonResponse(response_data)
'''




##el bueno##
# class DashboardView(CreateView):
#     template_name="dashboard/index.html"
#     form_class = SimuladorForm
#     success_url = reverse_lazy('dashboard_app:index')
    
#     def get_context_data(self, **kwargs):
#         context = super(DashboardView, self).get_context_data(**kwargs)
#         user = self.kwargs.get('pk')
#         #user_id = self.kwargs.get('pk')
#         #user_id = self.kwargs.get('user_id')
#         #print("Valor de user_id:", user_id)
#         context['pk'] = user
#         context['simula'] = Simulador.objects.filter(id=user)
        

#         return context
    
#     def form_valid(self, form):
        
#         # user_id = self.kwargs.get('user_id')
#         # usuario_actual = get_object_or_404(User, pk=user_id)
        
#         tipo_credito = form.cleaned_data['tipo_credito']
#         plazo_nombre = form.cleaned_data['plazo_nombre']
#         amount = form.cleaned_data['amount']
#         interest_rate = form.cleaned_data['interest_rate']
#         term = form.cleaned_data['term']

#         # Realiza el cálculo
#         monthly_interest_rate = (interest_rate / 12) / 100
#         num_payments = term * 12
#         monthly_payment = (amount * monthly_interest_rate) / (1 - (1 + monthly_interest_rate) ** -num_payments) + (amount / 12) 

#         # Guarda los resultados en la base de datos o donde lo necesites
#         # Aquí se asume que hay un modelo Loan para guardar los resultados
        
#         loan = Simulador(amount=amount, tipo_credito = tipo_credito,plazo_nombre=plazo_nombre, interest_rate=interest_rate, term=term, monthly_payment=monthly_payment)
#         loan.save()
        
#         # url_crear_simulador = reverse('crear_simulador', kwargs={'user_id': user_id})
        
#         # # Guarda el simulador asociándolo al usuario actual
#         # simulador = Simulador.objects.create(
#         #     tipo_credito=tipo_credito,
#         #     plazo_nombre=plazo_nombre,
#         #     amount=amount,
#         #     interest_rate=interest_rate,
#         #     term=term,
#         #     monthly_payment=monthly_payment
#         # )
#         # usuario_actual.simulador = simulador
#         # usuario_actual.save()

#         response_data = {'monthly_payment': monthly_payment}
#         return JsonResponse(response_data)

def obtener_interes(request):
    if request.method == 'GET':
        product_id = request.GET.get('product_id')
        try:
            plazo = Plazo.objects.get(id=product_id)
            interest = plazo.interes_credito
            return JsonResponse({'interest': interest})
        except Productos.DoesNotExist:
            return JsonResponse({'interest': None})

def obtener_moratorio(request):
    if request.method == 'GET':
        producto_id = request.GET.get('producto_id')
        try:
            moratorio = Plazo.objects.get(id=producto_id)
            interes_mora = moratorio.interes_moratorio
            return JsonResponse({'interes_mora': interes_mora})
        except Plazo.DoesNotExist:
            return JsonResponse({'interes_mora':None})
            
        
def obtener_plazo(request):
    if request.method == 'GET':
        product_id = request.GET.get('product_id')
        try:
            product = Plazo.objects.get(id=product_id)
            plazo = product.semanas
            return JsonResponse({'plazo': plazo})
        except Productos.DoesNotExist:
            return JsonResponse({'plazo': None})
          


class PreguntasRespuestas(TemplateView):
    template_name = 'dashboard/preguntas-respuestas.html'
 
 

    
#####productos grupal#####
    
class CreateGrupal(CreateView):
    model = ProductoCreditoGrupal
    form_class = FormProductosGrupal
    template_name = 'dashboard/productos/nuevo-grupal.html'
    success_url = reverse_lazy('dashboard_app:productos_gral')
    
class EditarGrupal(UpdateView):
    model = ProductoCreditoGrupal
    template_name = 'dashboard/productos/editar-grupal.html'
    form_class = FormProductosGrupal
    success_url = reverse_lazy('dashboard_app:productos_gral')  
    
#####productos grupal#####  

        
    
#####productos#####


class ProductosView(ListView):
    
    model = Productos
    template_name = 'dashboard/productos/productos.html'
    #permission_required = ('productos.permiso_admin')
    context_object_name = 'productos'
    
    
    
    def get_queryset(self):
        producto = Productos.objects.all()
        return  producto
    
    def get_context_data(self, **kwargs):
        context = super(ProductosView,self).get_context_data(**kwargs)
        
        context["plazo"] = Plazo.objects.all()  
        context["grupal"] = ProductoCreditoGrupal.objects.all()
        context['prestamos'] = Prestamo.objects.all()
    
        return context
    
class CreateProductosView(CreateView):
    model=Prestamo
    form_class = PrestamoForm
    template_name = 'dashboard/productos/nuevo-prestamo.html'
    success_url = reverse_lazy('dashboard_app:productos_gral')
# class CreateProductosView(CreateView):
#     model=Productos
#     form_class = ProductosForm
#     template_name = 'dashboard/productos/nuevo-producto.html'
#     success_url = reverse_lazy('dashboard_app:productos_gral')

class EditarProducto(UpdateView):
    model = Productos
    template_name = 'dashboard/productos/editar-productos.html'
    form_class = ProductosForm
    success_url = reverse_lazy('dashboard_app:productos_gral')  
    
class EliminarProducto(DeleteView):
    model = Productos
    template_name = 'dashboard/productos/eliminar-productos.html'
    form_class = ProductosForm
    success_url = reverse_lazy('dashboard_app:productos_gral') 

#####productos#####

#####plazo#####

class CreatePlazoView(CreateView):
    model = Plazo
    form_class = PlazoPagoForm
    template_name = 'dashboard/plazos/nuevo-plazo.html'
    success_url = reverse_lazy('dashboard_app:productos_gral')
    
class EditarPlazoView(UpdateView):
    model = Plazo
    form_class = PlazoPagoForm
    template_name = 'dashboard/plazos/editar-plazo.html'
    success_url = reverse_lazy('dashboard_app:productos_gral') 

class EliminarPlazo(DeleteView):
    model = Plazo
    template_name = 'dashboard/plazos/eliminar-plazo.html'
    form_class = PlazoPagoForm
    success_url = reverse_lazy('dashboard_app:productos_gral') 
    
#####plazo#####

##### seccion usuarios ######


@login_required
#@csrf_exempt
def guardar_firma(request, user_id):
    user = get_object_or_404(User, id=user_id)

    if request.method == 'POST':
        signature_data = request.POST.get('signature', None)

        if signature_data:
            # Convertir la cadena base64 en una imagen
            format, imgstr = signature_data.split(';base64,')  # Separar el encabezado de los datos base64
            ext = format.split('/')[-1]  # Obtener la extensión del archivo
            signature_filename = f'{user_id}_signature.{ext}'
            signature_img = ContentFile(base64.b64decode(imgstr), name=signature_filename)

            # Guardar la imagen en el campo firma_imagen
            user.firma_imagen_personal = signature_img
            user.firma_digital_personal = signature_data  # Limpiar el campo firma_digital, ya que ahora tienes la imagen
            user.save()

            return JsonResponse({'success': True})
        else:
            return JsonResponse({'error': 'Datos de firma no proporcionados'}, status=400)
    else:
        return JsonResponse({'error': 'Método no permitido'}, status=405)




class EditarUsuarioUsers(UpdateView):
    model = User
    template_name = 'dashboard/registro-usuario/completar-registro.html'
    form_class = UserChangeForm
    success_url = reverse_lazy('dashboard_app:index')
    
    # def form_valid(self,form):
    #     signature_data = self.request.POST.get('signature', None)
    #     imagen_perfil_data = self.request.FILES.get('imagen_perfil',None)
        
            
            
    #     if imagen_perfil_data:
    #         form.instance.imagen_perfil = self.procesar_imagen_perfil(imagen_perfil_data)
    #         print("Formulario válido")
    #     else:
    #         print("Errores en el formulario:", form.errors)
        
        
    #     if signature_data:
    #         # Guardar la firma en tu modelo GrupoCreditoPersonal
            
            
    #         ## ultima actualizacion 
    #         # Convertir la cadena base64 en una imagen
    #         format, imgstr = signature_data.split(';base64,')  # Separar el encabezado de los datos base64
    #         ext = format.split('/')[-1]  # Obtener la extensión del archivo
    #         user_id = self.request.user.id
    #         signature_filename = f'{user_id}_signature.{ext}'
    #         signature_img = ContentFile(base64.b64decode(imgstr), name=signature_filename)
    #         #signature_img = ContentFile(base64.b64decode(imgstr), name=f'{self.object.token}_signature.{ext}')

    #         # Guardar la imagen en el campo firma_imagen
    #         form.instance.firma_imagen_personal = signature_img
    #         form.instance.firma_digital_personal = signature_data  # Limpiar el campo firma_digital, ya que ahora tienes la imagen
            
        
    #     self.object = form.save()
    #     return super().form_valid(form)
    
    # def procesar_imagen_perfil(self, imagen_perfil_data):
    #     # Puedes personalizar este método según tus necesidades
    #     # En este ejemplo, simplemente asignamos la imagen al campo de imagen de perfil
    #     return imagen_perfil_data
    
    
# @login_required
# @csrf_exempt
# def guardar_firma(request):
#     if request.method == 'POST':
#         firma_base64 = request.POST.get('firma_digital_personal', '')
        
#         # Accede al usuario actual
#         usuario_actual = request.user

#         # Asigna la firma al campo en el modelo User
#         usuario_actual.firma_digital_personal = firma_base64
#         usuario_actual.save()
        
#         return JsonResponse({'success': True})
#     else:
#         return JsonResponse({'error': 'Método no permitido'}, status=405)   
   
    
class AvisoPrivacidad(TemplateView):
    template_name = 'dashboard/aviso-privacidad.html'
    
class TerminosCondiciones(TemplateView):
    template_name = 'dashboard/terminos-condiciones.html'
    
##### seccion usuarios ######
    
##### seccion pdf ###### 
class PdfDocument(View):
    login_url = '/login/'
    
    def get(self, request, *args, **kwargs):
        user = request.user
        imagen_yaab = ImageYaab.objects.all()
        empleados = User.objects.filter(id=user.id)
        
        data = {
            'count': empleados.count(),
            'empleados': empleados,
            'imagen_yaab_url': imagen_yaab,
            'nombre':user,
            #'montos': montos,
            'image_path': '/admin/media/profile.jpg',            
            
        }
        output_path = 'static/media/solicitud.pdf'
        pdf = render_to_pdf('dashboard/pdf.html', data,output_path)
        if pdf:
            print("PDF guardado correctamente")
        else:
            print("PDF guardado correctamente")
        
        return HttpResponse("PDF generado y guardado")
        


    
##### seccion pdf ###### 

### seccion pdf  credito grupal ###
class PdfDocumentGrupal(View):
    
    def convertir_a_letras(self, numero):
        unidades = ['', 'uno', 'dos', 'tres', 'cuatro', 'cinco', 'seis', 'siete', 'ocho', 'nueve']
        decenas = ['', 'diez', 'veinte', 'treinta', 'cuarenta', 'cincuenta', 'sesenta', 'setenta', 'ochenta', 'noventa']
        especiales = {10: 'diez', 11: 'once', 12: 'doce', 13: 'trece', 14: 'catorce', 15: 'quince', 16: 'dieciséis', 17: 'diecisiete', 18: 'dieciocho', 19: 'diecinueve'}
        centenas = ['', 'ciento', 'doscientos', 'trescientos', 'cuatrocientos', 'quinientos', 'seiscientos', 'setecientos', 'ochocientos', 'novecientos']

        if 1 <= numero <= 99:
            if numero in especiales:
                return especiales[numero]
            else:
                return decenas[numero // 10] + ('' if numero % 10 == 0 else '  ' + unidades[numero % 10])
        elif 100 <= numero <= 999:
            return centenas[numero // 100] + ('' if numero % 100 == 0 else ' ' + self.convertir_a_letras(numero % 100))
        elif 1000 <= numero <= 999999:
            return self.convertir_a_letras(numero // 1000) + ' mil' + ('' if numero % 1000 == 0 else ' ' + self.convertir_a_letras(numero % 1000))
        elif 1000000 <= numero <= 999999999:
            return self.convertir_a_letras(numero // 1000000) + ' millones' + ('' if numero % 1000000 == 0 else ' ' + self.convertir_a_letras(numero % 1000000))
        else:
            return "Número no soportado"  # Puedes agregar más lógica para números mayores si es necesario
    
    def get(self, request, *args, **kwargs):
        token = self.request.GET.get('token')
        
        monto = CorreosCreditoGrupal.objects.all()
        imagen_yaab = ImageYaab.objects.all()
        user = get_object_or_404(GrupoCreditoPersonal, token=token)
        users_list = [user]
        
        producto_credito_grupal = user.productocreditogrupal
        
        if producto_credito_grupal:
            monto_grupal = CorreosCreditoGrupal.objects.filter(participantes_numero=producto_credito_grupal).values('monto_vacantes').first()
            print(monto_grupal)
            print('hola a todos')
        else:
            monto_grupal = None
            
        monto_letras = self.convertir_a_letras(int(monto_grupal['monto_vacantes'])) if monto_grupal else None
        
        imagen_yaab = ImageYaab.objects.all()
        
        locale.setlocale(locale.LC_TIME, 'es_ES.utf8')
        fecha_actual = datetime.now()
        
        fecha_formateada = fecha_actual.strftime('%d de %B de %Y')
       
        data = {
            'monto_grupal':monto_grupal['monto_vacantes']if monto_grupal else None,
            'monto_letras':monto_letras,
            'fecha':fecha_formateada,
            'imagen_yaab_url': imagen_yaab,
            'nombre':users_list,
            'image_path': '/admin/media/profile.jpg',            
            
        }
        output_path = 'static/media/solicitud.pdf'
        pdf = render_to_pdf('dashboard/hola_soy_pdf.html', data,output_path)

        if pdf:
            # Abre el archivo PDF generado y lo devuelve como respuesta
            with open(output_path, 'rb') as pdf_file:
                response = HttpResponse(pdf_file.read(), content_type='application/pdf')
                response['Content-Disposition'] = 'inline; filename="hola_soy_pdf.pdf"'  # Cambia el nombre del archivo si quieres
                return response
        else:
            return HttpResponse("Error al generar el PDF")

### seccion pdf  credito grupal ###


    

##### seccion mifiel ###### 
@login_required
def crearMifiel(request):
    
    client = Client(app_id=settings.MIFIEL_API_TOKEN, secret_key=settings.MIFIEL_API_TOKEN_SECRET)
  
    user = request.user
    
    name = user.first_name
    email = user.email
    tax_id = user.rfc
    
    signatories = [
        {
            'name': name,
            'email': email,
            'tax_id': tax_id 
        }
    ]
    viewers = [
        {
           
            'email': 'paulina.gutierrez@yaab.mx'
        }
    ]
    file_path = 'static/media/solicitud.pdf'
    
    document = Document.create(
        client=client,
        signatories=signatories,
        viewers=viewers,
        file=file_path,
    )   
    
    # return document
    return HttpResponse("Documento creado")

##### seccion mifiel ###### 


class InfoBuro(TemplateView):
    template_name = 'dashboard/buro-credito.html'
    


### pruebas simulador ##### 
class PrestamoCreateView(CreateView):
    model = Prestamo
    form_class = PrestamoForm
    template_name = 'dashboard/prestamo_form.html'
    success_url = reverse_lazy('dashboard_app:nuevo_prestamo') 
    
class SimPrestamoCreateView(CreateView):
    model = SimuladorPrueba
    form_class = SimPruebas
    template_name = 'dashboard/sim_prest.html'
    success_url = reverse_lazy('dashboard_app:sim_prestamo') 
    
    def get_context_data(self, **kwargs):
        context = super(SimPrestamoCreateView,self).get_context_data(**kwargs)
        #context['montos_prestamo'] = Prestamo.objects.values_list('monto', flat=True).distinct()
        #context['montos_prestamo'] = Prestamo.objects.exclude(monto__isnull=True).values_list('monto', flat=True)
        context['montos_prestamo'] = Prestamo.objects.values_list('monto', flat=True)
        context['prestamos'] = Prestamo.objects.select_related('tipo_prestamo').all().order_by('id')
        context['tabla_prestamos'] = Prestamo.objects.all()
        
        return context
    
    def form_valid(self, form):
        try:
            # Puedes procesar el índice y realizar otras acciones aquí
            selected_index = int(self.request.POST.get('selected_index'))

            # Intenta acceder a la instancia de Prestamo según el índice
            prestamo_instance = Prestamo.objects.get(id=selected_index)

            # Crea una instancia de tu modelo y guárdala
            simulador_prueba = SimuladorPrueba(nombre_prestamo=prestamo_instance)
            simulador_prueba.save()

            return JsonResponse({'success': True})
        except Prestamo.DoesNotExist:
            # Maneja el caso donde el Prestamo con el índice dado no existe
            return JsonResponse({'success': False, 'error': 'Prestamo no encontrado'}, status=404)
        except Exception as e:
            # Maneja otras excepciones generales
            return JsonResponse({'success': False, 'error': str(e)}, status=500)
    
    # def form_valid(self, form):
    #     #tipo_prestamo = Prestamo.objects.first()  
        
    #     #tipo_prestamo = Prestamo.objects.filter(monto=monto_seleccionado).first()
        
    #     tipo_prestamo_id = form.cleaned_data['tipo_prestamo']
    #     tipo_prestamo = Prestamo.objects.select_related('tipo_prestamo').get(id=tipo_prestamo_id)
        
    #     form.instance.tipo_prestamo = tipo_prestamo
    #     #form.instance.nombre_prestamo_seleccionado = tipo_prestamo.nombre_producto
       
    #     return super().form_valid(form)

# class ObtenerDetallesPrestamoView(View):
#     def get(self, request, *args, **kwargs):
        
        
            
#         tipo_prestamo_id = request.GET.get('tipo_prestamo_id')
#         nombre_prestamo = Prestamo.objects.get(pk=tipo_prestamo_id)

#         # Supongamos que Prestamo tiene campos 'monto' y 'plazo'
#         response_data = {
#             'prestamo_tipo': nombre_prestamo.tipo_prestamo.tipo_credito,
#             'producto_nombre': nombre_prestamo.nombre_producto,
#             'monto': nombre_prestamo.monto,
#             'periodo_tipo': nombre_prestamo.tipo_periodo.periodo_credito,
#             'plazo': nombre_prestamo.plazo,
#             'ordinario_interes': nombre_prestamo.interes_ordinario,
#             'moratorio_interes': nombre_prestamo.interes_moratorio,
#             'pago_mensual': nombre_prestamo.pago_mensual,
#         }

#         return JsonResponse(response_data)
    
    
    
class SimuladorPruebaCreateView(CreateView):
    model = SimuladorPrueba
    form_class = SimuladorPruebaForm
    template_name = 'dashboard/sim_prest.html'

    def form_valid(self, form):
        # Personaliza el manejo de los montos seleccionados aquí
        # Puedes procesar la cadena de montos y guardarlos como sea necesario
        # Por ejemplo, puedes dividir la cadena por comas y convertirla en una lista
        montos_seleccionados = form.cleaned_data['montos_seleccionados'].split(',')
        # Realiza la lógica de almacenamiento según tus necesidades

        return super().form_valid(form)
        
class PruebaSimulaView(CreateView):
    model = PruebaSimula
    form_class = PruebaSimulaForms
    template_name = 'dashboard/simula_prest.html'
    success_url = reverse_lazy('dashboard_app:pruebas_simula') 
    
    
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)

    #     # Obtén los montos que necesitas, por ejemplo, todos los montos de Prestamo
    #     montos_prestamo = Prestamo.objects.values_list('monto', flat=True)

    #     # Añade el formulario al contexto junto con los montos
    #     context['form'] = PruebaSimulaForms(montos_prestamo=montos_prestamo)

    #     return context

    
        
    


'''

@require_GET
def obtener_informacion_prestamo(request):
    monto_seleccionado = request.GET.get('monto')
    prestamo = get_object_or_404(Prestamo, monto=monto_seleccionado)

    data = {
        'monto': prestamo.monto,
        'plazo': prestamo.plazo,
        # Otros campos según sea necesario
    }

    return JsonResponse(data)
'''

    
   
        
    
    
    
        
        
        
                
    
    
    
 

