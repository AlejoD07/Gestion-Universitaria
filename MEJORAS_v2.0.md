# 🎓 Sistema de Gestión Universitaria - Versión 2.0

## 📋 Descripción General

Sistema web integrado para la administración académica, financiera y operativa de instituciones de educación superior. Implementa control de acceso basado en roles (RBAC) con 6 perfiles de usuario y 5 módulos funcionales interconectados.

---

## 🚀 Novedades en v2.0

### ✨ Mejoras Implementadas

1. **Roles Simplificados**: Reducción de 19 roles a 6 principales:
   - 👤 **Administrador** - Acceso total
   - 👨‍🏫 **Profesor** - Académica + Solicitudes
   - 🎓 **Estudiante** - Académica + Solicitudes
   - 💼 **Contador** - Contabilidad + Solicitudes
   - 👥 **Recursos Humanos** - RRHH + Solicitudes
   - 📦 **Inventario** - Inventario + Solicitudes

2. **Diseño Mejorado**:
   - Bootstrap 5 responsive
   - Gradientes y animaciones smooth
   - Interfaz intuitiva por rol
   - Indicadores visuales claros de permisos

3. **Control de Acceso (RBAC)**:
   - Middleware de validación simplificado
   - Acceso granular por módulo
   - Indicadores visuales de módulos bloqueados
   - Redirección segura a página de permisos denegados

4. **Datos de Prueba**:
   - Management command `setup_roles_usuarios`
   - 8 usuarios predefinidos (1 por rol + extras)
   - 5 facultades
   - 5 programas académicos
   - Período académico 2024-1

---

## 🔐 Credenciales de Acceso

### 1️⃣ Administrador - Acceso Total
```
Documento: 1001
Contraseña: Administrador Sistema
Módulos: Todos (Académica, Contabilidad, RRHH, Inventario, Solicitudes)
```

### 2️⃣ Profesor (2 disponibles)
```
Documento: 2001
Contraseña: Juan Pérez López
Módulos: Académica, Solicitudes

Documento: 2002
Contraseña: María García Rodríguez
Módulos: Académica, Solicitudes
```

### 3️⃣ Estudiante (2 disponibles)
```
Documento: 3001
Contraseña: Carlos Martínez
Código: EST-3001 | Semestre: 3
Módulos: Académica, Solicitudes

Documento: 3002
Contraseña: Ana López Jiménez
Código: EST-3002 | Semestre: 3
Módulos: Académica, Solicitudes
```

### 4️⃣ Recursos Humanos
```
Documento: 4001
Contraseña: Director RRHH
Módulos: RRHH, Solicitudes
```

### 5️⃣ Contador
```
Documento: 5001
Contraseña: Contador Sistema
Módulos: Contabilidad, Solicitudes
```

### 6️⃣ Inventario
```
Documento: 6001
Contraseña: Jefe Inventario
Módulos: Inventario, Solicitudes
```

---

## 🗂️ Estructura del Proyecto

```
DjangoGestionUniversitaria/
├── gestionUniversitaria/          # Configuración central
│   ├── settings.py                 # BD, apps, middleware, templates
│   ├── urls.py                     # Rutas principales
│   ├── views.py                    # Login, logout, dashboard
│   ├── access.py                   # RBAC y matriz de permisos ✨ MEJORADO
│   ├── middleware.py               # Validación de acceso por rol
│   └── wsgi.py
│
├── gestionAcademica/               # Módulo académico
│   ├── models.py                   # Usuario, Rol, Estudiante, Materia, etc.
│   ├── views.py
│   ├── urls.py
│   └── management/commands/
│       └── setup_roles_usuarios.py # ✨ NUEVO - Setup automático
│
├── Contabilidad/                   # Módulo contable
│   ├── models.py                   # Nómina, Presupuesto, Ingreso
│   ├── views.py
│   └── urls.py
│
├── RecursosHumanos/                # Módulo RRHH
│   ├── models.py                   # Empleado, Contrato, Novedades
│   ├── views.py
│   └── urls.py
│
├── inventario/                     # Módulo de inventario
│   ├── models.py                   # Item, Préstamo, Categoría
│   ├── views.py
│   └── urls.py
│
├── solicitudes/                    # Módulo de solicitudes
│   ├── models.py                   # Solicitud, Historial, Comentarios
│   ├── views.py
│   └── urls.py
│
├── templates/                      # Templates compartidos
│   ├── base.html                   # ✨ NUEVO - Base con navbar
│   ├── login.html                  # ✨ MEJORADO - Bootstrap 5
│   ├── home_general.html           # ✨ MEJORADO - Dashboard por rol
│   └── sin_permiso.html            # ✨ MEJORADO - Página de acceso denegado
│
├── manage.py
├── requirements.txt
└── db.sqlite3
```

