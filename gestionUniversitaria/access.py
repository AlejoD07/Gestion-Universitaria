import unicodedata

from gestionAcademica.models import PermisoRolModulo, Usuario


MODULOS = {
    'academica': {
        'nombre': 'Gestion Academica',
        'url': '/academica/',
        'descripcion': 'Usuarios academicos, estudiantes, programas, materias, inscripciones, notas y asistencias.',
        'icono': 'M12 3 2 8l10 5 10-5-10-5Zm-7 8.2V15c0 1.7 3.1 4 7 4s7-2.3 7-4v-3.8l-7 3.5-7-3.5Z',
    },
    'contabilidad': {
        'nombre': 'Contabilidad',
        'url': '/contabilidad/',
        'descripcion': 'Presupuestos, nomina, ingresos y areas del organigrama financiero.',
        'icono': 'M4 4h16v16H4V4Zm3 3v3h10V7H7Zm0 5v2h3v-2H7Zm5 0v2h5v-2h-5Zm-5 4v2h3v-2H7Zm5 0v2h5v-2h-5Z',
    },
    'rrhh': {
        'nombre': 'Recursos Humanos',
        'url': '/rrhh/inicio/',
        'descripcion': 'Empleados, areas de trabajo, novedades y certificados laborales.',
        'icono': 'M12 12a4 4 0 1 0 0-8 4 4 0 0 0 0 8Zm-8 8c.7-3.4 3.8-6 8-6s7.3 2.6 8 6H4Z',
    },
    'inventario': {
        'nombre': 'inventario',
        'url': '/inventario/home/',
        'descripcion': 'Items, categorias, prestamos y control de stock academico.',
        'icono': 'M4 7l8-4 8 4-8 4-8-4Zm0 3l8 4 8-4v7l-8 4-8-4v-7Z',
    },
    'solicitudes': {
        'nombre': 'Solicitudes',
        'url': '/solicitudes/home/',
        'descripcion': 'Radicacion y seguimiento de solicitudes, quejas, reclamos y adjuntos.',
        'icono': 'M6 3h9l3 3v15H6V3Zm8 1.5V7h2.5L14 4.5ZM8 10h8v2H8v-2Zm0 4h8v2H8v-2Z',
    },
}

TODOS_LOS_MODULOS = ['academica', 'contabilidad', 'rrhh', 'inventario', 'solicitudes']

ROLE_MODULES = {
    'super administrador': TODOS_LOS_MODULOS,
    'administrador general': TODOS_LOS_MODULOS,
    'administrador': TODOS_LOS_MODULOS,
    'admin': TODOS_LOS_MODULOS,

    'coordinador academico': ['academica', 'solicitudes'],
    'profesor': ['academica', 'solicitudes'],
    'estudiante': ['academica', 'solicitudes'],

    'contador': ['contabilidad', 'solicitudes'],
    'contabilidad': ['contabilidad', 'solicitudes'],
    'director financiero': ['contabilidad', 'solicitudes'],
    'auxiliar contable': ['contabilidad', 'solicitudes'],

    'recursos humanos': ['rrhh', 'solicitudes'],
    'rrhh': ['rrhh', 'solicitudes'],
    'director talento humano': ['rrhh', 'solicitudes'],
    'auxiliar talento humano': ['rrhh', 'solicitudes'],

    'inventario': ['inventario', 'solicitudes'],
    'coordinador inventario': ['inventario', 'solicitudes'],
    'auxiliar inventario': ['inventario', 'solicitudes'],

    'solicitudes': ['solicitudes'],
    'gestor solicitudes': ['solicitudes'],
}


def normalizar_rol(nombre):
    texto = str(nombre or '').strip().lower()
    texto = unicodedata.normalize('NFKD', texto)
    return ''.join(caracter for caracter in texto if not unicodedata.combining(caracter))


def modulos_por_rol(nombre_rol):
    permisos_bd = modulos_por_rol_bd(nombre_rol)
    if permisos_bd is not None:
        return permisos_bd
    return modulos_por_rol_predeterminado(nombre_rol)


def modulos_por_rol_predeterminado(nombre_rol):
    rol = normalizar_rol(nombre_rol)
    if rol in ROLE_MODULES:
        return ROLE_MODULES[rol]
    if 'super' in rol or 'admin' in rol or 'rector' in rol:
        return TODOS_LOS_MODULOS
    if 'prof' in rol or 'estudiante' in rol or 'academ' in rol:
        return ['academica', 'solicitudes']
    if 'cont' in rol or 'financ' in rol:
        return ['contabilidad', 'solicitudes']
    if 'humano' in rol or 'talento' in rol or 'rrhh' in rol:
        return ['rrhh', 'solicitudes']
    if 'invent' in rol:
        return ['inventario', 'solicitudes']
    if 'solicitud' in rol:
        return ['solicitudes']
    return ['solicitudes']


def modulos_por_rol_bd(nombre_rol):
    rol_normalizado = normalizar_rol(nombre_rol)
    permisos = (
        PermisoRolModulo.objects
        .select_related('rol')
        .filter(rol__nombre_rol__iexact=str(nombre_rol or '').strip())
    )
    if not permisos.exists():
        permisos = [
            permiso
            for permiso in PermisoRolModulo.objects.select_related('rol').all()
            if normalizar_rol(permiso.rol.nombre_rol) == rol_normalizado
        ]
        if not permisos:
            return None
        return [permiso.modulo for permiso in permisos if permiso.activo]
    return list(permisos.filter(activo=True).values_list('modulo', flat=True))


def permisos_iniciales_para_rol(nombre_rol):
    return list(modulos_por_rol_predeterminado(nombre_rol))


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
    return rol in ('super administrador', 'administrador general', 'administrador', 'admin') or 'super' in rol
