from django.db import models


class Nomina(models.Model):
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
        verbose_name = "Nómina"
        verbose_name_plural = "Nóminas"


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