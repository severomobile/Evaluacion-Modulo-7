"""
admin.py — Registro de modelos en el panel de administración de Django.
"""

from django.contrib import admin
from .models import Usuario, Transaccion


@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display  = ('nombre_completo', 'email', 'balance', 'fecha_creacion')
    search_fields = ('nombre', 'apellido', 'email')
    list_filter   = ('fecha_creacion',)
    readonly_fields = ('fecha_creacion',)


@admin.register(Transaccion)
class TransaccionAdmin(admin.ModelAdmin):
    list_display  = ('usuario', 'tipo', 'monto', 'fecha')
    search_fields = ('usuario__nombre', 'usuario__apellido', 'descripcion')
    list_filter   = ('tipo', 'fecha')
    readonly_fields = ('fecha',)
