"""
Vistas para el sistema de calificacion con actividades y porcentajes.
Permiten que el profesor cree actividades por corte, califique estudiantes y
consulte la nota final calculada automaticamente.
"""

from decimal import Decimal, InvalidOperation

from django.contrib import messages
from django.db.models import Max
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from gestionUniversitaria.access import usuario_actual
from .models import (
    Actividad,
    CalificacionActividad,
    Corte,
    Inscripcion,
    Materia,
    Nota,
    PeriodoAcademico,
)


CORTES_DEFINITIVA = {
    1: Decimal('0.30'),
    2: Decimal('0.30'),
    3: Decimal('0.40'),
}


def es_profesor(request):
    """Verifica si el usuario actual tiene rol de profesor."""
    rol = str(request.session.get('usuario_rol', '')).lower()
    return 'prof' in rol


def profesor_actual(request):
    """Obtiene el usuario profesor actual."""
    if not es_profesor(request):
        return None
    return usuario_actual(request)


def _valores_formulario_actividad(request, actividad=None):
    if request.method == 'POST':
        return {
            'nombre': request.POST.get('nombre', ''),
            'tipo': request.POST.get('tipo', 'OTRO'),
            'porcentaje': request.POST.get('porcentaje', ''),
            'descripcion': request.POST.get('descripcion', ''),
            'periodo': request.POST.get('periodo', ''),
            'numero_corte': request.POST.get('numero_corte', '1'),
        }

    if actividad:
        return {
            'nombre': actividad.nombre,
            'tipo': actividad.tipo,
            'porcentaje': actividad.porcentaje,
            'descripcion': actividad.descripcion,
            'periodo': str(actividad.periodo_id),
            'numero_corte': str(actividad.numero_corte),
        }

    return {
        'nombre': '',
        'tipo': 'OTRO',
        'porcentaje': '',
        'descripcion': '',
        'periodo': '',
        'numero_corte': '1',
    }


def materias_profesor(request):
    """Dashboard del profesor con sus materias y acciones de calificacion."""
    if not es_profesor(request):
        return redirect('sin_permiso')

    profesor = profesor_actual(request)
    materias = Materia.objects.filter(
        profesor=profesor,
        activa=True,
    ).prefetch_related(
        'actividades',
        'inscripcion_set',
    ).select_related('programa')

    context = {
        'materias': materias,
        'total_materias': materias.count(),
        'titulo': 'Mis Materias - Gestion de Calificaciones',
    }
    return render(request, 'academica/profesor_materias.html', context)


def crear_actividad(request, materia_id):
    """Crea una actividad con porcentaje dentro de una materia, periodo y corte."""
    if not es_profesor(request):
        return redirect('sin_permiso')

    profesor = profesor_actual(request)
    materia = get_object_or_404(Materia, pk=materia_id, profesor=profesor, activa=True)
    form_values = _valores_formulario_actividad(request)
    alert_message = ''

    if request.method == 'POST':
        try:
            nombre = request.POST.get('nombre', '').strip()
            tipo = request.POST.get('tipo', 'OTRO')
            porcentaje = Decimal(request.POST.get('porcentaje', '0'))
            descripcion = request.POST.get('descripcion', '').strip()
            periodo_id = request.POST.get('periodo')
            numero_corte = int(request.POST.get('numero_corte', '1'))

            if not nombre:
                alert_message = 'El nombre de la actividad es requerido.'
                messages.error(request, alert_message)
                raise ValueError()

            if porcentaje <= 0 or porcentaje > 100:
                alert_message = 'El porcentaje debe estar entre 0 y 100.'
                messages.error(request, alert_message)
                raise ValueError()

            if numero_corte not in (1, 2, 3):
                alert_message = 'El corte seleccionado no es valido.'
                messages.error(request, alert_message)
                raise ValueError()

            periodo = get_object_or_404(PeriodoAcademico, pk=periodo_id)
            porcentajes_existentes = Actividad.objects.filter(
                materia=materia,
                periodo=periodo,
                numero_corte=numero_corte,
                activa=True,
            ).values_list('porcentaje', flat=True)

            suma_actual = sum(porcentajes_existentes, Decimal('0.00'))
            suma_porcentajes = suma_actual + porcentaje
            if suma_porcentajes > Decimal('100.00'):
                alert_message = (
                    f'La suma de porcentajes del corte {numero_corte} seria '
                    f'{suma_porcentajes}%. Actualmente suma {suma_actual}%.'
                )
                messages.error(request, alert_message)
                raise ValueError()

            actividad = Actividad.objects.create(
                materia=materia,
                periodo=periodo,
                numero_corte=numero_corte,
                nombre=nombre,
                tipo=tipo,
                porcentaje=porcentaje,
                descripcion=descripcion,
                activa=True,
            )

            inscripciones = Inscripcion.objects.filter(
                materia=materia,
                periodo=periodo,
                activa=True,
            )
            for inscripcion in inscripciones:
                CalificacionActividad.objects.get_or_create(
                    inscripcion=inscripcion,
                    actividad=actividad,
                )

            messages.success(
                request,
                f'Actividad "{nombre}" creada para el corte {numero_corte} con {porcentaje}%.',
            )
            messages.info(
                request,
                f'Se crearon espacios de calificacion para {inscripciones.count()} estudiantes.',
            )
            return redirect('profesor_calificar_actividad', actividad_id=actividad.pk)

        except (ValueError, InvalidOperation):
            pass

    context = {
        'materia': materia,
        'periodos': PeriodoAcademico.objects.all(),
        'tipos_actividad': Actividad.TIPOS_ACTIVIDAD,
        'cortes': Corte.CORTES,
        'form_values': form_values,
        'alert_message': alert_message,
        'titulo': f'Crear Actividad - {materia.nombre}',
    }
    return render(request, 'academica/profesor_crear_actividad.html', context)


