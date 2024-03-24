from django import forms
from django_select2 import forms as select2forms
from .models import RegistroPagosModel, RegistroCreditos,EstatusCredito
from applications.dashboard.models import SimuladorPrueba

class NumeroContratoSelect2Widget(select2forms.Select2Widget):
    def label_from_instance(self, obj):
        return obj.numero_contrato


class RegistroPagosForm(forms.ModelForm):  
    
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     # Cambiar el queryset para utilizar el campo identificador_unico
    #     self.fields['simulador'].queryset = SimuladorPrueba.objects.all().values_list('identificador_unico', flat=True) 
    #.values_list('identificador_unico', flat=True),

    
    simulador = forms.ModelChoiceField(
        queryset=SimuladorPrueba.objects.all(),
        label='Numero de contrato:',
        empty_label='Seleccionar',
        widget=NumeroContratoSelect2Widget(
            attrs={
                'id': 'id_simulador',
                'class': 'form-control mb-2'
            }
        )
        
        
    )
    
    
    monto_pagado = forms.DecimalField(
        
        label = 'Monto a pagar: ',
        required=False,
        widget= forms.widgets.NumberInput(
            attrs={
                'id': 'id_monto_total_registro',
                'class':'form-control mb-2',
                'placeholder':'ingrese la cantidad...',
                
            }
        )
    )
    
    comprobante_pago =forms.FileField(
        label = "Comprobante de Pago: ",
        required=False,
        widget=forms.ClearableFileInput(
                attrs={
                    
                    'class':'form-control mb-2',
                    'placeholder':'ingresa el archivo...',
                    'type': 'file',
                    
                }
            ),        
        
    )
    
    
    
    class Meta:
        model = RegistroPagosModel
        fields = ['simulador','monto_pagado','comprobante_pago','numero_pago']
        
    
    
        