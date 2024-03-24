from typing import Any
import sympy as yaab
from django.db.models.query import QuerySet
from django.shortcuts import render,redirect
from decimal import Decimal
from django.views.generic import TemplateView,ListView,CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from applications.users.models import User,EstadoCivilValues
from applications.dashboard.models import SimuladorPrueba
from .models import RegistroCreditos,EstatusCredito,RegistroPagosModel
from .forms import RegistroPagosForm
from datetime import timedelta,datetime
from django.utils import timezone
from django.urls import reverse_lazy,reverse
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views import View
#from dateutil.relativedelta import relativedelta
from django.db.models import Sum






# Create your views here.



class ControlCalificaciones(ListView):
    template_name = 'calificaciones/control-calificaciones.html'
    context_object_name = 'usuarios'
    
    def get_queryset(self):
        
        usuarios_filtro = EstadoCivilValues.objects.all()      
        
        return usuarios_filtro

    def get_context_data(self, **kwargs) :
        context = super(ControlCalificaciones,self).get_context_data(**kwargs)
        usuarios = EstadoCivilValues.objects.filter(valor_numerico_edad__isnull=False,
        valor_numerico_estado_civil__isnull=False,
        valor_numerico_empleo__isnull=False)
        
        suma_total = 0
        
        
        for usuario in usuarios:
            suma_total += (usuario.valor_numerico_edad or 0) + (usuario.valor_numerico_estado_civil or 0) + (usuario.valor_numerico_empleo or 0)
            # suma_total += usuario.valor_numerico_edad + usuario.valor_numerico_estado_civil + usuario.valor_numerico_empleo
        
        context['cliente'] =usuarios
        context["suma_total"] = suma_total
        return context
    
    
class ViewRegistroCreditos(ListView):
    template_name = "calificaciones/registro-creditos.html"
    context_object_name = 'registros'
        
    def get_queryset(self):
        
        #registro_usuarios = User.objects.filter(solicitud=True)
        registro_usuarios = RegistroCreditos.objects.filter(cliente__solicitud=True)
        
        return registro_usuarios
    
class ViewCreditosStatusEstatico(ListView):
    template_name = 'calificaciones/creditos-estatus-estatico.html'
    context_object_name ='estatus'
    
    def get_queryset(self):
        
        usuarios_con_solicitud_true = User.objects.filter(solicitud=True)
        estatus_usuarios = SimuladorPrueba.objects.filter(usuario_user__in=usuarios_con_solicitud_true)
        
        simuladores_data = []
        
        for simulador in estatus_usuarios:
            usuario = simulador.usuario_user
        
            numero_contrato = simulador.identificador_unico
            nombre_usuario = usuario.first_name + usuario.last_name
            fecha_desembolso = usuario.fecha_solicitud
            monto_total_calculado = simulador.nombre_prestamo.monto * Decimal(simulador.nombre_prestamo.interes_moratorio)
            desembolso = simulador.nombre_prestamo.monto - (simulador.nombre_prestamo.monto * 0.05)
            pago_men = simulador.nombre_prestamo.pago_mensual
            tiempo = simulador.nombre_prestamo.plazo
            monto_pagado_hasta_hoy = simulador.nombre_prestamo.pago_mensual * 4
            saldo_pendiente = monto_total_calculado - monto_pagado_hasta_hoy
            monto_morosidad_calculo = (pago_men * Decimal(1.2)) * 3
            saldo_mas_morosidad_return = saldo_pendiente + monto_morosidad_calculo

            fecha_proxima = simulador.usuario_user.fecha_proximo_viernes.replace(tzinfo=timezone.utc) if simulador.usuario_user.fecha_proximo_viernes else None
            registros_previos = SimuladorPrueba.objects.filter(usuario_user=usuario).exclude(pk=simulador.pk)

            if registros_previos.exists():
                tipo = 'Renovado'
            else:
                tipo = 'Nuevo'

            if fecha_proxima:
                estatus = 'Atraso' if timezone.now() > fecha_proxima else 'Al corriente'
            else:
                estatus = 'Fecha próxima no disponible'

            simulador_data = {
                'numero_contrato': numero_contrato,
                'nombre_usuario': nombre_usuario,
                'fecha_desembolso': fecha_desembolso,
                'monto_total_calculado': monto_total_calculado,
                'desembolso': desembolso,
                'pago_mensual': pago_men,
                'tiempo': tiempo,
                'monto_pagado_hasta_hoy': monto_pagado_hasta_hoy,
                'saldo_pendiente': saldo_pendiente,
                'monto_morosidad': monto_morosidad_calculo,
                'saldo_mas_morosidad': saldo_mas_morosidad_return,
                'tipo': tipo,
                'estatus': estatus,
                
            }

            simuladores_data.append(simulador_data)
        
        return simuladores_data
    
