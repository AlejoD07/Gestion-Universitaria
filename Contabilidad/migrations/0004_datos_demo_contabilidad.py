import datetime
from decimal import Decimal

from django.db import migrations


def nombre_completo(empleado):
    return ' '.join([parte for parte in [
        empleado.primer_nombre,
        empleado.segundo_nombre,
        empleado.primer_apellido,
        empleado.segundo_apellido,
    ] if parte])


def crear_datos_demo_contabilidad(apps, schema_editor):
    AreaContable = apps.get_model('Contabilidad', 'AreaContable')
    Nomina = apps.get_model('Contabilidad', 'Nomina')
    Presupuesto = apps.get_model('Contabilidad', 'Presupuesto')
    Ingreso = apps.get_model('Contabilidad', 'Ingreso')
    Empleado = apps.get_model('RecursosHumanos', 'Empleado')

    for area in ['Academica', 'Contabilidad', 'Recursos Humanos', 'inventario', 'Bienestar Universitario']:
        AreaContable.objects.get_or_create(nombre=area, defaults={'activa': True})

    nominas = [
        (9500, 'Mayo', 2026, Decimal('3200000'), Decimal('120000'), Decimal('0'), Decimal('180000'), datetime.date(2026, 5, 30), 'pendiente'),
        (9100, 'Mayo', 2026, Decimal('3600000'), Decimal('0'), Decimal('250000'), Decimal('210000'), datetime.date(2026, 5, 30), 'pendiente'),
        (9200, 'Abril', 2026, Decimal('3300000'), Decimal('0'), Decimal('0'), Decimal('190000'), datetime.date(2026, 4, 30), 'pagado'),
    ]
    for documento, mes, anio, salario, extras, comisiones, deducciones, fecha_pago, estado in nominas:
        empleado = Empleado.objects.filter(documento=documento).first()
        if not empleado:
            continue
        contrato = getattr(empleado, 'contratos', None)
        cargo = contrato.cargo.cargo if contrato and contrato.cargo else ''
        area = contrato.area.area if contrato and contrato.area else ''
        nomina = Nomina.objects.filter(empleado_cedula=str(documento), mes=mes, anio=anio).first()
        if not nomina:
            nomina = Nomina()
        nomina.empleado = empleado
        nomina.empleado_nombre = nombre_completo(empleado)
        nomina.empleado_cedula = str(documento)
        nomina.cargo = cargo
        nomina.area = area
        nomina.mes = mes
        nomina.anio = anio
        nomina.salario_base = salario
        nomina.horas_extras = extras
        nomina.comisiones = comisiones
        nomina.deducciones = deducciones
        nomina.fecha_pago = fecha_pago
        nomina.estado = estado
        nomina.total_pago = salario + extras + comisiones - deducciones
        nomina.save()

    presupuestos = [
        ('Presupuesto Nomina Docentes', 'Academica', Decimal('90000000'), Decimal('36500000'), 'Mayo', 2026, 'Pago de planta docente y apoyo academico.'),
        ('Renovacion Equipos Laboratorio', 'inventario', Decimal('45000000'), Decimal('12500000'), 'Mayo', 2026, 'Compra y mantenimiento de equipos academicos.'),
        ('Capacitacion Administrativa', 'Recursos Humanos', Decimal('12000000'), Decimal('3200000'), 'Abril', 2026, 'Formacion interna del personal administrativo.'),
    ]
    for nombre, area, asignado, gastado, mes, anio, descripcion in presupuestos:
        presupuesto = Presupuesto.objects.filter(nombre=nombre, mes=mes, anio=anio).first()
        if not presupuesto:
            presupuesto = Presupuesto()
        presupuesto.nombre = nombre
        presupuesto.area = area
        presupuesto.monto_asignado = asignado
        presupuesto.monto_gastado = gastado
        presupuesto.mes = mes
        presupuesto.anio = anio
        presupuesto.descripcion = descripcion
        presupuesto.save()

    ingresos = [
        ('Matriculas periodo 2026-I', Decimal('185000000'), datetime.date(2026, 2, 10), 'Matriculas', 'Ingreso por matriculas de estudiantes activos.'),
        ('Convenio practica empresarial', Decimal('22000000'), datetime.date(2026, 3, 15), 'Convenios', 'Aporte por convenio interinstitucional.'),
        ('Cursos de extension', Decimal('8500000'), datetime.date(2026, 4, 8), 'Educacion continua', 'Inscripciones a cursos libres.'),
    ]
    for concepto, monto, fecha, fuente, descripcion in ingresos:
        ingreso = Ingreso.objects.filter(concepto=concepto, fecha=fecha).first()
        if not ingreso:
            ingreso = Ingreso()
        ingreso.concepto = concepto
        ingreso.monto = monto
        ingreso.fecha = fecha
        ingreso.fuente = fuente
        ingreso.descripcion = descripcion
        ingreso.save()


class Migration(migrations.Migration):

    dependencies = [
        ('RecursosHumanos', '0005_datos_demo_empleados'),
        ('Contabilidad', '0003_nomina_empleado'),
    ]

    operations = [
        migrations.RunPython(crear_datos_demo_contabilidad, migrations.RunPython.noop),
    ]