---

## 🚀 Instalación y Uso

### Prerequisitos
- Python 3.8+
- pip

### Instalación

1. **Clonar y acceder al proyecto**
   ```bash
   cd "DjangoGestionUniversitaria"
   ```

2. **Instalar dependencias**
   ```bash
   pip install -r requirements.txt
   ```

3. **Crear roles y usuarios de prueba**
   ```bash
   python manage.py setup_roles_usuarios
   ```

4. **Ejecutar servidor**
   ```bash
   python manage.py runserver
   ```

5. **Acceder a la plataforma**
   - 🌐 URL: http://127.0.0.1:8000/login/
   - 📝 Usar credenciales de la sección anterior

---

## 📊 Módulos Disponibles

### 📚 1. Gestión Académica
- Usuarios y roles
- Estudiantes y programas
- Materias y asignaciones
- Inscripciones
- Notas y asistencias
- **Acceso**: Admin, Profesor, Estudiante

### 💰 2. Contabilidad
- Nómina de empleados
- Presupuestos
- Ingresos
- Áreas contables
- **Acceso**: Admin, Contador

### 👥 3. Recursos Humanos
- Empleados
- Áreas y cargos
- Contratos
- Novedades laborales
- Certificados laborales
- **Acceso**: Admin, Recursos Humanos

### 📦 4. Inventario
- Items y categorías
- Préstamos
- Control de stock
- **Acceso**: Admin, Inventario

### 📋 5. Solicitudes
- Radicación
- Seguimiento
- Quejas y reclamos
- Documentos adjuntos
- Histórico completo
- **Acceso**: Todos

---

## 🔒 Seguridad y Control de Acceso

### Flujo de Autenticación
```
1. Usuario ingresa documento + nombre
2. Sistema valida credenciales en BD
3. Sesión se crea con rol y módulos permitidos
4. Middleware valida acceso en cada petición
5. Módulos no autorizados muestran "Sin acceso"
```

### Matriz de Permisos

| Rol | Académica | Contabilidad | RRHH | Inventario | Solicitudes |
|-----|-----------|--------------|------|-----------|------------|
| **Administrador** | ✅ | ✅ | ✅ | ✅ | ✅ |
| **Profesor** | ✅ | ❌ | ❌ | ❌ | ✅ |
| **Estudiante** | ✅ | ❌ | ❌ | ❌ | ✅ |
| **Contador** | ❌ | ✅ | ❌ | ❌ | ✅ |
| **RRHH** | ❌ | ❌ | ✅ | ❌ | ✅ |
| **Inventario** | ❌ | ❌ | ❌ | ✅ | ✅ |

### Variables de Sesión
```python
{
    'usuario_academico_id': int,        # ID único del usuario
    'usuario_nombre': str,              # Nombre completo
    'usuario_rol': str,                 # Rol actual
    'usuario_modulos': list,            # Módulos permitidos
}
```

---

## 🎨 Mejoras Visuales

### Templates Base (✨ Nuevo)
- Navbar responsive con datos de usuario
- Footer consistente
- CSS custom con variables de color
- Animaciones suaves

### Login Mejorado
- Diseño bicolumna (información + formulario)
- Gradiente atractivo
- Credenciales de demo integradas
- Validación clara de errores
- Icono animado por rol

### Dashboard por Rol
- Cards interactivas de módulos
- Indicadores visuales de permisos
- Información de sesión clara
- Alertas de seguridad
- Acceso directo a cada módulo

