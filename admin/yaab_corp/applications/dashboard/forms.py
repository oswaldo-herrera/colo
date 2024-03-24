from django import forms 
from django.db.models import Min,Max
from .models import Productos,Plazo,Simulador,ProductoCreditoGrupal,Prestamo,SimuladorPrueba,TipoPrestamo,Periodo,PruebaSimula

from applications.users.models import User



class SimuladorForm(forms.ModelForm):
    
    tipo_credito = forms.ModelChoiceField(
        queryset= Productos.objects.all(),
        label = 'Tipo de crédito',        
        required=False,
        empty_label="Seleccionar",
        initial= 0,
        widget= forms.Select(
            attrs={
                'id':'id_tipo_credito',
                'class':'form-control btn btn-outline-light w-25 mt-2 rounded-pill',
                'placeholder':'Seleccionar',
                
            }
        )
    )
    
    amount = forms.DecimalField(
        label='Monto',
        required=False,
        widget=forms.widgets.NumberInput(
            attrs={
                'id': 'id_amount',
                'class': 'input-range d-none',                
                'type': 'range',
                'onchange':'rangeSlide(this.value)',
                'onmousemove':'rangeSlide(this.value)'
            }
        )
    )
    
    
    interest_rate = forms.DecimalField(
        label='Interés',
        required=False,
        widget= forms.NumberInput(
            attrs={
                'id': 'id_interest_rate',
                'class':'form-control',
                
                
            }
        )
    )
        
    interest_moratorio = forms.DecimalField(
        label='Interés moratorio',
        required=False,
        widget= forms.NumberInput(
            attrs={
                'id': 'id_interest_moratorio',
                'class':'form-control',
                
                
            }
        )
    )
    
    plazo_nombre = forms.ModelChoiceField(
        queryset= Plazo.objects.all(),
        label = 'Tipo de plazo',
        required=False,
        empty_label='Seleccionar',
        initial= 0,
        widget= forms.Select(
            attrs={
                'id':'id_plazo_nombre',
                'class':'form-control btn btn-outline-light w-25 mt-1 rounded-pill',
                'placeholder':'Tipo de plazo'
            }
        )
    )

    term = forms.IntegerField(
        
        label = 'Pagos',
        required=False,
        widget= forms.widgets.NumberInput(
            attrs={
                'id': 'id_term',
                'class':'input-range d-none',
                'type':'range',
                'placeholder':'12,14,16...',
                'onchange':'rangeSlideTerm(this.value)',
                'onmousemove':'rangeSlideTerm(this.value)'
            }
        )
    )
        
    class Meta:
        model = Simulador
        fields = ['tipo_credito','amount','interest_rate','plazo_nombre', 'term','interest_moratorio']


class ProductosForm(forms.ModelForm):
    nombre_credito =forms.CharField(
        max_length = 50,
        label = "Credito",
        required=False,
        widget=forms.TextInput(
                attrs={
                    'class':'form-control ',
                    'placeholder':'Credito...',
                    
                }
            )        
    )
    
    class Meta:
        model = Productos
        fields = ['nombre_credito']
        
        
        
class PlazoPagoForm(forms.ModelForm):
    
    nombre_credito = forms.CharField(
       max_length= 50,
        label='Credito',
        required=False,
        widget=forms.TextInput(
            attrs={
                'class':'form-control',
                'placeholder': 'nombre credito...',
            }
        )
    )
    
    plazo_tiempo = forms.CharField(
       max_length= 50,
        label='Plazo',
        required=False,
        widget=forms.TextInput(
            attrs={
                'class':'form-control',
                'placeholder': 'semanal,quincenal o mensual...',
            }
        )
    )
    
    interes_credito =forms.DecimalField(        
        label = "Interes",
        required=False,
        widget=forms.NumberInput(
                attrs={
                    'class':'form-control ',
                    'placeholder':'Interes...',
                    
                }
            )        
    )
    
    
    interes_moratorio =forms.DecimalField(        
        label = "Interes Moratorio",
        required=False,
        widget=forms.NumberInput(
                attrs={
                    'class':'form-control ',
                    'placeholder':'Interes moratorio...',
                    
                }
            )        
    )
    
    class Meta:
        model = Plazo 
        fields = ['nombre_credito','plazo_tiempo','interes_credito','interes_moratorio']
        
