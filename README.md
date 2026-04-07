# 💼 Alke Wallet — Módulo 7

Aplicación web desarrollada con **Django + SQLite** para la gestión de usuarios y transacciones financieras. Proyecto de evaluación del Módulo 7 — Alkemy.

---

## 📐 Arquitectura del Proyecto

```
alke_wallet/
│
├── alke_wallet/              # Configuración del proyecto Django
│   ├── settings.py           # Variables de entorno, BD, apps instaladas
│   ├── urls.py               # Rutas raíz (delega a wallet.urls)
│   └── wsgi.py               # Punto de entrada WSGI
│
├── wallet/                   # Aplicación principal
│   ├── migrations/
│   │   └── 0001_initial.py   # Migración inicial (Usuario + Transaccion)
│   ├── templates/wallet/
│   │   ├── base.html         # Layout base con navbar Bootstrap 5
│   │   ├── dashboard.html    # Vista resumen del sistema
│   │   ├── usuarios/         # Templates CRUD de usuarios
│   │   └── transacciones/    # Templates CRUD de transacciones
│   ├── admin.py              # Registro en panel de administración
│   ├── apps.py               # Configuración de la app
│   ├── forms.py              # Formularios con validaciones
│   ├── models.py             # Modelos ORM: Usuario, Transaccion
│   ├── urls.py               # Rutas de la app wallet
│   └── views.py              # Lógica CRUD + reglas de negocio
│
├── db.sqlite3                # Base de datos (se genera al migrar)
├── manage.py                 # CLI de administración Django
└── requirements.txt          # Dependencias del proyecto
```

---

## 🗃️ Modelo de Datos

### Usuario
| Campo          | Tipo           | Descripción                          |
|----------------|----------------|--------------------------------------|
| id             | BigAutoField   | Clave primaria autogenerada          |
| nombre         | CharField(100) | Nombre de pila                       |
| apellido       | CharField(100) | Apellido                             |
| email          | EmailField     | Correo único (identificador natural) |
| balance        | DecimalField   | Saldo disponible (≥ 0.00)           |
| fecha_creacion | DateTimeField  | Timestamp automático de creación     |

### Transaccion
| Campo       | Tipo           | Descripción                                  |
|-------------|----------------|----------------------------------------------|
| id          | BigAutoField   | Clave primaria autogenerada                  |
| usuario     | ForeignKey     | Relación N:1 con Usuario (CASCADE)           |
| tipo        | CharField(3)   | `DEP` Depósito / `RET` Retiro / `TRF` Transferencia |
| monto       | DecimalField   | Importe de la operación (> 0.00)            |
| descripcion | TextField      | Texto libre opcional                         |
| fecha       | DateTimeField  | Timestamp automático de creación             |

### Diagrama de relaciones
```
┌─────────────┐          ┌──────────────────┐
│   Usuario   │          │   Transaccion    │
├─────────────┤  1 ──< N ├──────────────────┤
│ id (PK)     │──────────│ id (PK)          │
│ nombre      │          │ usuario_id (FK)  │
│ apellido    │          │ tipo             │
│ email       │          │ monto            │
│ balance     │          │ descripcion      │
│ fecha_crec  │          │ fecha            │
└─────────────┘          └──────────────────┘
```

---

## ⚙️ Instalación y Configuración

### 1. Requisitos previos
- Python 3.10 o superior
- pip

### 2. Clonar / descomprimir el proyecto
```bash
unzip alke_wallet.zip
cd alke_wallet
```

### 3. Crear y activar entorno virtual
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### 4. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 5. Aplicar migraciones
```bash
python manage.py migrate
```

### 6. (Opcional) Crear superusuario para el panel admin
```bash
python manage.py createsuperuser
```

### 7. Ejecutar el servidor de desarrollo
```bash
python manage.py runserver
```

Abrir en el navegador: **http://127.0.0.1:8000**

---

## 🧭 Rutas Disponibles

| URL                                  | Vista                  | Descripción                   |
|--------------------------------------|------------------------|-------------------------------|
| `/`                                  | dashboard              | Panel de resumen              |
| `/usuarios/`                         | usuario_lista          | Listado de usuarios           |
| `/usuarios/nuevo/`                   | usuario_crear          | Formulario crear usuario      |
| `/usuarios/<pk>/`                    | usuario_detalle        | Detalle + historial           |
| `/usuarios/<pk>/editar/`             | usuario_editar         | Editar usuario                |
| `/usuarios/<pk>/eliminar/`           | usuario_eliminar       | Confirmar eliminación         |
| `/transacciones/`                    | transaccion_lista      | Listado de transacciones      |
| `/transacciones/nueva/`              | transaccion_crear      | Registrar transacción         |
| `/transacciones/<pk>/editar/`        | transaccion_editar     | Editar transacción            |
| `/transacciones/<pk>/eliminar/`      | transaccion_eliminar   | Confirmar eliminación         |
| `/admin/`                            | Django Admin           | Panel de administración       |

---

## ✅ Reglas de Negocio Implementadas

- **Depósito** → suma el monto al balance del usuario.
- **Retiro / Transferencia** → descuenta el monto; se rechaza si el balance es insuficiente.
- **Editar transacción** → revierte el efecto anterior y aplica el nuevo de forma atómica.
- **Eliminar transacción** → revierte el efecto sobre el balance antes de borrar.
- Todas las operaciones sobre balance usan `db_transaction.atomic()` para garantizar consistencia.

---

## 🛠️ Tecnologías Utilizadas

| Tecnología      | Versión  | Rol                          |
|-----------------|----------|------------------------------|
| Python          | 3.10+    | Lenguaje base                |
| Django          | 4.2.x    | Framework web + ORM          |
| SQLite          | (built-in)| Base de datos relacional     |
| Bootstrap       | 5.3.2    | Estilos e interfaz (CDN)     |
| Bootstrap Icons | 1.11.3   | Iconografía (CDN)            |

---

## 📦 Comandos Útiles

```bash
# Generar nuevas migraciones tras modificar modelos
python manage.py makemigrations

# Aplicar migraciones pendientes
python manage.py migrate

# Ver migraciones aplicadas
python manage.py showmigrations

# Shell interactivo para consultas ORM
python manage.py shell

# Ejemplos de operaciones ORM en el shell:
# >>> from wallet.models import Usuario, Transaccion
# >>> Usuario.objects.all()
# >>> Usuario.objects.filter(balance__gt=0)
# >>> Transaccion.objects.select_related('usuario').filter(tipo='DEP')
```

---

## 📸 Capturas de Pantalla

Las capturas se encuentran en la carpeta `screenshots/` dentro del proyecto.
Para reproducirlas, levantar el servidor con `python manage.py runserver` y navegar cada sección.

```
screenshots/
├── 01_dashboard.png
├── 02_usuarios_lista.png
├── 03_usuario_detalle.png
├── 04_transacciones_lista.png
└── 05_migraciones_terminal.png
```

| Archivo | Qué mostrar |
|---|---|
| `01_dashboard.png` | Dashboard con el resumen general del sistema y últimas transacciones cargadas |
| `02_usuarios_lista.png` | Lista de usuarios con balances y botones de acción (crear, editar, eliminar) |
| `03_usuario_detalle.png` | Detalle de un usuario con su historial completo de transacciones |
| `04_transacciones_lista.png` | Lista de transacciones mostrando depósitos, retiros y transferencias |
| `05_migraciones_terminal.png` | Terminal con la ejecución exitosa de `python manage.py migrate` |

---

## 👤 Autoría

Proyecto desarrollado como evaluación del **Módulo 7 — Desarrollo Web con Django**