# def calcular_corrida_financiera(self, pago_mensual, plazo, fecha_solicitud, monto_pagado = None, frecuencia_pago='semanal'):
    #     detalles_pago = []        
    #     fecha_actual = fecha_solicitud
        
        
        
    #     if fecha_solicitud is None:
    #         fecha_solicitud = datetime.now().date()  # Asigna la fecha actual si no hay fecha de solicitud
            
    #     for numero_pago in range(1, plazo + 1):
            
    #         if frecuencia_pago == 'semanal':
    #             fecha_pago_estimada = fecha_solicitud + timedelta(weeks=numero_pago)
    #         elif frecuencia_pago == 'mensual':
    #             fecha_pago_estimada = fecha_solicitud + timedelta(days=30 * numero_pago) 
            
            
    #         diferencia = fecha_pago_estimada - fecha_solicitud
            
    #         detalle_pago = {
    #             'numero_pago': numero_pago,
    #             'fecha_pago': fecha_solicitud,
    #             'pago_mensual': pago_mensual
    #         }
    #         # Si es el primer pago y se proporciona el monto pagado, establecerlo
    #         if diferencia.days >= 0:
    #             detalle_pago = {
    #                 'numero_pago': numero_pago,
    #                 'fecha_pago': fecha_pago_estimada,
    #                 'pago_mensual': pago_mensual,
    #                 'diferencia_pago': diferencia.days,
    #                 'monto_pagado': 0,  # Inicialmente, no se ha realizado ningún pago
    #                 'estado_pago': pago_mensual  # Inicialmente, el estado del pago es el monto completo
    #             }
                
    #             detalles_pago.append(detalle_pago)


    #     return detalles_pago
        
    
    
    ### el estable bien ######
    # def calcular_corrida_financiera(self, pago_mensual, plazo, fecha_solicitud, monto_pagado = None, frecuencia_pago='semanal'):
    #     detalles_pago = []        
    #     fecha_actual = fecha_solicitud
        
    #     if fecha_actual is None:
    #         fecha_actual = timezone.now().date()  # Asigna la fecha actual si no hay fecha de solicitud
    #     for numero_pago in range(1, plazo + 1):
    #         detalle_pago = {
    #             'numero_pago': numero_pago,
    #             'fecha_pago': fecha_actual,
    #             'pago_mensual': pago_mensual
    #         }
    #         # Si es el primer pago y se proporciona el monto pagado, establecerlo
    #         if numero_pago == 1 and monto_pagado is not None:
    #             diferencia =  pago_mensual - monto_pagado
    #             detalle_pago['monto_pagado'] = monto_pagado
    #             detalle_pago['diferencia_pago'] = diferencia
    #             if diferencia == 0 or monto_pagado == 0:
    #                 detalle_pago['estado_pago'] = 0
    #             else:
    #                 detalle_pago['estado_pago'] = diferencia
    #         detalles_pago.append(detalle_pago)
    #         # Actualizar la fecha para el próximo pago según la frecuencia de pago
    #         if frecuencia_pago == 'semanal':
    #             fecha_actual += timedelta(days=7)
    #         elif frecuencia_pago == 'mensual':
    #             fecha_actual += timedelta(days=30)  # Suponiendo meses de 30 días para simplificar

    #     return detalles_pago
    
    # def calcular_corrida_financiera(self, pago_mensual, plazo, fecha_solicitud, monto_pagado = None, frecuencia_pago='semanal'):
    #     detalles_pago = []
        
    #     fecha_actual = fecha_solicitud
    #     if fecha_actual is None:
    #         fecha_actual = timezone.now().date()  # Asigna la fecha actual si no hay fecha de solicitud
    #     for numero_pago in range(1, plazo + 1):
    #         detalle_pago = {
    #             'numero_pago': numero_pago,
    #             'fecha_pago': fecha_actual,
    #             'pago_mensual': pago_mensual
    #         }
    #         # Si es el primer pago y se proporciona el monto pagado, establecerlo
    #         if numero_pago == 1 and monto_pagado is not None:
    #             diferencia =  pago_mensual - monto_pagado
    #             detalle_pago['monto_pagado'] = monto_pagado
    #             detalle_pago['diferencia_pago'] = diferencia
    #             if diferencia == 0 or monto_pagado == 0:
    #                 detalle_pago['estado_pago'] = 0
    #             else:
    #                 detalle_pago['estado_pago'] = diferencia
    #         detalles_pago.append(detalle_pago)
    #         # Actualizar la fecha para el próximo pago según la frecuencia de pago
    #         if frecuencia_pago == 'semanal':
    #             fecha_actual += timedelta(days=7)
    #         elif frecuencia_pago == 'mensual':
    #             fecha_actual += timedelta(days=30)  # Suponiendo meses de 30 días para simplificar

    #     return detalles_pago


    
