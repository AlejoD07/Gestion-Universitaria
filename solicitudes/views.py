from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist

# from .forms.formulario_registro import FormularioRegistro
from .forms.formulario_quejas import FormularioQuejas
from . import models

# Create your views here.
def home(request):
    return render(request, 'home.html')

def home_redirect(request):
    return redirect('home')

def ejemplo_for(request, id):
    try:
        solicitud = models.Solicitud.objects.get(id=id)
        return render(request, 'ejemplo_for.html', {'solicitud': solicitud, 'status': 200})
    except Exception as e:
        print("Error al obtener la solicitud:", e)
        return render(request, 'ejemplo_for.html', {'solicitud': None, 'status': 404})

def ejemplo_if(request, id):
	registros = [
		{
			'id': 1,
			'tipo': 'Certificado estudios',
			'fecha': '23/03/2026',
			'estado': 'Pendiente',
			'usuario': 'Pedro Clemente'
		},
		{
			'id': 2,
            'tipo': 'Cambio de horario',
            'fecha': '20/03/2026',
            'estado': 'Aprobada',
            'usuario': 'Daniel Márquez'
		},
		{
			'id': 3,
            'tipo': 'Inconformidad con las clases',
            'fecha': '24/03/2026',
            'estado': 'En proceso',
            'usuario': 'Juanita López'
		}
	]

	registro = None

	for i in registros:
		if i ['id'] == id:
			registro = i
			break

	return render(request, 'ejemplo_if.html', {'registro': registro})

# def view_form_registro(request):

#     return render(request, 'formulario_registro.html', {'form': FormularioRegistro})

def view_form_quejas(request):
    if request.method == "GET":
        request.session['usuario_id'] = 1
        return render(request, 'formulario_quejas.html', {'formulario_quejas': FormularioQuejas, 'statusForm': 200})
    elif request.method == "POST":
        # Insertar BD
        print("Hola", request.POST["tipos"], request.POST["prioridad"], request.POST["observaciones"])
        
        id = request.session.get('usuario_id')
        tipos = request.POST["tipos"]
        prioridad = request.POST["prioridad"]
        observaciones = request.POST["observaciones"]

        try:
            nueva_solicitud = models.Solicitud.objects.create(
                usuario_id=id,
                tipo_id=tipos,
                estado_id=4,
                prioridad=prioridad
            )
            print("\nSolicitud creada con éxito:", nueva_solicitud)

            historial = models.HistorialSolicitud.objects.create(
                solicitud=nueva_solicitud,
                estado_id=4,
                comentario=observaciones
            )
            print("\nHistorial creado con éxito:", historial)

            comentario = models.ComentariosSolicitud.objects.create(
                solicitud=nueva_solicitud,
                usuario_id=id,
                comentario=observaciones
            )
            print("\nComentario creada con éxito:", nueva_solicitud)

            return redirect('solicitudes:detalle_solicitud', id=nueva_solicitud.id)
        
        except Exception as e:
            print("Error al crear la solicitud:", e)
            return render(request, 'formulario_quejas.html', {'formulario_quejas': FormularioQuejas, 'exitoso': False})
        
def detalle_solicitud(request, id):
    try:
        solicitudes = models.HistorialSolicitud.objects.filter(solicitud_id=id).order_by('-fecha')

        return render(request, 'detalle_solicitud.html', {'solicitudes': solicitudes, 'status': 200, 'id': id})
    except ObjectDoesNotExist:
        print("La solicitud con id", id, "no existe.")
        return render(request, 'detalle_solicitud.html', {'solicitud': None, 'status': 404})