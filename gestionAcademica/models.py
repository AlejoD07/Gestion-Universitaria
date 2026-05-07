from django.db import models

# Create your models here.

class Rol(models.Model):
    id_rol = models.BigIntegerField(unique=True, db_index=True, primary_key=True)
    nombre_rol =models.CharField(max_length=20)
    
    def __str__(self):
        return self.nombre_rol


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