def editar_actividad(request, actividad_id):
    """Edita una actividad existente y recalcula su peso dentro del corte."""
    if not es_profesor(request):
        return redirect('sin_permiso')

    profesor = profesor_actual(request)
    actividad = get_object_or_404(
        Actividad,
        pk=actividad_id,
        materia__profesor=profesor,
        activa=True,
    )
    materia = actividad.materia
    form_values = _valores_formulario_actividad(request, actividad)
    alert_message = ''

    if request.method == 'POST':
        try:
            nombre = request.POST.get('nombre', '').strip()
            tipo = request.POST.get('tipo', 'OTRO')
            porcentaje = Decimal(request.POST.get('porcentaje', '0'))
            descripcion = request.POST.get('descripcion', '').strip()
            periodo_id = request.POST.get('periodo')
            numero_corte = int(request.POST.get('numero_corte', '1'))

            if not nombre:
                alert_message = 'El nombre de la actividad es requerido.'
                messages.error(request, alert_message)
                raise ValueError()

            if porcentaje <= 0 or porcentaje > 100:
                alert_message = 'El porcentaje debe estar entre 0 y 100.'
                messages.error(request, alert_message)
                raise ValueError()

            if numero_corte not in (1, 2, 3):
                alert_message = 'El corte seleccionado no es valido.'
                messages.error(request, alert_message)
                raise ValueError()

            periodo = get_object_or_404(PeriodoAcademico, pk=periodo_id)
            porcentajes_existentes = Actividad.objects.filter(
                materia=materia,
                periodo=periodo,
                numero_corte=numero_corte,
                activa=True,
            ).exclude(pk=actividad.pk).values_list('porcentaje', flat=True)

            suma_actual = sum(porcentajes_existentes, Decimal('0.00'))
            suma_porcentajes = suma_actual + porcentaje
            if suma_porcentajes > Decimal('100.00'):
                alert_message = (
                    f'La suma de porcentajes del corte {numero_corte} seria '
                    f'{suma_porcentajes}%. Actualmente suma {suma_actual}% sin esta actividad.'
                )
                messages.error(request, alert_message)
                raise ValueError()

            actividad.nombre = nombre
            actividad.tipo = tipo
            actividad.porcentaje = porcentaje
            actividad.descripcion = descripcion
            actividad.periodo = periodo
            actividad.numero_corte = numero_corte
            actividad.save()

            inscripciones = Inscripcion.objects.filter(
                materia=materia,
                periodo=periodo,
                activa=True,
            )
            for inscripcion in inscripciones:
                CalificacionActividad.objects.get_or_create(
                    inscripcion=inscripcion,
                    actividad=actividad,
                )

            messages.success(request, f'Actividad "{nombre}" actualizada correctamente.')
            return redirect('profesor_gestionar_actividades', materia_id=materia.pk)

        except (ValueError, InvalidOperation):
            pass

    context = {
        'materia': materia,
        'actividad': actividad,
        'periodos': PeriodoAcademico.objects.all(),
        'tipos_actividad': Actividad.TIPOS_ACTIVIDAD,
        'cortes': Corte.CORTES,
        'form_values': form_values,
        'alert_message': alert_message,
        'titulo': f'Editar Actividad - {materia.nombre}',
    }
    return render(request, 'academica/profesor_crear_actividad.html', context)


