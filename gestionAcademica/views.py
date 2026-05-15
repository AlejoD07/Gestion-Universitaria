from django.contrib import messages
from django.db.models import ProtectedError
from django.db.models import Q
from decimal import Decimal, InvalidOperation
from django.shortcuts import get_object_or_404, redirect, render
from gestionUniversitaria.access import es_administrador_global, usuario_actual

from .models import (
    Asistencia,
    Estudiante,
    Facultad,
    Inscripcion,
    Materia,
    Nota,
    PeriodoAcademico,
    Programa,
    Rol,
    TipoDocumento,
    Usuario,
)



def _es_profesor_actual(request):
    rol = str(request.session.get('usuario_rol', '')).lower()
    return 'prof' in rol and not es_administrador_global(request)


def _profesor_actual(request):
    if not _es_profesor_actual(request):
        return None
    return usuario_actual(request)


def _materias_visibles(request):
    materias = Materia.objects.select_related('programa', 'programa__facultad', 'profesor')
    profesor = _profesor_actual(request)
    if profesor:
        materias = materias.filter(profesor=profesor)
    return materias


def _inscripciones_visibles(request):
    inscripciones = Inscripcion.objects.select_related('estudiante', 'materia', 'materia__profesor', 'periodo')
    profesor = _profesor_actual(request)
    if profesor:
        inscripciones = inscripciones.filter(materia__profesor=profesor)
    return inscripciones
def _opciones(queryset, seleccionado=None):
    return [
        {
            'valor': objeto.pk,
            'texto': str(objeto),
            'seleccionado': str(objeto.pk) == str(seleccionado),
        }
        for objeto in queryset
    ]


def _opciones_inscripciones(request, seleccionado=None):
    inscripciones = _inscripciones_visibles(request)
    return [
        {
            'valor': inscripcion.pk,
            'texto': f'{inscripcion.estudiante} - {inscripcion.materia} - {inscripcion.periodo}',
            'seleccionado': str(inscripcion.pk) == str(seleccionado),
        }
        for inscripcion in inscripciones
    ]


def _eliminar_registro(request, modelo, pk, redireccion):
    registro = get_object_or_404(modelo, pk=pk)
    try:
        registro.delete()
    except ProtectedError:
        messages.error(request, 'No se puede eliminar este registro porque tiene informacion relacionada.')
    return redirect(redireccion)


def _validar_valor_nota(request):
    try:
        valor = Decimal(request.POST['valor'])
    except (InvalidOperation, KeyError):
        messages.error(request, 'La nota debe ser un numero valido.')
        return None

    if valor < Decimal('0') or valor > Decimal('5.00'):
        messages.error(request, 'La nota debe estar entre 0.00 y 5.00.')
        return None

    return valor


def _actualizar_promedio_estudiante(estudiante):
    valores = Nota.objects.filter(
        inscripcion__estudiante=estudiante
    ).values_list('valor', flat=True)

    if valores:
        promedio = sum(valores) / Decimal(len(valores))
    else:
        promedio = Decimal('0')

    estudiante.promedio = promedio.quantize(Decimal('0.01'))
    estudiante.save()


def inicio(request):
    context = {
        'total_usuarios': Usuario.objects.count(),
        'total_profesores': Usuario.objects.filter(id_rol__nombre_rol__icontains='prof').count(),
        'total_estudiantes': Estudiante.objects.count(),
        'total_materias': _materias_visibles(request).count(),
        'total_inscripciones': _inscripciones_visibles(request).count(),
        'total_notas': Nota.objects.count(),
        'total_asistencias': Asistencia.objects.count(),
    }
    return render(request, 'gestionAcademica/paginas/inicio.html', context)


def lista_roles(request):
    roles = Rol.objects.all()
    filas = [[rol.id_rol, rol.nombre_rol, rol.id_rol] for rol in roles]
    return render(request, 'gestionAcademica/paginas/lista.html', {
        'titulo': 'Roles',
        'crear_url': 'crear_rol',
        'encabezados': ['ID', 'Nombre', 'Acciones'],
        'filas': filas,
        'editar_url': 'editar_rol',
        'eliminar_url': 'eliminar_rol',
        'vacio': 'No hay roles registrados.',
    })


