from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from . import models
from . import forms
from django.db.models import ProtectedError
from django.contrib import messages

# Create your views here.
def home(request):
    total_items = models.Item.objects.count()

    prestados = models.Item.objects.filter(estado_item = "2").count()

    mantenimiento = models.Item.objects.filter(estado_item = "3").count()

    danados = models.Item.objects.filter(estado_item = "4").count()

    data = {
        "total_items": total_items,
        "prestados": prestados,
        "mantenimiento": mantenimiento,
        "danados": danados,
    }

    return render(request, 'main_home.html', data)


def categorias(request):
    categorias = models.Categoria.objects.all()

    data = {
        "categorias": categorias
    }

    return render(request, 'categorias.html', data)


def crear_categoria(request):
    return render(request, 'formulario_categoria.html', {'formulario': forms.FormularioCategoria})


def guardar_categoria(request):
    if request.method == "POST":
        nombre = request.POST["nombre_categoria"]
        descripcion = request.POST["descripcion_categoria"]


        nueva_categoria = models.Categoria.objects.create(
            nombre_categoria = nombre,
            descripcion_categoria = descripcion
        )

        return redirect('inventario:categorias')

    return redirect('inventario:crear_categoria')


def actualizar_categoria(request, id):
    categoria = models.Categoria.objects.get(id = id)

    if request.method == "POST":
        nombre = request.POST["nombre_categoria"]
        descripcion = request.POST["descripcion_categoria"]

        categoria.nombre_categoria = nombre
        categoria.descripcion_categoria = descripcion

        categoria.save()

        return redirect('inventario:categorias')
    else:
        formulario = forms.FormularioCategoria(initial={
            "nombre_categoria": categoria.nombre_categoria,
            "descripcion_categoria": categoria.descripcion_categoria
        })

    return render(request, 'formulario_categoria.html', {
        'formulario': formulario,
        'categoria': categoria
    })


def eliminar_categoria(request, id):
    categoria = models.Categoria.objects.get(id = id)

    try:
        categoria.delete()
        messages.success(request, "Categoría eliminada correctamente")
    except ProtectedError:
        messages.error(request, "No puedes eliminar esta categoría porque tiene items asociados")

    return redirect('inventario:categorias')


def items(request):
    items = models.Item.objects.all()
    categorias = models.Categoria.objects.all()

    data = {
        "items": items,
        "categorias": categorias
    }

    return render(request, 'items.html', data)


def crear_item(request):
    categorias = models.Categoria.objects.all()

    return render(request, 'formulario_item.html', {'formulario': forms.FormularioItem, 'categorias': categorias})


def guardar_item(request):
    if request.method == "POST":
        nombre = request.POST["nombre_item"]
        marca = request.POST["marca_item"]
        descripcion = request.POST["descripcion_item"]
        ubicacion = request.POST["ubicacion_item"]
        fecha_compra = request.POST["fecha_compra"]
        valor = request.POST["valor_item"]
        estado = request.POST["estado_item"]
        categoria = request.POST["categoria"]
        categoria_item = models.Categoria.objects.get(id=categoria)

        nuevo_item = models.Item.objects.create(
            nombre_item = nombre,
            marca_item = marca,
            descripcion_item = descripcion,
            ubicacion_item = ubicacion,
            fecha_compra = fecha_compra,
            valor_item = valor,
            estado_item = estado,
            categoria = categoria_item,
        )

        return redirect('inventario:items')

    return redirect('inventario:crear_item')


def actualizar_item(request, id):
    item = models.Item.objects.get(id = id)
    categorias = models.Categoria.objects.all()

    if request.method == "POST":
        nombre = request.POST["nombre_item"]
        descripcion = request.POST["descripcion_item"]
        ubicacion = request.POST["ubicacion_item"]
        estado = request.POST["estado_item"]
        categoria = request.POST["categoria"]
        categoria_item = models.Categoria.objects.get(id=categoria)


        item.nombre_item = nombre
        item.descripcion_item = descripcion
        item.ubicacion_item = ubicacion
        item.estado_item = estado
        item.categoria = categoria_item

        item.save()

        return redirect('inventario:items')
    else:
        formulario = forms.FormularioItem(initial={
            "nombre_item": item.nombre_item,
            "descripcion_item": item.descripcion_item,
            "ubicacion_item": item.ubicacion_item,
            "estado_item": item.estado_item,
            "categoria_item": item.categoria
        })

    return render(request, 'formulario_item.html', {
        'formulario': formulario,
        'item': item,
        'categorias': categorias
    })


def eliminar_item(request, id):
    item = models.Item.objects.get(id = id)

    try:
        item.delete()
        messages.success(request, "Item eliminado correctamente")
    except ProtectedError:
        messages.error(request, "No puedes eliminar este item porque tiene prestamos asociados")
    

    return redirect('inventario:items')


def prestamos(request):
    prestamos = models.Prestamo.objects.all()
    items = models.Item.objects.all()

    data = {
        "prestamos": prestamos,
        "items": items
    }

    return render(request, 'prestamos.html', data)


def crear_prestamo(request):
    items = models.Item.objects.all()

    return render(request, 'formulario_prestamo.html', {'formulario': forms.FormularioPrestamo, 'items': items})


def guardar_prestamo(request):
    if request.method == "POST":
        devolucion_esperada = request.POST["fecha_devolucion_esperada"]
        estado = request.POST["estado_prestamo"]
        observaciones = request.POST["observaciones_entrega"]
        item = request.POST["item"]
        item_prestamo = models.Item.objects.get(id=item)

        nuevo_prestamo = models.Prestamo.objects.create(
            fecha_devolucion_esperada = devolucion_esperada,
            estado_prestamo = estado,
            observaciones_entrega = observaciones,
            item = item_prestamo,
        )

        return redirect('inventario:prestamos')

    return redirect('inventario:crear_prestamo')


def actualizar_prestamo(request, id):
    prestamo = models.Prestamo.objects.get(id = id)

    if request.method == "POST":
        devolucion_esperada = request.POST["fecha_devolucion_esperada"]
        devolucion = request.POST["fecha_devolucion"]

        if devolucion == "":
            devolucion = None

        estado = request.POST["estado_prestamo"]
        observaciones = request.POST["observaciones_devolucion"]

        prestamo.fecha_devolucion_esperada = devolucion_esperada
        prestamo.fecha_devolucion = devolucion
        prestamo.estado_prestamo = estado
        prestamo.observaciones_devolucion = observaciones

        prestamo.save()

        return redirect('inventario:prestamos')
    else:
        formulario = forms.FormularioPrestamo(initial={
            "fecha_devolucion_esperada": prestamo.fecha_devolucion_esperada,
            "estado_prestamo": prestamo.estado_prestamo,
            "observaciones_devolucion": prestamo.observaciones_devolucion,
            "item": prestamo.item
        })

    return render(request, 'formulario_prestamo.html', {
        'formulario': formulario,
        'prestamo': prestamo,
        'items': items
    })


def eliminar_prestamo(request, id):
    prestamo = models.Prestamo.objects.get(id = id)

    prestamo.delete()

    return redirect('inventario:prestamos')


def lista_inventario(request):
    data = models.Item.objects.all()

    data_envio = {
        'items': data,
    }

    return render(request, 'lista_inventario.html', data_envio)