class ViewCreditosStatus(ListView):
    template_name = "calificaciones/creditos-estatus.html"
    context_object_name = 'estatus'
    
    def calcular_corrida_financiera(self, pago_mensual, plazo, fecha_solicitud, monto_pagado = None, frecuencia_pago='semanal'):
        detalles_pago = []        
        fecha_actual = fecha_solicitud
        # index_pago_registrado = 0
        monto_restante = pago_mensual * plazo
        
        numero_pago = 1
        
        
        if fecha_actual is None:
            fecha_actual = timezone.now().date()  # Asigna la fecha actual si no hay fecha de solicitud
            
        # for numero_pago in range(1, plazo + 1):
            detalle_pago = {
                'numero_pago': numero_pago,
                'fecha_pago': fecha_actual,
                'pago_mensual': pago_mensual
            }
            # # Si es el primer pago y se proporciona el monto pagado, establecerlo
            #numero_pago == numero_pago and
            if  monto_pagado is not None:
            #if monto_pagado is not None and index_pago_registrado < numero_pago:
                #index_pago_registrado += 1
                                
                monto_a_pagar  = min(monto_pagado,monto_restante)
                detalle_pago['monto_pagado'] = monto_a_pagar 
                monto_restante -= monto_a_pagar
                
                diferencia =  pago_mensual - monto_a_pagar
                
                detalle_pago['diferencia_pago'] = diferencia
                
                if diferencia == 0 or monto_a_pagar  == 0:
                    detalle_pago['estado_pago'] = 0
                else:
                    detalle_pago['estado_pago'] = diferencia
                
                if diferencia < 0 :
                    numero_pago += 1
                    monto_pagado = diferencia * -1
                    self.calcular_corrida_financiera(pago_mensual, plazo, fecha_solicitud, monto_pagado, frecuencia_pago='semanal')
                    
                    
                
                 
                     
                #index_pago_registrado += 1
                    
            detalles_pago.append(detalle_pago)
            # Actualizar la fecha para el próximo pago según la frecuencia de pago
            if frecuencia_pago == 'semanal':
                fecha_actual += timedelta(days=7)
            elif frecuencia_pago == 'mensual':
                fecha_actual += timedelta(days=30)  # Suponiendo meses de 30 días para simplificar

        return detalles_pago
    
    # def calcular_corrida_financiera(self, pago_mensual, plazo, fecha_solicitud, monto_pagado = None,frecuencia_pago='semanal',numero_pago=1):
    #     detalles_pago = []
        
    #     fecha_actual = fecha_solicitud
    #     if fecha_actual is None:
    #         fecha_actual = timezone.now().date()  # Asigna la fecha actual si no hay fecha de solicitud
    #     for pago in range(1, plazo + 1):
    #         detalle_pago = {
    #             'numero_pago': pago,
    #             'fecha_pago': fecha_actual,
    #             'pago_mensual': pago_mensual
    #         }
    #         # Si es el primer pago y se proporciona el monto pagado, establecerlo
    #         if pago == numero_pago  and monto_pagado is not None:
                
    #             detalle_pago['monto_pagado'] = monto_pagado
    #             diferencia =  pago_mensual - monto_pagado
    #             detalle_pago['diferencia_pago'] = diferencia
    #             detalle_pago['estado_pago'] = 0 if diferencia == 0 or monto_pagado == 0 else diferencia
    #             # if diferencia == 0 or monto_pagado == 0:
    #             #     detalle_pago['estado_pago'] = 0
    #             # else:
    #             #     detalle_pago['estado_pago'] = diferencia
    #         detalles_pago.append(detalle_pago)
    #         # Actualizar la fecha para el próximo pago según la frecuencia de pago
    #         if frecuencia_pago == 'semanal':
    #             fecha_actual += timedelta(days=7)
    #         elif frecuencia_pago == 'mensual':
    #             fecha_actual += timedelta(days=30)  # Suponiendo meses de 30 días para simplificar

    #     return detalles_pago
    
    def get_queryset(self):
        estatus_usuarios = SimuladorPrueba.objects.all()
        #usuarios_con_solicitud_true = User.objects.filter(solicitud=True)
        #estatus_usuarios = SimuladorPrueba.objects.filter(usuario_user__in=usuarios_con_solicitud_true)

        simuladores_data = []
        
        #monto_pagado_hasta_hoy = 0
        
        for simulador in estatus_usuarios:
            usuario = simulador.usuario_user
            
            # ultimo_pago_registrado = RegistroPagosModel.objects.filter(simulador=simulador).order_by('-numero_pago').first()
            # numero_pago = ultimo_pago_registrado.numero_pago if ultimo_pago_registrado else 0

            
            monto_pagado = RegistroPagosModel.objects.filter(simulador=simulador).aggregate(Sum('monto_pagado'))['monto_pagado__sum']
            
            monto_pagado = monto_pagado or 0
            
            corrida_financiera = self.calcular_corrida_financiera(
                simulador.nombre_prestamo.pago_mensual,
                simulador.nombre_prestamo.plazo,
                usuario.fecha_solicitud,
                monto_pagado,
                # frecuencia_pago='semanal',
                # numero_pago=numero_pago
                
            )
            
            

            numero_contrato = simulador.identificador_unico
            nombre_usuario = usuario.first_name + usuario.last_name
            fecha_desembolso = usuario.fecha_solicitud
            monto_total_calculado = simulador.nombre_prestamo.monto * Decimal(simulador.nombre_prestamo.interes_moratorio)
            desembolso = simulador.nombre_prestamo.monto - (simulador.nombre_prestamo.monto * 0.05)
            pago_men = simulador.nombre_prestamo.pago_mensual
            tiempo = simulador.nombre_prestamo.plazo
            monto_pagado_hasta_hoy = simulador.nombre_prestamo.pago_mensual * 4
            saldo_pendiente = monto_total_calculado - monto_pagado_hasta_hoy
            monto_morosidad_calculo = (pago_men * Decimal(1.2)) * 3
            saldo_mas_morosidad_return = saldo_pendiente + monto_morosidad_calculo

            fecha_proxima = simulador.usuario_user.fecha_proximo_viernes.replace(tzinfo=timezone.utc) if simulador.usuario_user.fecha_proximo_viernes else None
            registros_previos = SimuladorPrueba.objects.filter(usuario_user=usuario).exclude(pk=simulador.pk)

            if registros_previos.exists():
                tipo = 'Renovado'
            else:
                tipo = 'Nuevo'

            if fecha_proxima:
                estatus = 'Atraso' if timezone.now() > fecha_proxima else 'Al corriente'
            else:
                estatus = 'Fecha próxima no disponible'

            simulador_data = {
                'numero_contrato': numero_contrato,
                'nombre_usuario': nombre_usuario,
                'fecha_desembolso': fecha_desembolso,
                'monto_total_calculado': monto_total_calculado,
                'desembolso': desembolso,
                'pago_mensual': pago_men,
                'tiempo': tiempo,
                'monto_pagado_hasta_hoy': monto_pagado_hasta_hoy,
                'saldo_pendiente': saldo_pendiente,
                'monto_morosidad': monto_morosidad_calculo,
                'saldo_mas_morosidad': saldo_mas_morosidad_return,
                'tipo': tipo,
                'estatus': estatus,
                'corrida_financiera': corrida_financiera,
            }

            simuladores_data.append(simulador_data)

        return simuladores_data
    
    def post(self, request, *args, **kwargs):
        form = RegistroPagosForm(request.POST, request.FILES)
        if form.is_valid():
            # Obtener el simulador seleccionado del formulario
            simulador_id = request.POST.get('simulador')
            simulador = SimuladorPrueba.objects.get(id=simulador_id)
            
            # Guardar el formulario
            registro_pago = form.save(commit=False)

            # Asignar el simulador al registro de pago
            registro_pago.simulador = simulador
            registro_pago.save()

            # Obtener el monto del pago registrado
            monto_pagado = registro_pago.monto_pagado
            #numero_pago = registro_pago.numero_pago

            # Obtener la corrida financiera del simulador
            corrida_financiera = self.calcular_corrida_financiera(
                simulador.nombre_prestamo.pago_mensual,
                simulador.nombre_prestamo.plazo,
                simulador.usuario_user.fecha_solicitud
            )
            
            for pago in corrida_financiera:
                if pago['numero_pago'] == monto_pagado:
                    # Actualizar el monto pagado del pago correspondiente
                    pago['monto_pagado'] = registro_pago.monto_pagado
                    pago['estado_pago'] = pago['pago_mensual'] - registro_pago.monto_pagado
                    break

            # # Iterar sobre los pagos en la corrida financiera
            # for pago in corrida_financiera:
            #     # Calcular la diferencia entre el monto pagado y el monto del pago actual
            #     diferencia = monto_pagado - pago['pago_mensual']
            #     if diferencia >= 0:
            #         # Restar la diferencia del monto del pago actual
            #         pago['pago_mensual'] -= diferencia
            #         monto_pagado -= diferencia
            #     else:
            #         break  # Detener el bucle si ya no hay diferencia por restar
            
            # for pago in corrida_financiera:
            #     # Calcular la diferencia entre el monto pagado y el monto del pago actual
            #     diferencia = monto_pagado - pago['pago_mensual']
            #     if diferencia >= 0:
            #         # Restar la diferencia del monto del pago actual
            #         pago['pago_mensual'] -= diferencia
            #         monto_pagado -= diferencia
            #     else:
            #         # Establecer el monto pagado para el pago actual
            #         pago['pago_mensual'] = monto_pagado
            #         monto_pagado = 0  # La diferencia llegó a cero
                    
            #     # Si la diferencia llega a cero, asignar el pago adicional al siguiente pago
            #     if monto_pagado == 0:
            #         # Obtener el índice del pago actual en la lista
            #         indice_pago_actual = corrida_financiera.index(pago)
                    
            #         # Avanzar al siguiente pago en la lista
            #         if indice_pago_actual + 1 < len(corrida_financiera):
            #             siguiente_pago = corrida_financiera[indice_pago_actual + 1]
                        
            #             # Asignar el monto pagado al siguiente pago y actualizar el monto pagado restante
            #             siguiente_pago['pago_mensual'] -= monto_pagado
            #             monto_pagado = 0  # Reiniciar el monto pagado para el siguiente ciclo
                    
            #         break  # Detener el bucle si ya no hay diferencia por restar

            # Guardar la corrida financiera actualizada en el simulador
            simulador.corrida_financiera = corrida_financiera
            simulador.save()

            return redirect('calificaciones_app:estatus_credito')  # Redirigir a la misma página
        else:
            # Manejar caso de formulario no válido
            return render(request, 'calificaciones/creditos-estatus.html', {'form': form})
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['registro_pagos_form'] = RegistroPagosForm()

        return context
    
