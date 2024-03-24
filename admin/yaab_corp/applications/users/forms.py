from django.forms import ModelForm,widgets
from django import forms
from django.utils.safestring import mark_safe
from django.template.loader import render_to_string
from datetime import datetime
from .models import User,CorreosCreditoGrupal,GrupoCreditoPersonal
from applications.dashboard.models import ProductoCreditoGrupal
from django.utils.translation import gettext_lazy as _



# class SignaturePadWidget(forms.widgets.Widget):
#     template_name = 'users/widgets/signature_pad_widget.html'
    
    

#     class Media:
#         js = ('https://cdn.jsdelivr.net/npm/signature_pad@2.3.2/signature_pad.js',)

# class SignaturePadFormField(forms.CharField):
#     widget = SignaturePadWidget


class UserCreationForm(forms.ModelForm):
    # Define los campos que deseas incluir en el formulario
   
    email =forms.EmailField(
        label = "Email",
        
        widget=forms.EmailInput(
                attrs={
                    # h-75 rounded-pill ml-1
                    'class':'form-control ',
                    'type': 'email',
                    'placeholder':'usuario@ejemplo.com',
                    
                }
            )        
    )
        
    password1 =forms.CharField(
        max_length=50,
        label = "Contraseña",
        widget=forms.PasswordInput(
                attrs={
                    'class':'form-control ',                    
                    'placeholder':'contraseña',
                    
                }
            )        
    )
    
      
    password2 =forms.CharField(
        max_length=50,
        label = "Contraseña",
        
        widget=forms.PasswordInput(
                attrs={
                    'class':'form-control ',                    
                    'placeholder':'confirmar contraseña...',
                    
                }
            )        
    )
    
    first_name =forms.CharField(
        max_length = 50,
        label = "Usuario",
        
        widget=forms.TextInput(
                attrs={
                    'class':'form-control ',
                    'placeholder':'nombres...',
                    
                }
            )        
    )
    
    last_name =forms.CharField(
        max_length = 50,
        label = "Usuario",
        
        widget=forms.TextInput(
                attrs={
                    'class':'form-control ',
                    'placeholder':'primer apellido...',
                    
                }
            )        
    )
   
    second_name =forms.CharField(
        max_length = 50,
        label = "Usuario",
        
        widget=forms.TextInput(
                attrs={
                    'class':'form-control ',
                    'placeholder':'segundo apellido...',
                    
                }
            )        
    )
    
    class Meta:
        model = User
        fields = ('email', 'password1', 'password2', 'first_name', 'last_name','second_name')
        

