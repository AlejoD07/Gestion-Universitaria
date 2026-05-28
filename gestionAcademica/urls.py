from django.urls import path

from . import views
from . import views_calificaciones


urlpatterns = [
    path('', views.inicio, name='academica_inicio'),
    path('inicio/', views.inicio, name='inicio'),

    path('roles/', views.lista_roles, name='lista_roles'),
    path('roles/crear/', views.crear_rol, name='crear_rol'),
    path('roles/editar/<int:id>/', views.editar_rol, name='editar_rol'),
    path('roles/eliminar/<int:id>/', views.eliminar_rol, name='eliminar_rol'),

    path('tipos-documento/', views.lista_tipos_documento, name='lista_tipos_documento'),
    path('tipos-documento/crear/', views.crear_tipo_documento, name='crear_tipo_documento'),
    path('tipos-documento/editar/<int:id>/', views.editar_tipo_documento, name='editar_tipo_documento'),
    path('tipos-documento/eliminar/<int:id>/', views.eliminar_tipo_documento, name='eliminar_tipo_documento'),

    path('usuarios/', views.lista_usuarios, name='lista_usuarios'),
    path('lista-usuarios/', views.lista_usuarios, name='lista-usuarios'),
    path('profesores/', views.lista_profesores, name='lista_profesores'),
    path('profesores/asignaciones/', views.asignaciones_docentes, name='asignaciones_docentes'),
    path('profesores/asignaciones/<int:id>/', views.editar_asignacion_docente, name='editar_asignacion_docente'),
    path('usuarios/crear/', views.crear_usuario, name='crear_usuario'),
    path('usuarios/editar/<int:id>/', views.editar_usuario, name='editar_usuario'),
    path('usuarios/eliminar/<int:id>/', views.eliminar_usuario, name='eliminar_usuario'),

    path('programas/', views.lista_programas, name='lista_programas'),
    path('programas/crear/', views.crear_programa, name='crear_programa'),
    path('programas/editar/<int:id>/', views.editar_programa, name='editar_programa'),
    path('programas/eliminar/<int:id>/', views.eliminar_programa, name='eliminar_programa'),

    path('estudiantes/', views.lista_estudiantes, name='lista_estudiantes'),
    path('estudiantes/crear/', views.crear_estudiante, name='crear_estudiante'),
    path('estudiantes/editar/<int:id>/', views.editar_estudiante, name='editar_estudiante'),
    path('estudiantes/eliminar/<int:id>/', views.eliminar_estudiante, name='eliminar_estudiante'),

    path('materias/', views.lista_materias, name='lista_materias'),
    path('materias/crear/', views.crear_materia, name='crear_materia'),
    path('materias/editar/<int:id>/', views.editar_materia, name='editar_materia'),
    path('materias/eliminar/<int:id>/', views.eliminar_materia, name='eliminar_materia'),

    path('periodos/', views.lista_periodos, name='lista_periodos'),
    path('periodos/crear/', views.crear_periodo, name='crear_periodo'),
    path('periodos/editar/<int:id>/', views.editar_periodo, name='editar_periodo'),
    path('periodos/eliminar/<int:id>/', views.eliminar_periodo, name='eliminar_periodo'),

    path('inscripciones/', views.lista_inscripciones, name='lista_inscripciones'),
    path('inscripciones/crear/', views.crear_inscripcion, name='crear_inscripcion'),
    path('inscripciones/editar/<int:id>/', views.editar_inscripcion, name='editar_inscripcion'),
    path('inscripciones/eliminar/<int:id>/', views.eliminar_inscripcion, name='eliminar_inscripcion'),

    path('notas/', views.lista_notas, name='lista_notas'),
    path('notas/crear/', views.crear_nota, name='crear_nota'),
    path('notas/editar/<int:id>/', views.editar_nota, name='editar_nota'),
    path('notas/eliminar/<int:id>/', views.eliminar_nota, name='eliminar_nota'),

    path('asistencias/', views.lista_asistencias, name='lista_asistencias'),
    path('asistencias/crear/', views.crear_asistencia, name='crear_asistencia'),
    path('asistencias/editar/<int:id>/', views.editar_asistencia, name='editar_asistencia'),
    path('asistencias/eliminar/<int:id>/', views.eliminar_asistencia, name='eliminar_asistencia'),

    # NUEVAS RUTAS PARA SISTEMA MEJORADO DE CALIFICACIONES
    path('profesor/materias/', views_calificaciones.materias_profesor, name='profesor_materias'),
    path('profesor/actividad/crear/<int:materia_id>/', views_calificaciones.crear_actividad, name='profesor_crear_actividad'),
    path('profesor/actividad/editar/<int:actividad_id>/', views_calificaciones.editar_actividad, name='profesor_editar_actividad'),
    path('profesor/actividad/calificar/<int:actividad_id>/', views_calificaciones.calificar_actividad, name='profesor_calificar_actividad'),
    path('profesor/reporte/corte/<int:actividad_id>/', views_calificaciones.reporte_corte, name='profesor_reporte_corte'),
    path('profesor/actividades/<int:materia_id>/', views_calificaciones.gestionar_actividades, name='profesor_gestionar_actividades'),
    path('profesor/definitivas/<int:materia_id>/', views_calificaciones.definitivas_materia, name='profesor_definitivas_materia'),

    path('saludo-autor/<int:id_usuario>/', views.saludo_autor, name='saludo-autor'),
]
