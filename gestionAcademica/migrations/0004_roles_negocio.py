from django.db import migrations


ROLES_NEGOCIO = [
    (99, 'Super Administrador'),
    (1, 'Administrador General'),
    (8, 'Coordinador Académico'),
    (9, 'Secretaría Académica'),
    (2, 'Profesor'),
    (3, 'Estudiante'),
    (10, 'Director Financiero'),
    (4, 'Contador'),
    (11, 'Auxiliar Contable'),
    (12, 'Director Talento Humano'),
    (5, 'Auxiliar Talento Humano'),
    (13, 'Coordinador inventario'),
    (6, 'Auxiliar inventario'),
    (7, 'Gestor Solicitudes'),
]

USUARIOS_DEMO = [
    (9000, 'Camilo Restrepo', 99),
    (9001, 'Daniela Pardo', 1),
    (9700, 'Sergio Alvarez', 8),
    (9701, 'Paula Medina', 9),
    (9500, 'Mariana Gomez', 2),
    (9600, 'Andres Felipe Rios', 3),
    (9101, 'Director Financiero', 10),
    (9100, 'Carolina Vargas', 4),
    (9102, 'Auxiliar Contable', 11),
    (9201, 'Director Talento Humano', 12),
    (9200, 'Natalia Herrera', 5),
    (9301, 'Coordinador inventario', 13),
    (9300, 'Miguel Torres', 6),
    (9400, 'Sofia Martinez', 7),
]


def crear_roles_negocio(apps, schema_editor):
    Rol = apps.get_model('gestionAcademica', 'Rol')
    TipoDocumento = apps.get_model('gestionAcademica', 'TipoDocumento')
    Usuario = apps.get_model('gestionAcademica', 'Usuario')
    Facultad = apps.get_model('gestionAcademica', 'Facultad')

    tipo_documento, _ = TipoDocumento.objects.get_or_create(
        id_tipo_doc=1,
        defaults={'nombre_tipo_doc': 'Cedula'}
    )
    facultad_general, _ = Facultad.objects.get_or_create(nombre='Facultad General')

    for rol_id, nombre in ROLES_NEGOCIO:
        rol, creado = Rol.objects.get_or_create(
            id_rol=rol_id,
            defaults={'nombre_rol': nombre}
        )
        if not creado and rol.nombre_rol != nombre:
            rol.nombre_rol = nombre
            rol.save()

    for documento, nombre, rol_id in USUARIOS_DEMO:
        usuario, creado = Usuario.objects.get_or_create(
            id_usuario=documento,
            defaults={
                'nombre_usuario': nombre,
                'activo': True,
                'id_tipo_documento': tipo_documento,
                'id_rol_id': rol_id,
                'facultad': facultad_general,
            }
        )
        if not creado:
            usuario.nombre_usuario = nombre
            usuario.activo = True
            usuario.id_tipo_documento = tipo_documento
            usuario.id_rol_id = rol_id
            if usuario.facultad_id is None:
                usuario.facultad = facultad_general
            usuario.save()


class Migration(migrations.Migration):

    dependencies = [
        ('gestionAcademica', '0003_roles_facultades_profesor'),
    ]

    operations = [
        migrations.RunPython(crear_roles_negocio, migrations.RunPython.noop),
    ]
