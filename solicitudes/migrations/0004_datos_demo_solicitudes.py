from django.db import migrations


def crear_datos_demo_solicitudes(apps, schema_editor):
    Rol = apps.get_model('solicitudes', 'Rol')
    TipoDocumento = apps.get_model('solicitudes', 'TipoDocumento')
    Usuario = apps.get_model('solicitudes', 'Usuario')
    TiposSolicitud = apps.get_model('solicitudes', 'TiposSolicitud')
    EstadosSolicitud = apps.get_model('solicitudes', 'EstadosSolicitud')
    Solicitud = apps.get_model('solicitudes', 'Solicitud')
    HistorialSolicitud = apps.get_model('solicitudes', 'HistorialSolicitud')
    ComentariosSolicitud = apps.get_model('solicitudes', 'ComentariosSolicitud')

    rol_estudiante, _ = Rol.objects.get_or_create(nombre_rol='Estudiante')
    rol_admin, _ = Rol.objects.get_or_create(nombre_rol='Gestor Solicitudes')
    tipo_doc, _ = TipoDocumento.objects.get_or_create(nombre_tipo_doc='Cedula')

    estudiante, _ = Usuario.objects.get_or_create(
        email='estudiante.demo@universidad.edu.co',
        defaults={
            'nombre_usuario': 'Andres Felipe Rios',
            'activo': True,
            'id_tipo_documento': tipo_doc,
            'id_rol': rol_estudiante,
        },
    )
    gestor, _ = Usuario.objects.get_or_create(
        email='solicitudes@universidad.edu.co',
        defaults={
            'nombre_usuario': 'Sofia Martinez',
            'activo': True,
            'id_tipo_documento': tipo_doc,
            'id_rol': rol_admin,
        },
    )

    pendiente, _ = EstadosSolicitud.objects.get_or_create(nombre='Pendiente')
    proceso, _ = EstadosSolicitud.objects.get_or_create(nombre='En proceso')
    cerrada, _ = EstadosSolicitud.objects.get_or_create(nombre='Cerrada')

    tipo_solicitud, _ = TiposSolicitud.objects.get_or_create(nombre='Solicitud', defaults={'descripcion': 'Tramites academicos o administrativos.'})
    tipo_queja, _ = TiposSolicitud.objects.get_or_create(nombre='Queja', defaults={'descripcion': 'Inconformidades sobre servicios o procesos.'})
    tipo_reclamo, _ = TiposSolicitud.objects.get_or_create(nombre='Reclamo', defaults={'descripcion': 'Reclamaciones formales sobre derechos o procesos.'})

    datos = [
        (estudiante, tipo_solicitud, proceso, 'Media', 'Solicitud de certificado academico en proceso.'),
        (estudiante, tipo_queja, pendiente, 'Alta', 'Queja por demora en respuesta de tramite.'),
        (gestor, tipo_reclamo, cerrada, 'Baja', 'Reclamo revisado y cerrado por el area responsable.'),
    ]

    for usuario, tipo, estado, prioridad, comentario in datos:
        solicitud = Solicitud.objects.filter(usuario=usuario, tipo=tipo, prioridad=prioridad).first()
        if not solicitud:
            solicitud = Solicitud.objects.create(usuario=usuario, tipo=tipo, estado=estado, prioridad=prioridad)
        else:
            solicitud.estado = estado
            solicitud.save()
        HistorialSolicitud.objects.get_or_create(
            solicitud=solicitud,
            estado=estado,
            comentario=comentario,
        )
        ComentariosSolicitud.objects.get_or_create(
            solicitud=solicitud,
            usuario=usuario,
            comentario=comentario,
        )


class Migration(migrations.Migration):

    dependencies = [
        ('solicitudes', '0003_documento_solicitud'),
    ]

    operations = [
        migrations.RunPython(crear_datos_demo_solicitudes, migrations.RunPython.noop),
    ]
