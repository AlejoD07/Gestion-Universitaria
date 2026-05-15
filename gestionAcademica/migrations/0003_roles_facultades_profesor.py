from django.db import migrations, models
import django.db.models.deletion


def crear_roles_y_facultades(apps, schema_editor):
    Rol = apps.get_model('gestionAcademica', 'Rol')
    TipoDocumento = apps.get_model('gestionAcademica', 'TipoDocumento')
    Usuario = apps.get_model('gestionAcademica', 'Usuario')
    Facultad = apps.get_model('gestionAcademica', 'Facultad')

    roles = [
        (1, 'Administrador'),
        (2, 'Profesor'),
        (3, 'Estudiante'),
        (4, 'Contabilidad'),
        (5, 'Recursos Humanos'),
        (6, 'inventario'),
        (7, 'Solicitudes'),
        (99, 'Super Administrador'),
    ]
    for rol_id, nombre in roles:
        Rol.objects.get_or_create(id_rol=rol_id, defaults={'nombre_rol': nombre})

    tipo_documento, _ = TipoDocumento.objects.get_or_create(
        id_tipo_doc=1,
        defaults={'nombre_tipo_doc': 'Cedula'}
    )
    facultad, _ = Facultad.objects.get_or_create(nombre='Facultad General')

    usuarios_base = [
        (9000, 'Super Administrador', 99),
        (9100, 'Usuario Contabilidad', 4),
        (9200, 'Usuario Recursos Humanos', 5),
        (9300, 'Usuario inventario', 6),
        (9400, 'Usuario Solicitudes', 7),
        (9500, 'Profesor Demo', 2),
        (9600, 'Estudiante Demo', 3),
    ]
    for documento, nombre, rol_id in usuarios_base:
        usuario, creado = Usuario.objects.get_or_create(
            id_usuario=documento,
            defaults={
                'nombre_usuario': nombre,
                'activo': True,
                'id_tipo_documento': tipo_documento,
                'id_rol_id': rol_id,
                'facultad': facultad,
            }
        )
        if not creado and usuario.facultad_id is None:
            usuario.facultad = facultad
            usuario.save()


class Migration(migrations.Migration):

    dependencies = [
        ('gestionAcademica', '0002_usuario_admin_base'),
    ]

    operations = [
        migrations.CreateModel(
            name='Facultad',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100, unique=True)),
                ('activa', models.BooleanField(default=True)),
            ],
        ),
        migrations.AddField(
            model_name='usuario',
            name='facultad',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='gestionAcademica.facultad'),
        ),
        migrations.AddField(
            model_name='programa',
            name='facultad',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='gestionAcademica.facultad'),
        ),
        migrations.AddField(
            model_name='materia',
            name='profesor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='materias_asignadas', to='gestionAcademica.usuario'),
        ),
        migrations.RunPython(crear_roles_y_facultades, migrations.RunPython.noop),
    ]