def crear_rol(request):
    if request.method == 'POST':
        Rol.objects.create(
            id_rol=request.POST['id_rol'],
            nombre_rol=request.POST['nombre_rol'],
        )
        return redirect('lista_roles')
    return render(request, 'gestionAcademica/paginas/formulario.html', {
        'titulo': 'Nuevo Rol',
        'volver_url': 'lista_roles',
        'campos': [
            {'label': 'ID rol', 'name': 'id_rol', 'type': 'number', 'required': True},
            {'label': 'Nombre rol', 'name': 'nombre_rol', 'type': 'text', 'required': True},
        ],
    })


def editar_rol(request, id):
    rol = get_object_or_404(Rol, id_rol=id)
    if request.method == 'POST':
        rol.nombre_rol = request.POST['nombre_rol']
        rol.save()
        return redirect('lista_roles')
    return render(request, 'gestionAcademica/paginas/formulario.html', {
        'titulo': 'Editar Rol',
        'volver_url': 'lista_roles',
        'campos': [
            {'label': 'Nombre rol', 'name': 'nombre_rol', 'type': 'text', 'value': rol.nombre_rol, 'required': True},
        ],
    })


def eliminar_rol(request, id):
    return _eliminar_registro(request, Rol, id, 'lista_roles')


def lista_tipos_documento(request):
    tipos = TipoDocumento.objects.all()
    filas = [[tipo.id_tipo_doc, tipo.nombre_tipo_doc, tipo.id_tipo_doc] for tipo in tipos]
    return render(request, 'gestionAcademica/paginas/lista.html', {
        'titulo': 'Tipos de Documento',
        'crear_url': 'crear_tipo_documento',
        'encabezados': ['ID', 'Nombre', 'Acciones'],
        'filas': filas,
        'editar_url': 'editar_tipo_documento',
        'eliminar_url': 'eliminar_tipo_documento',
        'vacio': 'No hay tipos de documento registrados.',
    })


def crear_tipo_documento(request):
    if request.method == 'POST':
        TipoDocumento.objects.create(
            id_tipo_doc=request.POST['id_tipo_doc'],
            nombre_tipo_doc=request.POST['nombre_tipo_doc'],
        )
        return redirect('lista_tipos_documento')
    return render(request, 'gestionAcademica/paginas/formulario.html', {
        'titulo': 'Nuevo Tipo de Documento',
        'volver_url': 'lista_tipos_documento',
        'campos': [
            {'label': 'ID tipo documento', 'name': 'id_tipo_doc', 'type': 'number', 'required': True},
            {'label': 'Nombre', 'name': 'nombre_tipo_doc', 'type': 'text', 'required': True},
        ],
    })


def editar_tipo_documento(request, id):
    tipo = get_object_or_404(TipoDocumento, id_tipo_doc=id)
    if request.method == 'POST':
        tipo.nombre_tipo_doc = request.POST['nombre_tipo_doc']
        tipo.save()
        return redirect('lista_tipos_documento')
    return render(request, 'gestionAcademica/paginas/formulario.html', {
        'titulo': 'Editar Tipo de Documento',
        'volver_url': 'lista_tipos_documento',
        'campos': [
            {'label': 'Nombre', 'name': 'nombre_tipo_doc', 'type': 'text', 'value': tipo.nombre_tipo_doc, 'required': True},
        ],
    })


def eliminar_tipo_documento(request, id):
    return _eliminar_registro(request, TipoDocumento, id, 'lista_tipos_documento')


def lista_usuarios(request):
    usuarios = Usuario.objects.select_related('id_tipo_documento', 'id_rol')
    filas = [
        [
            usuario.id_usuario,
            usuario.nombre_usuario,
            usuario.id_tipo_documento,
            usuario.id_rol,
            'Activo' if usuario.activo else 'Inactivo',
            usuario.id_usuario,
        ]
        for usuario in usuarios
    ]
    return render(request, 'gestionAcademica/paginas/lista.html', {
        'titulo': 'Usuarios',
        'crear_url': 'crear_usuario',
        'encabezados': ['Documento', 'Nombre', 'Tipo', 'Rol', 'Estado', 'Acciones'],
        'filas': filas,
        'editar_url': 'editar_usuario',
        'eliminar_url': 'eliminar_usuario',
        'vacio': 'No hay usuarios registrados.',
    })


