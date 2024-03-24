from django.db import models
from django.db.models.signals import post_save,pre_save

from django.dispatch import receiver
from django.contrib.auth.models import User 
from django.utils import timezone


#from applications.calificaciones.models import RegistroPagosModel

# Create your models here.

class Productos(models.Model):
    nombre_credito = models.CharField(max_length=100,blank=True,null=True)
    
    def __str__(self):
        return str(self.nombre_credito) 
    
##### pruebas ##### 
class TipoPrestamo(models.Model):
    tipo_credito = models.CharField(max_length=100,blank=True,null=True)
    
    class Meta:
        verbose_name = 'Tipo prestamo'
        verbose_name_plural = 'Tipo prestamo'
       
    def __str__(self):
        return str(self.tipo_credito) 
class Periodo(models.Model):
    periodo_credito = models.CharField(max_length=100,blank=True,null=True)
    
    class Meta:
        verbose_name = 'Periodo'
        verbose_name_plural = 'Periodos'
       

    def __str__(self):
        return str(self.periodo_credito) 


class Prestamo(models.Model):
    tipo_prestamo = models.ForeignKey(TipoPrestamo, on_delete=models.CASCADE,blank=True,null=True)
    nombre_producto = models.CharField(max_length=50,blank=True,null=True)   
    monto = models.IntegerField(blank=True,null=True)
    tipo_periodo = models.ForeignKey(Periodo, on_delete=models.CASCADE,blank=True,null=True)
    plazo = models.IntegerField(blank=True,null=True)  # "mensual" o "semanal"
    interes_ordinario = models.DecimalField(max_digits=5, decimal_places=2,blank=True,null=True)
    interes_moratorio = models.DecimalField(max_digits=5, decimal_places=2,blank=True,null=True)
    pago_mensual = models.DecimalField(max_digits=10, decimal_places=2,blank=True,null=True)
    
    
    
    class Meta:
        verbose_name = 'Credito'
        verbose_name_plural = 'Creditos'
       

    def __str__(self):
        return str(self.monto) + ' - ' + str(self.plazo) + ' - ' + str(self.tipo_periodo)
        #return str(self.monto) + ' - ' + str(self.plazo) + ' - ' + str(self.tipo_periodo)
    
    def calcular_pago_mensual(self):
        print("Calculando pago mensual...")
        if self.tipo_periodo.periodo_credito == 'Mensual':
            resultado = self.monto * (1 + self.interes_ordinario / 100)
        elif self.tipo_periodo.periodo_credito == 'Semanal':
            resultado = self.monto * (1 + self.interes_ordinario / 100) / 4  
        elif self.tipo_periodo.periodo_credito == 'Quincenal':
            resultado = self.monto * (1 + self.interes_ordinario / 100) / 2  
        else:
            resultado = 0  
        print(f"Resultado del cálculo: {resultado}")
        return resultado

    def save(self, *args, **kwargs):
        
        print(f"Monto: {self.monto}")
        print(f"Tipo de período: {self.tipo_periodo}")
        print(f"Interés ordinario: {self.interes_ordinario}")
        
        if not self.pago_mensual:  
            self.pago_mensual = self.calcular_pago_mensual()
        super().save(*args, **kwargs)
        
        print(f"Pago mensual calculado: {self.pago_mensual}")

class PruebaSimula(models.Model):
    montos_simulador = models.ForeignKey(Prestamo, on_delete=models.CASCADE,related_name='montos_simulador',null=True,blank=True)
    
    class Meta:
        verbose_name = 'Montos simulador'
        verbose_name_plural = 'Montos simulador'
       

    def __str__(self):
        return str(self.montos_simulador) 
    