class UserChangeForm(forms.ModelForm):
    
        
    
    
    email =forms.CharField(
        max_length = 50,
        label = "Usuario",
        required=False,
        widget=forms.TextInput(
                attrs={
                    'class':'form-control ',
                    'placeholder':'Usuario...',
                    
                }
            )        
    )
    
    
    
    
    first_name =forms.CharField(
        max_length = 50,
        label = "Nombre",
        required=False,
        widget=forms.TextInput(
                attrs={
                    'class':'form-control ',
                    'placeholder':'Nombre...',
                    
                }
            )        
    )
    
    last_name =forms.CharField(
        max_length = 50,
        label = "Apellido",
        required=False,
        widget=forms.TextInput(
                attrs={
                    'class':'form-control ',
                    'placeholder':'Apellido...',
                    
                }
            )        
    )
    
    second_name =forms.CharField(
        max_length = 50,
        label = "Segundo Apellido",
        required=True,
        widget=forms.TextInput(
                attrs={
                    'id': 'id_second_name',
                    'class':'form-control ',
                    'placeholder':'Apellido...',
                    
                }
            )        
    )
  
    
    telefono_particular =forms.CharField(
        max_length = 50,
        label = "Teléfono particular",
        required=False,
        widget=forms.TextInput(
                attrs={
                    'class':'form-control ',
                    'placeholder':'Teléfono...',
                    
                }
            )        
    )
        
    fecha_nac =forms.DateField(
        required=False,
        widget=forms.DateInput(
                attrs={
                    'id':'id_fecha_nac',
                    'class':'form-control',
                    'type': 'text',
                    'placeholder': 'ingresa tu fecha de nacimiento'
                       
                }
            )
           
    )
    
    curp_texto =forms.CharField(
        max_length = 50,
        label = "CURP",
        required=False,
        widget=forms.TextInput(
                attrs={
                    'class':'form-control ',
                    'placeholder':'Curp...',
                    
                }
            )        
    )
    
    curp =forms.FileField(
        label = "CURP",
        required=False,
        widget=forms.ClearableFileInput(
                attrs={
                    'accept':'application/pdf',
                    'class':'form-control ',
                    'placeholder':'CURP...',
                    'type': 'file',
                    
                }
            ),        
        help_text=_('Solo se permiten archivos PDF')
    )
    
    documento_ine =forms.FileField(
        label = "INE",
        required=False,
        widget=forms.ClearableFileInput(
                attrs={
                    'accept':'application/pdf',
                    'class':'form-control ',
                    'placeholder':'INE...',
                    'type': 'file',
                    
                }
            ),        
        help_text=_('Solo se permiten archivos PDF')
    )
    
    
    
    comprobante_domicilio =forms.FileField(
        label = "Comprobante domicilio:",
        required=False,
        widget=forms.ClearableFileInput(
                attrs={
                    'accept':'application/pdf',
                    'class':'form-control ',
                    'placeholder':'Comprobante domicilio:...',
                    'type': 'file',
                    
                    
                }
            ),        
        help_text=_('Solo se permiten archivos PDF')
    )
    
    documento_ine_aval =forms.FileField(
        label = "INE:",
        required=False,
        widget=forms.ClearableFileInput(
                attrs={
                    'accept':'application/pdf',
                    'class':'form-control ',
                    'placeholder':'INE:...',
                    'type':'file',
                    
                }
            ),        
        help_text=_('Solo se permiten archivos PDF')
    )
    
    
    comprobante_domicilio_aval =forms.FileField(
        label = "Comprobante domicilio:",
        required=False,
        widget=forms.ClearableFileInput(
                attrs={
                    'accept':'application/pdf',
                    'class':'form-control ',
                    'placeholder':'Comprobante domicilio:...',
                    'type':'file',
                    
                }
            ),        
        help_text=_('Solo se permiten archivos PDF')
    )
    
    curp_aval =forms.FileField(
        label = "CURP:",
        required=False,
        widget=forms.ClearableFileInput(
                attrs={
                    'accept':'application/pdf',
                    'class':'form-control ',
                    'placeholder':'CURP:...',
                    'type':'file',
                    
                }
            ),        
        help_text=_('Solo se permiten archivos PDF')
    )
    
    rfc =forms.CharField(
        max_length = 50,
        label = "RFC",
        required=False,
        widget=forms.TextInput(
                attrs={
                    'class':'form-control ',
                    'placeholder':'RFC...',
                    
                }
            )        
    )
    
    estado_civil =forms.CharField(
        max_length = 50,
        label = "Estado Civil",
        required=False,
        widget=forms.TextInput(
                attrs={
                    'class':'form-control ',
                    'placeholder':'Estado Civil...',
                    
                }
            )        
    )
    
    genero =forms.CharField(
        max_length = 50,
        label = "Genero",
        required=False,
        widget=forms.TextInput(
                attrs={
                    'class':'form-control ',
                    'placeholder':'Genero...',
                    
                }
            )        
    )
    
    nacionalidad =forms.CharField(
        max_length = 50,
        label = "Nacionalidad",
        required=False,
        widget=forms.TextInput(
                attrs={
                    'class':'form-control ',
                    'placeholder':'Nacionalidad...',
                    
                }
            )        
    )
    
    pais =forms.CharField(
        max_length = 50,
        label = "Pais",
        required=False,
        widget=forms.TextInput(
                attrs={
                    'class':'form-control ',
                    'placeholder':'Estado...',
                    
                }
            )        
    )
    
    estado =forms.CharField(
        max_length = 50,
        label = "Estado",
        required=False,
        widget=forms.TextInput(
                attrs={
                    'class':'form-control ',
                    'placeholder':'Estado...',
                    
                }
            )        
    )
    
    # celular =forms.CharField(
    #     max_length = 50,
    #     label = "Celular",
    #     required=False,
    #     widget=forms.TextInput(
    #             attrs={
    #                 'class':'form-control ',
    #                 'placeholder':'Celular...',
                    
    #             }
    #         )        
    # )
    
    numero_dependientes =forms.CharField(
        max_length = 50,
        label = "Dependientes",
        required=False,
        widget=forms.TextInput(
                attrs={
                    'class':'form-control ',
                    'placeholder':'Dependientes...',
                    
                }
            )        
    )
    
    
    calle_numero =forms.CharField(
        max_length = 50,
        label = "Calle y Numero",
        required=False,
        widget=forms.TextInput(
                attrs={
                    'class':'form-control ',
                    'placeholder':'Calle y numero...',
                    
                }
            )        
    )
    
    colonia =forms.CharField(
        max_length = 50,
        label = "Colonia",
        required=False,
        widget=forms.TextInput(
                attrs={
                    'class':'form-control ',
                    'placeholder':'Colonia...',
                    
                }
            )        
    )
    
    cp =forms.CharField(
        max_length = 50,
        label = "C.P.",
        required=False,
        widget=forms.TextInput(
                attrs={
                    'class':'form-control ',
                    'placeholder':'C.P....',
                    
                }
            )        
    )
    
    ciudad =forms.CharField(
        max_length = 50,
        label = "Ciudad",
        required=False,
        widget=forms.TextInput(
                attrs={
                    'class':'form-control ',
                    'placeholder':'Ciudad...',
                    
                }
            )        
    )
    
    estado_direccion =forms.CharField(
        max_length = 50,
        label = "Estado Direccion",
        required=False,
        widget=forms.TextInput(
                attrs={
                    'class':'form-control ',
                    'placeholder':'Estado Direccion...',
                    
                }
            )        
    )
    
    tipo_vivienda =forms.CharField(
        max_length = 50,
        label = "Tipo de vivienda",
        required=False,
        widget=forms.TextInput(
                attrs={
                    'class':'form-control ',
                    'placeholder':'Tipo de vivienda...',
                    
                }
            )        
    )
    
    
    años_radicando =forms.CharField(
        max_length = 50,
        label = "Años radicando",
        required=False,
        widget=forms.TextInput(
                attrs={
                    'class':'form-control ',
                    'placeholder':'años radicando...',
                    
                }
            )        
    )
    
    conyuge_pareja =forms.CharField(
        max_length = 50,
        label = "Conyuge",
        required=False,
        widget=forms.TextInput(
                attrs={
                    'class':'form-control ',
                    'placeholder':'conyuge...',
                    
                }
            )        
    )
    
    trabajo_conyuge =forms.CharField(
        max_length = 50,
        label = "Trabajo",
        required=False,
        widget=forms.TextInput(
                attrs={
                    'class':'form-control ',
                    'placeholder':'trabajo...',
                    
                }
            )        
    )
    
    antiguedad_laboral_conyuge =forms.CharField(
        max_length = 50,
        label = "Antiguedad laboral",
        required=False,
        widget=forms.TextInput(
                attrs={
                    'class':'form-control ',
                    'placeholder':'antiguedad laboral...',
                    
                }
            )        
    )
    
    telefono_conyuge =forms.CharField(
        max_length = 50,
        label = "Teléfono",
        required=False,
        widget=forms.TextInput(
                attrs={
                    'class':'form-control ',
                    'placeholder':'teléfono...',
                    
                }
            )        
    )
    
    referencia_personal_conyuge_1 =forms.CharField(
        max_length = 50,
        label = "Primer referencia ",
        required=False,
        widget=forms.TextInput(
                attrs={
                    'class':'form-control ',
                    'placeholder':'referencia...',
                    
                }
            )        
    )
    
    telefono_ref_conyuge_1 =forms.CharField(
        max_length = 50,
        label = "Teléfono",
        required=False,
        widget=forms.TextInput(
                attrs={
                    'class':'form-control ',
                    'placeholder':'teléfono...',
                    
                }
            )        
    )
    
    referencia_personal_conyuge_2 =forms.CharField(
        max_length = 50,
        label = "Segunda referencia ",
        required=False,
        widget=forms.TextInput(
                attrs={
                    'class':'form-control ',
                    'placeholder':'referencia...',
                    
                }
            )        
    )
    
    telefono_ref_conyuge_2 =forms.CharField(
        max_length = 50,
        label = "Primer referencia ",
        required=False,
        widget=forms.TextInput(
                attrs={
                    'class':'form-control ',
                    'placeholder':'referencia...',
                    
                }
            )        
    )
    
    nombre_negocio =forms.CharField(
        max_length = 50,
        label = "Nombre del negocio ",
        required=False,
        widget=forms.TextInput(
                attrs={
                    'class':'form-control ',
                    'placeholder':'negocio...',
                    
                }
            )        
    )
    
    giro =forms.CharField(
        max_length = 50,
        label = "Giro ",
        required=False,
        widget=forms.TextInput(
                attrs={
                    'class':'form-control ',
                    'placeholder':'giro...',
                    
                }
            )        
    )
    
    inmueble =forms.CharField(
        max_length = 50,
        label = "Inmueble ",
        required=False,
        widget=forms.TextInput(
                attrs={
                    'class':'form-control ',
                    'placeholder':'inmueble...',
                    
                }
            )        
    )
    
    años_antiguedad =forms.CharField(
        max_length = 50,
        label = "Años de antiguedad ",
        required=False,
        widget=forms.TextInput(
                attrs={
                    'class':'form-control ',
                    'placeholder':'antiguedad...',
                    
                }
            )        
    )
    
    calle_numero_negocio =forms.CharField(
        max_length = 50,
        label = "Calle y numero ",
        required=False,
        widget=forms.TextInput(
                attrs={
                    'class':'form-control ',
                    'placeholder':'calle...',
                    
                }
            )        
    )
    
    colonia_negocio =forms.CharField(
        max_length = 50,
        label = "Colonia del negocio ",
        required=False,
        widget=forms.TextInput(
                attrs={
                    'class':'form-control ',
                    'placeholder':'colonia...',
                    
                }
            )        
    )
    
    cp_negocio =forms.CharField(
        max_length = 50,
        label = "C.P. negocio ",
        required=False,
        widget=forms.TextInput(
                attrs={
                    'class':'form-control ',
                    'placeholder':'c.p. ...',
                    
                }
            )        
    )
    
    ciudad_negocio =forms.CharField(
        max_length = 50,
        label = "Ciudad ",
        required=False,
        widget=forms.TextInput(
                attrs={
                    'class':'form-control ',
                    'placeholder':'ciudad...',
                    
                }
            )        
    )
    
    estado_negocio =forms.CharField(
        max_length = 50,
        label = "Estado ",
        required=False,
        widget=forms.TextInput(
                attrs={
                    'class':'form-control ',
                    'placeholder':'estado...',
                    
                }
            )        
    )
    
    nombre_aval =forms.CharField(
        max_length = 50,
        label = "Nombre ",
        required=False,
        widget=forms.TextInput(
                attrs={
                    'class':'form-control ',
                    'placeholder':'nombre...',
                    
                }
            )        
    )
    
    primer_apellido =forms.CharField(
        max_length = 50,
        label = "Primer apellido ",
        required=False,
        widget=forms.TextInput(
                attrs={
                    'class':'form-control ',
                    'placeholder':'primer apellido...',
                    
                }
            )        
    )
    
    segundo_apellido =forms.CharField(
        max_length = 50,
        label = "Segundo apellido ",
        required=False,
        widget=forms.TextInput(
                attrs={
                    'class':'form-control ',
                    'placeholder':'segundo apellido...',
                    
                }
            )        
    )
    
    
    fecha_nac_aval =forms.DateField(
        required=False,
        widget=forms.DateInput(
                attrs={
                    'id':'id_fecha_nac_aval',
                    'class':'form-control ',
                    'type': 'text',
                    'placeholder': 'ingresa tu fecha de nacimiento',
                    
                    
                }
            )        
    )
    
    email_aval =forms.CharField(
        max_length = 50,
        label = "Email ",
        required=False,
        widget=forms.TextInput(
                attrs={
                    'class':'form-control ',
                    'placeholder':'email...',
                    
                }
            )        
    )
    
    genero_aval =forms.CharField(
        max_length = 50,
        label = "Genero ",
        required=False,
        widget=forms.TextInput(
                attrs={
                    'class':'form-control ',
                    'placeholder':'genero...',
                    
                }
            )        
    )
    
    ciudad_aval =forms.CharField(
        max_length = 50,
        label = "Ciudad ",
        required=False,
        widget=forms.TextInput(
                attrs={
                    'class':'form-control ',
                    'placeholder':'ciudad...',
                    
                }
            )        
    )
    
    estado_aval =forms.CharField(
        max_length = 50,
        label = "Estado ",
        required=False,
        widget=forms.TextInput(
                attrs={
                    'class':'form-control ',
                    'placeholder':'estado...',
                    
                }
            )        
    )
    
    rfc_aval =forms.CharField(
        max_length = 50,
        label = "RFC ",
        required=False,
        widget=forms.TextInput(
                attrs={
                    'class':'form-control ',
                    'placeholder':'rfc...',
                    
                }
            )        
    )
    
    calle_numero_aval =forms.CharField(
        max_length = 50,
        label = "Calle y numero ",
        required=False,
        widget=forms.TextInput(
                attrs={
                    'class':'form-control ',
                    'placeholder':'calle y numero...',
                    
                }
            )        
    )
    
    colonia_aval =forms.CharField(
        max_length = 50,
        label = "Colonia ",
        required=False,
        widget=forms.TextInput(
                attrs={
                    'class':'form-control ',
                    'placeholder':'colonia...',
                    
                }
            )        
    )
    
    cp_aval =forms.CharField(
        max_length = 50,
        label = "C.P. ",
        required=False,
        widget=forms.TextInput(
                attrs={
                    'class':'form-control ',
                    'placeholder':'c.p. ...',
                    
                }
            )        
    )
    
    relacion_titular =forms.CharField(
        max_length = 50,
        label = "Relacion con el titular ",
        required=False,
        widget=forms.TextInput(
                attrs={
                    'class':'form-control ',
                    'placeholder':'relacion...',
                    
                }
            )        
    )
    
    tipo_vivienda_aval =forms.CharField(
        max_length = 50,
        label = "Tipo de vivienda ",
        required=False,
        widget=forms.TextInput(
                attrs={
                    'class':'form-control ',
                    'placeholder':'vivienda...',
                    
                }
            )        
    )
    
    años_radicando_aval =forms.CharField(
        max_length = 50,
        label = "Años radicando ",
        required=False,
        widget=forms.TextInput(
                attrs={
                    'class':'form-control ',
                    'placeholder':'radicando...',
                    
                }
            )        
    )
    
    lugar_trabajo_aval =forms.CharField(
        max_length = 50,
        label = "Lugar de trabajo ",
        required=False,
        widget=forms.TextInput(
                attrs={
                    'class':'form-control ',
                    'placeholder':'lugar trabajo...',
                    
                }
            )        
    )
    
    antiguedad_trabajo_aval =forms.CharField(
        max_length = 50,
        label = "Antiguedad de trabajo ",
        required=False,
        widget=forms.TextInput(
                attrs={
                    'class':'form-control ',
                    'placeholder':'antiguedad trabajo...',
                    
                }
            )        
    )
    
    celular_aval =forms.CharField(
        max_length = 50,
        label = "Celular ",
        required=False,
        widget=forms.TextInput(
                attrs={
                    'class':'form-control ',
                    'placeholder':'celular...',
                    
                }
            )        
    )
    
    telefono_laboral_aval =forms.CharField(
        max_length = 50,
        label = "Telefono laboral ",
        required=False,
        widget=forms.TextInput(
                attrs={
                    
                    'class':'form-control',
                    'placeholder':'telefono...',
                    
                    
                }
            )        
    )
    
    
    
    aviso_privacidad = forms.BooleanField(
        label="Tu etiqueta de checkbox",
        required=False,
        widget=forms.CheckboxInput(attrs={
            
            'class': 'prestamo form-check-input',  
            
        })
    )
    
    confirmado = forms.BooleanField(
        label="Tu etiqueta de checkbox",
        required=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input',  
        })
    )
    
    
    rechazado = forms.BooleanField(
        label="Tu etiqueta de checkbox",
        required=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input',  
        })
    )
    
    buro_credito = forms.BooleanField(
        label="Tu etiqueta de checkbox",
        required=False,
        widget=forms.CheckboxInput(attrs={
            
            'class': 'prestamo form-check-input',  
            
        })
    )
    
    
    imagen_perfil= forms.ImageField(
        required=False,
        label='Imagen de Perfil',
        widget=forms.FileInput(
            attrs={
                'class':'form-control'
            }
        )
    )
    
    # firma_digital_personal = forms.CharField(
    #     max_length=500,
    #     required=False,
    #     widget=forms.Textarea(
    #         attrs={'rows': 3}
    #     )
    # )
    # firma_imagen_personal = forms.ImageField(
    #     required=False
    # )
    
    
    # firma_digital_personal = forms.FileField(
    #     label="Firma Digital Personal",
    #     required=False,
    #     widget=SignaturePadWidget(attrs={'accept': 'application/pdf'}),
    #     help_text=_('Solo se permiten archivos PDF')
    # )
    
    # firma_digital_personal = SignaturePadFormField(
    #     label="Firma Digital Personal",
    #     required=False,
    #     widget=SignaturePadWidget(attrs={'id': 'signature-field', 'class': 'signature-pad border border-secondary border-3 rounded', 'width': '300', 'height': '80'}),
    # )


    
    
    
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name','second_name','fecha_nac','curp','curp_texto','documento_ine','rfc','estado_civil','genero','nacionalidad','pais','estado','numero_dependientes','telefono_particular','calle_numero','colonia','cp','ciudad','estado_direccion','tipo_vivienda','años_radicando','conyuge_pareja','trabajo_conyuge','antiguedad_laboral_conyuge','telefono_conyuge','referencia_personal_conyuge_1','telefono_ref_conyuge_1','referencia_personal_conyuge_2','telefono_ref_conyuge_2','nombre_negocio','giro','inmueble','años_antiguedad','calle_numero_negocio','colonia_negocio','cp_negocio','ciudad_negocio','estado_negocio','nombre_aval','primer_apellido','segundo_apellido','fecha_nac_aval','curp_aval','genero_aval','ciudad_aval','estado_aval','rfc_aval','calle_numero_aval','colonia_aval','cp_aval','relacion_titular','tipo_vivienda_aval','años_radicando_aval','lugar_trabajo_aval','antiguedad_trabajo_aval','celular_aval','email_aval','telefono_laboral_aval','comprobante_domicilio','documento_ine_aval','comprobante_domicilio_aval','aviso_privacidad','confirmado','rechazado','buro_credito','imagen_perfil')
        
        
class CorreoGrupoCredito(forms.ModelForm):
    
    nombre_grupal = forms.ModelChoiceField(
        queryset=ProductoCreditoGrupal.objects.all(),
        label = 'Credito:',
        required=False,
        widget=forms.widgets.Select(
            attrs={
                'id':'id_nombre_grupal',
                'class': 'form-control',
                'placeholder': 'nombre grupal',
            }
        )
    )
    
    participantes_numero = forms.ModelChoiceField(
        #queryset=ProductoCreditoGrupal.objects.values_list('numero_participante', flat=True).distinct(),
        queryset=ProductoCreditoGrupal.objects.all(),
        label = 'Numero de Participantes',
        required=False,

        widget= forms.widgets.Select(
            attrs={
                'id':'id_participantes_numero',
                'class':'form-control mb-2 ',                
                'placeholder':'numero de particiapntes...',
                
            }
        ),
        
    )
    

    
    monto_vacantes = forms.DecimalField(
        
        label = 'Monto',
        required=False,
        widget= forms.widgets.NumberInput(
            attrs={
                'id':'id_monto_vacantes',
                'class':'form-control mb-2',               
                'placeholder':'monto...',
                'readonly': 'readonly',
                
            }
        )
    )
    
    correos_participantes = forms.EmailField(
        max_length=50,
        label="Coordinador",
        required=False,
        widget=forms.EmailInput(
            attrs={
                'id': 'email_1_grupal',
                'class': 'form-control mb-2',
                'placeholder': 'correo electrónico...',
            }
        )
    )
    
    
    names_grupal =forms.CharField(
        max_length = 50,
        label = "Nombre completo ",
        required=False,
        widget=forms.TextInput(
                attrs={
                    'class':'form-control mb-2',
                    'placeholder':'nombre...',
                    
                }
            )        
    )
    
    surnames_grupal =forms.CharField(
        max_length = 50,
        label = "Apellidos ",
        required=False,
        widget=forms.TextInput(
                attrs={
                    'class':'form-control mb-2',
                    'placeholder':'apellidos...',
                    
                }
            )        
    )
    
    correo_coordinador =forms.CharField(
        max_length = 50,
        label = "Correo electronico ",
        required=False,
        widget=forms.TextInput(
                attrs={
                    'class':'form-control mb-2',
                    'placeholder':'email...',
                    
                }
            )        
    )

    curp_texto_grupal =forms.CharField(
        max_length = 50,
        label = "CURP ",
        required=False,
        widget=forms.TextInput(
                attrs={
                    'class':'form-control mb-2',
                    'placeholder':'curp...',
                    
                }
            )        
    )
    
    rfc_grupal =forms.CharField(
        max_length = 50,
        label = "RFC ",
        required=False,
        widget=forms.TextInput(
                attrs={
                    'class':'form-control mb-2',
                    'placeholder':'rfc...',
                    
                }
            )        
    )
    
    celular_coordinador =forms.CharField(
        max_length = 50,
        label = "Celular ",
        required=False,
        widget=forms.TextInput(
                attrs={
                    'class':'form-control ',
                    'placeholder':'ingresa tu numero de celular...',
                    
                }
            )        
    )
    
    class Meta:
        model = CorreosCreditoGrupal
        fields =['nombre_grupal','participantes_numero','monto_vacantes','correos_participantes','names_grupal','surnames_grupal','curp_texto_grupal','rfc_grupal','celular_coordinador','correo_coordinador']
        
        
    def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields['participantes_numero'].empty_label = 'Seleccionar'
        
        
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     # Modificar las etiquetas de las opciones para incluir el nombre del grupo
    #     self.fields['participantes_numero'].label_from_instance = self.label_from_instance_custom

    # def label_from_instance_custom(self, obj):
    #     label = f"{obj.nombre_grupal} ({obj.numero_participante} participantes)" if obj.nombre_grupal else "Seleccionar"
    #     return label
        
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     # Modificar las etiquetas de las opciones para incluir el nombre del grupo
    #     self.fields['participantes_numero'].label_from_instance = lambda obj: f"{obj.nombre_grupal}"
    
    
    ##({obj.numero_participante} participantes)    
    # def __init__(self, *args, **kwargs):
    #         super().__init__(*args, **kwargs)
    #         self.fields['participantes_numero'].empty_label = 'Seleccionar'
        

