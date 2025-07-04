from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal
from django.contrib.auth.models import User

class MovimientoFinanciero(models.Model):
    CATEGORIA_CHOICES = [
        ('ingreso', 'Ingreso'),
        ('gasto', 'Gasto'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='movimientos')
    descripcion = models.CharField(max_length=200, verbose_name="Descripción")
    monto = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        validators=[MinValueValidator(Decimal('0.01'))],
        verbose_name="Monto"
    )
    categoria = models.CharField(
        max_length=10, 
        choices=CATEGORIA_CHOICES, 
        verbose_name="Categoría"
    )
    fecha = models.DateField(verbose_name="Fecha")
    notas = models.TextField(blank=True, null=True, verbose_name="Notas")
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    fecha_actualizacion = models.DateTimeField(auto_now=True, verbose_name="Fecha de actualización")

    class Meta:
        ordering = ['-fecha', '-fecha_creacion']
        verbose_name = "Movimiento Financiero"
        verbose_name_plural = "Movimientos Financieros"

    def __str__(self):
        return f"{self.descripcion} - {self.monto} ({self.categoria})"

    @property
    def es_ingreso(self):
        return self.categoria == 'ingreso'

    @property
    def es_gasto(self):
        return self.categoria == 'gasto'
