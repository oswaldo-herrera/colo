from django.db import models
from django.db.models.signals import post_save,pre_save
from django.dispatch import receiver
from django.utils import timezone
from applications.dashboard.models import Simulador,SimuladorPrueba
from applications.users.models import User

# Create your models here.


class RegistroCreditos(models.Model):
    cliente = models.ForeignKey(User,on_delete=models.CASCADE,related_name="cliente",blank=True,null=True)
    numero_contrato = models.CharField(max_length=12, unique=True, blank=True, null=True)  # Agregado este campo
    # monto_credito = models.ForeignKey(Simulador,on_delete=models.CASCADE,related_name="monto_credito",blank=True,null=True)
    # pago = models.ForeignKey(Simulador,on_delete=models.CASCADE,related_name="pago",blank=True,null=True)
    
    
    class Meta:
        verbose_name = "Credito"
        verbose_name_plural = "Creditos"
        
    def __str__(self):
        return str(self.numero_contrato)
    
    
# @receiver(post_save,sender=User)
# def crear_registros_creditos(sender,instance,created,**kwargs):
#     if instance.solicitud:
#         RegistroCreditos.objects.get_or_create(cliente=instance)
#     else:
#         RegistroCreditos.objects.filter(cliente=instance).delete()
        
#### este es el que tenemos que descativar ####  
# @receiver(pre_save,sender=RegistroCreditos)
# def generar_numero_contrato(sender, instance,**kwargs):
#     if not instance.numero_contrato:
#         fecha_solicitud = instance.cliente.fecha_solicitud.strftime('%d%m%y')
#         counter = RegistroCreditos.objects.filter(cliente=instance.cliente).count()+1
#         instance.numero_contrato = f"{fecha_solicitud}{counter:03d}"
        
        
class  EstatusCredito(models.Model):
    
    #cliente_estatus = models.ForeignKey(User,on_delete=models.CASCADE,related_name="cliente_estatus",blank=True,null=True)
    cliente_estatus = models.ForeignKey(SimuladorPrueba,on_delete=models.CASCADE,related_name="cliente_estatus",blank=True,null=True)
    numero_contrato_estatus = models.ForeignKey(RegistroCreditos,on_delete=models.CASCADE,related_name="contrato",blank=True,null=True)
    monto_total = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    desembolso = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    tipo = models.CharField(max_length=12, unique=True, blank=True, null=True)
    monto_pago_men = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    numero_de_pago = models.IntegerField(blank=True, null=True)
    monto_pagado = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    saldo = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    dias_morosidad = models.IntegerField(blank=True, null=True)
    monto_morosidad = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    saldo_mas_morosidad = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    estatus = models.CharField(max_length=12, unique=True, blank=True, null=True)
    
    
    
    
    
    class Meta:
        verbose_name = "Estatus"
        verbose_name_plural = "Estatus"
        
    def __str__(self):
        return str(self.numero_contrato_estatus)
    
@receiver(post_save, sender=RegistroCreditos)
def actualizar_numero_contrato_estatus(sender, instance, created, **kwargs):
    if created:
        # El objeto RegistroCreditos acaba de ser creado
        estatus_credito, created = EstatusCredito.objects.get_or_create(cliente_estatus=instance.cliente)
        estatus_credito.numero_contrato_estatus = instance
        
        estatus_credito.save()

# @receiver(post_save,sender=User)
# def crear_usuario_estatus(sender,instance,created,**kwargs):
#     if instance.solicitud:
#         EstatusCredito.objects.get_or_create(cliente_estatus=instance)
#     else:
#         EstatusCredito.objects.filter(cliente_estatus=instance).delete()


class RegistroPagosModel(models.Model):
    
    simulador = models.ForeignKey(SimuladorPrueba,on_delete = models.CASCADE,related_name='simulador_unico',blank=True,null=True)
    monto_pagado  = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    comprobante_pago  = models.FileField(upload_to='media/',blank=True,null=True)
    fecha_pago = models.DateTimeField(auto_now_add=True,blank=True,null=True)
    numero_pago = models.IntegerField(blank=True,null=True)
    #monto_restante = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    
    # def save(self, *args, **kwargs):
    #     # Calcula automáticamente el monto restante antes de guardar el objeto
    #     if self.numero_pago > 1:
    #         pagos_anteriores = RegistroPagosModel.objects.filter(simulador=self.simulador, numero_pago__lt=self.numero_pago)
    #         total_pagado_anteriormente = sum(p.monto_pagado for p in pagos_anteriores)
    #         self.monto_restante = self.simulador.nombre_prestamo.pago_mensual * self.numero_pago - total_pagado_anteriormente
    #     else:
    #         self.monto_restante = self.simulador.nombre_prestamo.pago_mensual

    #     super().save(*args, **kwargs)
    #usuario = models.CharField(max_length=50,blank=True,null=True)
    #archivo_pago = models.FileField(upload_to='archivos_pagos/', blank=True, null=True)

    #estatus_num_contrato = models.ForeignKey(RegistroCreditos,on_delete = models.CASCADE,related_name='estatus_num_contrato',blank=True,null=True)
    #valor_registro_credito = models.ForeignKey(RegistroCreditos,on_delete = models.CASCADE,related_name='num_contrato',blank=True,null=True)
    #num_contrato = models.CharField(max_length=50,blank=True,null=True)
    
    
    class Meta:
        verbose_name = 'Registro pago'
        verbose_name_plural = 'Registros pagos'
        
    
    
    def __str__(self):
        return  str(self.simulador)
    
    
# @receiver(pre_save, sender=RegistroPagosModel)
# def actualizar_monto_total(sender, instance, **kwargs):
#     # Verifica si el objeto tiene un valor en la clave externa num_contrato
#     if instance.num_contrato:
#         # Obtén el objeto EstatusCredito relacionado
#         estatus_credito = instance.num_contrato
#         # Actualiza el campo monto_total con el valor correspondiente de EstatusCredito
#         instance.monto_total = estatus_credito.monto_total
    
# @receiver(pre_save, sender=RegistroPagosModel)
# def auto_fill_registro_pagos_fields(sender, instance, **kwargs):
#     if instance.num_contrato:
#         instance.usuario = instance.num_contrato.cliente_estatus.username  # Puedes cambiar a lo que necesites
#         instance.monto_total = instance.num_contrato.monto_total
    
# @receiver(post_save, sender=RegistroCreditos)
# def actualizar_registro_pagos(sender, instance, created, **kwargs):
#     if created:
#         # El objeto RegistroCreditos acaba de ser creado
#         registro_pagos, _ = RegistroPagosModel.objects.get_or_create(num_contrato=instance)
        
#         registro_pagos.num_contrato = instance

#         # Puedes realizar otras actualizaciones o configuraciones según tus necesidades

#         registro_pagos.save()
        
        



        

        
    
