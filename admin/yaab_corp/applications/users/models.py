from django.db.models.signals import post_save,pre_save
from django.dispatch import receiver

from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser
from applications.dashboard.models import ProductoCreditoGrupal,Simulador,SimuladorPrueba
from django.utils import timezone
from datetime import timedelta,datetime
import numpy as np

class User(AbstractUser):
    
    # *************datos personales ***********
    email = models.EmailField(_('enmail adrees'),unique=True)
    username = models.CharField(max_length=150, unique=False, blank=True, null=True)
    edad=models.IntegerField(null=True,blank=True)
    first_name = models.CharField(max_length=30)
    imagen_perfil = models.ImageField(upload_to='perfil/',blank=True,null=True)
    last_name = models.CharField(max_length=30)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    second_name = models.CharField(max_length=30,blank=True,null=True)
    fecha_nac = models.DateField(null=True,blank=True)
    curp_texto = models.CharField(max_length=30,blank=True,null=True)
    curp = models.FileField(upload_to='users/',blank=True,null=True)
    rfc = models.CharField(max_length=30,blank=True,null=True)
    estado_civil = models.CharField(max_length=30,blank=True,null=True)
    genero = models.CharField(max_length=100,blank=True,null=True)
    nacionalidad = models.CharField(max_length=100,blank=True,null=True)
    pais = models.CharField(max_length=100,blank=True,null=True)
    estado = models.CharField(max_length=100,blank=True,null=True)
    empleo = models.CharField(max_length=100,blank=True,null=True)
    numero_dependientes = models.CharField(max_length=100,blank=True,null=True)
    telefono_particular = models.CharField(max_length=100,blank=True,null=True)
    documento_ine = models.FileField(upload_to='users/',blank=True,null=True)
    firma_digital_personal = models.TextField(max_length=500,blank=True, null=True)
    firma_imagen_personal = models.ImageField(upload_to='media/', blank=True, null=True)
     # *************datos personales ***********
     
      # *************direccion ***********
    calle_numero = models.CharField(max_length=100,blank=True,null=True)
    colonia = models.CharField(max_length=100,blank=True,null=True)
    cp = models.CharField(max_length=100,blank=True,null=True)
    ciudad = models.CharField(max_length=100,blank=True,null=True)
    estado_direccion = models.CharField(max_length=100,blank=True,null=True)
    tipo_vivienda = models.CharField(max_length=100,blank=True,null=True)
    años_radicando = models.CharField(max_length=100,blank=True,null=True)
    comprobante_domicilio = models.FileField(upload_to='users/',blank=True,null=True)
    # *************direccion ***********
    
     # *************referencias ***********      
    conyuge_pareja = models.CharField(max_length=100,blank=True,null=True)
    trabajo_conyuge = models.CharField(max_length=100,blank=True,null=True)
    antiguedad_laboral_conyuge = models.CharField(max_length=100,blank=True,null=True)
    telefono_conyuge = models.CharField(max_length=100,blank=True,null=True)
    referencia_personal_conyuge_1 = models.CharField(max_length=100,blank=True,null=True)
    telefono_ref_conyuge_1 = models.CharField(max_length=100,blank=True,null=True)
    referencia_personal_conyuge_2 = models.CharField(max_length=100,blank=True,null=True)
    telefono_ref_conyuge_2 = models.CharField(max_length=100,blank=True,null=True)
    # *************referencias ***********   
       
    # *************datos del comercio *********** 
    nombre_negocio = models.CharField(max_length=100,blank=True,null=True)
    giro = models.CharField(max_length=100,blank=True,null=True)
    inmueble = models.CharField(max_length=100,blank=True,null=True)
    años_antiguedad = models.CharField(max_length=100,blank=True,null=True)
    calle_numero_negocio = models.CharField(max_length=100,blank=True,null=True)
    colonia_negocio = models.CharField(max_length=100,blank=True,null=True)
    cp_negocio = models.CharField(max_length=100,blank=True,null=True)
    ciudad_negocio = models.CharField(max_length=100,blank=True,null=True)
    estado_negocio = models.CharField(max_length=100,blank=True,null=True)
    # *************datos del comercio *********** 
    
    # ************* datos aval *********** 
    
    nombre_aval = models.CharField(max_length=100,blank=True,null=True)
    primer_apellido = models.CharField(max_length=100,blank=True,null=True)
    segundo_apellido = models.CharField(max_length=100,blank=True,null=True)
    fecha_nac_aval = models.DateField(null=True,blank=True)
    curp_aval = models.FileField(upload_to='users/',blank=True,null=True)
    # curp_aval = models.CharField(max_length=100,blank=True,null=True) 
    genero_aval = models.CharField(max_length=100,blank=True,null=True)
    ciudad_aval = models.CharField(max_length=100,blank=True,null=True)
    estado_aval = models.CharField(max_length=100,blank=True,null=True)
    rfc_aval = models.CharField(max_length=100,blank=True,null=True)
    calle_numero_aval = models.CharField(max_length=100,blank=True,null=True)
    colonia_aval = models.CharField(max_length=100,blank=True,null=True)
    cp_aval = models.CharField(max_length=100,blank=True,null=True)
    relacion_titular = models.CharField(max_length=100,blank=True,null=True)
    tipo_vivienda_aval = models.CharField(max_length=100,blank=True,null=True)
    años_radicando_aval = models.CharField(max_length=100,blank=True,null=True)
    lugar_trabajo_aval = models.CharField(max_length=100,blank=True,null=True)
    antiguedad_trabajo_aval = models.CharField(max_length=100,blank=True,null=True)
    celular_aval = models.CharField(max_length=100,blank=True,null=True)
    email_aval = models.CharField(max_length=100,blank=True,null=True)
    telefono_laboral_aval = models.CharField(max_length=100,blank=True,null=True)
    documento_ine_aval = models.FileField(upload_to='users/',blank=True,null=True)
    comprobante_domicilio_aval = models.FileField(upload_to='users/',blank=True,null=True)
    
    # ************* datos aval *********** 
    
    aviso_privacidad = models.BooleanField(default=False,blank=True,null=True)
    solicitud = models.BooleanField(default=False,blank=True,null=True)
    confirmado = models.BooleanField(default=False,blank=True,null=True)
    rechazado = models.BooleanField(default=False,blank=True,null=True)
    buro_credito = models.BooleanField(default=False,blank=True,null=True)
    simulador = models.ForeignKey(Simulador,on_delete=models.CASCADE,related_name='simulador',blank=True,null=True)
    fecha_solicitud = models.DateTimeField(null=True, blank=True)
    fecha_proximo_viernes = models.DateTimeField(null=True, blank=True)
    
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    def __str__(self):
        return self.email
    


    
