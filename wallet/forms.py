"""
forms.py — Formularios para Usuario y Transaccion.

Cada formulario extiende ModelForm para aprovechar la validación
automática del ORM y añade validaciones de negocio adicionales.
"""

from django import forms
from .models import Usuario, Transaccion


class UsuarioForm(forms.ModelForm):
    """Formulario para crear y editar usuarios."""

    class Meta:
        model  = Usuario
        fields = ['nombre', 'apellido', 'email', 'balance']
        widgets = {
            'nombre':   forms.TextInput(attrs={
                'class': 'form-control', 'placeholder': 'Ej: Juan'
            }),
            'apellido': forms.TextInput(attrs={
                'class': 'form-control', 'placeholder': 'Ej: Pérez'
            }),
            'email':    forms.EmailInput(attrs={
                'class': 'form-control', 'placeholder': 'juan@ejemplo.com'
            }),
            'balance':  forms.NumberInput(attrs={
                'class': 'form-control', 'step': '0.01', 'min': '0'
            }),
        }

    def clean_balance(self):
        """Valida que el balance inicial no sea negativo."""
        balance = self.cleaned_data.get('balance')
        if balance is not None and balance < 0:
            raise forms.ValidationError('El balance no puede ser negativo.')
        return balance

    def clean_nombre(self):
        """Valida que el nombre sólo contenga letras y espacios."""
        nombre = self.cleaned_data.get('nombre', '').strip()
        if not nombre.replace(' ', '').isalpha():
            raise forms.ValidationError('El nombre solo puede contener letras.')
        return nombre.title()

    def clean_apellido(self):
        """Valida que el apellido sólo contenga letras y espacios."""
        apellido = self.cleaned_data.get('apellido', '').strip()
        if not apellido.replace(' ', '').isalpha():
            raise forms.ValidationError('El apellido solo puede contener letras.')
        return apellido.title()


class TransaccionForm(forms.ModelForm):
    """Formulario para registrar y editar transacciones."""

    class Meta:
        model  = Transaccion
        fields = ['usuario', 'tipo', 'monto', 'descripcion']
        widgets = {
            'usuario':    forms.Select(attrs={'class': 'form-select'}),
            'tipo':       forms.Select(attrs={'class': 'form-select'}),
            'monto':      forms.NumberInput(attrs={
                'class': 'form-control', 'step': '0.01', 'min': '0.01'
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control', 'rows': 3,
                'placeholder': 'Descripción opcional de la operación...'
            }),
        }

    def clean_monto(self):
        """Valida que el monto sea estrictamente positivo."""
        monto = self.cleaned_data.get('monto')
        if monto is not None and monto <= 0:
            raise forms.ValidationError('El monto debe ser mayor a cero.')
        return monto
