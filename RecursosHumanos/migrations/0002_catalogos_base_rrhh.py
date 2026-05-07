from django.db import migrations


def crear_catalogos_base(apps, schema_editor):
    TipoContrato = apps.get_model('RecursosHumanos', 'TipoContrato')
    Cargo = apps.get_model('RecursosHumanos', 'Cargo')
    Area = apps.get_model('RecursosHumanos', 'Area')

    for tipo_contrato in [
        'Termino Indefinido',
        'Termino Fijo',
        'Prestacion de Servicios',
        'Aprendizaje',
    ]:
        TipoContrato.objects.get_or_create(tipo_contrato=tipo_contrato)

    for cargo in [
        'Administrador',
        'Recursos Humanos',
        'Contador',
        'Soporte Tecnico',
        'Gerente',
        'Operario',
        'Profesor',
        'Coordinador Academico',
    ]:
        Cargo.objects.get_or_create(cargo=cargo)

    for area in [
        'Administrativo',
        'Planta Profesores',
        'Academica',
        'Contabilidad',
        'inventario',
    ]:
        Area.objects.get_or_create(area=area)


class Migration(migrations.Migration):

    dependencies = [
        ('RecursosHumanos', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(crear_catalogos_base, migrations.RunPython.noop),
    ]

