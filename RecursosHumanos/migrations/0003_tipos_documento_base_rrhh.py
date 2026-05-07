from django.db import migrations


def crear_tipos_documento(apps, schema_editor):
    TipoDocumento = apps.get_model('RecursosHumanos', 'TipoDocumento')

    tipos = [
        ('Cedula de Ciudadania', 'CC'),
        ('Pasaporte', 'PS'),
        ('Cedula de Extranjeria', 'CE'),
        ('Permiso Temporal', 'PT'),
        ('Tarjeta de Identidad', 'TI'),
    ]

    for nombre, abreviatura in tipos:
        TipoDocumento.objects.get_or_create(
            abreviatura=abreviatura,
            defaults={'tipo_documento': nombre},
        )


class Migration(migrations.Migration):

    dependencies = [
        ('RecursosHumanos', '0002_catalogos_base_rrhh'),
    ]

    operations = [
        migrations.RunPython(crear_tipos_documento, migrations.RunPython.noop),
    ]
