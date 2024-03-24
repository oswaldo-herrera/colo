from django.contrib import admin
from .models import Productos,Plazo,Simulador,ImageYaab,ProductoCreditoGrupal,Prestamo,TipoPrestamo,SimuladorPrueba,Periodo,PruebaSimula

# Register your models here.
admin.site.register(Productos)
admin.site.register(Plazo)
admin.site.register(Simulador)
admin.site.register(ImageYaab)
admin.site.register(ProductoCreditoGrupal)
admin.site.register(TipoPrestamo)
admin.site.register(Prestamo)
admin.site.register(SimuladorPrueba)
admin.site.register(Periodo)
admin.site.register(PruebaSimula)