class Ubicacion(models.Model):
    latitud = models.CharField(max_length=100,blank=True,null=True)
    longitud = models.CharField(max_length=100,blank=True,null=True)
    
    def __str__(self):
        return self.latitud + ' ' + str(self.id)
    
    
class CorreosCreditoGrupal(models.Model):
    participantes_numero = models.ForeignKey(ProductoCreditoGrupal, on_delete=models.CASCADE, related_name='numero_participantes',null=True,blank=True)
    monto_vacantes = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    correo_coordinador = models.CharField(max_length=30,blank=True,null=True)
    correos_participantes = models.TextField()
    names_grupal = models.CharField(max_length=30,blank=True,null=True)
    surnames_grupal = models.CharField(max_length=30,blank=True,null=True)
    curp_texto_grupal = models.CharField(max_length=30,blank=True,null=True)
    rfc_grupal = models.CharField(max_length=30,blank=True,null=True)
    celular_coordinador = models.CharField(max_length=100,blank=True,null=True)
    
    def __str__(self):
        return str(self.names_grupal) + ' ' + str(self.surnames_grupal)
        
    
    def guardar_correos(self, lista_correos,nombres,apellidos,curp,rfc,celular,participantes_id,monto,correo_personal):
        self.correos_participantes = ",".join(lista_correos)
        self.names_grupal = nombres
        self.surnames_grupal = apellidos
        self.curp_texto_grupal = curp
        self.rfc_grupal = rfc
        self.celular_coordinador = celular
        self.participantes_numero = participantes_id
        self.monto_vacantes = monto  
        self.correo_coordinador = correo_personal   
        self.save()
        
        
    