def calificar_actividad(request, actividad_id):
    """Permite calificar a los estudiantes inscritos en una actividad."""
    if not es_profesor(request):
        return redirect('sin_permiso')

    profesor = profesor_actual(request)
    actividad = get_object_or_404(
        Actividad,
        pk=actividad_id,
        materia__profesor=profesor,
        activa=True,
    )
    calificaciones = CalificacionActividad.objects.filter(
        actividad=actividad,
    ).select_related('inscripcion__estudiante__usuario')

    if request.method == 'POST':
        for calificacion in calificaciones:
            nota_str = request.POST.get(f'nota_{calificacion.pk}', '').strip()
            observaciones = request.POST.get(f'obs_{calificacion.pk}', '').strip()

            if not nota_str:
                calificacion.calificacion = None
                calificacion.observaciones = observaciones
                calificacion.save()
                continue

            try:
                nota = Decimal(nota_str)
            except InvalidOperation:
                messages.error(
                    request,
                    f'Nota invalida para {calificacion.inscripcion.estudiante.usuario}.',
                )
                continue

            if nota < Decimal('0') or nota > Decimal('5.00'):
                messages.error(
                    request,
                    f'La nota de {calificacion.inscripcion.estudiante.usuario} debe estar entre 0 y 5.',
                )
                continue

            calificacion.calificacion = nota
            calificacion.observaciones = observaciones
            calificacion.save()

        messages.success(request, 'Calificaciones guardadas correctamente.')
        return redirect('profesor_reporte_corte', actividad_id=actividad.pk)

    calificaciones_ingresadas = calificaciones.filter(calificacion__isnull=False).count()
    total_estudiantes = calificaciones.count()
    porcentaje_completado = (
        calificaciones_ingresadas / total_estudiantes * 100
        if total_estudiantes > 0
        else 0
    )

    context = {
        'actividad': actividad,
        'calificaciones': calificaciones,
        'calificaciones_ingresadas': calificaciones_ingresadas,
        'total_estudiantes': total_estudiantes,
        'porcentaje_completado': round(porcentaje_completado, 1),
        'titulo': f'Calificar "{actividad.nombre}" - {actividad.materia.nombre}',
    }
    return render(request, 'academica/profesor_calificar.html', context)


def reporte_corte(request, actividad_id):
    """Muestra el desglose y la nota final calculada del corte de una actividad."""
    if not es_profesor(request):
        return redirect('sin_permiso')

    profesor = profesor_actual(request)
    actividad = get_object_or_404(
        Actividad,
        pk=actividad_id,
        materia__profesor=profesor,
        activa=True,
    )
    inscripciones = Inscripcion.objects.filter(
        materia=actividad.materia,
        periodo=actividad.periodo,
        activa=True,
    ).select_related('estudiante__usuario')

    reporte = []
    for inscripcion in inscripciones:
        corte, _ = Corte.objects.get_or_create(
            inscripcion=inscripcion,
            numero_corte=actividad.numero_corte,
            defaults={
                'fecha_inicio': actividad.periodo.fecha_inicio,
                'fecha_fin': actividad.periodo.fecha_fin,
                'activo': True,
            },
        )
        detalles = corte.obtener_detalles_calificacion()
        nota_final = corte.calcular_nota_final()
        if nota_final is not None:
            _sincronizar_nota_corte(corte, nota_final)
        reporte.append({
            'estudiante': inscripcion.estudiante.usuario.nombre_usuario,
            'codigo': inscripcion.estudiante.codigo_estudiante,
            'detalles': detalles,
            'nota_final': nota_final,
            'completo': detalles['completo'] and nota_final is not None,
            'estado': _obtener_estado_nota(nota_final),
        })

    notas_finales = [item['nota_final'] for item in reporte if item['nota_final'] is not None]
    estadisticas = {
        'total_estudiantes': inscripciones.count(),
        'estudiantes_completos': sum(1 for item in reporte if item['completo']),
        'estudiantes_incompletos': sum(1 for item in reporte if not item['completo']),
        'promedio_clase': (sum(notas_finales) / len(notas_finales)) if notas_finales else None,
        'nota_minima': min(notas_finales) if notas_finales else None,
        'nota_maxima': max(notas_finales) if notas_finales else None,
    }

    context = {
        'actividad': actividad,
        'materia': actividad.materia,
        'reporte': reporte,
        'estadisticas': estadisticas,
        'titulo': f'Reporte de Notas - {actividad.materia.nombre}',
    }
    return render(request, 'academica/profesor_reporte_corte.html', context)


