"""
views.py — Vistas CRUD para Usuario y Transaccion.

Principios aplicados:
    - Single Responsibility: cada función maneja un único caso de uso.
    - DRY: lógica compartida centralizada en helpers y formularios.
    - Manejo de errores: bloques try/except con mensajes de feedback al usuario.
    - Validación de negocio: balance no puede quedar negativo en retiros.
"""

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db import transaction as db_transaction
from decimal import Decimal, InvalidOperation

from .models import Usuario, Transaccion
from .forms import UsuarioForm, TransaccionForm


# ══════════════════════════════════════════════════════════════════════════════
#  DASHBOARD
# ══════════════════════════════════════════════════════════════════════════════

def dashboard(request):
    """
    Vista principal: resumen del sistema.
    Muestra totales y las últimas transacciones registradas.
    """
    context = {
        'total_usuarios':     Usuario.objects.count(),
        'total_transacciones': Transaccion.objects.count(),
        'ultimas_transacciones': Transaccion.objects.select_related('usuario')[:5],
    }
    return render(request, 'wallet/dashboard.html', context)


# ══════════════════════════════════════════════════════════════════════════════
#  USUARIOS — CRUD
# ══════════════════════════════════════════════════════════════════════════════

def usuario_lista(request):
    """Lista todos los usuarios registrados."""
    usuarios = Usuario.objects.all()
    return render(request, 'wallet/usuarios/lista.html', {'usuarios': usuarios})


def usuario_detalle(request, pk):
    """Muestra el detalle de un usuario y su historial de transacciones."""
    usuario = get_object_or_404(Usuario, pk=pk)
    transacciones = usuario.transacciones.all()
    return render(request, 'wallet/usuarios/detalle.html', {
        'usuario': usuario,
        'transacciones': transacciones,
    })


def usuario_crear(request):
    """
    Crea un nuevo usuario.
    GET  → renderiza el formulario vacío.
    POST → valida, guarda y redirige a la lista.
    """
    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid():
            try:
                usuario = form.save()
                messages.success(request, f'Usuario "{usuario.nombre_completo}" creado exitosamente.')
                return redirect('usuario_lista')
            except Exception as e:
                messages.error(request, f'Error al crear el usuario: {e}')
    else:
        form = UsuarioForm()

    return render(request, 'wallet/usuarios/form.html', {
        'form': form,
        'titulo': 'Crear Usuario',
        'accion': 'Crear',
    })


def usuario_editar(request, pk):
    """
    Edita un usuario existente.
    GET  → formulario precargado con los datos actuales.
    POST → valida, actualiza y redirige a la lista.
    """
    usuario = get_object_or_404(Usuario, pk=pk)

    if request.method == 'POST':
        form = UsuarioForm(request.POST, instance=usuario)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, f'Usuario "{usuario.nombre_completo}" actualizado.')
                return redirect('usuario_lista')
            except Exception as e:
                messages.error(request, f'Error al actualizar el usuario: {e}')
    else:
        form = UsuarioForm(instance=usuario)

    return render(request, 'wallet/usuarios/form.html', {
        'form': form,
        'titulo': 'Editar Usuario',
        'accion': 'Guardar Cambios',
        'usuario': usuario,
    })


def usuario_eliminar(request, pk):
    """
    Elimina un usuario y todas sus transacciones (CASCADE).
    GET  → página de confirmación.
    POST → ejecuta la eliminación.
    """
    usuario = get_object_or_404(Usuario, pk=pk)

    if request.method == 'POST':
        try:
            nombre = usuario.nombre_completo
            usuario.delete()
            messages.success(request, f'Usuario "{nombre}" eliminado correctamente.')
            return redirect('usuario_lista')
        except Exception as e:
            messages.error(request, f'Error al eliminar el usuario: {e}')

    return render(request, 'wallet/usuarios/confirmar_eliminar.html', {'usuario': usuario})


# ══════════════════════════════════════════════════════════════════════════════
#  TRANSACCIONES — CRUD
# ══════════════════════════════════════════════════════════════════════════════

def transaccion_lista(request):
    """Lista todas las transacciones con sus usuarios relacionados."""
    transacciones = Transaccion.objects.select_related('usuario').all()
    return render(request, 'wallet/transacciones/lista.html', {'transacciones': transacciones})


