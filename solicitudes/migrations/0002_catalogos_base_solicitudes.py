from django.db import migrations


def crear_catalogos_base(apps, schema_editor):
    Rol = apps.get_model('solicitudes', 'Rol')
    TipoDocumento = apps.get_model('solicitudes', 'TipoDocumento')
    Usuario = apps.get_model('solicitudes', 'Usuario')
    TiposSolicitud = apps.get_model('solicitudes', 'TiposSolicitud')
    EstadosSolicitud = apps.get_model('solicitudes', 'EstadosSolicitud')

    rol, _ = Rol.objects.get_or_create(nombre_rol='Estudiante')
    tipo_doc, _ = TipoDocumento.objects.get_or_create(nombre_tipo_doc='Cedula')
    Usuario.objects.get_or_create(
        email='usuario@universidad.edu.co',
        defaults={
            'nombre_usuario': 'Usuario Demo',
            'activo': True,
            'id_tipo_documento': tipo_doc,
            'id_rol': rol,
        },
    )

    tipos = [
        ('Solicitud', 'Tramites academicos o administrativos.'),
        ('Queja', 'Inconformidades sobre servicios, clases o procesos.'),
        ('Reclamo', 'Reclamaciones formales sobre derechos o procesos.'),
    ]
    for nombre, descripcion in tipos:
        TiposSolicitud.objects.get_or_create(nombre=nombre, defaults={'descripcion': descripcion})

    for estado in ['Pendiente', 'En proceso', 'Aprobada', 'Radicada', 'Cerrada']:
        EstadosSolicitud.objects.get_or_create(nombre=estado)


class Migration(migrations.Migration):

    dependencies = [
        ('solicitudes', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(crear_catalogos_base, migrations.RunPython.noop),
    ]

