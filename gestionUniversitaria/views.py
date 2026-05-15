from django.shortcuts import redirect, render

from gestionAcademica.models import Usuario
from .access import guardar_usuario_en_sesion, modulos_visibles


def login_view(request):
    if request.session.get('usuario_academico_id'):
        return redirect('home_general')

    error = None
    siguiente = request.GET.get('next') or request.POST.get('next') or ''

    if request.method == 'POST':
        documento = request.POST.get('documento')
        clave = request.POST.get('clave')
        try:
            usuario = Usuario.objects.select_related('id_rol').get(id_usuario=documento, activo=True)
            if usuario.nombre_usuario == clave:
                guardar_usuario_en_sesion(request, usuario)
                if siguiente.startswith('/') and not siguiente.startswith('//'):
                    return redirect(siguiente)
                return redirect('home_general')
            error = 'Documento o clave incorrectos.'
        except Usuario.DoesNotExist:
            error = 'Documento o clave incorrectos.'

    return render(request, 'login.html', {'error': error, 'next': siguiente})


def logout_view(request):
    request.session.flush()
    return redirect('login')


def dashboard(request):
    if not request.session.get('usuario_academico_id'):
        return redirect('login')

    return render(request, 'home_general.html', {
        'modulos': modulos_visibles(request),
        'usuario_nombre': request.session.get('usuario_nombre'),
        'usuario_rol': request.session.get('usuario_rol'),
    })


def sin_permiso(request):
    return render(request, 'sin_permiso.html', status=403)
