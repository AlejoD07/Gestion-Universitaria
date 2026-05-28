from django import forms
from . import models

class FormularioCategoria(forms.Form):
    nombre_categoria = forms.CharField(label="Nombre Categoria", max_length=50, required=True)
    descripcion_categoria = forms.CharField(label="Descripción Categoria", max_length=250, required=False)


ESTADOS_ITEM = [
    ("1", "DISPONIBLE"),
    ("2", "PRESTADO"),
    ("3", "MANTENIMIENTO"),
    ("4", "DAÑADO"),
]


class FormularioItem(forms.Form):
    nombre_item = forms.CharField(label="Nombre Item", max_length=100, required=True)
    marca_item = forms.CharField(label="Marca Item", max_length=100, required=True)
    descripcion_item = forms.CharField(label="Descripción Item", help_text="Descripción del item del inventario", required=False)
    ubicacion_item = forms.CharField(label="Ubicación Item", max_length=50, help_text="Ej: Salon 203 - laboratorio", required=True)
    fecha_compra = forms.DateField(label="Fecha Compra", widget=forms.DateInput(attrs={'type':'date'}), required=True)
    valor_item = forms.DecimalField(label="Valor Item", max_digits=10, decimal_places=2, required=True)
    estado_item = forms.ChoiceField(choices=ESTADOS_ITEM, required=True)
    categoria = forms.ModelChoiceField(queryset=models.Categoria.objects.all())


ESTADOS_PRESTAMO = [
    ("1", "PRESTADO"),
    ("2", "DEVUELTO"),
    ("3", "ATRASADO"),
]


class FormularioPrestamo(forms.Form):
    fecha_devolucion_esperada = forms.DateField(label="Fecha Devolucion esperada", widget=forms.DateInput(attrs={'type':'date'}), required=True)
    fecha_devolucion = forms.DateField(label="Fecha de la devolucion", widget=forms.DateInput(attrs={'type':'date'}), required=False)
    estado_prestamo = forms.ChoiceField(choices=ESTADOS_PRESTAMO, required=True)
    observaciones_entrega = forms.CharField(help_text="El equipo no presenta ningun fallo, rasguño, golpe, etc", required=True)
    observaciones_devolucion = forms.CharField(help_text="El equipo se devuelve sin ninguna falla, rasguño, golpe, etc", required=False)
    item = forms.ModelChoiceField(queryset=models.Item.objects.filter(estado_item="1"), empty_label="Seleccione un item disponible")