def lista_profesores(request):
    profesores = Usuario.objects.select_related('id_tipo_documento', 'id_rol').filter(
        Q(id_rol__nombre_rol__icontains='profesor') | Q(id_rol__nombre_rol__icontains='prof')
    )
    filas = [
        [
            profesor.id_usuario,
            profesor.nombre_usuario,
            profesor.id_tipo_documento,
            profesor.id_rol,
            'Activo' if profesor.activo else 'Inactivo',
            profesor.id_usuario,
        ]
        for profesor in profesores
    ]
    return render(request, 'gestionAcademica/paginas/lista.html', {
        'titulo': 'Profesores',
        'crear_url': 'crear_usuario',
        'encabezados': ['Documento', 'Nombre', 'Tipo', 'Rol', 'Estado', 'Acciones'],
        'filas': filas,
        'editar_url': 'editar_usuario',
        'eliminar_url': 'eliminar_usuario',
        'vacio': 'No hay profesores registrados.',
    })


def crear_usuario(request):
    if request.method == 'POST':
        Usuario.objects.create(
            id_usuario=request.POST['id_usuario'],
            nombre_usuario=request.POST['nombre_usuario'],
            activo=request.POST.get('activo') == 'on',
            id_tipo_documento=get_object_or_404(TipoDocumento, pk=request.POST['id_tipo_documento']),
            id_rol=get_object_or_404(Rol, pk=request.POST['id_rol']),
            facultad=get_object_or_404(Facultad, pk=request.POST['facultad']) if request.POST.get('facultad') else None,
        )
        return redirect('lista_usuarios')
    return _render_usuario_form(request, 'Nuevo Usuario', 'lista_usuarios')


def editar_usuario(request, id):
    usuario = get_object_or_404(Usuario, id_usuario=id)
    if request.method == 'POST':
        usuario.nombre_usuario = request.POST['nombre_usuario']
        usuario.activo = request.POST.get('activo') == 'on'
        usuario.id_tipo_documento = get_object_or_404(TipoDocumento, pk=request.POST['id_tipo_documento'])
        usuario.id_rol = get_object_or_404(Rol, pk=request.POST['id_rol'])
        usuario.facultad = get_object_or_404(Facultad, pk=request.POST['facultad']) if request.POST.get('facultad') else None
        usuario.save()
        return redirect('lista_usuarios')
    return _render_usuario_form(request, 'Editar Usuario', 'lista_usuarios', usuario)


def _render_usuario_form(request, titulo, volver_url, usuario=None):
    campos = []
    if usuario is None:
        campos.append({'label': 'Documento usuario', 'name': 'id_usuario', 'type': 'number', 'required': True})
    campos.extend([
        {'label': 'Nombre usuario', 'name': 'nombre_usuario', 'type': 'text', 'value': getattr(usuario, 'nombre_usuario', ''), 'required': True},
        {'label': 'Tipo documento', 'name': 'id_tipo_documento', 'type': 'select', 'required': True, 'options': _opciones(TipoDocumento.objects.all(), getattr(getattr(usuario, 'id_tipo_documento', None), 'pk', None))},
        {'label': 'Rol', 'name': 'id_rol', 'type': 'select', 'required': True, 'options': _opciones(Rol.objects.all(), getattr(getattr(usuario, 'id_rol', None), 'pk', None))},
        {'label': 'Facultad', 'name': 'facultad', 'type': 'select', 'options': _opciones(Facultad.objects.filter(activa=True), getattr(getattr(usuario, 'facultad', None), 'pk', None))},
        {'label': 'Activo', 'name': 'activo', 'type': 'checkbox', 'checked': True if usuario is None else usuario.activo},
    ])
    return render(request, 'gestionAcademica/paginas/formulario.html', {'titulo': titulo, 'volver_url': volver_url, 'campos': campos})


def eliminar_usuario(request, id):
    return _eliminar_registro(request, Usuario, id, 'lista_usuarios')