class GrupoCreditoPersonal(models.Model):
    
    email = models.EmailField(unique=False,blank=True,null=True)
    first_name = models.CharField(max_length=30,blank=True,null=True)
    last_name = models.CharField(max_length=30,blank=True,null=True)
    second_name = models.CharField(max_length=30,blank=True,null=True)
    fecha_nac_grupal = models.DateField(null=True,blank=True)
    curp_texto = models.CharField(max_length=30,blank=True,null=True)
    curp = models.FileField(upload_to='users/',blank=True,null=True)
    rfc = models.CharField(max_length=30,blank=True,null=True)
    estado_civil = models.CharField(max_length=30,blank=True,null=True)
    genero = models.CharField(max_length=100,blank=True,null=True)
    nacionalidad = models.CharField(max_length=100,blank=True,null=True)
    pais = models.CharField(max_length=100,blank=True,null=True)
    estado = models.CharField(max_length=100,blank=True,null=True)
    celular = models.CharField(max_length=100,blank=True,null=True)
    numero_dependientes = models.CharField(max_length=100,blank=True,null=True)
    telefono_particular = models.CharField(max_length=100,blank=True,null=True)
    documento_ine_grupal = models.FileField(upload_to='users/',blank=True,null=True)
    
    calle_numero = models.CharField(max_length=100,blank=True,null=True)
    colonia = models.CharField(max_length=100,blank=True,null=True)
    cp = models.CharField(max_length=100,blank=True,null=True)
    ciudad = models.CharField(max_length=100,blank=True,null=True)
    estado_direccion = models.CharField(max_length=100,blank=True,null=True)
    tipo_vivienda = models.CharField(max_length=100,blank=True,null=True)
    años_radicando = models.CharField(max_length=100,blank=True,null=True)
    comprobante_domicilio = models.FileField(upload_to='users/',blank=True,null=True)
    token = models.CharField(max_length=100, unique=True, blank=True, null=True)
    firma_digital = models.TextField(max_length=500,blank=True, null=True)
    firma_imagen = models.ImageField(upload_to='media/', blank=True, null=True)
    aviso_privacidad_grupal = models.BooleanField(default=False,blank=True,null=True)
    buro_credito_grupal = models.BooleanField(default=False,blank=True,null=True)
    correos_credito = models.ForeignKey(CorreosCreditoGrupal,on_delete=models.CASCADE,related_name='correos_credito',null=True,blank=True)
    productocreditogrupal = models.ForeignKey(ProductoCreditoGrupal, on_delete=models.CASCADE,related_name='productocredito',null=True,blank=True)
    
    
    def __str__(self):
        return str(self.email) 
    
    
#OneToOneField
class EstadoCivilValues(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True,blank=True)
    valor_numerico_estado_civil = models.IntegerField(null=True,blank=True)
    valor_numerico_edad = models.IntegerField(null=True,blank=True)
    valor_numerico_empleo = models.IntegerField(null=True,blank=True)
    valor_numerico_total = models.IntegerField(null=True,blank=True)
    
    

    def __str__(self):
        return str(self.user) 
    
def calcular_y_actualizar_valor_total(instance):
    # Verificar que los valores no sean None antes de la suma
    valor_estado_civil = instance.valor_numerico_estado_civil if instance.valor_numerico_estado_civil is not None else 0
    valor_edad = instance.valor_numerico_edad if instance.valor_numerico_edad is not None else 0
    valor_empleo = instance.valor_numerico_empleo if instance.valor_numerico_empleo is not None else 0

    suma_total = valor_estado_civil + valor_edad + valor_empleo
    instance.valor_numerico_total = suma_total
    instance.save()

# def calcular_y_actualizar_valor_total(instance):
#     if instance.valor_numerico_estado_civil is not None and instance.valor_numerico_edad is not None and instance.valor_numerico_empleo is not None:
#         suma_total = instance.valor_numerico_estado_civil + instance.valor_numerico_edad + instance.valor_numerico_empleo
#         instance.valor_numerico_total = suma_total
#         instance.save()
    

# def calcular_y_actualizar_valor_total(instance):
#     suma_total = instance.valor_numerico_estado_civil + instance.valor_numerico_edad + instance.valor_numerico_empleo
    
#     instance.valor_numerico_total =  suma_total
    
#     instance.save()
    

@receiver(post_save, sender=User)   
def create_estado_civil_values(sender, instance, created, **kwargs):
    if created:
        EstadoCivilValues.objects.create(user=instance)
    else:
        estado_civil_values, created = EstadoCivilValues.objects.get_or_create(user=instance)

        estado_civil = instance.estado_civil
        edad = instance.edad
        empleo = instance.empleo

        if estado_civil == 'Soltero':
            estado_civil_values.valor_numerico_estado_civil = 10
        elif estado_civil == 'Casado':
            estado_civil_values.valor_numerico_estado_civil = 8
        
        if edad == 20:
            estado_civil_values.valor_numerico_edad = 10
        elif edad == 50:
            estado_civil_values.valor_numerico_edad = 8

        if empleo == 'Base':
            estado_civil_values.valor_numerico_empleo = 10
        elif empleo == 'Contrato':
            estado_civil_values.valor_numerico_empleo = 8
        
        # Verificar si estamos en el contexto de inicio de sesión antes de calcular y actualizar
        if not kwargs.get('raw', False):  
            calcular_y_actualizar_valor_total(estado_civil_values)

# Conectar la señal
post_save.connect(create_estado_civil_values, sender=User)

