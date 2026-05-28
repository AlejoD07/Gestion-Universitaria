import datetime

from django.db import migrations


def crear_datos_demo_rrhh(apps, schema_editor):
    TipoDocumento = apps.get_model('RecursosHumanos', 'TipoDocumento')
    TipoContrato = apps.get_model('RecursosHumanos', 'TipoContrato')
    Cargo = apps.get_model('RecursosHumanos', 'Cargo')
    Area = apps.get_model('RecursosHumanos', 'Area')
    Empleado = apps.get_model('RecursosHumanos', 'Empleado')
    Contrato = apps.get_model('RecursosHumanos', 'Contrato')
    Novedades = apps.get_model('RecursosHumanos', 'Novedades')
    NovedadesEmpleado = apps.get_model('RecursosHumanos', 'NovedadesEmpleado')

    tipo_doc, _ = TipoDocumento.objects.get_or_create(abreviatura='CC', defaults={'tipo_documento': 'Cedula de Ciudadania'})
    indefinido, _ = TipoContrato.objects.get_or_create(tipo_contrato='Termino Indefinido')
    fijo, _ = TipoContrato.objects.get_or_create(tipo_contrato='Termino Fijo')

    datos = [
        (9500, 'Mariana', '', 'Gomez', '', 'mariana.gomez@universidad.edu.co', 'Profesor', 'Planta Profesores', indefinido, 3200000),
        (9501, 'Laura', '', 'Mendoza', '', 'laura.mendoza@universidad.edu.co', 'Profesor', 'Planta Profesores', indefinido, 3400000),
        (9100, 'Carolina', '', 'Vargas', '', 'carolina.vargas@universidad.edu.co', 'Contador', 'Contabilidad', indefinido, 3600000),
        (9200, 'Natalia', '', 'Herrera', '', 'natalia.herrera@universidad.edu.co', 'Recursos Humanos', 'Administrativo', indefinido, 3300000),
        (9300, 'Miguel', '', 'Torres', '', 'miguel.torres@universidad.edu.co', 'Soporte Tecnico', 'inventario', fijo, 2800000),
        (1221313, 'Brayan', '', 'Salas', '', 'brayan.salas@universidad.edu.co', 'Profesor', 'Planta Profesores', indefinido, 3000000),
    ]

    empleados = []
    for documento, primer_nombre, segundo_nombre, primer_apellido, segundo_apellido, correo, cargo_nombre, area_nombre, tipo_contrato, salario in datos:
        cargo, _ = Cargo.objects.get_or_create(cargo=cargo_nombre)
        area, _ = Area.objects.get_or_create(area=area_nombre)
        empleado, _ = Empleado.objects.get_or_create(
            documento=documento,
            defaults={
                'primer_nombre': primer_nombre,
                'segundo_nombre': segundo_nombre,
                'primer_apellido': primer_apellido,
                'segundo_apellido': segundo_apellido,
                'correo': correo,
                'estado': True,
                'tipo_documento': tipo_doc,
            },
        )
        empleado.primer_nombre = primer_nombre
        empleado.segundo_nombre = segundo_nombre
        empleado.primer_apellido = primer_apellido
        empleado.segundo_apellido = segundo_apellido
        empleado.correo = correo
        empleado.estado = True
        empleado.tipo_documento = tipo_doc
        empleado.save()

        contrato, _ = Contrato.objects.get_or_create(
            empleado=empleado,
            defaults={
                'salario': salario,
                'fecha_ingreso': datetime.date(2024, 2, 1),
                'fecha_retiro': None,
                'cargo': cargo,
                'area': area,
                'tipo_contrato': tipo_contrato,
            },
        )
        contrato.salario = salario
        contrato.fecha_ingreso = datetime.date(2024, 2, 1)
        contrato.fecha_retiro = None
        contrato.cargo = cargo
        contrato.area = area
        contrato.tipo_contrato = tipo_contrato
        contrato.save()
        empleados.append(empleado)

    vacaciones, _ = Novedades.objects.get_or_create(novedad='Vacaciones', defaults={'observaciones': 'Periodo de descanso remunerado.'})
    incapacidad, _ = Novedades.objects.get_or_create(novedad='Incapacidad', defaults={'observaciones': 'Ausencia justificada por salud.'})

    NovedadesEmpleado.objects.get_or_create(
        empleado=empleados[0],
        novedades=vacaciones,
        fecha_inicial=datetime.date(2026, 4, 6),
        defaults={'fecha_final': datetime.date(2026, 4, 12)},
    )
    NovedadesEmpleado.objects.get_or_create(
        empleado=empleados[-1],
        novedades=incapacidad,
        fecha_inicial=datetime.date(2026, 5, 4),
        defaults={'fecha_final': datetime.date(2026, 5, 7)},
    )


class Migration(migrations.Migration):

    dependencies = [
        ('RecursosHumanos', '0004_novedades_base_rrhh'),
    ]

    operations = [
        migrations.RunPython(crear_datos_demo_rrhh, migrations.RunPython.noop),
    ]