# def post(self, request, *args, **kwargs):
    #     form = RegistroPagosForm(request.POST, request.FILES)
    #     if form.is_valid():
    #         simulador_id = request.POST.get('simulador')
    #         simulador = SimuladorPrueba.objects.get(id=simulador_id)
    #         registro_pago = form.save(commit=False)
    #         registro_pago.simulador = simulador
    #         registro_pago.save()
    #         monto_pagado = registro_pago.monto_pagado

    #         corrida_financiera = self.calcular_corrida_financiera(
    #             simulador.nombre_prestamo.pago_mensual,
    #             simulador.nombre_prestamo.plazo,
    #             simulador.usuario_user.fecha_solicitud
    #         )

    #         for pago in corrida_financiera:
    #             if pago['fecha_pago'] > simulador.usuario_user.fecha_solicitud:
    #                 break
    #             diferencia = monto_pagado - pago['pago_mensual']
    #             if diferencia >= 0:
    #                 pago['monto_pagado'] += pago['pago_mensual']
    #                 monto_pagado -= pago['pago_mensual']

    #         simulador.corrida_financiera = corrida_financiera
    #         simulador.save()

    #         return redirect('calificaciones_app:estatus_credito')
    #     else:
    #         return render(request, 'calificaciones/creditos-estatus.html', {'form': form})
    
    # def post(self, request, *args, **kwargs):
    #     form = RegistroPagosForm(request.POST, request.FILES)
    #     if form.is_valid():
    #         # Obtener el simulador seleccionado del formulario
    #         simulador_id = request.POST.get('simulador')
    #         simulador = SimuladorPrueba.objects.get(id=simulador_id)
            
    #         # Guardar el formulario
    #         registro_pago = form.save(commit=False)

    #         # Asignar el simulador al registro de pago
    #         registro_pago.simulador = simulador
    #         registro_pago.save()

    #         # Obtener el monto del pago registrado
    #         monto_pagado = registro_pago.monto_pagado

    #         # Obtener la corrida financiera del simulador
    #         corrida_financiera = self.calcular_corrida_financiera(
    #             simulador.nombre_prestamo.pago_mensual,
    #             simulador.nombre_prestamo.plazo,
    #             simulador.usuario_user.fecha_solicitud
    #         )

    #         # Iterar sobre los pagos en la corrida financiera
    #         for pago in corrida_financiera:
    #             # Calcular la diferencia entre el monto pagado y el monto del pago actual
    #             diferencia = monto_pagado - pago['pago_mensual']
    #             if diferencia >= 0:
    #                 # Restar la diferencia del monto del pago actual
    #                 pago['pago_mensual'] -= diferencia
    #                 monto_pagado -= diferencia
    #             else:
    #                 #Establecer el monto pagado para el pago actual
    #                 pago['pago_mensual'] = monto_pagado
    #                 monto_pagado = 0  # La diferencia llegó a cero
                
    #             #Si la diferencia llega a cero, asignar el pago adicional al siguiente pago
    #             if monto_pagado == 0:
    #                 # Obtener el índice del pago actual en la lista
    #                 indice_pago_actual = corrida_financiera.index(pago)
                    
    #                 # Avanzar al siguiente pago en la lista
    #                 if indice_pago_actual + 1 < len(corrida_financiera):
    #                     siguiente_pago = corrida_financiera[indice_pago_actual + 1]
                        
    #                     # Asignar el monto pagado al siguiente pago y actualizar el monto pagado restante
    #                     siguiente_pago['pago_mensual'] -= monto_pagado
    #                     monto_pagado = 0  # Reiniciar el monto pagado para el siguiente ciclo
                    
    #                 break  # Detener el bucle si ya no hay diferencia por restar
            
    #         # for pago in corrida_financiera:
    #         #     # Calcular la diferencia entre el monto pagado y el monto del pago actual
    #         #     diferencia = monto_pagado - pago['pago_mensual']
    #         #     if diferencia >= 0:
    #         #         # Restar la diferencia del monto del pago actual
    #         #         pago['pago_mensual'] -= diferencia
    #         #         monto_pagado -= diferencia
    #         #     else:
    #         #         # Establecer el monto pagado para el pago actual
    #         #         pago['pago_mensual'] = monto_pagado
    #         #         monto_pagado = 0  # La diferencia llegó a cero
                    
    #         #     # Si la diferencia llega a cero, asignar el pago adicional al siguiente pago
    #         #     if monto_pagado == 0:
    #         #         # Obtener el índice del pago actual en la lista
    #         #         indice_pago_actual = corrida_financiera.index(pago)
                    
    #         #         # Avanzar al siguiente pago en la lista
    #         #         if indice_pago_actual + 1 < len(corrida_financiera):
    #         #             siguiente_pago = corrida_financiera[indice_pago_actual + 1]
                        
    #         #             # Asignar el monto pagado al siguiente pago y actualizar el monto pagado restante
    #         #             siguiente_pago['pago_mensual'] -= monto_pagado
    #         #             monto_pagado = 0  # Reiniciar el monto pagado para el siguiente ciclo
                    
    #         #         break  # Detener el bucle si ya no hay diferencia por restar

    #         # Guardar la corrida financiera actualizada en el simulador
    #         simulador.corrida_financiera = corrida_financiera
    #         simulador.save()

    #         return redirect('calificaciones_app:estatus_credito')  # Redirigir a la misma página
    #     else:
    #         # Manejar caso de formulario no válido
    #         return render(request, 'calificaciones/creditos-estatus.html', {'form': form})
    
    # el mas estable #####
    # def post(self, request, *args, **kwargs):
    #     form = RegistroPagosForm(request.POST, request.FILES)
    #     if form.is_valid():
    #         # Obtener el simulador seleccionado del formulario
    #         simulador_id = request.POST.get('simulador')
    #         simulador = SimuladorPrueba.objects.get(id=simulador_id)
            
    #         # Guardar el formulario
    #         registro_pago = form.save(commit=False)

    #         # Asignar el simulador al registro de pago
    #         registro_pago.simulador = simulador
    #         registro_pago.save()

    #         # Obtener el monto del pago registrado
    #         monto_pagado = registro_pago.monto_pagado

    #         # Obtener la corrida financiera del simulador
    #         corrida_financiera = self.calcular_corrida_financiera(
    #             simulador.nombre_prestamo.pago_mensual,
    #             simulador.nombre_prestamo.plazo,
    #             simulador.usuario_user.fecha_solicitud
    #         )

    #         # Iterar sobre los pagos en la corrida financiera
    #         for pago in corrida_financiera:
    #             # Calcular la diferencia entre el monto pagado y el monto del pago actual
    #             diferencia = monto_pagado - pago['pago_mensual']
    #             if diferencia >= 0:
    #                 # Restar la diferencia del monto del pago actual
    #                 pago['pago_mensual'] -= diferencia
    #                 monto_pagado -= diferencia
    #             else:
    #                 break  # Detener el bucle si ya no hay diferencia por restar
            
    #         # for pago in corrida_financiera:
    #         #     # Calcular la diferencia entre el monto pagado y el monto del pago actual
    #         #     diferencia = monto_pagado - pago['pago_mensual']
    #         #     if diferencia >= 0:
    #         #         # Restar la diferencia del monto del pago actual
    #         #         pago['pago_mensual'] -= diferencia
    #         #         monto_pagado -= diferencia
    #         #     else:
    #         #         # Establecer el monto pagado para el pago actual
    #         #         pago['pago_mensual'] = monto_pagado
    #         #         monto_pagado = 0  # La diferencia llegó a cero
                    
    #         #     # Si la diferencia llega a cero, asignar el pago adicional al siguiente pago
    #         #     if monto_pagado == 0:
    #         #         # Obtener el índice del pago actual en la lista
    #         #         indice_pago_actual = corrida_financiera.index(pago)
                    
    #         #         # Avanzar al siguiente pago en la lista
    #         #         if indice_pago_actual + 1 < len(corrida_financiera):
    #         #             siguiente_pago = corrida_financiera[indice_pago_actual + 1]
                        
    #         #             # Asignar el monto pagado al siguiente pago y actualizar el monto pagado restante
    #         #             siguiente_pago['pago_mensual'] -= monto_pagado
    #         #             monto_pagado = 0  # Reiniciar el monto pagado para el siguiente ciclo
                    
    #         #         break  # Detener el bucle si ya no hay diferencia por restar

    #         # Guardar la corrida financiera actualizada en el simulador
    #         simulador.corrida_financiera = corrida_financiera
    #         simulador.save()

    #         return redirect('calificaciones_app:estatus_credito')  # Redirigir a la misma página
    #     else:
    #         # Manejar caso de formulario no válido
    #         return render(request, 'calificaciones/creditos-estatus.html', {'form': form})

    # def post(self, request, *args, **kwargs):
    #     form = RegistroPagosForm(request.POST, request.FILES)
    #     if form.is_valid():
    #         # Guardar el formulario
    #         registro_pago = form.save(commit=False)

    #         # Obtener el simulador seleccionado del formulario
    #         simulador_id = request.POST.get('simulador')
    #         simulador = SimuladorPrueba.objects.get(id=simulador_id)

    #         # Asignar el simulador al registro de pago
    #         registro_pago.simulador = simulador
    #         registro_pago.save()

    #         # Obtener el monto del pago registrado
    #         monto_pagado = registro_pago.monto_pagado

    #         # Obtener la corrida financiera del simulador
    #         corrida_financiera = self.calcular_corrida_financiera(
    #             simulador.nombre_prestamo.pago_mensual,
    #             simulador.nombre_prestamo.plazo,
    #             simulador.usuario_user.fecha_solicitud
                
    #         )

    #         # Iterar sobre los pagos en la corrida financiera
    #         for pago in corrida_financiera:
    #             # Calcular la diferencia entre el monto pagado y el monto del pago actual
    #             diferencia = monto_pagado - pago['pago_mensual']
    #             if diferencia >= 0:
    #                 # Restar la diferencia del monto del pago actual
    #                 pago['pago_mensual'] -= diferencia
    #                 monto_pagado -= diferencia
    #             else:
    #                 break  # Detener el bucle si ya no hay diferencia por restar

    #         # Guardar la corrida financiera actualizada en el simulador
    #         simulador.corrida_financiera = corrida_financiera
    #         simulador.save()

    #         return redirect('calificaciones_app:estatus_credito')  # Redirigir a la misma página
    #     else:
    #         # Manejar caso de formulario no válido
    #         return render(request, 'calificaciones/creditos-estatus.html', {'form': form})


    
    
