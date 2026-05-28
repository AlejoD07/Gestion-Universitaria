from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

from gestionAcademica.models import PermisoRolModulo, Rol, Usuario
from .access import (
    MODULOS,
    es_administrador_global,
    guardar_usuario_en_sesion,
    modulos_por_rol,
    modulos_visibles,
    normalizar_rol,
    permisos_iniciales_para_rol,
)


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
        'es_admin_global': es_administrador_global(request),
    })


def sin_permiso(request):
    return render(request, 'sin_permiso.html', status=403)


def administrar_permisos_roles(request):
    if not request.session.get('usuario_academico_id'):
        return redirect('login')
    if not es_administrador_global(request):
        return redirect('sin_permiso')

    roles = Rol.objects.all().order_by('nombre_rol')
    _asegurar_permisos_roles(roles)

    if request.method == 'POST':
        rol = get_object_or_404(Rol, id_rol=request.POST.get('rol_id'))
        modulos_seleccionados = set(request.POST.getlist('modulos'))

        for clave in MODULOS.keys():
            permiso, _ = PermisoRolModulo.objects.get_or_create(
                rol=rol,
                modulo=clave,
                defaults={'activo': clave in modulos_seleccionados},
            )
            permiso.activo = clave in modulos_seleccionados
            permiso.save(update_fields=['activo'])

        if normalizar_rol(request.session.get('usuario_rol')) == normalizar_rol(rol.nombre_rol):
            request.session['usuario_modulos'] = modulos_por_rol(rol.nombre_rol)

        messages.success(request, f'Permisos actualizados para el rol {rol.nombre_rol}.')
        return redirect('administrar_permisos_roles')

    permisos_por_rol = []
    for rol in roles:
        permisos = {
            permiso.modulo: permiso.activo
            for permiso in rol.permisos_modulo.all()
        }
        modulos = [
            {
                'clave': clave,
                'nombre': datos['nombre'],
                'descripcion': datos['descripcion'],
                'activo': permisos.get(clave, False),
            }
            for clave, datos in MODULOS.items()
        ]
        permisos_por_rol.append({
            'rol': rol,
            'modulos': modulos,
        })

    return render(request, 'admin_permisos_roles.html', {
        'modulos_sistema': MODULOS,
        'permisos_por_rol': permisos_por_rol,
    })


def _asegurar_permisos_roles(roles):
    for rol in roles:
        modulos_default = set(permisos_iniciales_para_rol(rol.nombre_rol))
        for clave in MODULOS.keys():
            PermisoRolModulo.objects.get_or_create(
                rol=rol,
                modulo=clave,
                defaults={'activo': clave in modulos_default},
            )
