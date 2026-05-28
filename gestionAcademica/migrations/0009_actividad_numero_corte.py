from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestionAcademica', '0008_alter_actividad_descripcion_alter_actividad_nombre_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='actividad',
            name='numero_corte',
            field=models.IntegerField(
                choices=[(1, 'Corte 1'), (2, 'Corte 2'), (3, 'Corte 3')],
                default=1,
                help_text='Corte academico al que pertenece la actividad',
            ),
        ),
        migrations.AlterModelOptions(
            name='actividad',
            options={
                'ordering': ['materia', 'periodo', 'numero_corte', 'fecha_creacion'],
                'verbose_name_plural': 'Actividades',
            },
        ),
    ]