#el mas estable
    
# class ViewCreditosStatus(ListView):
#     template_name = "calificaciones/creditos-estatus.html"
#     context_object_name = 'estatus'
  
#     def calcular_corrida_financiera(self, pago_mensual, plazo, fecha_solicitud, frecuencia_pago='semanal'):
#         detalles_pago = []
#         fecha_actual = fecha_solicitud
#         if fecha_actual is None:
#             fecha_actual = timezone.now().date()  # Asigna la fecha actual si no hay fecha de solicitud
#         for numero_pago in range(1, plazo + 1):
#             detalle_pago = {
#                 'numero_pago': numero_pago,
#                 'fecha_pago': fecha_actual,
#                 'pago_mensual':pago_mensual
#             }
#             detalles_pago.append(detalle_pago)
#             # Actualizar la fecha para el próximo pago según la frecuencia de pago
#             if frecuencia_pago == 'semanal':
#                 fecha_actual += timedelta(days=7)
#             elif frecuencia_pago == 'mensual':
#                 fecha_actual += timedelta(days=30)  # Suponiendo meses de 30 días para simplificar
            
#         return detalles_pago
    
#     def get_queryset(self):
#         usuarios_con_solicitud_true = User.objects.filter(solicitud=True)
#         estatus_usuarios = SimuladorPrueba.objects.filter(usuario_user__in=usuarios_con_solicitud_true)
        
#         simuladores_data = []
        
#         for simulador in estatus_usuarios:
#             usuario = simulador.usuario_user
#             corrida_financiera = self.calcular_corrida_financiera(
#                 simulador.nombre_prestamo.pago_mensual,
#                 simulador.nombre_prestamo.plazo,
#                 usuario.fecha_solicitud
#             )
            
#             numero_contrato = simulador.identificador_unico
#             nombre_usuario = usuario.first_name + usuario.last_name
#             fecha_desembolso =usuario.fecha_solicitud
#             monto_total_calculado = simulador.nombre_prestamo.monto * Decimal(simulador.nombre_prestamo.interes_moratorio)
#             desembolso = simulador.nombre_prestamo.monto - (simulador.nombre_prestamo.monto * 0.05)
#             pago_men = simulador.nombre_prestamo.pago_mensual
#             tiempo = simulador.nombre_prestamo.plazo
#             monto_pagado_hasta_hoy = simulador.nombre_prestamo.pago_mensual * 4
#             saldo_pendiente = monto_total_calculado - monto_pagado_hasta_hoy
#             monto_morosidad_calculo = (pago_men * Decimal(1.2)) * 3
#             saldo_mas_morosidad_return = saldo_pendiente + monto_morosidad_calculo
            
#             fecha_proxima = simulador.usuario_user.fecha_proximo_viernes.replace(tzinfo=timezone.utc) if simulador.usuario_user.fecha_proximo_viernes else None
#             registros_previos = SimuladorPrueba.objects.filter(usuario_user=usuario).exclude(pk=simulador.pk)
            
#             if registros_previos.exists():
#                 tipo = 'Renovado'
#             else:
#                 tipo = 'Nuevo'
            
#             if fecha_proxima:
#                 estatus = 'Atraso' if timezone.now() > fecha_proxima else 'Al corriente'
#             else:
#                 estatus = 'Fecha próxima no disponible'
            
#             simulador_data = {
#                 'numero_contrato': numero_contrato,
#                 'nombre_usuario' :nombre_usuario,
#                 'fecha_desembolso': fecha_desembolso,
#                 'monto_total_calculado': monto_total_calculado,
#                 'desembolso': desembolso,
#                 'pago_mensual': pago_men,
#                 'tiempo': tiempo,
#                 'monto_pagado_hasta_hoy':monto_pagado_hasta_hoy,
#                 'saldo_pendiente': saldo_pendiente,
#                 'monto_morosidad': monto_morosidad_calculo,
#                 'saldo_mas_morosidad': saldo_mas_morosidad_return,
#                 'tipo': tipo,
#                 'estatus': estatus,
#                 'corrida_financiera': corrida_financiera,
#             }
            
