from django.shortcuts import render
from django.http import HttpResponse

def detalle_nomina(request):
    datos_nomina = {
        'empleado': 'Juan Pérez',
        'cargo': 'Docente Cátedra',
        'sueldo_base': 2500000,
        'horas_extras': 10,
        'comisiones': 150000,
        'activo': True,
        'conceptos': [
            {'nombre': 'Salario Base', 'valor': 2500000},
            {'nombre': 'Horas Extras', 'valor': 120000},
            {'nombre': 'Auxilio Transporte', 'valor': 140000},
        ]
    }
    return render(request, 'nomina.html', {'nomina': datos_nomina})

