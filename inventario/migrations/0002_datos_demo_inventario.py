import datetime
from decimal import Decimal

from django.db import migrations


def crear_datos_demo_inventario(apps, schema_editor):
    Categoria = apps.get_model('inventario', 'Categoria')
    Item = apps.get_model('inventario', 'Item')
    Prestamo = apps.get_model('inventario', 'Prestamo')

    categorias = {
        'Equipos Audiovisuales': 'Video beams, pantallas y equipos de apoyo para clase.',
        'Laboratorios': 'Equipos usados en laboratorios academicos.',
        'Computadores': 'Portatiles y equipos de computo institucionales.',
        'Electronica': 'Kits y componentes para practicas.',
    }
    categorias_creadas = {}
    for nombre, descripcion in categorias.items():
        categoria, _ = Categoria.objects.get_or_create(
            nombre_categoria=nombre,
            defaults={'descripcion_categoria': descripcion},
        )
        categoria.descripcion_categoria = descripcion
        categoria.save()
        categorias_creadas[nombre] = categoria

    items = [
        ('Video Beam Epson X41', 'Epson', 'Proyector para aulas multiples.', 'Salon 203', datetime.date(2024, 3, 10), Decimal('2450000'), '2', 'Equipos Audiovisuales'),
        ('Computador Portatil Dell 5420', 'Dell', 'Equipo para practicas de programacion.', 'Laboratorio 1', datetime.date(2024, 5, 20), Decimal('3800000'), '1', 'Computadores'),
        ('Microscopio Binocular', 'Nikon', 'Microscopio para practicas basicas.', 'Laboratorio Biologia', datetime.date(2023, 9, 2), Decimal('5200000'), '3', 'Laboratorios'),
        ('Kit Arduino Uno', 'Arduino', 'Kit para electronica basica.', 'Laboratorio Electronica', datetime.date(2025, 1, 15), Decimal('280000'), '1', 'Electronica'),
    ]
    items_creados = {}
    for nombre, marca, descripcion, ubicacion, fecha_compra, valor, estado, categoria_nombre in items:
        item = Item.objects.filter(nombre_item=nombre).first()
        if not item:
            item = Item.objects.create(
                nombre_item=nombre,
                marca_item=marca,
                descripcion_item=descripcion,
                ubicacion_item=ubicacion,
                fecha_compra=fecha_compra,
                valor_item=valor,
                estado_item=estado,
                categoria=categorias_creadas[categoria_nombre],
            )
        else:
            item.marca_item = marca
            item.descripcion_item = descripcion
            item.ubicacion_item = ubicacion
            item.fecha_compra = fecha_compra
            item.valor_item = valor
            item.estado_item = estado
            item.categoria = categorias_creadas[categoria_nombre]
            item.save()
        items_creados[nombre] = item

    prestamos = [
        (items_creados['Video Beam Epson X41'], datetime.date(2026, 6, 5), None, '1', 'Entregado con cable HDMI y control remoto.', ''),
        (items_creados['Kit Arduino Uno'], datetime.date(2026, 5, 20), datetime.date(2026, 5, 18), '2', 'Entregado completo para laboratorio.', 'Devuelto completo y funcional.'),
    ]
    for item, esperada, devolucion, estado, entrega, observacion_devolucion in prestamos:
        prestamo = Prestamo.objects.filter(item=item, fecha_devolucion_esperada=esperada).first()
        if not prestamo:
            Prestamo.objects.create(
                fecha_devolucion_esperada=esperada,
                fecha_devolucion=devolucion,
                estado_prestamo=estado,
                observaciones_entrega=entrega,
                observaciones_devolucion=observacion_devolucion,
                item=item,
            )
        else:
            prestamo.fecha_devolucion = devolucion
            prestamo.estado_prestamo = estado
            prestamo.observaciones_entrega = entrega
            prestamo.observaciones_devolucion = observacion_devolucion
            prestamo.save()


class Migration(migrations.Migration):

    dependencies = [
        ('inventario', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(crear_datos_demo_inventario, migrations.RunPython.noop),
    ]