def lista_programas(request):
    programas = Programa.objects.select_related('facultad')
    filas = [[programa.nombre, programa.facultad or 'Sin facultad', programa.id] for programa in programas]
    return render(request, 'gestionAcademica/paginas/lista.html', {
        'titulo': 'Programas',
        'crear_url': 'crear_programa',
        'encabezados': ['Nombre', 'Facultad', 'Acciones'],
        'filas': filas,
        'editar_url': 'editar_programa',
        'eliminar_url': 'eliminar_programa',
        'vacio': 'No hay programas registrados.',
    })


def crear_programa(request):
    if request.method == 'POST':
        Programa.objects.create(nombre=request.POST['nombre'], facultad=get_object_or_404(Facultad, pk=request.POST['facultad']) if request.POST.get('facultad') else None)
        return redirect('lista_programas')
    return render(request, 'gestionAcademica/paginas/formulario.html', {
        'titulo': 'Nuevo Programa',
        'volver_url': 'lista_programas',
        'campos': [
            {'label': 'Nombre', 'name': 'nombre', 'type': 'text', 'required': True},
            {'label': 'Facultad', 'name': 'facultad', 'type': 'select', 'options': _opciones(Facultad.objects.filter(activa=True))},
        ],
    })


def editar_programa(request, id):
    programa = get_object_or_404(Programa, id=id)
    if request.method == 'POST':
        programa.nombre = request.POST['nombre']
        programa.facultad = get_object_or_404(Facultad, pk=request.POST['facultad']) if request.POST.get('facultad') else None
        programa.save()
        return redirect('lista_programas')
    return render(request, 'gestionAcademica/paginas/formulario.html', {
        'titulo': 'Editar Programa',
        'volver_url': 'lista_programas',
        'campos': [
            {'label': 'Nombre', 'name': 'nombre', 'type': 'text', 'value': programa.nombre, 'required': True},
            {'label': 'Facultad', 'name': 'facultad', 'type': 'select', 'options': _opciones(Facultad.objects.filter(activa=True), getattr(getattr(programa, 'facultad', None), 'pk', None))},
        ],
    })


def eliminar_programa(request, id):
    return _eliminar_registro(request, Programa, id, 'lista_programas')


def lista_estudiantes(request):
    estudiantes = Estudiante.objects.select_related('usuario')
    filas = [[estudiante.usuario, estudiante.codigo_estudiante, estudiante.semestre, estudiante.promedio, estudiante.id] for estudiante in estudiantes]
    return render(request, 'gestionAcademica/paginas/lista.html', {
        'titulo': 'Estudiantes',
        'crear_url': 'crear_estudiante',
        'encabezados': ['Usuario', 'Codigo', 'Semestre', 'Promedio', 'Acciones'],
        'filas': filas,
        'editar_url': 'editar_estudiante',
        'eliminar_url': 'eliminar_estudiante',
        'vacio': 'No hay estudiantes registrados.',
    })


def crear_estudiante(request):
    if request.method == 'POST':
        Estudiante.objects.create(
            usuario=get_object_or_404(Usuario, pk=request.POST['usuario']),
            codigo_estudiante=request.POST['codigo_estudiante'],
            semestre=request.POST['semestre'],
            promedio=request.POST.get('promedio', 0),
        )
        return redirect('lista_estudiantes')
    return _render_estudiante_form(request, 'Nuevo Estudiante', 'lista_estudiantes')


def editar_estudiante(request, id):
    estudiante = get_object_or_404(Estudiante, id=id)
    if request.method == 'POST':
        estudiante.usuario = get_object_or_404(Usuario, pk=request.POST['usuario'])
        estudiante.codigo_estudiante = request.POST['codigo_estudiante']
        estudiante.semestre = request.POST['semestre']
        estudiante.promedio = request.POST.get('promedio', 0)
        estudiante.save()
        return redirect('lista_estudiantes')
    return _render_estudiante_form(request, 'Editar Estudiante', 'lista_estudiantes', estudiante)


def _render_estudiante_form(request, titulo, volver_url, estudiante=None):
    campos = [
        {'label': 'Usuario', 'name': 'usuario', 'type': 'select', 'required': True, 'options': _opciones(Usuario.objects.all(), getattr(getattr(estudiante, 'usuario', None), 'pk', None))},
        {'label': 'Codigo estudiante', 'name': 'codigo_estudiante', 'type': 'text', 'value': getattr(estudiante, 'codigo_estudiante', ''), 'required': True},
        {'label': 'Semestre', 'name': 'semestre', 'type': 'number', 'value': getattr(estudiante, 'semestre', ''), 'required': True},
        {'label': 'Promedio', 'name': 'promedio', 'type': 'number', 'step': '0.01', 'value': getattr(estudiante, 'promedio', 0), 'required': True},
    ]
    return render(request, 'gestionAcademica/paginas/formulario.html', {'titulo': titulo, 'volver_url': volver_url, 'campos': campos})


