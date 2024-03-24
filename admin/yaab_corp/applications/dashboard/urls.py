from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name = 'dashboard_app'

urlpatterns = [
    path("",views.DashboardView.as_view(), name="index"),
    #path("crear_simulador/<int:user_id>/", views.DashboardView.as_view(), name="crear_simulador"),
    path('preguntas-respuestas/',views.PreguntasRespuestas.as_view(),name='preguntas_respuestas'),
    path('productos/productos-gral/',views.ProductosView.as_view(),name='productos_gral'),
    
    ##### Grupal ####
    path("dashboard/productos/nuevo-grupal/",views.CreateGrupal.as_view(),name="nuevo_grupal"),
    path('dashboard/productos/editar-grupal/<int:pk>/',views.EditarGrupal.as_view(),name='editar_grupal'),
    ##### Grupal ####
    
    ##### producto #####
    path("dashboard/productos/nuevo-producto/",views.CreateProductosView.as_view(),name="nuevo_productos"),
    path('dashboard/productos/editar-productos/<int:pk>/',views.EditarProducto.as_view(),name='editar_productos'),
    path('dashboard/productos/eliminar-productos/<int:pk>/',views.EliminarProducto.as_view(),name='eliminar_productos'),
    
    ##### producto #####
    ##### plazo #####
    path("dashboard/plazos/nuevo-plazo/", views.CreatePlazoView.as_view(), name="nuevo_plazo"),
    path("dashboard/plazos/editar-plazo/<int:pk>/", views.EditarPlazoView.as_view(), name="editar_plazo"),
    path("dashboard/plazos/eliminar-plazo/<int:pk>", views.EliminarPlazo.as_view(), name="eliminar_plazo"),
    ##### plazo #####
    
    ##### obtener el interes ###
    path('obtener-interes/', views.obtener_interes, name='obtener_interes'),
    path('obtener-mora/', views.obtener_moratorio, name='obtener_mora'),
    path('obtener-plazo/', views.obtener_plazo, name='obtener_plazo'),
    ##### obtener el interes ###
    
    path("editar-usuario/<int:pk>", views.EditarUsuarioUsers.as_view(), name="editar_usuario"),
    path("terminos/", views.AvisoPrivacidad.as_view(), name="terminos_condiciones"),
    path("terminos-condiciones/", views.TerminosCondiciones.as_view(), name="terminos_condiciones_2"),
    
    path('pdf-documento/', views.PdfDocument.as_view(), name='pdf_documento'),
    
    path('generar_pdf/', views.PdfDocumentGrupal.as_view(), name='generar_pdf'),
    
    path('mifiel/', views.crearMifiel, name='mifiel'),
    
    path('info-buro/',views.InfoBuro.as_view(),name='info-buro'),
    path('guardar-firma/<int:user_id>/', views.guardar_firma, name='guardar_firma'),
    
    path('nuevo_prestamo/', views.PrestamoCreateView.as_view(), name='nuevo_prestamo'),
    path('sim_prestamo/', views.SimPrestamoCreateView.as_view(), name='sim_prestamo'),
    path('simulador_pruebas/', views.SimuladorPruebaCreateView.as_view(), name='simulador_pruebas'),
    path('pruebas_simula/', views.PruebaSimulaView.as_view(), name='pruebas_simula'),
    path('dashboard/get_nombre_producto/<int:prestamo_id>/', views.GetNombreProductoView.as_view(), name='get_nombre_producto'),
    #path('dashboard/get_nombre_producto/<int:prestamo_id>/', views.GetNombreProductoView.as_view(), name='get_nombre_producto'),
    #path('index/info-prestamo/', views.obtener_informacion_prestamo, name='info_prestamo'),
    #path('dashboard/obtener_detalles_prestamo/', views.ObtenerDetallesPrestamoView.as_view(), name='obtener_detalles_prestamo'),
    
]  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 
