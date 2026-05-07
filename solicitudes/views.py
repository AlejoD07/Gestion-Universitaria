from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist

from .forms.formulario_quejas import FormularioQuejas
from . import models


def _tipo_por_slug(tipo):
    mapa = {
        'solicitud': 'Solicitud',
        'queja': 'Queja',
        'reclamo': 'Reclamo',
    }
    nombre = mapa.get(tipo, tipo or 'Solicitud')
    return get_object_or_404(models.TiposSolicitud, nombre__iexact=nombre)


def _usuario_demo():
    rol, _ = models.Rol.objects.get_or_create(nombre_rol='Estudiante')
    tipo_doc, _ = models.TipoDocumento.objects.get_or_create(nombre_tipo_doc='Cedula')
    usuario, _ = models.Usuario.objects.get_or_create(
        email='usuario@universidad.edu.co',
        defaults={
            'nombre_usuario': 'Usuario Demo',
            'activo': True,
            'id_tipo_documento': tipo_doc,
            'id_rol': rol,
        },
    )
    return usuario


def home(request):
    return render(request, 'solicitudes/home.html')


def home_redirect(request):
    return redirect('solicitudes:home')


def lista_solicitudes(request, tipo=None):
    tipo_solicitud = _tipo_por_slug(tipo) if tipo else None
    solicitudes = models.Solicitud.objects.select_related('usuario', 'tipo', 'estado').order_by('-fecha_creacion')
    if tipo_solicitud:
        solicitudes = solicitudes.filter(tipo=tipo_solicitud)

    return render(request, 'solicitudes/lista_solicitudes.html', {
        'solicitudes': solicitudes,
        'tipo_solicitud': tipo_solicitud,
    })


def ejemplo_for(request, id):
    try:
        solicitud = models.Solicitud.objects.get(id=id)
        return render(request, 'solicitudes/ejemplo_for.html', {'solicitud': solicitud, 'status': 200})
    except Exception as e:
        print("Error al obtener la solicitud:", e)
        return render(request, 'solicitudes/ejemplo_for.html', {'solicitud': None, 'status': 404})


def ejemplo_if(request, id):
    registros = [
        {'id': 1, 'tipo': 'Certificado estudios', 'fecha': '23/03/2026', 'estado': 'Pendiente', 'usuario': 'Pedro Clemente'},
        {'id': 2, 'tipo': 'Cambio de horario', 'fecha': '20/03/2026', 'estado': 'Aprobada', 'usuario': 'Daniel Marquez'},
        {'id': 3, 'tipo': 'Inconformidad con las clases', 'fecha': '24/03/2026', 'estado': 'En proceso', 'usuario': 'Juanita Lopez'},
    ]

    registro = None
    for i in registros:
        if i['id'] == id:
            registro = i
            break

    return render(request, 'solicitudes/ejemplo_if.html', {'registro': registro})


def view_form_quejas(request, tipo=None):
    tipo_solicitud = _tipo_por_slug(tipo) if tipo else None

    if request.method == "GET":
        usuario = _usuario_demo()
        request.session['usuario_id'] = usuario.id
        return render(request, 'solicitudes/formulario_quejas.html', {
            'formulario_quejas': FormularioQuejas,
            'statusForm': 200,
            'tipo_solicitud': tipo_solicitud,
        })

    id_usuario = request.session.get('usuario_id') or _usuario_demo().id
    tipo_id = request.POST['tipos']
    prioridad = request.POST['prioridad']
    observaciones = request.POST['observaciones']
    estado, _ = models.EstadosSolicitud.objects.get_or_create(nombre='Radicada')

    try:
        nueva_solicitud = models.Solicitud.objects.create(
            usuario_id=id_usuario,
            tipo_id=tipo_id,
            estado=estado,
            prioridad=prioridad,
        )

        models.HistorialSolicitud.objects.create(
            solicitud=nueva_solicitud,
            estado=estado,
            comentario=observaciones,
        )

        models.ComentariosSolicitud.objects.create(
            solicitud=nueva_solicitud,
            usuario_id=id_usuario,
            comentario=observaciones,
        )

        return redirect('solicitudes:detalle_solicitud', id=nueva_solicitud.id)
    except Exception as e:
        print("Error al crear la solicitud:", e)
        return render(request, 'solicitudes/formulario_quejas.html', {
            'formulario_quejas': FormularioQuejas,
            'exitoso': False,
            'statusForm': 200,
            'tipo_solicitud': tipo_solicitud,
        })


def detalle_solicitud(request, id):
    try:
        solicitudes = models.HistorialSolicitud.objects.filter(solicitud_id=id).order_by('-fecha')
        return render(request, 'solicitudes/detalle_solicitud.html', {'solicitudes': solicitudes, 'status': 200, 'id': id})
    except ObjectDoesNotExist:
        print("La solicitud con id", id, "no existe.")
        return render(request, 'solicitudes/detalle_solicitud.html', {'solicitud': None, 'status': 404})
