from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from decimal import Decimal

from RecursosHumanos.models import Empleado
from .models import (
    AjustePresupuestal,
    AreaContable,
    ConceptoNominaImportada,
    DetalleNominaImportada,
    Ingreso,
    LoteNomina,
    Nomina,
    PartidaPresupuestal,
    PlanPresupuestal,
    Presupuesto,
    RevisionPresupuestal,
)


# ---------- AYUDAS ----------

def _nombre_completo_empleado(empleado):
    partes = [
        empleado.primer_nombre,
        empleado.segundo_nombre,
        empleado.primer_apellido,
        empleado.segundo_apellido,
    ]
    return ' '.join([str(parte).strip() for parte in partes if parte])


def _contrato_empleado(empleado):
    try:
        return empleado.contratos
    except Exception:
        return None


def _datos_empleado(empleado):
    contrato = _contrato_empleado(empleado)
    cargo = ''
    area = ''
    salario = ''

    if contrato:
        cargo = contrato.cargo.cargo if contrato.cargo else ''
        area = contrato.area.area if contrato.area else ''
        salario = contrato.salario or 0

    return {
        'id': empleado.id,
        'cedula': empleado.documento,
        'nombre': _nombre_completo_empleado(empleado),
        'cargo': cargo,
        'area': area,
        'salario': salario,
    }


def _valor_decimal(valor):
    return Decimal(str(valor or 0)).quantize(Decimal('0.01'))


def _buscar_empleado_por_cedula(cedula):
    cedula = str(cedula or '').strip()
    if not cedula:
        return None
    return Empleado.objects.select_related('contrato__cargo', 'contrato__area').filter(
        documento=cedula,
        estado=True,
    ).first()


def _llenar_nomina_desde_empleado(nomina, empleado):
    datos = _datos_empleado(empleado)
    nomina.empleado = empleado
    nomina.empleado_nombre = datos['nombre']
    nomina.empleado_cedula = str(datos['cedula'])
    nomina.cargo = datos['cargo']
    nomina.area = datos['area']
    return datos


def _guardar_nomina_desde_post(nomina, request):
    empleado = _buscar_empleado_por_cedula(request.POST.get('empleado_cedula'))
    if not empleado:
        return 'No existe un empleado activo en Recursos Humanos con esa cédula.'

    datos = _llenar_nomina_desde_empleado(nomina, empleado)
    if not datos['cargo'] or not datos['area']:
        return 'El empleado existe, pero no tiene contrato con cargo y área registrados.'

    nomina.mes = request.POST['mes']
    nomina.anio = request.POST['anio']
    nomina.salario_base = request.POST.get('salario_base') or datos['salario'] or 0
    nomina.horas_extras = request.POST.get('horas_extras', 0) or 0
    nomina.comisiones = request.POST.get('comisiones', 0) or 0
    nomina.deducciones = request.POST.get('deducciones', 0) or 0
    nomina.fecha_pago = request.POST['fecha_pago']
    nomina.estado = request.POST.get('estado', 'pendiente')
    nomina.calcular_total()
    nomina.save()
    return None


# ---------- INICIO ----------

def inicio(request):
    total_nominas = Nomina.objects.count()
    total_presupuestos = Presupuesto.objects.count()
    total_ingresos = Ingreso.objects.count()

    context = {
        'total_nominas': total_nominas,
        'total_presupuestos': total_presupuestos,
        'total_ingresos': total_ingresos,
    }
    return render(request, 'contabilidad/paginas/inicio.html', context)


# ---------- NOMINAS ----------

def lista_nominas(request):
    lotes = LoteNomina.objects.prefetch_related('detalles').all()
    nominas = Nomina.objects.select_related('empleado').all()
    return render(request, 'contabilidad/paginas/nominas.html', {
        'lotes': lotes,
        'nominas': nominas,
    })


def simular_importacion_nomina(request):
    if request.method == 'POST':
        mes = request.POST.get('mes') or 'Mayo'
        anio = int(request.POST.get('anio') or 2026)
        plataforma = request.POST.get('plataforma_origen') or 'Alegra'
        lote = _crear_lote_nomina_simulado(mes, anio, plataforma)
        return redirect('detalle_lote_nomina', id=lote.id)

    return render(request, 'contabilidad/paginas/importar_nomina.html', {
        'plataformas': ['Alegra', 'Siigo', 'World Office', 'Helisa', 'SAP SuccessFactors'],
    })


def detalle_lote_nomina(request, id):
    lote = get_object_or_404(
        LoteNomina.objects.prefetch_related('detalles__conceptos'),
        id=id,
    )
    return render(request, 'contabilidad/paginas/detalle_lote_nomina.html', {'lote': lote})