def transaccion_crear(request):
    """
    Crea una nueva transacción aplicando la regla de negocio:
      - DEPOSITO     → suma al balance del usuario.
      - RETIRO       → resta del balance; rechaza si saldo insuficiente.
      - TRANSFERENCIA → descuenta del balance (representación simplificada).

    Usa db_transaction.atomic() para garantizar consistencia:
    si falla la actualización del balance, la transacción no se guarda.
    """
    if request.method == 'POST':
        form = TransaccionForm(request.POST)
        if form.is_valid():
            try:
                with db_transaction.atomic():
                    transaccion = form.save(commit=False)
                    usuario = transaccion.usuario
                    monto = transaccion.monto

                    # ── Regla de negocio: validar saldo en retiros ──────────
                    if transaccion.tipo in (
                        Transaccion.TipoTransaccion.RETIRO,
                        Transaccion.TipoTransaccion.TRANSFERENCIA,
                    ):
                        if usuario.balance < monto:
                            messages.error(
                                request,
                                f'Saldo insuficiente. Balance actual: ${usuario.balance}'
                            )
                            return render(request, 'wallet/transacciones/form.html', {
                                'form': form,
                                'titulo': 'Nueva Transacción',
                                'accion': 'Registrar',
                            })
                        usuario.balance -= monto
                    else:
                        # DEPOSITO
                        usuario.balance += monto

                    usuario.save()
                    transaccion.save()

                messages.success(request, f'Transacción de ${monto} registrada exitosamente.')
                return redirect('transaccion_lista')

            except (InvalidOperation, Exception) as e:
                messages.error(request, f'Error al procesar la transacción: {e}')
    else:
        form = TransaccionForm()

    return render(request, 'wallet/transacciones/form.html', {
        'form': form,
        'titulo': 'Nueva Transacción',
        'accion': 'Registrar',
    })


def transaccion_editar(request, pk):
    """
    Edita una transacción existente.
    IMPORTANTE: revierte el efecto anterior sobre el balance y aplica el nuevo.
    """
    transaccion = get_object_or_404(Transaccion, pk=pk)

    if request.method == 'POST':
        form = TransaccionForm(request.POST, instance=transaccion)
        if form.is_valid():
            try:
                with db_transaction.atomic():
                    nueva = form.save(commit=False)
                    usuario = nueva.usuario
                    monto_anterior = transaccion.monto
                    tipo_anterior  = transaccion.tipo

                    # ── Revertir efecto anterior ────────────────────────────
                    if tipo_anterior in (
                        Transaccion.TipoTransaccion.RETIRO,
                        Transaccion.TipoTransaccion.TRANSFERENCIA,
                    ):
                        usuario.balance += monto_anterior
                    else:
                        usuario.balance -= monto_anterior

                    # ── Aplicar nuevo efecto ────────────────────────────────
                    if nueva.tipo in (
                        Transaccion.TipoTransaccion.RETIRO,
                        Transaccion.TipoTransaccion.TRANSFERENCIA,
                    ):
                        if usuario.balance < nueva.monto:
                            messages.error(request, 'Saldo insuficiente para esta operación.')
                            return render(request, 'wallet/transacciones/form.html', {
                                'form': form,
                                'titulo': 'Editar Transacción',
                                'accion': 'Guardar Cambios',
                            })
                        usuario.balance -= nueva.monto
                    else:
                        usuario.balance += nueva.monto

                    usuario.save()
                    nueva.save()

                messages.success(request, 'Transacción actualizada correctamente.')
                return redirect('transaccion_lista')

            except Exception as e:
                messages.error(request, f'Error al actualizar: {e}')
    else:
        form = TransaccionForm(instance=transaccion)

    return render(request, 'wallet/transacciones/form.html', {
        'form': form,
        'titulo': 'Editar Transacción',
        'accion': 'Guardar Cambios',
    })


def transaccion_eliminar(request, pk):
    """
    Elimina una transacción y revierte su efecto sobre el balance del usuario.
    GET  → confirmación.
    POST → eliminación atómica.
    """
    transaccion = get_object_or_404(Transaccion, pk=pk)

    if request.method == 'POST':
        try:
            with db_transaction.atomic():
                usuario = transaccion.usuario

                # ── Revertir efecto en el balance ───────────────────────────
                if transaccion.tipo in (
                    Transaccion.TipoTransaccion.RETIRO,
                    Transaccion.TipoTransaccion.TRANSFERENCIA,
                ):
                    usuario.balance += transaccion.monto
                else:
                    saldo_resultante = usuario.balance - transaccion.monto
                    usuario.balance = max(Decimal('0.00'), saldo_resultante)

                usuario.save()
                transaccion.delete()

            messages.success(request, 'Transacción eliminada y balance revertido.')
            return redirect('transaccion_lista')

        except Exception as e:
            messages.error(request, f'Error al eliminar: {e}')

    return render(request, 'wallet/transacciones/confirmar_eliminar.html', {
        'transaccion': transaccion
    })
