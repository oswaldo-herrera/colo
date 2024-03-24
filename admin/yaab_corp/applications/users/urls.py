from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

app_name = 'user_app'


urlpatterns = [
    path('registro/', views.RegistrarUsuario.as_view(), name='registro'),
    path('lista-usuarios/',views.ListaUsuarios.as_view(),name='lista_usuarios'),
    path('eliminar-usuarios/<int:pk>/',views.EliminarUsuarios.as_view(),name='eliminar_usuarios'),
    path('editar-usuarios/<int:pk>/',views.EditarUsuario.as_view(),name='editar_usuarios'),
    path('ubicacion/',views.guardar_ubicacion,name='ubicacion'),
    path('solicitud/<int:user_id>/', views.SolicitudCheck.as_view(), name='solicitud'),
    path('clientes/', views.ClientesAll.as_view(), name='clientes'),
    path('grupal/', views.GrupalCredito.as_view(), name='grupal'),
    path('correo-grupo-credito/', views.correo_grupo_credito, name='correo_grupo_credito'),
    
    path('obtener-monto/', views.obtener_monto, name='obtener_monto'),
    path('formulario-credito/', views.FormularioCreditoGrupal.as_view(), name='formulario_credito'),
    
    path('buro-credito/', views.ModalBruroCredito.as_view(), name='buro_credito'),
    path('aviso-privacidad-grupal/', views.AvisoPrivacidadGrupal.as_view(), name='aviso_privacidad_grupal'),
    
    #path('crear_simulador/<int:user_id>/', views.tu_vista_crear_simulador, name='crear_simulador'),
    
    
]  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 