#             simuladores_data.append(simulador_data)
        
#         return simuladores_data
       
    
#     def post(self, request, *args, **kwargs):
#         form = RegistroPagosForm(request.POST, request.FILES)
#         if form.is_valid():
          
#             form.save()
#             return redirect('calificaciones_app:estatus_credito')  # Redirigir a la misma página
#         else:
#             # Manejar caso de formulario no válido
#             return render(request, 'calificaciones/creditos-estatus.html', {'form': form})
    
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['registro_pagos_form'] = RegistroPagosForm()
     
#         return context
#el mas estable
    
    # def post(self, request, *args, **kwargs):
    #     form = RegistroPagosForm(request.POST, request.FILES)
    #     if form.is_valid():
    #         # Guardar el registro del pago en la base de datos
    #         simulador = form.cleaned_data['simulador']
    #         monto_pagado = form.cleaned_data['monto_pagado']
    #         comprobante_pago = form.cleaned_data['comprobante_pago']
    #         form.save()
                        
    #         return redirect('calificaciones_app:estatus_credito')  # Redirigir a la página de estatus de créditos
    #     else:
    #         # Manejar caso de formulario no válido
    #         # Por ejemplo, mostrar un mensaje de error o volver a renderizar el formulario con errores
    #         return render(request, 'calificaciones/creditos-estatus.html', {'form': form})
    
    
    
    # def get_queryset(self):
    #     #estatus_usuarios = EstatusCredito.objects.filter(cliente_estatus__solicitud=True)
    #     estatus_usuarios = SimuladorPrueba.objects.all()
    #     #usuarios_con_solicitud_true = User.objects.filter(solicitud=True)
    #     #estatus_usuarios = SimuladorPrueba.objects.filter(usuario_user__in=usuarios_con_solicitud_true)
    #     print("Número de registros obtenidos:", len(estatus_usuarios))
    #     fecha_hoy = timezone.now()
    #     corridas_financieras = {}
        
        
    #     for simulador in estatus_usuarios:
    #         usuario = simulador.usuario_user
    #         corrida_financiera = self.calcular_corrida_financiera(
    #             simulador.nombre_prestamo.pago_mensual,
    #             simulador.nombre_prestamo.plazo,
    #             usuario.fecha_solicitud
    #         )
            
    #         fecha_proxima = None
            
    #         # corrida_financiera = self.calcular_corrida_financiera(simulador.nombre_prestamo.pago_mensual, simulador.nombre_prestamo.plazo, usuario.fecha_solicitud)
            
    #         # corrida_financiera = self.calcular_corrida_financiera(simulador.nombre_prestamo.pago_mensual, simulador.nombre_prestamo.plazo,simulador.usuario_user,frecuencia_pago='semanal')
            
    #         # for detalle_pago in corrida_financiera:
    #         #     num_pago =  detalle_pago['numero_pago']
    #         #     registro_pago = SimuladorPrueba.objects.filter(identificador_unico=simulador).first()
                
    #         #     detalle_pago['documento'] = registro_pago.documento.url if registro_pago else None
                
    #         #     detalle_pago['numero_pago'] = num_pago
           
    #         #### aqui es donde se cren las formulas ####
            
            
    #         numero_contrato = simulador.identificador_unico
    #         monto_total_calculado = simulador.nombre_prestamo.monto * Decimal(simulador.nombre_prestamo.interes_moratorio)
    #         desembolso = simulador.nombre_prestamo.monto - (simulador.nombre_prestamo.monto * 0.05)
    #         pago_men = simulador.nombre_prestamo.pago_mensual
    #         tiempo = simulador.nombre_prestamo.plazo
    #         monto_pagado_hasta_hoy = simulador.nombre_prestamo.pago_mensual * 4
    #         saldo_pendiente= monto_total_calculado - monto_pagado_hasta_hoy
    #         monto_morosidad_calculo = (pago_men * Decimal(1.2)) * 3 # 1.2 es el interes moratio
    #         saldo_mas_morosidad_return = saldo_pendiente + monto_morosidad_calculo
    #         if simulador.usuario_user.fecha_proximo_viernes:
    #             fecha_proxima = simulador.usuario_user.fecha_proximo_viernes.replace(tzinfo=timezone.utc)
    #         registros_previos = SimuladorPrueba.objects.filter(usuario_user=usuario).exclude(pk=simulador.pk)
            
            
    #         #### aqui es donde se asigna el campo a mostrar ####
    #         if registros_previos.exists():
    #                 simulador.tipo = 'Renovado'
    #         else:
    #             simulador.tipo = 'Nuevo'
    #         if fecha_proxima is not None:
                
    #             if fecha_hoy > fecha_proxima:
    #                 simulador.estatus = 'Atraso'
    #             else:
    #                 simulador.estatus = 'Al corriente' 
    #         else:
    #             # Manejar el caso donde fecha_proxima es None
    #             simulador.estatus = 'Fecha próxima no disponible'
                
    #         #simulador.corrida_financiera = corrida_financiera
            
    #         simulador.corrida_financiera = corrida_financiera
    #         simulador.monto_total_calculado = monto_total_calculado
    #         simulador.desembolso = desembolso
    #         simulador.monto_pago_men = pago_men
    #         simulador.numero_de_pago = tiempo            
    #         simulador.saldo_mas_morosidad = saldo_mas_morosidad_return
    #         simulador.monto_morosidad = monto_morosidad_calculo
    #         simulador.saldo = saldo_pendiente
    #         simulador.monto_pagado = monto_pagado_hasta_hoy
    #         simulador.numero_contrato = numero_contrato
                
    
    #     return  estatus_usuarios
    
    
    
    # def calcular_corrida_financiera(self, monto_pago_men, numero_de_pago,usuario_user,frecuencia_pago='semanal'):
    #     corrida_financiera = []
        
    #     #fecha_pago = cliente_estatus.fecha_solicitud + relativedelta(months=1)
    #     fecha_pago = usuario_user.fecha_solicitud
        
    #     if frecuencia_pago == 'semanal':
    #         intervalo = relativedelta(weeks=1)
    #     elif frecuencia_pago == 'quincenal':
    #         intervalo = relativedelta(weeks=1)
    #     else:
    #         intervalo = relativedelta(months=1)

    #     for i in range(numero_de_pago):
    #         # Calcular el monto a pagar y otros detalles
    #         monto_a_pagar = monto_pago_men
    #         # Puedes realizar otros cálculos según sea necesario

    #         # Agregar detalles al registro de la corrida financiera
    #         detalle_pago = {
    #             'numero_pago': i + 1,
    #             'fecha_pago': fecha_pago,
    #             'monto_a_pagar': monto_a_pagar,
    #             # Puedes agregar más detalles según sea necesario
    #         }

    #         corrida_financiera.append(detalle_pago)
            
    #         fecha_pago += intervalo

    #     return corrida_financiera
        
        
        """ 
        for registro_credito in estatus_usuarios:
            
            usuario = registro_credito.cliente_estatus.first()
            # corrida_financiera = self.calcular_corrida_financiera(registro_credito.monto_pago_men, registro_credito.numero_de_pago,registro_credito.cliente_estatus,frecuencia_pago='semanal')
            
            # for detalle_pago in corrida_financiera:
            #     num_pago =  detalle_pago['numero_pago']
            #     registro_pago = RegistroPagosModel.objects.filter(num_contrato=registro_credito,numero_pago=num_pago).first()
                
            #     detalle_pago['documento'] = registro_pago.documento.url if registro_pago else None
                
            #     detalle_pago['numero_pago'] = num_pago
            
            
            if usuario :
                monto_total_calculado = usuario.nombre_prestamo.monto * Decimal(usuario.nombre_prestamo.interes_moratorio)
                desembolso = usuario.nombre_prestamo.monto - (usuario.nombre_prestamo.monto * 0.05)
                pago_men = usuario.nombre_prestamo.pago_mensual
                tiempo = usuario.nombre_prestamo.plazo
                monto_pagado_hasta_hoy = usuario.nombre_prestamo.pago_mensual * 4
                saldo_pendiente= monto_total_calculado - monto_pagado_hasta_hoy
                monto_morosidad_calculo = (pago_men * Decimal(1.2)) * 3 # 1.2 es el interes moratio
                saldo_mas_morosidad_return = saldo_pendiente + monto_morosidad_calculo
                fecha_proxima = usuario.usuario_user.fecha_proximo_viernes.replace(tzinfo=timezone.utc)
                registros_previos = EstatusCredito.objects.filter(cliente_estatus=usuario).exclude(pk=registro_credito.pk)
                
                if registros_previos.exists():
                    registro_credito.tipo = 'Renovado'
                else:
                    registro_credito.tipo = 'Nuevo'
                
                if fecha_hoy > fecha_proxima:
                    registro_credito.estatus = 'Atraso'
                else:
                    registro_credito.estatus = 'Al corriente' 
                
                #registro_credito.corrida_financiera = corrida_financiera
                
                registro_credito.saldo_mas_morosidad = saldo_mas_morosidad_return
                registro_credito.monto_morosidad = monto_morosidad_calculo
                registro_credito.saldo = saldo_pendiente
                registro_credito.monto_pagado = monto_pagado_hasta_hoy
                registro_credito.numero_de_pago = tiempo
                registro_credito.monto_pago_men = pago_men
                registro_credito.desembolso = desembolso
                registro_credito.monto_total = monto_total_calculado
                registro_credito.save()
        """
        
    
    # def calcular_corrida_financiera(self, monto_pago_men, numero_de_pago,cliente_estatus,frecuencia_pago='semanal'):
    #     corrida_financiera = []
        
    #     #fecha_pago = cliente_estatus.fecha_solicitud + relativedelta(months=1)
    #     fecha_pago = cliente_estatus.fecha_solicitud
        
    #     if frecuencia_pago == 'semanal':
    #         intervalo = relativedelta(weeks=1)
    #     elif frecuencia_pago == 'quincenal':
    #         intervalo = relativedelta(weeks=1)
    #     else:
    #         intervalo = relativedelta(months=1)

    #     for i in range(numero_de_pago):
    #         # Calcular el monto a pagar y otros detalles
    #         monto_a_pagar = monto_pago_men
    #         # Puedes realizar otros cálculos según sea necesario

    #         # Agregar detalles al registro de la corrida financiera
    #         detalle_pago = {
    #             'numero_pago': i + 1,
    #             'fecha_pago': fecha_pago,
    #             'monto_a_pagar': monto_a_pagar,
    #             # Puedes agregar más detalles según sea necesario
    #         }

    #         corrida_financiera.append(detalle_pago)
            
    #         fecha_pago += intervalo

    #     return corrida_financiera


