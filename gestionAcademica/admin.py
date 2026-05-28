from django.contrib import admin
from .models import (
    Rol, PermisoRolModulo, TipoDocumento, Usuario, Facultad, Programa,
    Estudiante, Materia, PeriodoAcademico, Inscripcion,
    Nota, Asistencia, Actividad, CalificacionActividad, Corte
)


class RolAdmin(admin.ModelAdmin):
    list_display = ('id_rol', 'nombre_rol')
    search_fields = ('nombre_rol',)


class PermisoRolModuloAdmin(admin.ModelAdmin):
    list_display = ('rol', 'modulo', 'activo')
    list_filter = ('modulo', 'activo')
    search_fields = ('rol__nombre_rol',)


class TipoDocumentoAdmin(admin.ModelAdmin):
    list_display = ('id_tipo_doc', 'nombre_tipo_doc')


class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('id_usuario', 'nombre_usuario', 'id_rol', 'activo')
    list_filter = ('id_rol', 'activo')
    search_fields = ('nombre_usuario', 'id_usuario')


class FacultadAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'activa')


class ProgramaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'facultad')
    list_filter = ('facultad',)


class EstudianteAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'codigo_estudiante', 'semestre', 'promedio')
    search_fields = ('codigo_estudiante', 'usuario__nombre_usuario')


class MateriaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'profesor', 'programa', 'creditos', 'activa')
    list_filter = ('programa', 'activa')
    search_fields = ('nombre',)


class PeriodoAcademicoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'fecha_inicio', 'fecha_fin')


class InscripcionAdmin(admin.ModelAdmin):
    list_display = ('estudiante', 'materia', 'periodo', 'fecha_inscripcion', 'activa')
    list_filter = ('materia', 'periodo', 'activa')
    search_fields = ('estudiante__usuario__nombre_usuario', 'materia__nombre')


class NotaAdmin(admin.ModelAdmin):
    list_display = ('inscripcion', 'corte', 'valor', 'fecha_registro')
    list_filter = ('corte', 'fecha_registro')
    search_fields = ('inscripcion__estudiante__usuario__nombre_usuario',)


class AsistenciaAdmin(admin.ModelAdmin):
    list_display = ('inscripcion', 'fecha', 'asiste')
    list_filter = ('fecha', 'asiste')


# NUEVOS MODELOS PARA SISTEMA MEJORADO DE CALIFICACIONES

class ActividadAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'tipo', 'porcentaje', 'materia', 'periodo', 'fecha_creacion', 'activa')
    list_filter = ('tipo', 'materia', 'periodo', 'activa', 'fecha_creacion')
    search_fields = ('nombre', 'materia__nombre')
    readonly_fields = ('fecha_creacion',)

    fieldsets = (
        ('Información Básica', {
            'fields': ('nombre', 'descripcion', 'tipo')
        }),
        ('Configuración Académica', {
            'fields': ('materia', 'periodo', 'porcentaje')
        }),
        ('Estado', {
            'fields': ('activa', 'fecha_creacion')
        }),
    )


class CalificacionActividadAdmin(admin.ModelAdmin):
    list_display = ('inscripcion', 'actividad', 'calificacion', 'fecha_calificacion')
    list_filter = ('actividad', 'fecha_calificacion')
    search_fields = ('inscripcion__estudiante__usuario__nombre_usuario', 'actividad__nombre')
    readonly_fields = ('fecha_calificacion',)

    fieldsets = (
        ('Relaciones', {
            'fields': ('inscripcion', 'actividad')
        }),
        ('Calificación', {
            'fields': ('calificacion', 'observaciones')
        }),
        ('Información del Sistema', {
            'fields': ('fecha_calificacion',),
            'classes': ('collapse',)
        }),
    )


class CorteAdmin(admin.ModelAdmin):
    list_display = ('inscripcion', 'numero_corte', 'fecha_inicio', 'fecha_fin', 'activo')
    list_filter = ('numero_corte', 'fecha_inicio', 'activo')
    search_fields = ('inscripcion__estudiante__usuario__nombre_usuario',)

    fieldsets = (
        ('Información del Corte', {
            'fields': ('inscripcion', 'numero_corte')
        }),
        ('Fechas', {
            'fields': ('fecha_inicio', 'fecha_fin')
        }),
        ('Estado', {
            'fields': ('activo',)
        }),
    )


# Registro de modelos
admin.site.register(Rol, RolAdmin)
admin.site.register(PermisoRolModulo, PermisoRolModuloAdmin)
admin.site.register(TipoDocumento, TipoDocumentoAdmin)
admin.site.register(Usuario, UsuarioAdmin)
admin.site.register(Facultad, FacultadAdmin)
admin.site.register(Programa, ProgramaAdmin)
admin.site.register(Estudiante, EstudianteAdmin)
admin.site.register(Materia, MateriaAdmin)
admin.site.register(PeriodoAcademico, PeriodoAcademicoAdmin)
admin.site.register(Inscripcion, InscripcionAdmin)
admin.site.register(Nota, NotaAdmin)
admin.site.register(Asistencia, AsistenciaAdmin)
admin.site.register(Actividad, ActividadAdmin)
admin.site.register(CalificacionActividad, CalificacionActividadAdmin)
admin.site.register(Corte, CorteAdmin)
