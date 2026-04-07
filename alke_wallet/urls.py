"""
URLs raíz del proyecto Alke Wallet.
"""

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('wallet.urls')),  # Delega todas las rutas a la app wallet
]