# def view_creditos_status(request):
#     template_name = "calificaciones/creditos-estatus.html"
#     context_object_name = 'estatus'
    
#     estatus_usuarios = EstatusCredito.objects.filter(cliente_estatus__solicitud=True)
    
#     for registro_credito in estatus_usuarios:
#         usuario = registro_credito.cliente_estatus
#         fecha_hoy = datetime.today()
        
        
#         if usuario:
#             monto_total_calculado = usuario.simulador.amount * Decimal(usuario.simulador.interest_moratorio)
#             desembolso = usuario.simulador.amount - (usuario.simulador.amount * 0.05)
#             pago_men = usuario.simulador.monthly_payment
#             tiempo = usuario.simulador.term
#             monto_pagado_hasta_hoy = usuario.simulador.monthly_payment * 4
#             saldo_pendiente= monto_total_calculado - monto_pagado_hasta_hoy
#             monto_morosidad_calculo = (pago_men * Decimal(1.2)) * 3
#             saldo_mas_morosidad_return = saldo_pendiente + monto_morosidad_calculo
#             fecha_proxima = usuario.fecha_proximo_viernes
            
            
#             if fecha_hoy >= fecha_proxima:
#                 registro_credito.estatus = 'Atraso'
#             else:
#                 registro_credito.estatus = 'Al corriente' 
            
#             registro_credito.saldo_mas_morosidad = saldo_mas_morosidad_return
#             registro_credito.monto_morosidad = monto_morosidad_calculo
#             registro_credito.saldo = saldo_pendiente
#             registro_credito.monto_pagado = monto_pagado_hasta_hoy
#             registro_credito.numero_de_pago = tiempo
#             registro_credito.monto_pago_men = pago_men
#             registro_credito.desembolso = desembolso
#             registro_credito.monto_total = monto_total_calculado
#             registro_credito.save()
    
#     context = {
#         'estatus': estatus_usuarios,
#     }
    
#     return render(request, template_name, context)


#class CorridaFinancieraListView(ListView):
#     model = SimuladorPrueba
#     template_name = 'calificaciones/creditos-estatus.html'

#     def get_queryset(self):
#         queryset = super().get_queryset()
#         # Filtrar simuladores por fecha de solicitud
#         queryset = queryset.filter(usuario_user__fecha_solicitud__lte=timezone.now())
#         return queryset

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         corrida_financiera = []
#         for simulador in context['object_list']:
#             # Calcular el monto total a pagar
#             monto_total = simulador.nombre_prestamo.pago_mensual
            
#             # Calcular la fecha de inicio y finalización de la corrida financiera
#             fecha_inicio = simulador.usuario_user.fecha_solicitud
#             fecha_final = fecha_inicio + timedelta(days=7)  # Corrida financiera de 7 días
            
#             # Calcular los pagos para cada 7 días
#             pagos = RegistroPagosModel.objects.filter(simulador=simulador,
#                                                        fecha_pago__range=(fecha_inicio, fecha_final))
#             monto_pagado = sum(pago.monto_pagado for pago in pagos)
#             monto_restante = monto_total - monto_pagado
            