class FormProductosGrupal(forms.ModelForm):
    
        
    nombre_grupal = forms.CharField(
        max_length= 50,
        label='Nombre Grupal',
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'nombre grupal',
            }
        )
    )
    
    numero_participante = forms.IntegerField(
        
        label = 'Participantes',
        required=False,
        widget= forms.widgets.NumberInput(
            attrs={
                
                'class':'form-control ',                
                'placeholder':'numero de particiapntes...',
                
            }
        )
    )
    
    monto_credito = forms.IntegerField(
        
        label = 'Monto',
        required=False,
        widget= forms.widgets.NumberInput(
            attrs={
                
                'class':'form-control ',               
                'placeholder':'monto...',
                
            }
        )
    )
    
    class Meta:
        model = ProductoCreditoGrupal
        fields = ['nombre_grupal','numero_participante','monto_credito']
        

class PrestamoForm(forms.ModelForm):
    
    tipo_prestamo = forms.ModelChoiceField(
        queryset= TipoPrestamo.objects.all(),
        label = '',        
        required=False,
        empty_label="Tipo prestamo",
        initial= 0,
        widget= forms.Select(
            attrs={
                'id':'id_tipo_prestamo',
                'class':'form-control btn btn-outline-secondary btn-sm w-50 mt-2 rounded texto-color',
                'placeholder':'Selecciona tu tipo de prestamo',
                
            }
        )
    )
    
    nombre_producto = forms.CharField(
        max_length= 50,
        label='Nombre credito',
        required=False,
        widget=forms.TextInput(
            attrs={
                'id':'id_plazo',
                'class': 'form-control',
                'placeholder': 'nombre de credito',
            }
        )
    )
    
    monto = forms.IntegerField(
        
        label = 'Monto',
        required=False,
        widget= forms.widgets.NumberInput(
            attrs={
                 'id':'id_monto',
                'class':'form-control ',               
                'placeholder':'monto...',
                
            }
        )
    )
    
    tipo_periodo = forms.ModelChoiceField(
        queryset= Periodo.objects.all(),
        label = '',        
        required=False,
        empty_label="Periodo",
        initial= 0,
        widget= forms.Select(
            attrs={
                'id':'id_tipo_prestamo',
                'class':'form-control btn btn-outline-secondary btn-sm w-50 mt-2 rounded texto-color',
                'placeholder':'Selecciona tu periodo',
                
            }
        )
    )
    
    plazo = forms.IntegerField(
        
        label = 'Plazo',
        required=False,
        widget= forms.widgets.NumberInput(
            attrs={
                 'id':'id_monto',
                'class':'form-control ',               
                'placeholder':'ingresa el numero de tiempo...',
                
            }
        )
    )
    
    interes_ordinario =forms.DecimalField(        
        label = "Interes ordinario",
        required=False,
        widget=forms.NumberInput(
                attrs={
                    'class':'form-control ',
                    'placeholder':'Interes ordinario...',
                    
                }
            )        
    )
    
    interes_moratorio =forms.DecimalField(        
        label = "Interes Moratorio",
        required=False,
        widget=forms.NumberInput(
                attrs={
                    'class':'form-control ',
                    'placeholder':'Interes moratorio...',
                    
                }
            )        
    )
    
    pago_mensual =forms.DecimalField(        
        label = "",
        required=False,
        widget=forms.NumberInput(
                attrs={
                    'class':'form-control d-none',
                    'placeholder':'pago ...',
                    
                }
            )        
    )
    
    class Meta:
        model = Prestamo
        fields = ['tipo_prestamo','nombre_producto', 'monto','tipo_periodo', 'plazo','interes_ordinario','interes_moratorio','pago_mensual']


