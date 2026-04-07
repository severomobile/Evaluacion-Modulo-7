# Generated migration — Alke Wallet Módulo 7
# Equivalente a: python manage.py makemigrations wallet

from django.db import migrations, models
import django.core.validators
import django.db.models.deletion
from decimal import Decimal


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        # ── Tabla: wallet_usuario ──────────────────────────────────────────
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id', models.BigAutoField(
                    auto_created=True, primary_key=True,
                    serialize=False, verbose_name='ID'
                )),
                ('nombre', models.CharField(
                    max_length=100, verbose_name='Nombre'
                )),
                ('apellido', models.CharField(
                    max_length=100, verbose_name='Apellido'
                )),
                ('email', models.EmailField(
                    max_length=254, unique=True,
                    verbose_name='Correo electrónico'
                )),
                ('balance', models.DecimalField(
                    decimal_places=2,
                    default=Decimal('0.00'),
                    max_digits=12,
                    validators=[
                        django.core.validators.MinValueValidator(Decimal('0.00'))
                    ],
                    verbose_name='Balance'
                )),
                ('fecha_creacion', models.DateTimeField(
                    auto_now_add=True,
                    verbose_name='Fecha de creación'
                )),
            ],
            options={
                'verbose_name': 'Usuario',
                'verbose_name_plural': 'Usuarios',
                'ordering': ['-fecha_creacion'],
            },
        ),
        # ── Tabla: wallet_transaccion ──────────────────────────────────────
        migrations.CreateModel(
            name='Transaccion',
            fields=[
                ('id', models.BigAutoField(
                    auto_created=True, primary_key=True,
                    serialize=False, verbose_name='ID'
                )),
                ('tipo', models.CharField(
                    choices=[
                        ('DEP', 'Depósito'),
                        ('RET', 'Retiro'),
                        ('TRF', 'Transferencia'),
                    ],
                    default='DEP',
                    max_length=3,
                    verbose_name='Tipo'
                )),
                ('monto', models.DecimalField(
                    decimal_places=2,
                    max_digits=12,
                    validators=[
                        django.core.validators.MinValueValidator(Decimal('0.01'))
                    ],
                    verbose_name='Monto'
                )),
                ('descripcion', models.TextField(
                    blank=True, null=True,
                    verbose_name='Descripción'
                )),
                ('fecha', models.DateTimeField(
                    auto_now_add=True,
                    verbose_name='Fecha'
                )),
                # ── Relación FK: Transaccion → Usuario (CASCADE) ───────────
                ('usuario', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='transacciones',
                    to='wallet.usuario',
                    verbose_name='Usuario'
                )),
            ],
            options={
                'verbose_name': 'Transacción',
                'verbose_name_plural': 'Transacciones',
                'ordering': ['-fecha'],
            },
        ),
    ]