#             # Agregar información a la lista de corrida financiera
#             corrida_financiera.append({
#                 'simulador': simulador,
#                 'fecha_inicio': fecha_inicio,
#                 'fecha_final': fecha_final,
#                 'monto_total': monto_total,
#                 'monto_pagado': monto_pagado,
#                 'monto_restante': monto_restante
#             })

#         context['corrida_financiera'] = corrida_financiera
#         return context


class CorridaFinancieraListView(ListView):
    template_name = "calificaciones/creditos-estatus.html"
    context_object_name = 'simuladores_con_pagos'

    def get_queryset(self):
        # Obtener todos los simuladores con sus respectivos registros de pago
        simuladores_con_pagos = []

        # Obtener todos los simuladores
        simuladores = SimuladorPrueba.objects.all()

        # Calcular la fecha de inicio y finalización de la corrida financiera
        #             fecha_inicio = simulador.usuario_user.fecha_solicitud
        #             fecha_final = fecha_inicio + timedelta(days=7)  # Corrida financiera de 7 días
        
        # Iterar sobre cada simulador y obtener sus registros de pago
        for simulador in simuladores:
            fecha_solicitud = simulador.usuario_user.fecha_solicitud
            
            
            if fecha_solicitud:
                
                fecha_actual = datetime.now().date()
                proxima_fecha_solicitud = fecha_solicitud + timedelta(days=7)
                # dias_pasados = (fecha_actual - fecha_solicitud).days
                # semanas_pasadas = dias_pasados // 7
                # proxima_fecha_solicitud = fecha_solicitud + timedelta(weeks=semanas_pasadas + 1)
            
            
            
                registros_pago = RegistroPagosModel.objects.filter(simulador=simulador).order_by('fecha_pago')

                # Calcular los montos a pagar, montos pagados y montos restantes
                monto_a_pagar = simulador.nombre_prestamo.pago_mensual
                monto_total_pagado = 0
                pagos = []
                plazo = simulador.nombre_prestamo.plazo

                for i, pago in enumerate(registros_pago, start=1):
                    
                    monto_total_pagado += pago.monto_pagado
                    monto_restante = monto_a_pagar * i - monto_total_pagado
                    pagos.append({
                        'numero_pago': i,
                        'fecha_pago': pago.fecha_pago,
                        'monto_a_pagar': monto_a_pagar,
                        'monto_pagado': pago.monto_pagado,
                        'monto_restante': monto_restante
                    })
                    
                if not registros_pago:
                    for i in range(1, plazo + 1):
                        proxima_fecha_solicitud = fecha_solicitud + timedelta(days=7)
                        
                        monto_restante = monto_a_pagar * i
                        pagos.append({
                            'numero_pago': i,
                            'fecha_pago': proxima_fecha_solicitud,
                            'monto_a_pagar': monto_a_pagar,
                            'monto_pagado': 0,
                            'monto_restante': monto_restante
                        })


                simuladores_con_pagos.append({'simulador': simulador, 'pagos': pagos})

        return simuladores_con_pagos


    
    
class RegistroPagos(CreateView):
    model = RegistroPagosModel
    template_name = 'calificaciones/registro-pagos.html'
    form_class =RegistroPagosForm
    success_url = reverse_lazy('calificaciones_app:registro_pagos')
    #context_object_name = 'registros_pagos'
    
    
    def form_valid(self, form):
        # Obtener el simulador asociado al registro de pago
        simulador = form.cleaned_data['simulador']
        # Obtener el último registro de pago para calcular el número de pago
        ultimo_pago = RegistroPagosModel.objects.filter(simulador=simulador).order_by('-fecha_pago').first()
        numero_pago = 1 if not ultimo_pago else ultimo_pago.numero_pago + 1
        # Calcular el monto restante
        monto_restante = simulador.nombre_prestamo.pago_mensual * numero_pago - form.cleaned_data['monto_pagado']
        # Asignar el número de pago y el monto restante al registro de pago
        form.instance.numero_pago = numero_pago
        form.instance.monto_restante = monto_restante
        return super().form_valid(form)
    
    
    ###### el original
    
    # def form_valid(self, form):
    #     # Asigna el usuario actual al campo "usuario" del formulario
    #     # form.instance.usuario = self.request.user

    #     # Realiza la solicitud AJAX para obtener los datos de EstatusCredito
    #     num_contrato_id = form.cleaned_data['num_contrato'].id
    #     estatus_credito = EstatusCredito.objects.get(pk=num_contrato_id)

    #     # Actualiza los campos del formulario con los datos obtenidos
    #     form.instance.monto_total_registro = estatus_credito.monto_pago_men
        
    #     form.instance.documento = form.cleaned_data['documento']
        
    #     form.save()
    #     # Otros campos que desees actualizar...

    #     return super().form_valid(form)    
 
    
def obtener_monto_total(request):
    if request.method == 'GET':
        num_contrato_id = request.GET.get('num_contrato_id')
        try:
            estatus_credito = SimuladorPrueba.objects.get(id=num_contrato_id)
            monto_total = estatus_credito.nombre_prestamo.pago_mensual
            usuario = estatus_credito.usuario_user.email
            return JsonResponse({'monto_total': monto_total,'usuario': usuario})
        except estatus_credito.DoesNotExist:
            return JsonResponse({'monto_total': None,'usuario': None})
        
# def obtener_monto_total(request):
#     if request.method == 'GET':
#         num_contrato_id = request.GET.get('num_contrato_id')
#         try:
#             estatus_credito = EstatusCredito.objects.get(id=num_contrato_id)
#             monto_total = estatus_credito.monto_pago_men
#             usuario = estatus_credito.cliente_estatus.email
#             return JsonResponse({'monto_total': monto_total,'usuario': usuario})
#         except estatus_credito.DoesNotExist:
#             return JsonResponse({'monto_total': None,'usuario': None})
    
    
#class GetEstatusCreditoDataView(View):
    # def get(self, request, num_contrato, *args, **kwargs):
    #     estatus_credito = get_object_or_404(EstatusCredito, numero_contrato_estatus=num_contrato)
    #     usuario = estatus_credito.cliente_estatus.username
    #     monto_total = estatus_credito.monto_total
    #     # data = {
    #     #     'usuario': estatus_credito.cliente_estatus.username,
    #     #     'monto_total': estatus_credito.monto_total,
    #     # }
    #     return JsonResponse({'usuario': usuario,'monto_total':monto_total})
    
    
# class GetNombreProductoView(View):
#     def get(self, request, prestamo_id, *args, **kwargs):
#         prestamo = get_object_or_404(Prestamo, id=prestamo_id)
#         nombre_producto = prestamo.nombre_producto
#         tipo_prestamo_nombre = prestamo.tipo_prestamo.tipo_credito if prestamo.tipo_prestamo else None
#         return JsonResponse({'nombre_producto': nombre_producto,'tipo_prestamo':tipo_prestamo_nombre})
    
    
    
    
         
        
    
    
    
    
    
    