def validar_lote_nomina(request, id):
    lote = get_object_or_404(LoteNomina, id=id)
    if lote.estado != 'contabilizado':
        lote.estado = 'validado' if not lote.detalles.filter(estado='inconsistencia').exists() else 'inconsistencias'
        lote.save()
    return redirect('detalle_lote_nomina', id=lote.id)


def contabilizar_lote_nomina(request, id):
    lote = get_object_or_404(LoteNomina, id=id)
    lote.estado = 'contabilizado'
    lote.observaciones = 'Lote contabilizado en simulacion de integracion.'
    lote.save()
    return redirect('detalle_lote_nomina', id=lote.id)


def _crear_lote_nomina_simulado(mes, anio, plataforma):
    codigo_base = f"NOM-{anio}-{str(mes).upper()[:3]}"
    consecutivo = LoteNomina.objects.filter(codigo__startswith=codigo_base).count() + 1
    lote = LoteNomina.objects.create(
        codigo=f"{codigo_base}-{consecutivo:03d}",
        plataforma_origen=plataforma,
        mes=mes,
        anio=anio,
        estado='importado',
        observaciones='Importacion simulada desde plataforma contable externa.',
    )

    empleados = Empleado.objects.filter(estado=True)[:12]
    total_devengado = Decimal('0.00')
    total_deducciones = Decimal('0.00')
    total_neto = Decimal('0.00')

    for empleado in empleados:
        datos = _datos_empleado(empleado)
        salario = _valor_decimal(datos['salario'])
        auxilio = Decimal('162000.00') if salario and salario <= Decimal('2600000.00') else Decimal('0.00')
        bonificacion = (salario * Decimal('0.03')).quantize(Decimal('0.01'))
        salud = (salario * Decimal('0.04')).quantize(Decimal('0.01'))
        pension = (salario * Decimal('0.04')).quantize(Decimal('0.01'))
        retencion = (salario * Decimal('0.02')).quantize(Decimal('0.01')) if salario >= Decimal('5000000.00') else Decimal('0.00')
        libranza = Decimal('50000.00') if int(empleado.id) % 2 == 0 else Decimal('0.00')
        devengado = salario + auxilio + bonificacion
        deducciones = salud + pension + retencion + libranza
        neto = devengado - deducciones

        estado = 'ok' if datos['cargo'] and datos['area'] else 'inconsistencia'
        mensaje = '' if estado == 'ok' else 'Empleado sin contrato completo en Recursos Humanos.'
        detalle = DetalleNominaImportada.objects.create(
            lote=lote,
            empleado=empleado,
            empleado_nombre=datos['nombre'],
            empleado_cedula=str(datos['cedula']),
            cargo=datos['cargo'],
            area=datos['area'],
            salario_base=salario,
            total_devengado=devengado,
            total_deducciones=deducciones,
            neto_pagar=neto,
            estado=estado,
            mensaje_validacion=mensaje,
        )

        conceptos = [
            ('devengado', 'DEV001', 'Salario basico', salario),
            ('devengado', 'DEV002', 'Auxilio de transporte', auxilio),
            ('devengado', 'DEV003', 'Bonificacion institucional', bonificacion),
            ('deduccion', 'DED001', 'Salud empleado', salud),
            ('deduccion', 'DED002', 'Pension empleado', pension),
            ('deduccion', 'DED003', 'Retencion en la fuente', retencion),
            ('deduccion', 'DED004', 'Libranza', libranza),
        ]
        for tipo, codigo, nombre, valor in conceptos:
            if valor > 0:
                ConceptoNominaImportada.objects.create(
                    detalle=detalle,
                    tipo=tipo,
                    codigo=codigo,
                    nombre=nombre,
                    valor=valor,
                )

        total_devengado += devengado
        total_deducciones += deducciones
        total_neto += neto

    lote.total_empleados = empleados.count()
    lote.total_devengado = total_devengado
    lote.total_deducciones = total_deducciones
    lote.total_neto = total_neto
    lote.estado = 'inconsistencias' if lote.detalles.filter(estado='inconsistencia').exists() else 'importado'
    lote.save()
    return lote


def buscar_empleado_nomina(request):
    empleado = _buscar_empleado_por_cedula(request.GET.get('cedula'))
    if not empleado:
        return JsonResponse({'encontrado': False, 'mensaje': 'Empleado no encontrado o inactivo.'}, status=404)
    return JsonResponse({'encontrado': True, 'empleado': _datos_empleado(empleado)})


def crear_nomina(request):
    if request.method == 'POST':
        nomina = Nomina()
        error = _guardar_nomina_desde_post(nomina, request)
        if error:
            return render(request, 'contabilidad/paginas/crear_nomina.html', {
                'error_empleado': error,
                'datos_formulario': request.POST,
            }, status=400)
        return redirect('lista_nominas')

    return render(request, 'contabilidad/paginas/crear_nomina.html')


