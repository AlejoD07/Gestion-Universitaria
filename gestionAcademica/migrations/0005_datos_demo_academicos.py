from decimal import Decimal
import datetime

from django.db import migrations


def crear_datos_demo_academicos(apps, schema_editor):
    Facultad = apps.get_model('gestionAcademica', 'Facultad')
    Rol = apps.get_model('gestionAcademica', 'Rol')
    TipoDocumento = apps.get_model('gestionAcademica', 'TipoDocumento')
    Usuario = apps.get_model('gestionAcademica', 'Usuario')
    Estudiante = apps.get_model('gestionAcademica', 'Estudiante')
    Programa = apps.get_model('gestionAcademica', 'Programa')
    Materia = apps.get_model('gestionAcademica', 'Materia')
    PeriodoAcademico = apps.get_model('gestionAcademica', 'PeriodoAcademico')
    Inscripcion = apps.get_model('gestionAcademica', 'Inscripcion')
    Nota = apps.get_model('gestionAcademica', 'Nota')
    Asistencia = apps.get_model('gestionAcademica', 'Asistencia')

    tipo_doc, _ = TipoDocumento.objects.get_or_create(id_tipo_doc=1, defaults={'nombre_tipo_doc': 'Cedula'})
    rol_profesor, _ = Rol.objects.get_or_create(id_rol=2, defaults={'nombre_rol': 'Profesor'})
    rol_estudiante, _ = Rol.objects.get_or_create(id_rol=3, defaults={'nombre_rol': 'Estudiante'})

    ingenieria, _ = Facultad.objects.get_or_create(nombre='Facultad de Ingenieria')
    administrativas, _ = Facultad.objects.get_or_create(nombre='Facultad de Ciencias Administrativas')

    profesores = [
        (9500, 'Mariana Gomez', ingenieria),
        (9501, 'Laura Mendoza', administrativas),
    ]
    for documento, nombre, facultad in profesores:
        usuario, _ = Usuario.objects.get_or_create(
            id_usuario=documento,
            defaults={
                'nombre_usuario': nombre,
                'activo': True,
                'id_tipo_documento': tipo_doc,
                'id_rol': rol_profesor,
                'facultad': facultad,
            },
        )
        usuario.nombre_usuario = nombre
        usuario.activo = True
        usuario.id_tipo_documento = tipo_doc
        usuario.id_rol = rol_profesor
        usuario.facultad = facultad
        usuario.save()

    estudiantes = [
        (9600, 'Andres Felipe Rios', 'EST-2026-001', 4, Decimal('4.20'), ingenieria),
        (9601, 'Camila Torres', 'EST-2026-002', 3, Decimal('4.05'), ingenieria),
        (9602, 'Nicolas Ramirez', 'EST-2026-003', 2, Decimal('3.80'), administrativas),
    ]
    estudiantes_creados = {}
    for documento, nombre, codigo, semestre, promedio, facultad in estudiantes:
        usuario, _ = Usuario.objects.get_or_create(
            id_usuario=documento,
            defaults={
                'nombre_usuario': nombre,
                'activo': True,
                'id_tipo_documento': tipo_doc,
                'id_rol': rol_estudiante,
                'facultad': facultad,
            },
        )
        usuario.nombre_usuario = nombre
        usuario.activo = True
        usuario.id_tipo_documento = tipo_doc
        usuario.id_rol = rol_estudiante
        usuario.facultad = facultad
        usuario.save()

        estudiante, _ = Estudiante.objects.get_or_create(
            usuario=usuario,
            defaults={'codigo_estudiante': codigo, 'semestre': semestre, 'promedio': promedio},
        )
        estudiante.codigo_estudiante = codigo
        estudiante.semestre = semestre
        estudiante.promedio = promedio
        estudiante.save()
        estudiantes_creados[documento] = estudiante

    sistemas, _ = Programa.objects.get_or_create(nombre='Ingenieria de Sistemas', defaults={'facultad': ingenieria})
    sistemas.facultad = ingenieria
    sistemas.save()
    administracion, _ = Programa.objects.get_or_create(nombre='Administracion de Empresas', defaults={'facultad': administrativas})
    administracion.facultad = administrativas
    administracion.save()

    profesor_ingenieria = Usuario.objects.get(id_usuario=9500)
    profesor_admin = Usuario.objects.get(id_usuario=9501)

    materias = [
        (1001, 'Programacion I', 3, 'Fundamentos de programacion y logica.', sistemas, profesor_ingenieria),
        (1002, 'Calculo Diferencial', 4, 'Funciones, limites y derivadas.', sistemas, profesor_ingenieria),
        (1003, 'Contabilidad Basica', 3, 'Registros contables y estados financieros.', administracion, profesor_admin),
        (1004, 'Gestion del Talento Humano', 3, 'Procesos basicos de talento humano.', administracion, profesor_admin),
    ]
    materias_creadas = {}
    for materia_id, nombre, creditos, descripcion, programa, profesor in materias:
        materia, _ = Materia.objects.get_or_create(
            id_materia=materia_id,
            defaults={
                'nombre': nombre,
                'creditos': creditos,
                'descripcion': descripcion,
                'activa': True,
                'programa': programa,
                'profesor': profesor,
            },
        )
        materia.nombre = nombre
        materia.creditos = creditos
        materia.descripcion = descripcion
        materia.activa = True
        materia.programa = programa
        materia.profesor = profesor
        materia.save()
        materias_creadas[materia_id] = materia

    periodo, _ = PeriodoAcademico.objects.get_or_create(
        nombre='2026-I',
        defaults={'fecha_inicio': datetime.date(2026, 2, 1), 'fecha_fin': datetime.date(2026, 6, 15)},
    )

    inscripciones = [
        (9600, 1001),
        (9600, 1002),
        (9601, 1001),
        (9601, 1002),
        (9602, 1003),
        (9602, 1004),
    ]
    inscripciones_creadas = []
    for documento, materia_id in inscripciones:
        inscripcion, _ = Inscripcion.objects.get_or_create(
            estudiante=estudiantes_creados[documento],
            materia=materias_creadas[materia_id],
            periodo=periodo,
            defaults={'fecha_inscripcion': datetime.date(2026, 1, 20), 'activa': True},
        )
        inscripcion.activa = True
        inscripcion.save()
        inscripciones_creadas.append(inscripcion)

    notas = [
        (5001, inscripciones_creadas[0], 1, Decimal('4.30'), 'Buen trabajo en talleres.'),
        (5002, inscripciones_creadas[0], 2, Decimal('4.10'), 'Debe reforzar ejercicios practicos.'),
        (5003, inscripciones_creadas[1], 1, Decimal('3.90'), 'Cumple con las actividades.'),
        (5004, inscripciones_creadas[2], 1, Decimal('4.60'), 'Excelente participacion.'),
        (5005, inscripciones_creadas[4], 1, Decimal('3.80'), 'Entrega completa.'),
        (5006, inscripciones_creadas[5], 1, Decimal('4.00'), 'Buen desempeno.'),
    ]
    for nota_id, inscripcion, corte, valor, observaciones in notas:
        nota, _ = Nota.objects.get_or_create(
            id_nota=nota_id,
            defaults={
                'inscripcion': inscripcion,
                'corte': corte,
                'valor': valor,
                'observaciones': observaciones,
            },
        )
        nota.inscripcion = inscripcion
        nota.corte = corte
        nota.valor = valor
        nota.observaciones = observaciones
        nota.save()

    for inscripcion in inscripciones_creadas:
        for fecha, asiste in [(datetime.date(2026, 2, 5), True), (datetime.date(2026, 2, 12), True), (datetime.date(2026, 2, 19), False)]:
            Asistencia.objects.get_or_create(inscripcion=inscripcion, fecha=fecha, defaults={'asiste': asiste})


class Migration(migrations.Migration):

    dependencies = [
        ('gestionAcademica', '0004_roles_negocio'),
    ]

    operations = [
        migrations.RunPython(crear_datos_demo_academicos, migrations.RunPython.noop),
    ]
