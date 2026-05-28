from django.db import models
from django.utils import timezone
from decimal import Decimal


class AreaContable(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    activa = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre


class Nomina(models.Model):
    empleado = models.ForeignKey('RecursosHumanos.Empleado', on_delete=models.PROTECT, null=True, blank=True, related_name='nominas')
    empleado_nombre = models.CharField(max_length=100)
    empleado_cedula = models.CharField(max_length=20)
    cargo = models.CharField(max_length=100)
    area = models.CharField(max_length=100)
    mes = models.CharField(max_length=20)
    anio = models.IntegerField()
    salario_base = models.DecimalField(max_digits=10, decimal_places=2)
    horas_extras = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    comisiones = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    deducciones = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_pago = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    fecha_pago = models.DateField()
    estado = models.CharField(max_length=20, default='pendiente')

    def calcular_total(self):
        self.total_pago = float(self.salario_base) + float(self.horas_extras) + float(self.comisiones) - float(self.deducciones)
        return self.total_pago

    def __str__(self):
        return f"{self.empleado_nombre} - {self.mes} {self.anio}"

    class Meta:
        verbose_name = "Nomina"
        verbose_name_plural = "Nominas"


class LoteNomina(models.Model):
    ESTADOS = [
        ('importado', 'Importado'),
        ('validado', 'Validado'),
        ('inconsistencias', 'Con inconsistencias'),
        ('contabilizado', 'Contabilizado'),
    ]

    codigo = models.CharField(max_length=30, unique=True)
    plataforma_origen = models.CharField(max_length=80)
    mes = models.CharField(max_length=20)
    anio = models.IntegerField()
    fecha_importacion = models.DateTimeField(default=timezone.now)
    total_empleados = models.IntegerField(default=0)
    total_devengado = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    total_deducciones = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    total_neto = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    estado = models.CharField(max_length=20, choices=ESTADOS, default='importado')
    observaciones = models.TextField(blank=True)

    class Meta:
        verbose_name = "Lote de nomina"
        verbose_name_plural = "Lotes de nomina"
        ordering = ['-anio', '-fecha_importacion']

    def __str__(self):
        return f"{self.codigo} - {self.plataforma_origen}"


class DetalleNominaImportada(models.Model):
    ESTADOS = [
        ('ok', 'OK'),
        ('inconsistencia', 'Inconsistencia'),
    ]

    lote = models.ForeignKey(LoteNomina, on_delete=models.CASCADE, related_name='detalles')
    empleado = models.ForeignKey('RecursosHumanos.Empleado', on_delete=models.PROTECT, null=True, blank=True, related_name='detalles_nomina')
    empleado_nombre = models.CharField(max_length=120)
    empleado_cedula = models.CharField(max_length=20)
    cargo = models.CharField(max_length=100, blank=True)
    area = models.CharField(max_length=100, blank=True)
    salario_base = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total_devengado = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total_deducciones = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    neto_pagar = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    estado = models.CharField(max_length=20, choices=ESTADOS, default='ok')
    mensaje_validacion = models.CharField(max_length=250, blank=True)

    class Meta:
        verbose_name = "Detalle de nomina importada"
        verbose_name_plural = "Detalles de nomina importada"
        ordering = ['empleado_nombre']

    def __str__(self):
        return f"{self.empleado_nombre} - {self.lote.codigo}"


class ConceptoNominaImportada(models.Model):
    TIPOS = [
        ('devengado', 'Devengado'),
        ('deduccion', 'Deduccion'),
    ]

    detalle = models.ForeignKey(DetalleNominaImportada, on_delete=models.CASCADE, related_name='conceptos')
    tipo = models.CharField(max_length=20, choices=TIPOS)
    codigo = models.CharField(max_length=20)
    nombre = models.CharField(max_length=120)
    valor = models.DecimalField(max_digits=12, decimal_places=2)

    class Meta:
        verbose_name = "Concepto de nomina importada"
        verbose_name_plural = "Conceptos de nomina importada"
        ordering = ['tipo', 'codigo']

    def __str__(self):
        return f"{self.nombre} - {self.valor}"


class Presupuesto(models.Model):
    nombre = models.CharField(max_length=150)
    area = models.CharField(max_length=100)
    monto_asignado = models.DecimalField(max_digits=12, decimal_places=2)
    monto_gastado = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    mes = models.CharField(max_length=20)
    anio = models.IntegerField()
    descripcion = models.TextField(blank=True)

    def saldo_disponible(self):
        return self.monto_asignado - self.monto_gastado

    def __str__(self):
        return f"{self.nombre} - {self.mes} {self.anio}"

    class Meta:
        verbose_name = "Presupuesto"
        verbose_name_plural = "Presupuestos"


class PlanPresupuestal(models.Model):
    ESTADOS = [
        ('borrador', 'Borrador'),
        ('aprobado', 'Aprobado'),
        ('ejecucion', 'En ejecucion'),
        ('cerrado', 'Cerrado'),
    ]

    nombre = models.CharField(max_length=150)
    anio = models.IntegerField(unique=True)
    estado = models.CharField(max_length=20, choices=ESTADOS, default='borrador')
    fecha_aprobacion = models.DateField(null=True, blank=True)
    descripcion = models.TextField(blank=True)

    class Meta:
        verbose_name = "Plan presupuestal"
        verbose_name_plural = "Planes presupuestales"
        ordering = ['-anio']

    def __str__(self):
        return f"{self.nombre} - {self.anio}"

    def total_inicial(self):
        return sum((partida.monto_inicial for partida in self.partidas.all()), Decimal('0.00'))

    def total_ajustes(self):
        return sum((partida.total_ajustes() for partida in self.partidas.all()), Decimal('0.00'))

    def total_vigente(self):
        return self.total_inicial() + self.total_ajustes()

    def total_ejecutado(self):
        return sum((partida.monto_ejecutado for partida in self.partidas.all()), Decimal('0.00'))

    def total_disponible(self):
        return self.total_vigente() - self.total_ejecutado()


class PartidaPresupuestal(models.Model):
    plan = models.ForeignKey(PlanPresupuestal, on_delete=models.CASCADE, related_name='partidas')
    area = models.CharField(max_length=100)
    concepto = models.CharField(max_length=150)
    monto_inicial = models.DecimalField(max_digits=14, decimal_places=2)
    monto_ejecutado = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    descripcion = models.TextField(blank=True)

    class Meta:
        verbose_name = "Partida presupuestal"
        verbose_name_plural = "Partidas presupuestales"
        ordering = ['area', 'concepto']

    def __str__(self):
        return f"{self.area} - {self.concepto}"

    def total_ajustes(self):
        total = Decimal('0.00')
        for ajuste in self.ajustes.filter(estado='aprobado'):
            if ajuste.tipo == 'aumento':
                total += ajuste.valor
            elif ajuste.tipo in ('reduccion', 'traslado_salida'):
                total -= ajuste.valor
            elif ajuste.tipo == 'traslado_entrada':
                total += ajuste.valor
        return total

    def presupuesto_vigente(self):
        return self.monto_inicial + self.total_ajustes()

    def disponible(self):
        return self.presupuesto_vigente() - self.monto_ejecutado

    def porcentaje_ejecucion(self):
        vigente = self.presupuesto_vigente()
        if not vigente:
            return Decimal('0.00')
        return ((self.monto_ejecutado / vigente) * Decimal('100')).quantize(Decimal('0.01'))


class RevisionPresupuestal(models.Model):
    DECISIONES = [
        ('mantener', 'Mantener'),
        ('ajustar', 'Ajustar'),
        ('congelar', 'Congelar'),
        ('ampliar', 'Ampliar'),
    ]

    plan = models.ForeignKey(PlanPresupuestal, on_delete=models.CASCADE, related_name='revisiones')
    trimestre = models.IntegerField(choices=[(1, 'Trimestre 1'), (2, 'Trimestre 2'), (3, 'Trimestre 3'), (4, 'Trimestre 4')])
    fecha_revision = models.DateField(default=timezone.now)
    decision = models.CharField(max_length=20, choices=DECISIONES)
    observaciones = models.TextField()

    class Meta:
        verbose_name = "Revision presupuestal"
        verbose_name_plural = "Revisiones presupuestales"
        ordering = ['-fecha_revision']
        unique_together = ('plan', 'trimestre')

    def __str__(self):
        return f"{self.plan} - T{self.trimestre}"


class AjustePresupuestal(models.Model):
    TIPOS = [
        ('aumento', 'Aumento'),
        ('reduccion', 'Reduccion'),
        ('traslado_entrada', 'Traslado de entrada'),
        ('traslado_salida', 'Traslado de salida'),
    ]

    ESTADOS = [
        ('solicitado', 'Solicitado'),
        ('aprobado', 'Aprobado'),
        ('rechazado', 'Rechazado'),
    ]

    partida = models.ForeignKey(PartidaPresupuestal, on_delete=models.CASCADE, related_name='ajustes')
    tipo = models.CharField(max_length=25, choices=TIPOS)
    valor = models.DecimalField(max_digits=14, decimal_places=2)
    motivo = models.TextField()
    fecha = models.DateField(default=timezone.now)
    estado = models.CharField(max_length=20, choices=ESTADOS, default='aprobado')

    class Meta:
        verbose_name = "Ajuste presupuestal"
        verbose_name_plural = "Ajustes presupuestales"
        ordering = ['-fecha']

    def __str__(self):
        return f"{self.get_tipo_display()} - {self.valor}"


class Ingreso(models.Model):
    concepto = models.CharField(max_length=150)
    monto = models.DecimalField(max_digits=12, decimal_places=2)
    fecha = models.DateField()
    fuente = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)

    def __str__(self):
        return f"{self.concepto} - ${self.monto}"

    class Meta:
        verbose_name = "Ingreso"
        verbose_name_plural = "Ingresos"
