from django.db import models

class Categoria(models.Model):
    nombre_categoria = models.CharField(max_length=100)
    descripcion_categoria = models.TextField(help_text="Descripción de la categoria del inventario", blank=True, null=True)
    fecha_creacion_categoria = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre_categoria


ESTADOS_ITEM = [
    ("1", "DISPONIBLE"),
    ("2", "PRESTADO"),
    ("3", "MANTENIMIENTO"),
    ("4", "DAÑADO"), 
]


class Item(models.Model):
    nombre_item = models.CharField(max_length=200)
    marca_item = models.CharField(max_length=100)
    descripcion_item = models.TextField(help_text="Descripción del item del inventario", blank=True, null=True)
    ubicacion_item = models.CharField(max_length=50, help_text="Ej: Salon 203 - laboratorio")
    fecha_registro = models.DateTimeField(auto_now_add=True)
    fecha_compra = models.DateField()
    valor_item = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    estado_item = models.CharField(max_length=14, choices=ESTADOS_ITEM, default="1")
    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.PROTECT,
        related_name="categorias",
        related_query_name="categoria"
    )

    def __str__(self):
        return self.nombre_item 
    

ESTADOS_PRESTAMO = [
    ("1", "PRESTADO"),
    ("2", "DEVUELTO"),
    ("3", "ATRASADO"),
]


class Prestamo(models.Model):
    fecha_prestamo = models.DateTimeField(auto_now_add=True)
    fecha_devolucion_esperada = models.DateField()
    fecha_devolucion = models.DateField(null=True, blank=True)
    estado_prestamo = models.CharField(max_length=9, choices=ESTADOS_PRESTAMO, default="1")
    observaciones_entrega = models.TextField(help_text="El equipo no presenta ningun fallo, rasguño, golpe, etc")
    observaciones_devolucion = models.TextField(help_text="El equipo se devuelve sin ninguna falla, rasguño, golpe, etc", blank=True, null=True)
    item = models.ForeignKey(
        Item,
        on_delete = models.PROTECT,
        related_name="items",
        related_query_name="item"
    )



