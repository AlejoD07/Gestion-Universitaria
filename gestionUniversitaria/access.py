from django.shortcuts import redirect, render

from gestionAcademica.models import Usuario


MODULOS = {
    'academica': {
        'nombre': 'Gestión Académica',
        'url': '/academica/',
        'descripcion': 'Usuarios, estudiantes, materias, notas y asistencias.',
        'icono': 'M12 3 2 8l10 5 10-5-10-5Zm-7 8.2V15c0 1.7 3.1 4 7 4s7-2.3 7-4v-3.8l-7 3.5-7-3.5Z',
    },
    'contabilidad': {
        'nombre': 'Contabilidad',
        'url': '/contabilidad/',
        'descripcion': 'Presupuestos, nómina e ingresos institucionales.',
        'icono': 'M4 4h16v16H4V4Zm3 3v3h10V7H7Zm0 5v2h3v-2H7Zm5 0v2h5v-2h-5Zm-5 4v2h3v-2H7Zm5 0v2h5v-2h-5Z',
    },
    'rrhh': {
        'nombre': 'Recursos Humanos',
        'url': '/rrhh/inicio/',
        'descripcion': 'Empleados, áreas, novedades y certificados.',
        'icono': 'M12 12a4 4 0 1 0 0-8 4 4 0 0 0 0 8Zm-8 8c.7-3.4 3.8-6 8-6s7.3 2.6 8 6H4Z',
    },
    'inventario': {
        'nombre': 'inventario',
        'url': '/inventario/home/',
        'descripcion': 'Items, categorías, préstamos y control de stock.',
        'icono': 'M4 7l8-4 8 4-8 4-8-4Zm0 3l8 4 8-4v7l-8 4-8-4v-7Z',
    },
    'solicitudes': {
        'nombre': 'Solicitudes',
        'url': '/solicitudes/home/',
        'descripcion': 'Solicitudes, quejas, reclamos y documentos adjuntos.',
        'icono': 'M6 3h9l3 3v15H6V3Zm8 1.5V7h2.5L14 4.5ZM8 10h8v2H8v-2Zm0 4h8v2H8v-2Z',
    },
}

ROLE_MODULES = {
    'super administrador': ['academica', 'contabilidad', 'rrhh', 'inventario', 'solicitudes'],
    'administrador': ['academica', 'contabilidad', 'rrhh', 'inventario', 'solicitudes'],
    'admin': ['academica', 'contabilidad', 'rrhh', 'inventario', 'solicitudes'],
    'profesor': ['academica', 'solicitudes'],
    'estudiante': ['academica', 'solicitudes'],
    'contabilidad': ['contabilidad', 'solicitudes'],
    'contador': ['contabilidad', 'solicitudes'],
    'recursos humanos': ['rrhh', 'solicitudes'],
    'rrhh': ['rrhh', 'solicitudes'],
    'inventario': ['inventario', 'solicitudes'],
    'solicitudes': ['solicitudes'],
}


def normalizar_rol(nombre):
    return str(nombre or '').strip().lower()


def modulos_por_rol(nombre_rol):
    rol = normalizar_rol(nombre_rol)
    if rol in ROLE_MODULES:
        return ROLE_MODULES[rol]
    if 'super' in rol:
        return ROLE_MODULES['super administrador']
    if 'admin' in rol:
        return ROLE_MODULES['administrador']
    if 'prof' in rol:
        return ROLE_MODULES['profesor']
    if 'estudiante' in rol:
        return ROLE_MODULES['estudiante']
    if 'cont' in rol:
        return ROLE_MODULES['contabilidad']
    if 'humano' in rol or 'rrhh' in rol:
        return ROLE_MODULES['recursos humanos']
    if 'invent' in rol:
        return ROLE_MODULES['inventario']
    return ['solicitudes']


def guardar_usuario_en_sesion(request, usuario):
    rol = usuario.id_rol.nombre_rol
    modulos = modulos_por_rol(rol)
    request.session['usuario_academico_id'] = usuario.id_usuario
    request.session['usuario_nombre'] = usuario.nombre_usuario
    request.session['usuario_rol'] = rol
    request.session['usuario_modulos'] = modulos


def usuario_actual(request):
    usuario_id = request.session.get('usuario_academico_id')
    if not usuario_id:
        return None
    try:
        return Usuario.objects.select_related('id_rol', 'id_tipo_documento', 'facultad').get(id_usuario=usuario_id, activo=True)
    except Usuario.DoesNotExist:
        request.session.flush()
        return None


def modulos_visibles(request):
    permitidos = request.session.get('usuario_modulos', [])
    return [dict(MODULOS[clave], clave=clave) for clave in permitidos if clave in MODULOS]


def puede_ver_modulo(request, modulo):
    return modulo in request.session.get('usuario_modulos', [])


def es_administrador_global(request):
    rol = normalizar_rol(request.session.get('usuario_rol'))
    return 'admin' in rol or 'super' in rol
