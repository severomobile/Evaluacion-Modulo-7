"""
urls.py — Rutas de la aplicación wallet.

Convención de nombres:
    usuario_*      → CRUD de usuarios
    transaccion_*  → CRUD de transacciones
"""

from django.urls import path
from . import views

urlpatterns = [
    # ── Dashboard ─────────────────────────────────────────────────────────
    path('', views.dashboard, name='dashboard'),

    # ── Usuarios ──────────────────────────────────────────────────────────
    path('usuarios/',                  views.usuario_lista,    name='usuario_lista'),
    path('usuarios/nuevo/',            views.usuario_crear,    name='usuario_crear'),
    path('usuarios/<int:pk>/',         views.usuario_detalle,  name='usuario_detalle'),
    path('usuarios/<int:pk>/editar/',  views.usuario_editar,   name='usuario_editar'),
    path('usuarios/<int:pk>/eliminar/', views.usuario_eliminar, name='usuario_eliminar'),

    # ── Transacciones ──────────────────────────────────────────────────────
    path('transacciones/',                  views.transaccion_lista,    name='transaccion_lista'),
    path('transacciones/nueva/',            views.transaccion_crear,    name='transaccion_crear'),
    path('transacciones/<int:pk>/editar/',  views.transaccion_editar,   name='transaccion_editar'),
    path('transacciones/<int:pk>/eliminar/', views.transaccion_eliminar, name='transaccion_eliminar'),
]
