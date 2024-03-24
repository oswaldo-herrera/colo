from django.db import models
from applications.users.models import User
from applications.dashboard.models import Productos,Plazo,Simulador

# Create your models here.
class Solicitud(models.Model):
    users_solicitud = models.ForeignKey(User,on_delete=models.CASCADE,related_name='solicitud_users',null=True,blank=True)
    
    class Meta:
        verbose_name = 'Bandeja_Solicitud'
        verbose_name_plural = 'Bandeja_Solicitudes'
        
    def __str__(self):
        return str(self.users_solicitud)