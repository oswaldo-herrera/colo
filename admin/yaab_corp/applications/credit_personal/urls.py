from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name = 'credit_personal_app'

urlpatterns = [
    path("solicitud/",views.BandejaSolicitud.as_view(), name="solicitud"),
    path('bandeja-solicitud-html/', views.BandejaSolicitudHtml.as_view(), name='bandeja_solicitud_html'),
    path('pdf-documento/<int:user_id>/', views.PdfDocumentId.as_view(), name='pdf-documento'),
    path('mifiel/<int:user_id>/', views.crearMifiel, name='mifiel'),
    path('confirmados/', views.BandejaConfirmados.as_view(), name='confirmados'),
    path('marcar-usuario-confirmado/<int:user_id>/', views.MarcarUsuarioConfirmado.as_view(), name='marcar_usuario_confirmado'),
    path('rechazado/<int:user_id>/', views.MarcarUsuarioRechazado.as_view(), name='rechazado'),
    
    
]
