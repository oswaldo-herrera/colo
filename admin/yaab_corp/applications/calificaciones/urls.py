from django.urls import path
from . import views

app_name = 'calificaciones_app'

urlpatterns = [
    path("control-calificaciones/",views.ControlCalificaciones.as_view(),name="control_calificaciones"),
    path("registro-credito/",views.ViewRegistroCreditos.as_view(),name="registro_credito"),
    path("estatus-credito/",views.ViewCreditosStatus.as_view(),name="estatus_credito"),
    path("corrida-credito/",views.CorridaFinancieraListView.as_view(),name="corrida_credito"),
    path("estatus-credito-estatico/",views.ViewCreditosStatusEstatico.as_view(),name="estatus_credito_estatico"),
    path("registro-pagos/",views.RegistroPagos.as_view(),name="registro_pagos"),
    path('obtener_monto_total/', views.obtener_monto_total, name='obtener_monto_total'),
    #path('get_estatus_credito_data/<int:num_contrato>/', views.GetEstatusCreditoDataView.as_view(), name='get_estatus_credito_data'),
    #path("estatus-credito/",views.view_creditos_status,name="estatus_credito"),
]