def eliminar_estudiante(request, id):
    return _eliminar_registro(request, Estudiante, id, 'lista_estudiantes')


def lista_materias(request):
    materias = Materia.objects.select_related('programa')
    filas = [[materia.id_materia, materia.nombre, materia.programa, materia.creditos, 'Activa' if materia.activa else 'Inactiva', materia.id_materia] for materia in materias]
    return render(request, 'gestionAcademica/paginas/lista.html', {
        'titulo': 'Materias',
        'crear_url': 'crear_materia',
        'encabezados': ['ID', 'Nombre', 'Programa', 'Creditos', 'Estado', 'Acciones'],
        'filas': filas,
        'editar_url': 'editar_materia',
        'eliminar_url': 'eliminar_materia',
        'vacio': 'No hay materias registradas.',
    })


def crear_materia(request):
    if request.method == 'POST':
        Materia.objects.create(
            id_materia=request.POST['id_materia'],
            nombre=request.POST['nombre'],
            creditos=request.POST.get('creditos', 3),
            descripcion=request.POST.get('descripcion', ''),
            activa=request.POST.get('activa') == 'on',
            programa=get_object_or_404(Programa, pk=request.POST['programa']),
            profesor=get_object_or_404(Usuario, pk=request.POST['profesor']) if request.POST.get('profesor') else None,
        )
        return redirect('lista_materias')
    return _render_materia_form(request, 'Nueva Materia', 'lista_materias')


def editar_materia(request, id):
    materia = get_object_or_404(Materia, id_materia=id)
    if request.method == 'POST':
        materia.nombre = request.POST['nombre']
        materia.creditos = request.POST.get('creditos', 3)
        materia.descripcion = request.POST.get('descripcion', '')
        materia.activa = request.POST.get('activa') == 'on'
        materia.programa = get_object_or_404(Programa, pk=request.POST['programa'])
        materia.profesor = get_object_or_404(Usuario, pk=request.POST['profesor']) if request.POST.get('profesor') else None
        materia.save()
        return redirect('lista_materias')
    return _render_materia_form(request, 'Editar Materia', 'lista_materias', materia)


def _render_materia_form(request, titulo, volver_url, materia=None):
    campos = []
    if materia is None:
        campos.append({'label': 'ID materia', 'name': 'id_materia', 'type': 'number', 'required': True})
    campos.extend([
        {'label': 'Nombre', 'name': 'nombre', 'type': 'text', 'value': getattr(materia, 'nombre', ''), 'required': True},
        {'label': 'Programa', 'name': 'programa', 'type': 'select', 'required': True, 'options': _opciones(Programa.objects.select_related('facultad'), getattr(getattr(materia, 'programa', None), 'pk', None))},
        {'label': 'Profesor asignado', 'name': 'profesor', 'type': 'select', 'options': _opciones(Usuario.objects.filter(id_rol__nombre_rol__icontains='prof'), getattr(getattr(materia, 'profesor', None), 'pk', None))},
        {'label': 'Creditos', 'name': 'creditos', 'type': 'number', 'value': getattr(materia, 'creditos', 3), 'required': True},
        {'label': 'Descripción', 'name': 'descripcion', 'type': 'textarea', 'value': getattr(materia, 'descripcion', '')},
        {'label': 'Activa', 'name': 'activa', 'type': 'checkbox', 'checked': True if materia is None else materia.activa},
    ])
    return render(request, 'gestionAcademica/paginas/formulario.html', {'titulo': titulo, 'volver_url': volver_url, 'campos': campos})


def eliminar_materia(request, id):
    return _eliminar_registro(request, Materia, id, 'lista_materias')


