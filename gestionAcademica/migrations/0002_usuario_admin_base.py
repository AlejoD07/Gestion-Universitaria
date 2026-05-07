from django.db import migrations


def crear_usuario_admin(apps, schema_editor):
    Rol = apps.get_model('gestionAcademica', 'Rol')
    TipoDocumento = apps.get_model('gestionAcademica', 'TipoDocumento')
    Usuario = apps.get_model('gestionAcademica', 'Usuario')

    rol_admin, _ = Rol.objects.get_or_create(
        id_rol=1,
        defaults={'nombre_rol': 'Administrador'},
    )
    if rol_admin.nombre_rol != 'Administrador':
        rol_admin.nombre_rol = 'Administrador'
        rol_admin.save()

    tipo_documento, _ = TipoDocumento.objects.get_or_create(
        id_tipo_doc=1,
        defaults={'nombre_tipo_doc': 'Cedula'},
    )

    Usuario.objects.get_or_create(
        id_usuario=1001,
        defaults={
            'nombre_usuario': 'Admin Academico',
            'activo': True,
            'id_tipo_documento': tipo_documento,
            'id_rol': rol_admin,
        },
    )


class Migration(migrations.Migration):

    dependencies = [
        ('gestionAcademica', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(crear_usuario_admin, migrations.RunPython.noop),
    ]
