from django.db import models

# Create your models here.
class Rol(models.Model):
    nombre_rol =models.CharField(max_length=20)
    
    def __str__(self):
        return self.nombre_rol

class TipoDocumento(models.Model):
    nombre_tipo_doc =models.CharField(max_length=20)
    
    def __str__(self):
        return self.nombre_tipo_doc

class Usuario(models.Model):
    nombre_usuario = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
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

class TiposSolicitud(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()

    def __str__(self):
        return self.nombre

class EstadosSolicitud(models.Model):
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre

class Solicitud(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    tipo = models.ForeignKey(TiposSolicitud, on_delete=models.CASCADE)
    estado = models.ForeignKey(EstadosSolicitud, on_delete=models.CASCADE)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    prioridad = models.CharField(max_length=20)

    def __str__(self):
        return f"Solicitud {self.id} - {self.tipo}"

class HistorialSolicitud(models.Model):
    solicitud = models.ForeignKey(Solicitud, on_delete=models.CASCADE)
    estado = models.ForeignKey(EstadosSolicitud, on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)
    comentario = models.TextField()

    def __str__(self):
        return f"Historial {self.id} - {self.solicitud}"

class ComentariosSolicitud(models.Model):
    solicitud = models.ForeignKey(Solicitud, on_delete=models.CASCADE)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    comentario = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comentario {self.id} - {self.solicitud}"
class DocumentoSolicitud(models.Model):
    solicitud = models.ForeignKey(Solicitud, on_delete=models.CASCADE, related_name='documentos')
    archivo = models.FileField(upload_to='solicitudes/documentos/')
    nombre_original = models.CharField(max_length=255, blank=True)
    fecha_carga = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre_original or str(self.archivo)