def lista_periodos(request):
    periodos = PeriodoAcademico.objects.all()
    filas = [[periodo.nombre, periodo.fecha_inicio, periodo.fecha_fin, periodo.id] for periodo in periodos]
    return render(request, 'gestionAcademica/paginas/lista.html', {
        'titulo': 'Periodos Académicos',
        'crear_url': 'crear_periodo',
        'encabezados': ['Nombre', 'Fecha inicio', 'Fecha fin', 'Acciones'],
        'filas': filas,
        'editar_url': 'editar_periodo',
        'eliminar_url': 'eliminar_periodo',
        'vacio': 'No hay periodos registrados.',
    })


def crear_periodo(request):
    if request.method == 'POST':
        PeriodoAcademico.objects.create(
            nombre=request.POST['nombre'],
            fecha_inicio=request.POST['fecha_inicio'],
            fecha_fin=request.POST['fecha_fin'],
        )
        return redirect('lista_periodos')
    return _render_periodo_form(request, 'Nuevo Periodo Académico', 'lista_periodos')


def editar_periodo(request, id):
    periodo = get_object_or_404(PeriodoAcademico, id=id)
    if request.method == 'POST':
        periodo.nombre = request.POST['nombre']
        periodo.fecha_inicio = request.POST['fecha_inicio']
        periodo.fecha_fin = request.POST['fecha_fin']
        periodo.save()
        return redirect('lista_periodos')
    return _render_periodo_form(request, 'Editar Periodo Académico', 'lista_periodos', periodo)


def _render_periodo_form(request, titulo, volver_url, periodo=None):
    campos = [
        {'label': 'Nombre', 'name': 'nombre', 'type': 'text', 'value': getattr(periodo, 'nombre', ''), 'required': True},
        {'label': 'Fecha inicio', 'name': 'fecha_inicio', 'type': 'date', 'value': getattr(periodo, 'fecha_inicio', ''), 'required': True},
        {'label': 'Fecha fin', 'name': 'fecha_fin', 'type': 'date', 'value': getattr(periodo, 'fecha_fin', ''), 'required': True},
    ]
    return render(request, 'gestionAcademica/paginas/formulario.html', {'titulo': titulo, 'volver_url': volver_url, 'campos': campos})


def eliminar_periodo(request, id):
    return _eliminar_registro(request, PeriodoAcademico, id, 'lista_periodos')


def lista_inscripciones(request):
    inscripciones = _inscripciones_visibles(request)
    filas = [[inscripcion.estudiante, inscripcion.materia, inscripcion.periodo, inscripcion.fecha_inscripcion, 'Activa' if inscripcion.activa else 'Inactiva', inscripcion.id] for inscripcion in inscripciones]
    return render(request, 'gestionAcademica/paginas/lista.html', {
        'titulo': 'Inscripciones',
        'crear_url': 'crear_inscripcion',
        'encabezados': ['Estudiante', 'Materia', 'Periodo', 'Fecha', 'Estado', 'Acciones'],
        'filas': filas,
        'editar_url': 'editar_inscripcion',
        'eliminar_url': 'eliminar_inscripcion',
        'vacio': 'No hay inscripciones registradas.',
    })


def crear_inscripcion(request):
    if request.method == 'POST':
        Inscripcion.objects.create(
            estudiante=get_object_or_404(Estudiante, pk=request.POST['estudiante']),
            materia=get_object_or_404(Materia, pk=request.POST['materia']),
            periodo=get_object_or_404(PeriodoAcademico, pk=request.POST['periodo']),
            fecha_inscripcion=request.POST['fecha_inscripcion'],
            activa=request.POST.get('activa') == 'on',
        )
        return redirect('lista_inscripciones')
    return _render_inscripcion_form(request, 'Nueva Inscripcion', 'lista_inscripciones')


def editar_inscripcion(request, id):
    inscripcion = get_object_or_404(Inscripcion, id=id)
    if request.method == 'POST':
        inscripcion.estudiante = get_object_or_404(Estudiante, pk=request.POST['estudiante'])
        inscripcion.materia = get_object_or_404(Materia, pk=request.POST['materia'])
        inscripcion.periodo = get_object_or_404(PeriodoAcademico, pk=request.POST['periodo'])
        inscripcion.fecha_inscripcion = request.POST['fecha_inscripcion']
        inscripcion.activa = request.POST.get('activa') == 'on'
        inscripcion.save()
        return redirect('lista_inscripciones')
    return _render_inscripcion_form(request, 'Editar Inscripcion', 'lista_inscripciones', inscripcion)