def gestionar_actividades(request, materia_id):
    """Lista actividades de una materia agrupadas por periodo y corte."""
    if not es_profesor(request):
        return redirect('sin_permiso')

    profesor = profesor_actual(request)
    materia = get_object_or_404(Materia, pk=materia_id, profesor=profesor, activa=True)
    actividades = Actividad.objects.filter(
        materia=materia,
        activa=True,
    ).prefetch_related('calificaciones').select_related('periodo')

    actividades_por_periodo = {}
    for actividad in actividades:
        periodo_key = f'{actividad.periodo} - Corte {actividad.numero_corte}'
        if periodo_key not in actividades_por_periodo:
            actividades_por_periodo[periodo_key] = {
                'periodo': actividad.periodo,
                'numero_corte': actividad.numero_corte,
                'actividades': [],
                'suma_porcentajes': Decimal('0.00'),
                'porcentajes_completos': False,
            }

        actividades_por_periodo[periodo_key]['actividades'].append(actividad)
        actividades_por_periodo[periodo_key]['suma_porcentajes'] += actividad.porcentaje

    for datos_periodo in actividades_por_periodo.values():
        datos_periodo['porcentajes_completos'] = (
            abs(datos_periodo['suma_porcentajes'] - Decimal('100.00')) <= Decimal('0.01')
        )

    context = {
        'materia': materia,
        'actividades_por_periodo': actividades_por_periodo,
        'titulo': f'Actividades - {materia.nombre}',
    }
    return render(request, 'academica/profesor_actividades.html', context)


def definitivas_materia(request, materia_id):
    """Consolidado de nota definitiva por estudiante para una materia y periodo."""
    if not es_profesor(request):
        return redirect('sin_permiso')

    profesor = profesor_actual(request)
    materia = get_object_or_404(Materia, pk=materia_id, profesor=profesor, activa=True)
    periodos = PeriodoAcademico.objects.filter(
        inscripcion__materia=materia,
        inscripcion__activa=True,
    ).distinct().order_by('-fecha_inicio', 'nombre')

    periodo_id = request.GET.get('periodo')
    periodo = None
    if periodo_id:
        periodo = get_object_or_404(periodos, pk=periodo_id)
    elif periodos.exists():
        periodo = periodos.first()

    inscripciones = Inscripcion.objects.none()
    if periodo:
        inscripciones = Inscripcion.objects.filter(
            materia=materia,
            periodo=periodo,
            activa=True,
        ).select_related('estudiante__usuario').order_by('estudiante__codigo_estudiante')

    consolidado = []
    for inscripcion in inscripciones:
        _sincronizar_cortes_calculados(inscripcion)
        notas_por_corte = _notas_por_corte(inscripcion)
        definitiva = _calcular_definitiva(notas_por_corte)
        consolidado.append({
            'estudiante': inscripcion.estudiante.usuario.nombre_usuario,
            'codigo': inscripcion.estudiante.codigo_estudiante,
            'corte_1': notas_por_corte.get(1),
            'corte_2': notas_por_corte.get(2),
            'corte_3': notas_por_corte.get(3),
            'definitiva': definitiva,
            'estado': _estado_definitiva(definitiva),
            'completa': definitiva is not None,
        })

    definitivas = [item['definitiva'] for item in consolidado if item['definitiva'] is not None]
    estadisticas = {
        'total_estudiantes': len(consolidado),
        'completos': sum(1 for item in consolidado if item['completa']),
        'pendientes': sum(1 for item in consolidado if not item['completa']),
        'aprobados': sum(1 for item in consolidado if item['definitiva'] is not None and item['definitiva'] >= Decimal('3.00')),
        'promedio': (sum(definitivas) / Decimal(len(definitivas))).quantize(Decimal('0.01')) if definitivas else None,
    }

    context = {
        'materia': materia,
        'periodos': periodos,
        'periodo': periodo,
        'periodo_id': str(periodo.pk) if periodo else '',
        'consolidado': consolidado,
        'estadisticas': estadisticas,
        'fecha_generacion': timezone.now(),
        'titulo': f'Definitivas - {materia.nombre}',
    }
    return render(request, 'academica/profesor_definitivas.html', context)


