from django.contrib import admin
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from .models import User,Ubicacion,CorreosCreditoGrupal,GrupoCreditoPersonal,EstadoCivilValues

# Register your models here.

admin.site.register(User)
admin.site.register(Ubicacion)
admin.site.register(CorreosCreditoGrupal)
admin.site.register(GrupoCreditoPersonal)
admin.site.register(Permission)
admin.site.register(ContentType)
admin.site.register(EstadoCivilValues)