class SimuladorPruebaForm(forms.ModelForm):
    # nombre_prestamo = forms.ModelChoiceField(
    #     #queryset= Prestamo.objects.values_list('monto',flat=True).distinct(),
    #     queryset= Prestamo.objects.all(),
    #     label = '',        
    #     required=False,
    #     empty_label="Monto",
    #     initial= 0,
    #     widget= forms.Select(
    #         attrs={
    #             'id':'id_nombre_prestamo',
    #             'class':'form-control btn btn-outline-light btn-sm  mt-2 rounded texto-color mb-3',
    #             'placeholder':'Selecciona tu monto',
    #             #'type': 'range',
              
                
    #         }
    #     )
    # )
    class Meta:
        model = SimuladorPrueba
        fields = ['nombre_prestamo', 'montos_seleccionados']   
    
    montos_seleccionados = forms.IntegerField(
        widget=forms.TextInput(attrs={'type': 'range', 'min': '0', 'max': '100000', 'step': '1000'})
    )     
class SimPruebas(forms.ModelForm):
    
    nombre_prestamo = forms.ModelChoiceField(
        queryset=Prestamo.objects.all().order_by('id'),
        label='Selecciona el prestamo de tu interes: ',
        required=False,
        empty_label='Seleccionar',
        widget=forms.Select(
            attrs={
                'id': 'id_nombre_prestamo',
                'class': 'select-style',
                #'style': 'background: #333333; width:100%; color:white;',
                'placeholder': 'Selecciona tu monto',                
                
            }
        )
    )
    
    
    usuario_user = forms.ModelChoiceField(
        queryset=User.objects.all(),
        label='',
        required=False,
        empty_label='Seleccionar',
        widget=forms.Select(
            attrs={
                'id': 'id_usuario_user',
                'class': 'select-style',
                #'style': 'background: #333333; width:100%; color:white;',
                'placeholder': 'Selecciona tu usuario',                
                
            }
        )
    )
    
    
    class Meta:
        model = SimuladorPrueba
        fields = ['nombre_prestamo','usuario_user']
    
class PruebaSimulaForms(forms.ModelForm):
    
    class Meta:
        model = PruebaSimula
        fields = ['montos_simulador']
    
    # montos_simulador = forms.ModelChoiceField(
    #     #queryset=Prestamo.objects.all().values_list('monto', flat=True),
    #      queryset=Prestamo.objects.all(), 
    #     widget=forms.NumberInput(attrs={
    #         'id':'id_montos_simulador',            
    #         'type': 'range'
    #     }),
    #     label='Montos Simulador'
    # )
    
    
        
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
        
    #     # Personalizar el widget del campo montos_simulador
    #     self.fields['montos_simulador'].widget = forms.TextInput()
    #     # Agregar opciones personalizadas al widget, por ejemplo, clases CSS o atributos adicionales
    #     self.fields['montos_simulador'].widget.attrs.update({'class': 'custom-input-class'})
        
        
    
    
    # tipo_prestamo = forms.ModelChoiceField(
    #     #queryset= Prestamo.objects.values_list('monto',flat=True).distinct(),
    #     queryset= Prestamo.objects.all(),
    #     label = '',        
    #     required=False,
    #     empty_label="Monto",
    #     initial= 0,
    #     widget= forms.Select(
    #         attrs={
    #             'id':'id_tipo_prestamo',
    #             'class':'form-control btn btn-outline-light btn-sm  mt-2 rounded texto-color mb-3',
    #             'placeholder':'Selecciona tu monto',
    #             #'type': 'range',
    #           
                
    #         }
    #     )
    # )
    
    # tipo_prestamo = forms.ChoiceField(
    #     choices=[(prestamo.monto, prestamo.monto) for prestamo in Prestamo.objects.all()],
    #     label='Monto del préstamo',
    #     widget= forms.Select(
    #         attrs={
    #             'id':'id_tipo_prestamo',
    #             'class':'form-control btn btn-outline-light btn-sm  mt-2 rounded texto-color mb-3',
    #             'placeholder':'Selecciona tu monto',
                
                
    #         }
    #     )
    # )
    
        
        
    
    
    
        
        


    