def _render_inscripcion_form(request, titulo, volver_url, inscripcion=None):
    campos = [
        {'label': 'Estudiante', 'name': 'estudiante', 'type': 'select', 'required': True, 'options': _opciones(Estudiante.objects.all(), getattr(getattr(inscripcion, 'estudiante', None), 'pk', None))},
        {'label': 'Materia', 'name': 'materia', 'type': 'select', 'required': True, 'options': _opciones(_materias_visibles(request), getattr(getattr(inscripcion, 'materia', None), 'pk', None))},
        {'label': 'Periodo', 'name': 'periodo', 'type': 'select', 'required': True, 'options': _opciones(PeriodoAcademico.objects.all(), getattr(getattr(inscripcion, 'periodo', None), 'pk', None))},
        {'label': 'Fecha inscripcion', 'name': 'fecha_inscripcion', 'type': 'date', 'value': getattr(inscripcion, 'fecha_inscripcion', ''), 'required': True},
        {'label': 'Activa', 'name': 'activa', 'type': 'checkbox', 'checked': True if inscripcion is None else inscripcion.activa},
    ]
    return render(request, 'gestionAcademica/paginas/formulario.html', {'titulo': titulo, 'volver_url': volver_url, 'campos': campos})


def eliminar_inscripcion(request, id):
    return _eliminar_registro(request, Inscripcion, id, 'lista_inscripciones')


def lista_notas(request):
    notas = Nota.objects.select_related('inscripcion__estudiante', 'inscripcion__materia', 'inscripcion__materia__profesor', 'inscripcion__periodo')
    profesor = _profesor_actual(request)
    if profesor:
        notas = notas.filter(inscripcion__materia__profesor=profesor)
    filas = [
        [
            nota.id_nota,
            nota.inscripcion.estudiante,
            nota.inscripcion.materia,
            nota.inscripcion.periodo,
            nota.corte,
            nota.valor,
            nota.id_nota,
        ]
        for nota in notas
    ]
    return render(request, 'gestionAcademica/paginas/lista.html', {
        'titulo': 'Notas',
        'crear_url': 'crear_nota',
        'encabezados': ['ID', 'Estudiante', 'Materia', 'Periodo', 'Corte', 'Nota', 'Acciones'],
        'filas': filas,
        'editar_url': 'editar_nota',
        'eliminar_url': 'eliminar_nota',
        'vacio': 'No hay notas registradas.',
    })


def crear_nota(request):
    if request.method == 'POST':
        valor = _validar_valor_nota(request)
        if valor is None:
            return _render_nota_form(request, 'Nueva Nota', 'lista_notas')

        Nota.objects.create(
            id_nota=request.POST['id_nota'],
            inscripcion=get_object_or_404(Inscripcion, pk=request.POST['inscripcion']),
            corte=request.POST['corte'],
            valor=valor,
            observaciones=request.POST.get('observaciones', ''),
        )
        _actualizar_promedio_estudiante(get_object_or_404(Inscripcion, pk=request.POST['inscripcion']).estudiante)
        return redirect('lista_notas')
    return _render_nota_form(request, 'Nueva Nota', 'lista_notas')


def editar_nota(request, id):
    nota = get_object_or_404(Nota, id_nota=id)
    estudiante_anterior = nota.inscripcion.estudiante
    if request.method == 'POST':
        valor = _validar_valor_nota(request)
        if valor is None:
            return _render_nota_form(request, 'Editar Nota', 'lista_notas', nota)

        nota.inscripcion = get_object_or_404(Inscripcion, pk=request.POST['inscripcion'])
        nota.corte = request.POST['corte']
        nota.valor = valor
        nota.observaciones = request.POST.get('observaciones', '')
        nota.save()
        _actualizar_promedio_estudiante(estudiante_anterior)
        _actualizar_promedio_estudiante(nota.inscripcion.estudiante)
        return redirect('lista_notas')
    return _render_nota_form(request, 'Editar Nota', 'lista_notas', nota)


