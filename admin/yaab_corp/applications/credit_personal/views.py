from typing import Any
from django.shortcuts import render
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.db.models import Count
from django.shortcuts import get_object_or_404
from django.views import View
from django.views.generic import TemplateView,ListView
from mifiel import Document, Client
from .models import Solicitud
from applications.users.models import User,GrupoCreditoPersonal
from applications.dashboard.models import ImageYaab
from applications.users.mixins import ValidarPermisosMixin
from .utils import render_to_pdf

# Create your views here.


class BandejaSolicitud(ListView):
    
    template_name = 'credit_personal/bandeja-solicitud.html'
    context_object_name = 'usuarios'
    
    def get_queryset(self):
        
         # Obtener la lista de usuarios 
        usuarios_con_aviso = User.objects.filter(solicitud=True)
        
        
        # Agregar el conteo de solicitudes pendientes para cada usuario
        usuarios_con_aviso = usuarios_con_aviso.annotate(num_solicitudes_pendientes=Count('email'))
        
        return usuarios_con_aviso
    
    def get_context_data(self, **kwargs):
        context = super(BandejaSolicitud,self).get_context_data(**kwargs)
        usuarios_grupo_credito = GrupoCreditoPersonal.objects.filter(buro_credito_grupal=True)
        
        context['usuarios_grupales'] = usuarios_grupo_credito.annotate(num_solicitudes_pendientes_grupal=Count('email'))
        
        return context
        
    
    def render_to_response(self, context, **response_kwargs):
        data = {
            'usuarios': list(context['usuarios'].values()),  # Convertir los usuarios a lista de diccionarios
            'usuarios_grupales': list(context['usuarios_grupales'].values()),
        }
        
        return JsonResponse(data)

class BandejaSolicitudHtml(ListView):
    
    template_name = 'credit_personal/bandeja-solicitud.html'
    context_object_name = 'usuarios'
    
    def get_queryset(self):
        
        lista_usuarios = User.objects.filter(solicitud=True)
        
        lista_usuarios = lista_usuarios.exclude(confirmado=True)
        lista_usuarios = lista_usuarios.exclude(rechazado=True)
    
        return lista_usuarios
    
    def get_context_data(self, **kwargs):
        context = super(BandejaSolicitudHtml,self).get_context_data(**kwargs)
        grupos_creditos = GrupoCreditoPersonal.objects.filter(buro_credito_grupal=True).order_by('id')
        
        print([item.id for item in grupos_creditos])
        for item in grupos_creditos:
            if item.correos_credito:
                correos = item.correos_credito.correos_participantes.split(',')
                item.correos_lista = correos
            else:
                item.correos_lista = []
        
        context['grupos_creditos'] = grupos_creditos
        return context
    
    
    
    

class MarcarUsuarioConfirmado(View):
    def post(self, request, user_id):
        try:
            user = User.objects.get(pk=user_id)
            user.confirmado = True 
            user.solicitud = False 
            user.save()
            return JsonResponse({'message': 'Usuario marcado como confirmado correctamente'})
        except User.DoesNotExist:
            return JsonResponse({'message': 'Usuario no encontrado'}, status=404)

class MarcarUsuarioRechazado(View):
    def post(self, request, user_id):
        try:
            user = User.objects.get(pk=user_id)
            user.rechazado = True  
            user.solicitud = False 
            user.save()
            return JsonResponse({'message': 'Usuario marcado como confirmado correctamente'})
        except User.DoesNotExist:
            return JsonResponse({'message': 'Usuario no encontrado'}, status=404)
    
    
class BandejaConfirmados(ListView):
    template_name = 'credit_personal/confirmados.html'
    context_object_name = 'confirmados'
    
    def get_queryset(self):
        lista_usuarios = User.objects.filter(confirmado=True)
    
        return lista_usuarios
    
    def get_context_data(self, **kwargs):
        context = super(BandejaConfirmados,self).get_context_data(**kwargs)
        context["rechazados"] = User.objects.filter(rechazado=True)
        return context
    
    
    


##### seccion pdf ###### 
class PdfDocumentId(View):
        
    def get(self, request,user_id, *args, **kwargs):
        user = get_object_or_404(User, id=user_id)
        imagen_yaab = ImageYaab.objects.all()
        empleados = User.objects.filter(id=user.id)
       
        data = {
            'count': empleados.count(),
            'empleados': empleados,
            'imagen_yaab_url': imagen_yaab,
            'nombre':user,
         
        }
        output_path = 'static/media/solicitud.pdf'
        pdf = render_to_pdf('dashboard/pdf.html', data,output_path)
        if pdf:
            print("PDF guardado correctamente")
        else:
            print("PDF guardado correctamente")
        
        return HttpResponse("PDF generado y guardado")
    
##### seccion pdf ###### 
    

##### seccion mifiel ###### 
def crearMifiel(request,user_id):
    
    client = Client(app_id=settings.MIFIEL_API_TOKEN, secret_key=settings.MIFIEL_API_TOKEN_SECRET)
    user = get_object_or_404(User, id=user_id)
    
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
    
    
    return HttpResponse("Documento creado")
##### seccion mifiel ###### 
    
