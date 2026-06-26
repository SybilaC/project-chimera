from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator


class Categoria(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)

    def __str__(self):
        return self.nombre


class Servicio(models.Model):
    nombre = models.CharField(max_length=150)
    descripcion = models.TextField()
    precio = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(1)]
    )
    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.CASCADE,
        related_name='servicios'
    )
    imagen_url = models.URLField(blank=True)
    disponible = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre


class Carrito(models.Model):
    usuario = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )
    creado = models.DateTimeField(auto_now_add=True)

    def total(self):
        return sum(item.subtotal() for item in self.items.all())

    def __str__(self):
        return f"Carrito de {self.usuario.username}"


class ItemCarrito(models.Model):
    carrito = models.ForeignKey(
        Carrito,
        on_delete=models.CASCADE,
        related_name='items'
    )
    servicio = models.ForeignKey(
        Servicio,
        on_delete=models.CASCADE
    )
    cantidad = models.PositiveIntegerField(
        default=1,
        validators=[MinValueValidator(1)]
    )

    def subtotal(self):
        return self.servicio.precio * self.cantidad

    def __str__(self):
        return f"{self.servicio.nombre} x {self.cantidad}"


class Orden(models.Model):
    usuario = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    fecha = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    def __str__(self):
        return f"Orden #{self.id} - {self.usuario.username}"


class ItemOrden(models.Model):
    orden = models.ForeignKey(
        Orden,
        on_delete=models.CASCADE,
        related_name='items'
    )
    servicio = models.ForeignKey(
        Servicio,
        on_delete=models.CASCADE
    )
    cantidad = models.PositiveIntegerField()
    precio_unitario = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    def subtotal(self):
        return self.precio_unitario * self.cantidad

    def __str__(self):
        return f"{self.servicio.nombre} x {self.cantidad}"