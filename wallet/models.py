"""
models.py — Definición del modelo de datos de Alke Wallet.

Modelos:
    - Usuario: representa a un cliente de la billetera digital.
    - Transaccion: representa una operación financiera asociada a un usuario.

Relaciones:
    - Usuario (1) ──< Transaccion (N)  →  ForeignKey con CASCADE
"""

from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal


class Usuario(models.Model):
    """
    Representa a un usuario/cliente de Alke Wallet.

    Campos:
        nombre        — Nombre de pila del usuario.
        apellido      — Apellido del usuario.
        email         — Correo único, utilizado como identificador natural.
        balance       — Saldo disponible en la billetera (nunca negativo).
        fecha_creacion — Timestamp automático al crear el registro.
    """

    nombre = models.CharField(
        max_length=100,
        verbose_name='Nombre'
    )
    apellido = models.CharField(
        max_length=100,
        verbose_name='Apellido'
    )
    email = models.EmailField(
        unique=True,
        verbose_name='Correo electrónico'
    )
    balance = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal('0.00'),
        validators=[MinValueValidator(Decimal('0.00'))],
        verbose_name='Balance'
    )
    fecha_creacion = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Fecha de creación'
    )

    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
        ordering = ['-fecha_creacion']

    def __str__(self):
        return f'{self.nombre} {self.apellido} — {self.email}'

    @property
    def nombre_completo(self):
        """Retorna el nombre completo del usuario."""
        return f'{self.nombre} {self.apellido}'


class Transaccion(models.Model):
    """
    Representa una operación financiera vinculada a un Usuario.

    Tipos de transacción:
        DEPOSITO    — Ingreso de fondos al balance.
        RETIRO      — Egreso de fondos del balance.
        TRANSFERENCIA — Movimiento entre cuentas (representación informativa).

    Campos:
        usuario     — FK al Usuario propietario de la transacción.
        tipo        — Categoría de la operación (choices).
        monto       — Importe de la operación (debe ser positivo).
        descripcion — Texto libre opcional para detallar la operación.
        fecha       — Timestamp automático al crear el registro.
    """

    class TipoTransaccion(models.TextChoices):
        DEPOSITO      = 'DEP', 'Depósito'
        RETIRO        = 'RET', 'Retiro'
        TRANSFERENCIA = 'TRF', 'Transferencia'

    usuario = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        related_name='transacciones',
        verbose_name='Usuario'
    )
    tipo = models.CharField(
        max_length=3,
        choices=TipoTransaccion.choices,
        default=TipoTransaccion.DEPOSITO,
        verbose_name='Tipo'
    )
    monto = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))],
        verbose_name='Monto'
    )
    descripcion = models.TextField(
        blank=True,
        null=True,
        verbose_name='Descripción'
    )
    fecha = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Fecha'
    )

    class Meta:
        verbose_name = 'Transacción'
        verbose_name_plural = 'Transacciones'
        ordering = ['-fecha']

    def __str__(self):
        return f'[{self.get_tipo_display()}] ${self.monto} — {self.usuario.nombre_completo}'
