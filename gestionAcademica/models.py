from django.db import models

# Create your models here.

class Facultad(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    activa = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre


class Rol(models.Model):
    id_rol = models.BigIntegerField(unique=True, db_index=True, primary_key=True)
    nombre_rol =models.CharField(max_length=20)

    def __str__(self):
        return self.nombre_rol


class PermisoRolModulo(models.Model):
    MODULOS = [
        ('academica', 'Gestion Academica'),
        ('contabilidad', 'Contabilidad'),
        ('rrhh', 'Recursos Humanos'),
        ('inventario', 'inventario'),
        ('solicitudes', 'Solicitudes'),
    ]

    rol = models.ForeignKey(
        Rol,
        on_delete=models.CASCADE,
        related_name='permisos_modulo'
    )
    modulo = models.CharField(max_length=30, choices=MODULOS)
    activo = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Permiso por rol'
        verbose_name_plural = 'Permisos por rol'
        unique_together = ('rol', 'modulo')
        ordering = ['rol__nombre_rol', 'modulo']

    def __str__(self):
        estado = 'activo' if self.activo else 'inactivo'
        return f'{self.rol} - {self.modulo} ({estado})'


class TipoDocumento(models.Model):
    id_tipo_doc = models.BigIntegerField(unique=True, db_index=True, primary_key=True)
    nombre_tipo_doc =models.CharField(max_length=20)

    def __str__(self):
        return self.nombre_tipo_doc

class Usuario(models.Model):
    id_usuario = models.BigIntegerField(unique=True, db_index=True, primary_key=True)
    nombre_usuario = models.CharField(max_length=200)
    activo = models.BooleanField(default=True)
    id_tipo_documento = models.ForeignKey(
        TipoDocumento,
        on_delete=models.PROTECT
    )
    id_rol = models.ForeignKey(
        Rol,
        on_delete=models.PROTECT
    )
    facultad = models.ForeignKey(
        Facultad,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    def __str__(self):
        return f"{self.nombre_usuario}"

class Estudiante(models.Model):
    usuario = models.OneToOneField(
        Usuario,
        on_delete=models.PROTECT
    )
    codigo_estudiante = models.CharField(max_length=20)
    semestre = models.IntegerField()
    promedio = models.DecimalField(max_digits=4, decimal_places=2, default=0)

    def __str__(self):
        return self.codigo_estudiante

class Programa(models.Model):
    nombre = models.CharField(max_length=100)
    facultad = models.ForeignKey(
        Facultad,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    def __str__(self):
        return self.nombre

class Materia(models.Model):
    id_materia = models.BigIntegerField(unique=True, db_index=True, primary_key=True)
    nombre = models.CharField(max_length=100)
    creditos = models.IntegerField(default=3)
    descripcion = models.TextField(blank=True)
    activa = models.BooleanField(default=True)
    programa = models.ForeignKey(
        Programa,
        on_delete=models.PROTECT
    )
    profesor = models.ForeignKey(
        Usuario,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='materias_asignadas'
    )

    def __str__(self):
        return self.nombre

class PeriodoAcademico(models.Model):
    nombre = models.CharField(max_length=100)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()

    def __str__(self):
        return self.nombre

class Inscripcion(models.Model):
    estudiante = models.ForeignKey(
        Estudiante,
        on_delete=models.PROTECT
    )
    materia = models.ForeignKey(
        Materia,
        on_delete=models.PROTECT
    )
    periodo = models.ForeignKey(
        PeriodoAcademico,
        on_delete=models.PROTECT
    )
    fecha_inscripcion = models.DateField()
    activa = models.BooleanField(default=True)

    def __str__(self):
        return f"el estudainte {self.estudiante} inscribio la materia {self.materia} "

class Nota(models.Model):
    id_nota = models.BigIntegerField(unique=True, db_index=True, primary_key=True)
    inscripcion = models.ForeignKey(
        Inscripcion,
        on_delete=models.PROTECT
    )
    corte = models.IntegerField(null=False, blank=False)
    valor = models.DecimalField(max_digits=4, decimal_places=2, null=False, blank=False)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    observaciones = models.TextField(blank=True, help_text="Observaciones del profesor")

    def __str__(self):
        return f"La nota es {self.valor}"

class Asistencia(models.Model):
    inscripcion = models.ForeignKey(
        Inscripcion,
        on_delete=models.PROTECT
    )
    fecha = models.DateField()
    asiste = models.BooleanField(default=True)

    def __str__(self):
        return f"la asistencia del dia {self.fecha}"


# ============================================================================
# SISTEMA MEJORADO DE CALIFICACIÓN CON ACTIVIDADES Y PORCENTAJES
# ============================================================================

class Actividad(models.Model):
    """
    Representa una evaluación (quiz, taller, examen, etc.) en una materia.
    Cada actividad tiene un porcentaje del total de la nota final.
    """
    TIPOS_ACTIVIDAD = [
        ('QUIZ', 'Quiz'),
        ('TALLER', 'Taller'),
        ('PARCIAL', 'Examen Parcial'),
        ('FINAL', 'Examen Final'),
        ('PROYECTO', 'Proyecto'),
        ('PARTICIPACION', 'Participación'),
        ('OTRO', 'Otro'),
    ]

    nombre = models.CharField(
        max_length=200,
        help_text='Ej: Quiz 1, Taller Algoritmos, Examen Parcial'
    )
    descripcion = models.TextField(
        blank=True,
        help_text='Descripción de la actividad'
    )
    tipo = models.CharField(
        max_length=20,
        choices=TIPOS_ACTIVIDAD,
        default='OTRO'
    )
    porcentaje = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        help_text='Porcentaje de la nota final (ej: 15.00 = 15%)'
    )
    numero_corte = models.IntegerField(
        choices=[(1, 'Corte 1'), (2, 'Corte 2'), (3, 'Corte 3')],
        default=1,
        help_text='Corte academico al que pertenece la actividad'
    )
    materia = models.ForeignKey(
        Materia,
        on_delete=models.CASCADE,
        related_name='actividades'
    )
    periodo = models.ForeignKey(
        PeriodoAcademico,
        on_delete=models.CASCADE
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    activa = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = 'Actividades'
        ordering = ['materia', 'periodo', 'numero_corte', 'fecha_creacion']

    def __str__(self):
        return f"{self.nombre} - Corte {self.numero_corte} ({self.porcentaje}%)"

    def get_tipo_display_icon(self):
        """Retorna una etiqueta corta para mostrar el tipo de actividad."""
        iconos = {
            'QUIZ': 'Quiz',
            'TALLER': 'Taller',
            'PARCIAL': 'Parcial',
            'FINAL': 'Final',
            'PROYECTO': 'Proyecto',
            'PARTICIPACION': 'Participacion',
            'OTRO': 'Actividad',
        }
        return iconos.get(self.tipo, 'Actividad')


class CalificacionActividad(models.Model):
    """
    La calificación (nota) que un estudiante obtiene en una actividad específica.
    Una actividad puede tener una calificación por cada estudiante inscrito.
    """
    inscripcion = models.ForeignKey(
        Inscripcion,
        on_delete=models.CASCADE,
        related_name='calificaciones_actividades'
    )
    actividad = models.ForeignKey(
        Actividad,
        on_delete=models.CASCADE,
        related_name='calificaciones'
    )
    calificacion = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        null=True,
        blank=True,
        help_text='Nota de 0.0 a 5.0'
    )
    observaciones = models.TextField(
        blank=True,
        help_text='Observaciones del profesor (retroalimentación)'
    )
    fecha_calificacion = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Calificaciones de Actividades'
        unique_together = ('inscripcion', 'actividad')
        ordering = ['inscripcion', 'actividad']

    def __str__(self):
        return f"{self.inscripcion.estudiante} - {self.actividad.nombre}: {self.calificacion or 'Sin calificar'}"

    def get_aporte_nota_final(self):
        """
        Calcula cuánto aporta esta calificación a la nota final.
        Fórmula: calificacion * (porcentaje / 100)
        """
        if self.calificacion is None:
            return None
        from decimal import Decimal
        return self.calificacion * (self.actividad.porcentaje / Decimal('100'))

    def obtener_estado(self):
        """Retorna el estado: 'Excelente', 'Bueno', 'Aceptable', 'Deficiente', 'Sin calificar'"""
        from decimal import Decimal

        if self.calificacion is None:
            return 'Sin calificar'
        if self.calificacion >= Decimal('4.50'):
            return 'Excelente'
        elif self.calificacion >= Decimal('4.00'):
            return 'Muy Bueno'
        elif self.calificacion >= Decimal('3.50'):
            return 'Bueno'
        elif self.calificacion >= Decimal('3.00'):
            return 'Aceptable'
        else:
            return 'Deficiente'


class Corte(models.Model):
    """
    Representa un corte (seguimiento académico) de una materia en un período.
    La nota del corte se calcula automáticamente como la suma ponderada de las actividades.

    Ejemplo:
    - Quiz 1 (15%): 4.5 → aporta 0.675
    - Taller (15%): 4.0 → aporta 0.600
    - Parcial (35%): 3.8 → aporta 1.330
    - Proyecto (35%): 4.2 → aporta 1.470
    - Nota Final = 0.675 + 0.600 + 1.330 + 1.470 = 4.075
    """
    CORTES = [(i, f'Corte {i}') for i in range(1, 4)]

    inscripcion = models.ForeignKey(
        Inscripcion,
        on_delete=models.CASCADE,
        related_name='cortes'
    )
    numero_corte = models.IntegerField(
        choices=CORTES,
        help_text='Número del corte (1, 2 o 3)'
    )
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    activo = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = 'Cortes'
        unique_together = ('inscripcion', 'numero_corte')
        ordering = ['inscripcion', 'numero_corte']

    def __str__(self):
        return f"Corte {self.numero_corte} - {self.inscripcion.estudiante}"

    def calcular_nota_final(self):
        """
        Calcula la nota final del corte como suma ponderada.
        Retorna None si aún hay actividades sin calificar.
        """
        from decimal import Decimal

        # Obtener actividades de este período
        actividades = self.inscripcion.materia.actividades.filter(
            periodo=self.inscripcion.periodo,
            numero_corte=self.numero_corte,
            activa=True
        )

        if not actividades.exists():
            return None

        nota_total = Decimal('0.00')
        total_porcentaje = Decimal('0.00')

        for actividad in actividades:
            try:
                calificacion = CalificacionActividad.objects.get(
                    inscripcion=self.inscripcion,
                    actividad=actividad
                )
                if calificacion.calificacion is not None:
                    aporte = calificacion.get_aporte_nota_final()
                    nota_total += aporte
                    total_porcentaje += actividad.porcentaje
            except CalificacionActividad.DoesNotExist:
                # Si una actividad no tiene calificación, la nota es None
                return None

        # Acepta diferencias minimas de centesimas por redondeos de captura.
        if abs(total_porcentaje - Decimal('100.00')) > Decimal('0.01'):
            return None

        # Redondear a 2 decimales
        return round(nota_total, 2)

    def obtener_detalles_calificacion(self):
        """
        Retorna un diccionario con el desglose de calificaciones.
        Útil para mostrar en la interfaz.
        """
        actividades = self.inscripcion.materia.actividades.filter(
            periodo=self.inscripcion.periodo,
            numero_corte=self.numero_corte,
            activa=True
        ).order_by('fecha_creacion')

        detalles = {
            'actividades': [],
            'nota_final': self.calcular_nota_final(),
            'completo': True
        }

        for actividad in actividades:
            try:
                calificacion = CalificacionActividad.objects.get(
                    inscripcion=self.inscripcion,
                    actividad=actividad
                )
                if calificacion.calificacion is None:
                    detalles['completo'] = False

                detalles['actividades'].append({
                    'nombre': actividad.nombre,
                    'tipo': actividad.get_tipo_display_icon(),
                    'porcentaje': float(actividad.porcentaje),
                    'calificacion': float(calificacion.calificacion) if calificacion.calificacion is not None else None,
                    'aporte': float(calificacion.get_aporte_nota_final()) if calificacion.calificacion is not None else None,
                    'estado': calificacion.obtener_estado(),
                    'observaciones': calificacion.observaciones,
                })
            except CalificacionActividad.DoesNotExist:
                detalles['completo'] = False
                detalles['actividades'].append({
                    'nombre': actividad.nombre,
                    'tipo': actividad.get_tipo_display_icon(),
                    'porcentaje': float(actividad.porcentaje),
                    'calificacion': None,
                    'aporte': None,
                    'estado': 'Sin calificar',
                    'observaciones': '',
                })

        return detalles
