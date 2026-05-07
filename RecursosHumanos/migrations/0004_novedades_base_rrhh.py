from django.db import migrations


def crear_novedades_base(apps, schema_editor):
    Novedades = apps.get_model('RecursosHumanos', 'Novedades')

    novedades = [
        (
            'Vacaciones',
            'Durante las vacaciones no se paga ARL y el pago de parafiscales es opcional segun politica de la empresa.',
        ),
        (
            'Incapacidad',
            'No se paga ARL. A partir del tercer dia, la incapacidad se paga al 66.66% del salario minimo legal vigente.',
        ),
        (
            'Suspension',
            'Durante la suspension solo se realiza el pago de pension correspondiente.',
        ),
    ]

    for novedad, observaciones in novedades:
        Novedades.objects.get_or_create(
            novedad=novedad,
            defaults={'observaciones': observaciones},
        )


class Migration(migrations.Migration):

    dependencies = [
        ('RecursosHumanos', '0003_tipos_documento_base_rrhh'),
    ]

    operations = [
        migrations.RunPython(crear_novedades_base, migrations.RunPython.noop),
    ]