class FormularioGRupoCreditoPersona(forms.ModelForm):
    
    email =forms.CharField(
        max_length = 50,
        label = "Usuario",
        required=False,
        widget=forms.TextInput(
                attrs={
                    'class':'form-control ',
                    'placeholder':'Usuario...',
                    'readonly':'readonly',
                    
                }
            )        
    )
    
    first_name =forms.CharField(
        max_length = 50,
        label = "Nombre",
        required=False,
        widget=forms.TextInput(
                attrs={
                    'class':'form-control ',
                    'placeholder':'Nombre...',
                    
                }
            )        
    )
    
    last_name =forms.CharField(
        max_length = 50,
        label = "Apellido",
        required=False,
        widget=forms.TextInput(
                attrs={
                    'class':'form-control ',
                    'placeholder':'Apellido...',
                    
                }
            )        
    )
    
    second_name =forms.CharField(
        max_length = 50,
        label = "Apellido",
        required=False,
        widget=forms.TextInput(
                attrs={
                    'class':'form-control ',
                    'placeholder':'Apellido...',
                    
                }
            )        
    )
  
    
    telefono_particular =forms.CharField(
        max_length = 50,
        label = "Teléfono particular",
        required=False,
        widget=forms.TextInput(
                attrs={
                    'class':'form-control ',
                    'placeholder':'Teléfono...',
                    
                }
            )        
    )
        
    fecha_nac_grupal =forms.DateField(
        required=False,
        widget=forms.DateInput(
                attrs={
                    'id':'id_fecha_nac_grupal',
                    'class':'form-control',
                    'type': 'text',
                    'placeholder': 'ingresa tu fecha de nacimiento'
                       
                }
            )
           
    )
    
    curp_texto =forms.CharField(
        max_length = 50,
        label = "CURP",
        required=False,
        widget=forms.TextInput(
                attrs={
                    'class':'form-control ',
                    'placeholder':'Curp...',
                    
                }
            )        
    )
    
    curp =forms.FileField(
        label = "CURP",
        required=False,
        widget=forms.ClearableFileInput(
                attrs={
                    'accept':'application/pdf',
                    'class':'form-control ',
                    'placeholder':'CURP...',
                    'type': 'file',
                    
                }
            ),        
        help_text=_('Solo se permiten archivos PDF')
    )
    
    
    
    documento_ine_grupal =forms.FileField(
        label = "INE",
        required=False,
        widget=forms.ClearableFileInput(
                attrs={
                    'accept':'application/pdf',
                    'class':'form-control ',
                    'placeholder':'INE...',
                    'type': 'file',
                    
                }
            ),        
        help_text=_('Solo se permiten archivos PDF')
    )
    
    
    
    comprobante_domicilio =forms.FileField(
        label = "Comprobante domicilio:",
        required=False,
        widget=forms.ClearableFileInput(
                attrs={
                    'accept':'application/pdf',
                    'class':'form-control ',
                    'placeholder':'Comprobante domicilio:...',
                    'type': 'file',
                    
                    
                }
            ),        
        help_text=_('Solo se permiten archivos PDF')
    )
    
    rfc =forms.CharField(
        max_length = 50,
        label = "RFC",
        required=False,
        widget=forms.TextInput(
                attrs={
                    'class':'form-control ',
                    'placeholder':'RFC...',
                    
                }
            )        
    )
    
    estado_civil =forms.CharField(
        max_length = 50,
        label = "Estado Civil",
        required=False,
        widget=forms.TextInput(
                attrs={
                    'class':'form-control ',
                    'placeholder':'Estado Civil...',
                    
                }
            )        
    )
        
    genero =forms.CharField(
        max_length = 50,
        label = "Genero",
        required=False,
        widget=forms.TextInput(
                attrs={
                    'class':'form-control ',
                    'placeholder':'Genero...',
                    
                }
            )        
    )
    
    nacionalidad =forms.CharField(
        max_length = 50,
        label = "Nacionalidad",
        required=False,
        widget=forms.TextInput(
                attrs={
                    'class':'form-control ',
                    'placeholder':'Nacionalidad...',
                    
                }
            )        
    )
    
    pais =forms.CharField(
        max_length = 50,
        label = "Pais",
        required=False,
        widget=forms.TextInput(
                attrs={
                    'class':'form-control ',
                    'placeholder':'Estado...',
                    
                }
            )        
    )
    
    estado =forms.CharField(
        max_length = 50,
        label = "Estado",
        required=False,
        widget=forms.TextInput(
                attrs={
                    'class':'form-control ',
                    'placeholder':'Estado...',
                    
                }
            )        
    )
    
    celular =forms.CharField(
        max_length = 50,
        label = "Celular",
        required=False,
        widget=forms.TextInput(
                attrs={
                    'class':'form-control ',
                    'placeholder':'Celular...',
                    
                }
            )        
    )
    
    numero_dependientes =forms.CharField(
        max_length = 50,
        label = "Dependientes",
        required=False,
        widget=forms.TextInput(
                attrs={
                    'class':'form-control ',
                    'placeholder':'Dependientes...',
                    
                }
            )        
    )
    
    calle_numero =forms.CharField(
        max_length = 50,
        label = "Calle y Numero",
        required=False,
        widget=forms.TextInput(
                attrs={
                    'class':'form-control ',
                    'placeholder':'Calle y numero...',
                    
                }
            )        
    )
    
    colonia =forms.CharField(
        max_length = 50,
        label = "Colonia",
        required=False,
        widget=forms.TextInput(
                attrs={
                    'class':'form-control ',
                    'placeholder':'Colonia...',
                    
                }
            )        
    )
    
    cp =forms.CharField(
        max_length = 50,
        label = "C.P.",
        required=False,
        widget=forms.TextInput(
                attrs={
                    'class':'form-control ',
                    'placeholder':'C.P....',
                    
                }
            )        
    )
    
    ciudad =forms.CharField(
        max_length = 50,
        label = "Ciudad",
        required=False,
        widget=forms.TextInput(
                attrs={
                    'class':'form-control ',
                    'placeholder':'Ciudad...',
                    
                }
            )        
    )
    
    estado_direccion =forms.CharField(
        max_length = 50,
        label = "Estado Direccion",
        required=False,
        widget=forms.TextInput(
                attrs={
                    'class':'form-control ',
                    'placeholder':'Estado Direccion...',
                    
                }
            )        
    )
    
    tipo_vivienda =forms.CharField(
        max_length = 50,
        label = "Tipo de vivienda",
        required=False,
        widget=forms.TextInput(
                attrs={
                    'class':'form-control ',
                    'placeholder':'Tipo de vivienda...',
                    
                }
            )        
    )
    
    años_radicando =forms.CharField(
        max_length = 50,
        label = "Años radicando",
        required=False,
        widget=forms.TextInput(
                attrs={
                    'class':'form-control ',
                    'placeholder':'años radicando...',
                    
                }
            )        
    )
    
    token =forms.CharField(
        max_length = 50,
        label = "Token",
        required=False,
        widget=forms.TextInput(
                attrs={
                    'class':'form-control ',
                    'placeholder':'token...',
                    'readonly':'readonly',
                    
                }
            )        
    )
    
    aviso_privacidad_grupal = forms.BooleanField(
        label="Tu etiqueta de checkbox",
        required=False,
        widget=forms.CheckboxInput(attrs={
            
            'class': 'prestamo form-check-input',  
            
        })
    )
    
    buro_credito_grupal = forms.BooleanField(
        label="Tu etiqueta de checkbox",
        required=False,
        widget=forms.CheckboxInput(attrs={
            
            'class': 'prestamo form-check-input',  
            
        })
    )
    
    
    class Meta:
        model = GrupoCreditoPersonal
        fields = ['email','first_name','last_name','second_name','telefono_particular','fecha_nac_grupal','curp_texto','curp','documento_ine_grupal','comprobante_domicilio','rfc','estado_civil','genero','nacionalidad','pais','estado','celular','numero_dependientes','calle_numero','colonia','cp','ciudad','estado_direccion','tipo_vivienda','años_radicando','token','aviso_privacidad_grupal','buro_credito_grupal']