def editar_nomina(request, id):
    nomina = get_object_or_404(Nomina, id=id)

    if request.method == 'POST':
        error = _guardar_nomina_desde_post(nomina, request)
        if error:
            return render(request, 'contabilidad/paginas/editar_nomina.html', {
                'nomina': nomina,
                'error_empleado': error,
                'datos_formulario': request.POST,
            }, status=400)
        return redirect('lista_nominas')

    return render(request, 'contabilidad/paginas/editar_nomina.html', {'nomina': nomina})


def eliminar_nomina(request, id):
    nomina = get_object_or_404(Nomina, id=id)
    nomina.delete()
    return redirect('lista_nominas')


# ---------- PRESUPUESTOS ----------

def lista_presupuestos(request):
    planes = PlanPresupuestal.objects.prefetch_related('partidas', 'revisiones').all()
    presupuestos = Presupuesto.objects.all()
    return render(request, 'contabilidad/paginas/presupuestos.html', {
        'planes': planes,
        'presupuestos': presupuestos,
    })


def crear_plan_presupuestal(request):
    if request.method == 'POST':
        plan = PlanPresupuestal.objects.create(
            nombre=request.POST['nombre'],
            anio=request.POST['anio'],
            estado=request.POST.get('estado', 'borrador'),
            fecha_aprobacion=request.POST.get('fecha_aprobacion') or None,
            descripcion=request.POST.get('descripcion', ''),
        )
        return redirect('detalle_plan_presupuestal', id=plan.id)

    return render(request, 'contabilidad/paginas/crear_plan_presupuestal.html')


def crear_plan_presupuestal_demo(request):
    anio = int(request.POST.get('anio', 2026)) if request.method == 'POST' else 2026
    plan, creado = PlanPresupuestal.objects.get_or_create(
        anio=anio,
        defaults={
            'nombre': f'Presupuesto Institucional {anio}',
            'estado': 'ejecucion',
            'descripcion': 'Plan anual demo con partidas por area y concepto.',
        },
    )
    if creado or not plan.partidas.exists():
        _crear_partidas_demo(plan)
    return redirect('detalle_plan_presupuestal', id=plan.id)


def detalle_plan_presupuestal(request, id):
    plan = get_object_or_404(
        PlanPresupuestal.objects.prefetch_related('partidas__ajustes', 'revisiones'),
        id=id,
    )
    partidas = plan.partidas.all()
    estadisticas = {
        'total_inicial': plan.total_inicial(),
        'total_ajustes': plan.total_ajustes(),
        'total_vigente': plan.total_vigente(),
        'total_ejecutado': plan.total_ejecutado(),
        'total_disponible': plan.total_disponible(),
    }
    return render(request, 'contabilidad/paginas/detalle_plan_presupuestal.html', {
        'plan': plan,
        'partidas': partidas,
        'revisiones': plan.revisiones.all(),
        'estadisticas': estadisticas,
    })


def crear_partida_presupuestal(request, plan_id):
    plan = get_object_or_404(PlanPresupuestal, id=plan_id)
    if request.method == 'POST':
        PartidaPresupuestal.objects.create(
            plan=plan,
            area=request.POST['area'],
            concepto=request.POST['concepto'],
            monto_inicial=request.POST['monto_inicial'],
            monto_ejecutado=request.POST.get('monto_ejecutado', 0) or 0,
            descripcion=request.POST.get('descripcion', ''),
        )
        return redirect('detalle_plan_presupuestal', id=plan.id)
    return render(request, 'contabilidad/paginas/form_partida_presupuestal.html', {
        'plan': plan,
        'areas': AreaContable.objects.filter(activa=True),
    })


def registrar_revision_presupuestal(request, plan_id):
    plan = get_object_or_404(PlanPresupuestal, id=plan_id)
    if request.method == 'POST':
        RevisionPresupuestal.objects.update_or_create(
            plan=plan,
            trimestre=request.POST['trimestre'],
            defaults={
                'fecha_revision': request.POST['fecha_revision'],
                'decision': request.POST['decision'],
                'observaciones': request.POST['observaciones'],
            },
        )
        return redirect('detalle_plan_presupuestal', id=plan.id)
    return render(request, 'contabilidad/paginas/form_revision_presupuestal.html', {
        'plan': plan,
        'decisiones': RevisionPresupuestal.DECISIONES,
    })


