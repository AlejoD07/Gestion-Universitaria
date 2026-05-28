from django.db import migrations, models
import django.db.models.deletion


def relacionar_nominas_con_empleados(apps, schema_editor):
    Nomina = apps.get_model('Contabilidad', 'Nomina')
    Empleado = apps.get_model('RecursosHumanos', 'Empleado')

    for nomina in Nomina.objects.all():
        cedula = str(nomina.empleado_cedula or '').strip()
        if not cedula:
            continue
        try:
            empleado = Empleado.objects.get(documento=cedula)
        except Empleado.DoesNotExist:
            continue
        nomina.empleado_id = empleado.id
        nomina.save(update_fields=['empleado'])


class Migration(migrations.Migration):

    dependencies = [
        ('RecursosHumanos', '0002_catalogos_base_rrhh'),
        ('Contabilidad', '0002_area_contable'),
    ]

    operations = [
        migrations.AddField(
            model_name='nomina',
            name='empleado',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='nominas', to='RecursosHumanos.empleado'),
        ),
        migrations.RunPython(relacionar_nominas_con_empleados, migrations.RunPython.noop),
    ]
