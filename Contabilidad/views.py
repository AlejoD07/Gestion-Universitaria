from django.shortcuts import render, get_object_or_404, redirect
from .models import Nomina, Presupuesto, Ingreso


# ---------- INICIO ----------

def inicio(request):
    total_nominas = Nomina.objects.count()
    total_presupuestos = Presupuesto.objects.count()
    total_ingresos = Ingreso.objects.count()

    context = {
        'total_nominas': total_nominas,
        'total_presupuestos': total_presupuestos,
        'total_ingresos': total_ingresos,
    }
    return render(request, 'contabilidad/paginas/inicio.html', context)


# ---------- NOMINAS ----------

def lista_nominas(request):
    nominas = Nomina.objects.all()
    return render(request, 'contabilidad/paginas/nominas.html', {'nominas': nominas})


def crear_nomina(request):
    if request.method == 'POST':
        nomina = Nomina()
        nomina.empleado_nombre = request.POST['empleado_nombre']
        nomina.empleado_cedula = request.POST['empleado_cedula']
        nomina.cargo = request.POST['cargo']
        nomina.area = request.POST['area']
        nomina.mes = request.POST['mes']
        nomina.anio = request.POST['anio']
        nomina.salario_base = request.POST['salario_base']
        nomina.horas_extras = request.POST.get('horas_extras', 0)
        nomina.comisiones = request.POST.get('comisiones', 0)
        nomina.deducciones = request.POST.get('deducciones', 0)
        nomina.fecha_pago = request.POST['fecha_pago']
        nomina.estado = request.POST.get('estado', 'pendiente')
        nomina.calcular_total()
        nomina.save()
        return redirect('lista_nominas')

    return render(request, 'contabilidad/paginas/crear_nomina.html')


def editar_nomina(request, id):
    nomina = get_object_or_404(Nomina, id=id)

    if request.method == 'POST':
        nomina.empleado_nombre = request.POST['empleado_nombre']
        nomina.empleado_cedula = request.POST['empleado_cedula']
        nomina.cargo = request.POST['cargo']
        nomina.area = request.POST['area']
        nomina.mes = request.POST['mes']
        nomina.anio = request.POST['anio']
        nomina.salario_base = request.POST['salario_base']
        nomina.horas_extras = request.POST.get('horas_extras', 0)
        nomina.comisiones = request.POST.get('comisiones', 0)
        nomina.deducciones = request.POST.get('deducciones', 0)
        nomina.fecha_pago = request.POST['fecha_pago']
        nomina.estado = request.POST.get('estado', 'pendiente')
        nomina.calcular_total()
        nomina.save()
        return redirect('lista_nominas')

    return render(request, 'contabilidad/paginas/editar_nomina.html', {'nomina': nomina})


def eliminar_nomina(request, id):
    nomina = get_object_or_404(Nomina, id=id)
    nomina.delete()
    return redirect('lista_nominas')


# ---------- PRESUPUESTOS ----------

def lista_presupuestos(request):
    presupuestos = Presupuesto.objects.all()
    return render(request, 'contabilidad/paginas/presupuestos.html', {'presupuestos': presupuestos})


def crear_presupuesto(request):
    if request.method == 'POST':
        presupuesto = Presupuesto()
        presupuesto.nombre = request.POST['nombre']
        presupuesto.area = request.POST['area']
        presupuesto.monto_asignado = request.POST['monto_asignado']
        presupuesto.monto_gastado = request.POST.get('monto_gastado', 0)
        presupuesto.mes = request.POST['mes']
        presupuesto.anio = request.POST['anio']
        presupuesto.descripcion = request.POST.get('descripcion', '')
        presupuesto.save()
        return redirect('lista_presupuestos')

    return render(request, 'contabilidad/paginas/crear_presupuesto.html')


def editar_presupuesto(request, id):
    presupuesto = get_object_or_404(Presupuesto, id=id)

    if request.method == 'POST':
        presupuesto.nombre = request.POST['nombre']
        presupuesto.area = request.POST['area']
        presupuesto.monto_asignado = request.POST['monto_asignado']
        presupuesto.monto_gastado = request.POST.get('monto_gastado', 0)
        presupuesto.mes = request.POST['mes']
        presupuesto.anio = request.POST['anio']
        presupuesto.descripcion = request.POST.get('descripcion', '')
        presupuesto.save()
        return redirect('lista_presupuestos')

    return render(request, 'contabilidad/paginas/editar_presupuesto.html', {'presupuesto': presupuesto})


def eliminar_presupuesto(request, id):
    presupuesto = get_object_or_404(Presupuesto, id=id)
    presupuesto.delete()
    return redirect('lista_presupuestos')


# ---------- INGRESOS ----------

def lista_ingresos(request):
    ingresos = Ingreso.objects.all()
    return render(request, 'contabilidad/paginas/ingresos.html', {'ingresos': ingresos})


def crear_ingreso(request):
    if request.method == 'POST':
        ingreso = Ingreso()
        ingreso.concepto = request.POST['concepto']
        ingreso.monto = request.POST['monto']
        ingreso.fecha = request.POST['fecha']
        ingreso.fuente = request.POST['fuente']
        ingreso.descripcion = request.POST.get('descripcion', '')
        ingreso.save()
        return redirect('lista_ingresos')

    return render(request, 'contabilidad/paginas/crear_ingreso.html')


def eliminar_ingreso(request, id):
    ingreso = get_object_or_404(Ingreso, id=id)
    ingreso.delete()
    return redirect('lista_ingresos')