def registrar_ajuste_presupuestal(request, partida_id):
    partida = get_object_or_404(PartidaPresupuestal.objects.select_related('plan'), id=partida_id)
    if request.method == 'POST':
        AjustePresupuestal.objects.create(
            partida=partida,
            tipo=request.POST['tipo'],
            valor=request.POST['valor'],
            motivo=request.POST['motivo'],
            fecha=request.POST['fecha'],
            estado=request.POST.get('estado', 'aprobado'),
        )
        return redirect('detalle_plan_presupuestal', id=partida.plan_id)
    return render(request, 'contabilidad/paginas/form_ajuste_presupuestal.html', {
        'partida': partida,
        'tipos': AjustePresupuestal.TIPOS,
        'estados': AjustePresupuestal.ESTADOS,
    })


def _crear_partidas_demo(plan):
    partidas = [
        ('Academica', 'Nomina docente', '850000000', '312000000'),
        ('Academica', 'Laboratorios y practicas', '180000000', '52000000'),
        ('Recursos Humanos', 'Capacitacion y bienestar', '95000000', '22000000'),
        ('Inventario', 'Renovacion tecnologica', '260000000', '87000000'),
        ('Contabilidad', 'Servicios financieros y auditoria', '120000000', '36000000'),
        ('Solicitudes', 'Atencion y soporte estudiantil', '70000000', '18000000'),
    ]
    for area, concepto, inicial, ejecutado in partidas:
        PartidaPresupuestal.objects.get_or_create(
            plan=plan,
            area=area,
            concepto=concepto,
            defaults={
                'monto_inicial': Decimal(inicial),
                'monto_ejecutado': Decimal(ejecutado),
                'descripcion': 'Partida demo para seguimiento presupuestal anual.',
            },
        )


def crear_presupuesto(request):
    if request.method == 'POST':
        presupuesto = Presupuesto()
        presupuesto.nombre = request.POST['nombre']
        presupuesto.area = request.POST['area']
        presupuesto.monto_asignado = request.POST['monto_asignado']
        presupuesto.monto_gastado = request.POST.get('monto_gastado', 0)
        presupuesto.mes = request.POST['mes']
        presupuesto.anio = request.POST['anio']
        presupuesto.descripcion = request.POST.get('descripcion', '')
        presupuesto.save()
        return redirect('lista_presupuestos')

    return render(request, 'contabilidad/paginas/crear_presupuesto.html', {'areas': AreaContable.objects.filter(activa=True)})


def editar_presupuesto(request, id):
    presupuesto = get_object_or_404(Presupuesto, id=id)

    if request.method == 'POST':
        presupuesto.nombre = request.POST['nombre']
        presupuesto.area = request.POST['area']
        presupuesto.monto_asignado = request.POST['monto_asignado']
        presupuesto.monto_gastado = request.POST.get('monto_gastado', 0)
        presupuesto.mes = request.POST['mes']
        presupuesto.anio = request.POST['anio']
        presupuesto.descripcion = request.POST.get('descripcion', '')
        presupuesto.save()
        return redirect('lista_presupuestos')

    return render(request, 'contabilidad/paginas/editar_presupuesto.html', {'presupuesto': presupuesto, 'areas': AreaContable.objects.filter(activa=True)})


def eliminar_presupuesto(request, id):
    presupuesto = get_object_or_404(Presupuesto, id=id)
    presupuesto.delete()
    return redirect('lista_presupuestos')


# ---------- INGRESOS ----------

def lista_ingresos(request):
    ingresos = Ingreso.objects.all()
    return render(request, 'contabilidad/paginas/ingresos.html', {'ingresos': ingresos})


def crear_ingreso(request):
    if request.method == 'POST':
        ingreso = Ingreso()
        ingreso.concepto = request.POST['concepto']
        ingreso.monto = request.POST['monto']
        ingreso.fecha = request.POST['fecha']
        ingreso.fuente = request.POST['fuente']
        ingreso.descripcion = request.POST.get('descripcion', '')
        ingreso.save()
        return redirect('lista_ingresos')

    return render(request, 'contabilidad/paginas/crear_ingreso.html')


def eliminar_ingreso(request, id):
    ingreso = get_object_or_404(Ingreso, id=id)
    ingreso.delete()
    return redirect('lista_ingresos')


# ---------- AREAS CONTABLES ----------

def lista_areas_contables(request):
    areas = AreaContable.objects.all().order_by('nombre')
    return render(request, 'contabilidad/paginas/areas_contables.html', {'areas': areas})


def crear_area_contable(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        if nombre:
            AreaContable.objects.get_or_create(nombre=nombre, defaults={'activa': request.POST.get('activa') == 'on'})
        return redirect('lista_areas_contables')
    return redirect('lista_areas_contables')


def cambiar_estado_area_contable(request, id):
    area = get_object_or_404(AreaContable, id=id)
    area.activa = not area.activa
    area.save()
    return redirect('lista_areas_contables')