#asignarle el nombre real 
class SimuladorPrueba(models.Model):
    nombre_prestamo = models.ForeignKey(Prestamo, on_delete=models.CASCADE,related_name='tipo_credito',null=True,blank=True)
    usuario_user = models.ForeignKey('users.User', on_delete=models.CASCADE,related_name='usario_user',null=True,blank=True)
    solicitud = models.BooleanField(default=False,blank=True,null=True)
    fecha_registro = models.DateTimeField(default=timezone.now, blank=True, null=True)
    identificador_unico = models.CharField(max_length=20, unique=True, blank=True, null=True)
    
    
    #montos_seleccionados = models.IntegerField(blank=True, null=True)
    #nombre_prestamo_seleccionado = models.CharField(max_length=50, blank=True, null=True)
    
    class Meta:
        verbose_name = 'Simulador prueba'
        verbose_name_plural = 'Simulador pruebas'
       

    def __str__(self):
        #return str(self.nombre_prestamo) + ' - ' + ' Contrato: ' + str(self.identificador_unico)
        return str(self.identificador_unico) + ' ' +   str(self.id)
    
    def save(self, *args, **kwargs):
        # Generar identificador único basado en la fecha y el número en aumento
        if not self.identificador_unico:
            # Convertir la fecha de registro a un formato específico (DDMMYYYY)
            fecha_formato = self.fecha_registro.strftime('%d%m%Y')
            # Obtener el último identificador único en la base de datos
            ultimo_identificador = SimuladorPrueba.objects.latest('id').identificador_unico if SimuladorPrueba.objects.exists() else 0
            if ultimo_identificador:
                # Obtener el número en aumento del último identificador
                ultimo_numero = int(ultimo_identificador[8:])  # Obtener los últimos dos dígitos del identificador
            else:
                ultimo_numero = 0
            # Incrementar el número en aumento
            nuevo_numero = (ultimo_numero + 1) % 100  # Limitar a dos dígitos (0-99)
            # Combinar la fecha y el número en aumento para formar el identificador único
            self.identificador_unico = f"{fecha_formato}{nuevo_numero:02d}"
        
        super().save(*args, **kwargs)
        
        



# @receiver(post_save, sender=SimuladorPrueba)
# def post_save_simulador_prueba(sender, instance, **kwargs):
#     # Verificar si el nombre del préstamo está vacío y asignarle el ID si es así
#     if not instance.nombre_prestamo:
#         instance.nombre_prestamo = instance.id
#         instance.save()

# @receiver(post_save, sender=SimuladorPrueba)
# def asignar_montos(sender, instance, **kwargs):
#     if not instance.montos_seleccionados:
#         # Accede a la relación ForeignKey para obtener el monto de Prestamo
#         monto_prestamo = instance.nombre_prestamo.monto
#         # Asigna el monto a montos_seleccionados
#         instance.montos_seleccionados = monto_prestamo
#         # Guarda el objeto SimuladorPrueba con el nuevo valor
#         instance.save()
        

    
    
    
    
    # @property
    # def monto_prestamo(self):
    #     return self.nombre_prestamo.monto if self.nombre_prestamo else None
    
##### pruebas ##### 

class Plazo(models.Model):  
    #nombre_credito = models.CharField(max_length=50,blank=True, null=True)  
    plazo_tiempo = models.CharField(max_length=100,blank=True,null=True) 
    interes_credito = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    interes_moratorio = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    

    class Meta:
        verbose_name = 'Plazo'
        verbose_name_plural = 'Plazos'
       

    def __str__(self):
        return str(self.plazo_tiempo) 



class Simulador(models.Model):
    tipo_credito = models.ForeignKey(Productos, on_delete=models.CASCADE,related_name='tipo_credito',null=True,blank=True)
    #tipo_credito = models.ForeignKey(Plazo, on_delete=models.CASCADE,related_name='tipo_credito',null=True,blank=True)
    plazo_nombre = models.ForeignKey(Plazo,on_delete=models.CASCADE,related_name='nombre_plazo',null=True,blank=True)
    term = models.IntegerField(null=True,blank=True)
    amount = models.IntegerField(null=True,blank=True) 
    interest_rate = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    interest_moratorio = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    monthly_payment = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    
    class Meta:
        verbose_name = 'Simulador'
        verbose_name_plural = 'Simuladores'
    
    def __str__(self):
        return str(self.id)
    
    
class ImageYaab(models.Model):
    
    top_image = models.ImageField( upload_to='solicitud/',blank=True,null=True)
    
    class Meta:
        verbose_name = 'imagen_yaab'

class NumberPerson(models.Model):
    numero_personas = models.CharField(max_length=100,blank=True,null=True)  

class MontoGrupal(models.Model):
    monto_grupal = models.CharField(max_length=100,blank=True,null=True)           
        
class ProductoCreditoGrupal(models.Model):
    nombre_grupal = models.CharField(max_length=100,blank=True,null=True)
    numero_participante = models.IntegerField(null=True,blank=True)  
    monto_credito= models.IntegerField(null=True,blank=True)
    
    
    class Meta:
        verbose_name = 'Credito Grupal'
        verbose_name_plural = 'Creditos Grupales'
    
    def __str__(self):
        return   str(self.numero_participante) + ' - ' + str(self.nombre_grupal)
    
    
    
    
