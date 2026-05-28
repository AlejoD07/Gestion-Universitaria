from django.db import migrations


def restaurar_usuarios_demo(apps, schema_editor):
    Facultad = apps.get_model('gestionAcademica', 'Facultad')
    Rol = apps.get_model('gestionAcademica', 'Rol')
    TipoDocumento = apps.get_model('gestionAcademica', 'TipoDocumento')
    Usuario = apps.get_model('gestionAcademica', 'Usuario')

    tipo_doc, _ = TipoDocumento.objects.get_or_create(id_tipo_doc=1, defaults={'nombre_tipo_doc': 'Cedula'})
    facultad, _ = Facultad.objects.get_or_create(nombre='Facultad General')

    roles = [
        (99, 'Super Administrador'),
        (1, 'Administrador'),
        (2, 'Profesor'),
        (3, 'Estudiante'),
        (4, 'Recursos Humanos'),
        (5, 'Contador'),
        (6, 'Inventario'),
        (7, 'Solicitudes'),
        (8, 'Coordinador Academico'),
    ]
    for rol_id, nombre in roles:
        rol, _ = Rol.objects.get_or_create(id_rol=rol_id, defaults={'nombre_rol': nombre})
        if rol_id in [99, 7, 8]:
            rol.nombre_rol = nombre
            rol.save()

    usuarios = [
        (9000, 'Camilo Restrepo', 99),
        (9001, 'Daniela Pardo', 1),
        (9700, 'Sergio Alvarez', 8),
        (9500, 'Mariana Gomez', 2),
        (9600, 'Andres Felipe Rios', 3),
        (9100, 'Carolina Vargas', 5),
        (9200, 'Natalia Herrera', 4),
        (9300, 'Miguel Torres', 6),
        (9400, 'Sofia Martinez', 7),
    ]
    for documento, nombre, rol_id in usuarios:
        usuario, _ = Usuario.objects.get_or_create(
            id_usuario=documento,
            defaults={
                'nombre_usuario': nombre,
                'activo': True,
                'id_tipo_documento': tipo_doc,
                'id_rol_id': rol_id,
                'facultad': facultad,
            },
        )
        usuario.nombre_usuario = nombre
        usuario.activo = True
        usuario.id_tipo_documento = tipo_doc
        usuario.id_rol_id = rol_id
        if usuario.facultad_id is None:
            usuario.facultad = facultad
        usuario.save()


class Migration(migrations.Migration):

    dependencies = [
        ('gestionAcademica', '0005_datos_demo_academicos'),
    ]

    operations = [
        migrations.RunPython(restaurar_usuarios_demo, migrations.RunPython.noop),
    ]