def _render_nota_form(request, titulo, volver_url, nota=None):
    campos = []
    if nota is None:
        campos.append({'label': 'ID nota', 'name': 'id_nota', 'type': 'number', 'required': True})
    campos.extend([
        {'label': 'Estudiante - Materia - Periodo', 'name': 'inscripcion', 'type': 'select', 'required': True, 'options': _opciones_inscripciones(request, getattr(getattr(nota, 'inscripcion', None), 'pk', None))},
        {'label': 'Corte', 'name': 'corte', 'type': 'number', 'value': getattr(nota, 'corte', ''), 'required': True},
        {'label': 'Valor', 'name': 'valor', 'type': 'number', 'step': '0.01', 'min': '0', 'max': '5.00', 'value': getattr(nota, 'valor', ''), 'required': True},
        {'label': 'Observaciones', 'name': 'observaciones', 'type': 'textarea', 'value': getattr(nota, 'observaciones', '')},
    ])
    return render(request, 'gestionAcademica/paginas/formulario.html', {'titulo': titulo, 'volver_url': volver_url, 'campos': campos})


def eliminar_nota(request, id):
    nota = get_object_or_404(Nota, id_nota=id)
    estudiante = nota.inscripcion.estudiante
    nota.delete()
    _actualizar_promedio_estudiante(estudiante)
    return redirect('lista_notas')


def lista_asistencias(request):
    asistencias = Asistencia.objects.select_related('inscripcion', 'inscripcion__materia')
    profesor = _profesor_actual(request)
    if profesor:
        asistencias = asistencias.filter(inscripcion__materia__profesor=profesor)
    filas = [[asistencia.inscripcion, asistencia.fecha, 'Asistio' if asistencia.asiste else 'No asistio', asistencia.id] for asistencia in asistencias]
    return render(request, 'gestionAcademica/paginas/lista.html', {
        'titulo': 'Asistencias',
        'crear_url': 'crear_asistencia',
        'encabezados': ['Inscripcion', 'Fecha', 'Estado', 'Acciones'],
        'filas': filas,
        'editar_url': 'editar_asistencia',
        'eliminar_url': 'eliminar_asistencia',
        'vacio': 'No hay asistencias registradas.',
    })


def crear_asistencia(request):
    if request.method == 'POST':
        Asistencia.objects.create(
            inscripcion=get_object_or_404(Inscripcion, pk=request.POST['inscripcion']),
            fecha=request.POST['fecha'],
            asiste=request.POST.get('asiste') == 'on',
        )
        return redirect('lista_asistencias')
    return _render_asistencia_form(request, 'Nueva Asistencia', 'lista_asistencias')


def editar_asistencia(request, id):
    asistencia = get_object_or_404(Asistencia, id=id)
    if request.method == 'POST':
        asistencia.inscripcion = get_object_or_404(Inscripcion, pk=request.POST['inscripcion'])
        asistencia.fecha = request.POST['fecha']
        asistencia.asiste = request.POST.get('asiste') == 'on'
        asistencia.save()
        return redirect('lista_asistencias')
    return _render_asistencia_form(request, 'Editar Asistencia', 'lista_asistencias', asistencia)


def _render_asistencia_form(request, titulo, volver_url, asistencia=None):
    campos = [
        {'label': 'Inscripcion', 'name': 'inscripcion', 'type': 'select', 'required': True, 'options': _opciones(Inscripcion.objects.all(), getattr(getattr(asistencia, 'inscripcion', None), 'pk', None))},
        {'label': 'Fecha', 'name': 'fecha', 'type': 'date', 'value': getattr(asistencia, 'fecha', ''), 'required': True},
        {'label': 'Asiste', 'name': 'asiste', 'type': 'checkbox', 'checked': True if asistencia is None else asistencia.asiste},
    ]
    return render(request, 'gestionAcademica/paginas/formulario.html', {'titulo': titulo, 'volver_url': volver_url, 'campos': campos})


def eliminar_asistencia(request, id):
    return _eliminar_registro(request, Asistencia, id, 'lista_asistencias')


def saludo_autor(request, id_usuario):
    usuario = get_object_or_404(Usuario, id_usuario=id_usuario)
    usuarios = Usuario.objects.all()
    return render(request, 'saludo_autor.html', {'usuario': usuario, 'usuarios': usuarios})




