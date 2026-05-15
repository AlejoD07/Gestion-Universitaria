from django.shortcuts import redirect
from django.urls import reverse

from .access import normalizar_rol, puede_ver_modulo


class RoleAccessMiddleware:
    MODULOS_POR_PREFIJO = {
        '/academica/': 'academica',
        '/contabilidad/': 'contabilidad',
        '/inventario/': 'inventario',
        '/rrhh/': 'rrhh',
        '/solicitudes/': 'solicitudes',
    }

    RUTAS_LIBRES = (
        '/login/',
        '/salir/',
        '/sin-permiso/',
        '/admin/',
        '/static/',
        '/media/',
    )

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path = request.path
        if path == '/' or any(path.startswith(ruta) for ruta in self.RUTAS_LIBRES):
            return self.get_response(request)

        for prefijo, modulo in self.MODULOS_POR_PREFIJO.items():
            if path.startswith(prefijo):
                if not request.session.get('usuario_academico_id'):
                    return redirect(f"{reverse('login')}?next={path}")
                if not puede_ver_modulo(request, modulo):
                    return redirect('sin_permiso')
                if modulo == 'academica' and self._academica_restringida(request, path):
                    return redirect('sin_permiso')
                break

        return self.get_response(request)

    def _academica_restringida(self, request, path):
        rol = normalizar_rol(request.session.get('usuario_rol'))
        if 'admin' in rol or 'super' in rol:
            return False
        if not ('prof' in rol or 'estudiante' in rol):
            return False

        rutas_lectura = (
            '/academica/',
            '/academica/inicio/',
            '/academica/materias/',
            '/academica/inscripciones/',
            '/academica/notas/',
            '/academica/asistencias/',
        )
        acciones_bloqueadas = ('/crear/', '/editar/', '/eliminar/')
        if any(accion in path for accion in acciones_bloqueadas):
            return True
        return not any(path == ruta for ruta in rutas_lectura)
