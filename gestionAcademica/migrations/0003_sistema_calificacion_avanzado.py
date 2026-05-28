# Generated migration for enhanced grading system

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gestionAcademica', '0002_usuario_admin_base'),
    ]

    operations = [
        # Actividad: evaluaciones que el profesor crea para una materia
        migrations.CreateModel(
            name='Actividad',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=200, help_text='Ej: Quiz 1, Taller, Examen Parcial')),
                ('descripcion', models.TextField(blank=True)),
                ('tipo', models.CharField(
                    choices=[
                        ('QUIZ', 'Quiz'),
                        ('TALLER', 'Taller'),
                        ('PARCIAL', 'Examen Parcial'),
                        ('FINAL', 'Examen Final'),
                        ('PROYECTO', 'Proyecto'),
                        ('PARTICIPACION', 'Participación'),
                        ('OTRO', 'Otro'),
                    ],
                    default='OTRO',
                    max_length=20
                )),
                ('porcentaje', models.DecimalField(
                    decimal_places=2,
                    max_digits=5,
                    help_text='Porcentaje de la nota final (ej: 15.00 = 15%)'
                )),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True)),
                ('activa', models.BooleanField(default=True)),
                ('materia', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='actividades',
                    to='gestionAcademica.materia'
                )),
                ('periodo', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    to='gestionAcademica.periodoacademico'
                )),
            ],
            options={
                'verbose_name_plural': 'Actividades',
                'ordering': ['materia', 'fecha_creacion'],
            },
        ),

        # CalificacionActividad: la nota que un estudiante obtiene en una actividad
        migrations.CreateModel(
            name='CalificacionActividad',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('calificacion', models.DecimalField(
                    blank=True,
                    decimal_places=2,
                    max_digits=4,
                    null=True,
                    help_text='Nota de 0.0 a 5.0'
                )),
                ('fecha_calificacion', models.DateTimeField(auto_now=True)),
                ('observaciones', models.TextField(blank=True, help_text='Observaciones del profesor')),
                ('actividad', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='calificaciones',
                    to='gestionAcademica.actividad'
                )),
                ('inscripcion', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='calificaciones_actividades',
                    to='gestionAcademica.inscripcion'
                )),
            ],
            options={
                'verbose_name_plural': 'Calificaciones de Actividades',
                'unique_together': {('inscripcion', 'actividad')},
                'ordering': ['inscripcion', 'actividad'],
            },
        ),
    ]
