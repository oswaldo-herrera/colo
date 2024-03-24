from django.contrib import admin
from .models import RegistroCreditos,EstatusCredito,RegistroPagosModel

# Register your models here.



admin.site.register(RegistroCreditos)
admin.site.register(EstatusCredito)
admin.site.register(RegistroPagosModel)

