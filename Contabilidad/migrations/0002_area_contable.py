from django.db import migrations, models


def crear_areas_contables(apps, schema_editor):
    AreaContable = apps.get_model('Contabilidad', 'AreaContable')
    areas = [
        'Rectoría',
        'Vicerrectoría Académica',
        'Facultad de Ingeniería',
        'Facultad de Ciencias Administrativas',
        'Bienestar Universitario',
        'Recursos Humanos',
        'inventario',
        'Contabilidad',
        'Solicitudes y Atención al Usuario',
    ]
    for area in areas:
        AreaContable.objects.get_or_create(nombre=area)


class Migration(migrations.Migration):

    dependencies = [
        ('Contabilidad', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AreaContable',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100, unique=True)),
                ('activa', models.BooleanField(default=True)),
            ],
        ),
        migrations.RunPython(crear_areas_contables, migrations.RunPython.noop),
    ]