@receiver(post_save, sender=User)
def update_fecha_solicitud(sender, instance, **kwargs):
    if instance.solicitud and not instance.fecha_solicitud:
        instance.fecha_solicitud = calcular_fecha_tres_dias_habiles()
        instance.save()
###### este      
@receiver(post_save, sender=User)        
def update_fecha_vieres(sender, instance, **kwargs):
    if instance.solicitud and not instance.fecha_proximo_viernes:
        instance.fecha_proximo_viernes = calcular_proximo_viernes()
        instance.save()
        
        
# def update_fechas(sender,instance,**kwargs):
#     if instance.solicitud:
#         if not instance.fecha_solicitud:
#             instance.fecha_solicitud = calcular_fecha_tres_dias_habiles()
#             with post_save.receivers_for(sender=User).disconnect():
#                 instance.save()
#         if not instance.fecha_proximo_viernes:
#             instance.fecha_proximo_viernes = calcular_proximo_viernes()
#             with post_save.receivers_for(sender=User).disconnect():
#                 instance.save()


        
post_save.connect(update_fecha_solicitud, sender=User)
        
def calcular_fecha_tres_dias_habiles():
    today = timezone.now()
    dias_habiles = 0
    
    while dias_habiles < 3:
        today += timezone.timedelta(days=1)
        if today.weekday() < 5:
            dias_habiles += 1
    
    return today

def calcular_proximo_viernes():
    today = datetime.now()
    dias_hasta_proximo_viernes = (4 - today.weekday() + 7) % 7
    proximo_viernes = today + timedelta(days=dias_hasta_proximo_viernes)
    
    proximo_viernes += timedelta(days=7)
    #proximo_viernes += timedelta(days=7)
    
    return proximo_viernes.date()

   
# @receiver(post_save, sender=User)   
# def create_estado_civil_values(sender, instance, created, **kwargs):
#     if created:
#         # Si es un nuevo usuario, crea un nuevo registro en EstadoCivilValues
#         EstadoCivilValues.objects.create(user=instance)
#     else:
#         # Si es una actualización, verifica si ya existe un registro en EstadoCivilValues
#         estado_civil_values, created = EstadoCivilValues.objects.get_or_create(user=instance)

#         # Actualiza los valores según el estado civil y la edad
#         estado_civil = instance.estado_civil
#         edad = instance.edad
#         empleo = instance.empleo

#         if estado_civil == 'Soltero':
#             estado_civil_values.valor_numerico_estado_civil = 10
#         elif estado_civil == 'Casado':
#             estado_civil_values.valor_numerico_estado_civil = 8
        
    
#         if edad == 20:
#             estado_civil_values.valor_numerico_edad = 10
#         elif edad == 50:
#             estado_civil_values.valor_numerico_edad = 8

#         if empleo == 'Base':
#             estado_civil_values.valor_numerico_empleo = 10
#         elif empleo == 'Contrato':
#             estado_civil_values.valor_numerico_empleo = 8
            
        
#         # Guarda los cambios en el EstadoCivilValues 
#         calcular_y_actualizar_valor_total(estado_civil_values)

# # Conectar la señal
# post_save.connect(create_estado_civil_values, sender=User)
    
    
    
    
    
    
# @receiver(post_save, sender=User)  
# def create_estado_civil_values(sender, instance, created, **kwargs):
#     """
#     Este receptor se ejecutará cada vez que se guarde un nuevo usuario.
#     Crea automáticamente un EstadoCivilValues asociado al nuevo usuario.
#     """
#     if created:
#         EstadoCivilValues.objects.create(user=instance)
        

# @receiver(post_save, sender=User)
# def create_estado_civil_values(sender, instance, created, **kwargs):
#     if created:
#         # Si es un nuevo usuario, crea un nuevo registro en EstadoCivilValues
#         EstadoCivilValues.objects.create(user=instance)
#     else:
#         # Si es una actualización, actualiza los valores según el estado civil y la edad
#         estado_civil = instance.estado_civil
#         edad = instance.edad

#         if estado_civil == 'Soltero':
#             instance.estadocivilvalues.valor_numerico_estado_civil = 10
#         elif estado_civil == 'Casado':
#             instance.estadocivilvalues.valor_numerico_estado_civil = 8

#         if edad == 20:
#             instance.estadocivilvalues.valor_numerico_edad = 10
#         elif edad == 50:
#             instance.estadocivilvalues.valor_numerico_edad = 8

#         # Guarda los cambios en el EstadoCivilValues
#         instance.estadocivilvalues.save()


        
# # Conectar la señal
# post_save.connect(create_estado_civil_values, sender=User)
    
    