### Página de Acceso Denegado
- Información clara del motivo
- Tabla de módulos disponibles
- Opciones de acción (volver, cambiar cuenta)

---

## 📝 Archivos Modificados/Creados

### ✨ Nuevos
- `gestionAcademica/management/commands/setup_roles_usuarios.py` - Setup automático
- `templates/base.html` - Template base reutilizable

### 🔧 Modificados
- `gestionUniversitaria/access.py` - RBAC simplificado
- `templates/login.html` - Diseño Bootstrap 5
- `templates/home_general.html` - Dashboard mejorado
- `templates/sin_permiso.html` - Page de acceso denegado

---

## 🔍 Verificación del Sistema

### Pruebas Realizadas ✅
1. ✅ Login con admin (acceso a 5 módulos)
2. ✅ Login con estudiante (acceso a 2 módulos)
3. ✅ RBAC funcionando correctamente
4. ✅ Módulos bloqueados muestran "Sin acceso"
5. ✅ Interfaz responsive en mobile y desktop
6. ✅ Bootstrap 5 integrando correctamente

---

## ⚙️ Configuración del Sistema

### settings.py - Líneas Clave
```python
DEBUG = True                                    # Cambiar a False en producción
SECRET_KEY = 'django-insecure-...'             # Cambiar en producción
ALLOWED_HOSTS = []                              # Configurar para producción
INSTALLED_APPS = [
    'gestionAcademica',      # Módulo académico
    'Contabilidad',          # Módulo contable
    'RecursosHumanos',       # Módulo RRHH
    'inventario',            # Módulo inventario
    'solicitudes',           # Módulo solicitudes
]
MIDDLEWARE = [
    '...RoleAccessMiddleware',   # Validación de acceso
    '...CsrfViewMiddleware',      # Protección CSRF
]
TIME_ZONE = 'America/Bogota'     # Zona horaria local
```

---

## 🚨 Notas Importantes

### Para Desarrollo
- ✅ DEBUG = True (visualizar errores)
- ✅ Credenciales en texto (para pruebas)
- ✅ SQLite3 local
- ✅ ALLOWED_HOSTS = []

### Para Producción 🔐
- ⚠️ Cambiar DEBUG = False
- ⚠️ Usar SECRET_KEY segura (variables de entorno)
- ⚠️ Migrar a PostgreSQL o MySQL
- ⚠️ Configurar ALLOWED_HOSTS
- ⚠️ Implementar hash bcrypt/PBKDF2 para contraseñas
- ⚠️ Habilitar HTTPS (SECURE_SSL_REDIRECT = True)
- ⚠️ Implementar 2FA
- ⚠️ Usar servidor WSGI (Gunicorn/uWSGI)
- ⚠️ Configurar CORS adecuadamente
- ⚠️ Implementar rate limiting

---

## 📞 Soporte y Documentación

### Estructuras de Base de Datos
Ver modelos en cada app:
- `gestionAcademica/models.py` - Académica (Usuario, Estudiante, Materia, etc.)
- `Contabilidad/models.py` - Nómina, Presupuesto, Ingreso
- `RecursosHumanos/models.py` - Empleado, Contrato, Novedades
- `inventario/models.py` - Item, Préstamo, Categoría
- `solicitudes/models.py` - Solicitud, Historial, Comentarios

### URLs del Sistema
- `/login/` - Página de ingreso
- `/` - Dashboard principal
- `/salir/` - Cerrar sesión
- `/sin-permiso/` - Acceso denegado
- `/academica/` - Módulo académico
- `/contabilidad/` - Módulo contable
- `/rrhh/` - Módulo RRHH
- `/inventario/` - Módulo inventario
- `/solicitudes/` - Módulo solicitudes
- `/admin/` - Panel administrativo Django

---

## 📄 Licencia

Sistema de Gestión Universitaria - Versión 2.0
Desarrollo: Mayo 2024
Ambiente: Desarrollo/Demostración

---

**Última actualización**: 27 de Mayo de 2026
**Versión**: 2.0
**Estado**: ✅ Operativo
