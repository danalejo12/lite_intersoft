from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal 
# Create your models here.


# Categoria y Producto

class Categoria(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre


class Producto(models.Model):
    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.PROTECT,
        related_name="productos"
    )

    sku = models.CharField(max_length=30, unique=True)
    nombre = models.CharField(max_length=150)
    descripcion = models.TextField(blank=True)

    precio_compra = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.00"))]
    )

    precio_venta = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.00"))]
    )

    stock = models.PositiveIntegerField(default=0)
    stock_minimo = models.PositiveIntegerField(default=5)

    activo = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nombre} - {self.sku}"

# Cliente

from django.db import models


class Cliente(models.Model):
    nombre = models.CharField(max_length=150)
    documento = models.CharField(
        max_length=20,
        unique=True
    )
    telefono = models.CharField(
        max_length=20,
        blank=True
    )
    correo = models.EmailField(blank=True)
    direccion = models.CharField(
        max_length=200,
        blank=True
    )
    fecha_registro = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.nombre} - {self.documento}"

# Ventas 

from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator
from decimal import Decimal


class Venta(models.Model):
    ESTADOS = [
        ("PENDIENTE", "Pendiente"),
        ("COMPLETADA", "Completada"),
        ("CANCELADA", "Cancelada"),
    ]

    numero = models.CharField(
        max_length=30,
        unique=True
    )

    cliente = models.ForeignKey(
        "Cliente",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="ventas"
    )

    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT
    )

    fecha = models.DateTimeField(auto_now_add=True)

    subtotal = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    impuesto = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    total = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    estado = models.CharField(
        max_length=15,
        choices=ESTADOS,
        default="PENDIENTE"
    )

    def __str__(self):
        return f"Venta {self.numero}"


class DetalleVenta(models.Model):
    venta = models.ForeignKey(
        Venta,
        on_delete=models.CASCADE,
        related_name="detalles"
    )

    producto = models.ForeignKey(
        "Producto",
        on_delete=models.PROTECT
    )

    cantidad = models.PositiveIntegerField(
        validators=[MinValueValidator(1)]
    )

    precio_unitario = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.00"))]
    )

    subtotal = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    def __str__(self):
        return f"{self.producto.nombre} x {self.cantidad}"

# modelo de inventario


from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator


class MovimientoStock(models.Model):
    TIPOS = [
        ("ENTRADA", "Entrada"),
        ("SALIDA", "Salida"),
        ("AJUSTE", "Ajuste"),
    ]

    producto = models.ForeignKey(
        "Producto",
        on_delete=models.PROTECT,
        related_name="movimientos"
    )

    tipo = models.CharField(
        max_length=10,
        choices=TIPOS
    )

    cantidad = models.PositiveIntegerField(
        validators=[MinValueValidator(1)]
    )

    stock_anterior = models.PositiveIntegerField()
    stock_nuevo = models.PositiveIntegerField()

    motivo = models.CharField(max_length=200)

    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT
    )

    venta = models.ForeignKey(
        "Venta",
        on_delete=models.PROTECT,
        null=True,
        blank=True
    )

    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.tipo} - {self.producto.nombre}"