def _obtener_estado_nota(nota):
    if nota is None:
        return 'Sin calificar'
    if nota >= Decimal('4.50'):
        return 'Excelente'
    if nota >= Decimal('4.00'):
        return 'Muy Bueno'
    if nota >= Decimal('3.50'):
        return 'Bueno'
    if nota >= Decimal('3.00'):
        return 'Aceptable'
    return 'Deficiente'


def _sincronizar_cortes_calculados(inscripcion):
    for numero_corte in (1, 2, 3):
        corte, _ = Corte.objects.get_or_create(
            inscripcion=inscripcion,
            numero_corte=numero_corte,
            defaults={
                'fecha_inicio': inscripcion.periodo.fecha_inicio,
                'fecha_fin': inscripcion.periodo.fecha_fin,
                'activo': True,
            },
        )
        nota_final = corte.calcular_nota_final()
        if nota_final is not None:
            _sincronizar_nota_corte(corte, nota_final)


def _notas_por_corte(inscripcion):
    notas = Nota.objects.filter(
        inscripcion=inscripcion,
        corte__in=(1, 2, 3),
    ).order_by('corte', '-id_nota')
    notas_por_corte = {}
    for nota in notas:
        notas_por_corte.setdefault(nota.corte, nota.valor)
    return notas_por_corte


def _calcular_definitiva(notas_por_corte):
    if not all(corte in notas_por_corte for corte in (1, 2, 3)):
        return None
    definitiva = sum(
        notas_por_corte[numero_corte] * peso
        for numero_corte, peso in CORTES_DEFINITIVA.items()
    )
    return definitiva.quantize(Decimal('0.01'))


def _estado_definitiva(definitiva):
    if definitiva is None:
        return 'Pendiente'
    if definitiva >= Decimal('3.00'):
        return 'Aprobado'
    return 'Reprobado'


def _sincronizar_nota_corte(corte, nota_final):
    """
    Mantiene la tabla historica Nota alineada con el calculo por actividades.
    La fuente de verdad del profesor es el desglose de actividades; Nota guarda
    el resultado final del corte para listados, promedios y reportes legacy.
    """
    notas = Nota.objects.filter(
        inscripcion=corte.inscripcion,
        corte=corte.numero_corte,
    )
    observacion = 'Calculada automaticamente desde actividades y porcentajes.'

    if notas.exists():
        notas.update(
            valor=nota_final,
            observaciones=observacion,
        )
    else:
        max_id = Nota.objects.aggregate(max_id=Max('id_nota'))['max_id'] or 0
        Nota.objects.create(
            id_nota=max_id + 1,
            inscripcion=corte.inscripcion,
            corte=corte.numero_corte,
            valor=nota_final,
            observaciones=observacion,
        )

    _actualizar_promedio_estudiante(corte.inscripcion.estudiante)


def _actualizar_promedio_estudiante(estudiante):
    valores = Nota.objects.filter(
        inscripcion__estudiante=estudiante,
    ).values_list('valor', flat=True)

    if valores:
        promedio = sum(valores) / Decimal(len(valores))
    else:
        promedio = Decimal('0')

    estudiante.promedio = promedio.quantize(Decimal('0.01'))
    estudiante.save()
