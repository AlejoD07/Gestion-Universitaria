from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('solicitudes', '0002_catalogos_base_solicitudes'),
    ]

    operations = [
        migrations.CreateModel(
            name='DocumentoSolicitud',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('archivo', models.FileField(upload_to='solicitudes/documentos/')),
                ('nombre_original', models.CharField(blank=True, max_length=255)),
                ('fecha_carga', models.DateTimeField(auto_now_add=True)),
                ('solicitud', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='documentos', to='solicitudes.solicitud')),
            ],
        ),
    ]
