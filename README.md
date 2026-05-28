# Gestión Universitaria

Sistema Django para centralizar módulos operativos de una universidad: Gestión Académica, Contabilidad, Recursos Humanos, inventario y Solicitudes.

## Problema que resuelve

En una universidad, cada área suele trabajar con información separada: profesores y materias por un lado, presupuesto por otro, empleados en otro sistema, inventario en hojas sueltas y solicitudes sin trazabilidad. Esta aplicación integra esos flujos en un solo punto de entrada y habilita módulos según el rol del usuario.

## Diferencial del sistema

- Login central con acceso por roles.
- Súper administrador con vista completa de todos los módulos.
- Profesores con acceso limitado a sus materias, notas, inscripciones y asistencias.
- Contabilidad con áreas parametrizadas desde el organigrama.
- Solicitudes, quejas y reclamos con soporte para documentos adjuntos.
- Interfaz visual unificada con color institucional naranja y navegación entre módulos.

## Credenciales demo

El usuario se ingresa con documento y la clave demo es el nombre del usuario.

- Súper administrador: `9000` / `Camilo Restrepo`
- Administrador: `1001` / `Daniela Pardo`
- Contabilidad: `9100` / `Carolina Vargas`
- Recursos Humanos: `9200` / `Natalia Herrera`
- inventario: `9300` / `Miguel Torres`
- Solicitudes: `9400` / `Sofia Martinez`
- Estudiante: `9600` / `Andres Felipe Rios`

## Ejecución en Git Bash

```bash
source venv/Scripts/activate
python manage.py migrate
python manage.py runserver 127.0.0.1:8000
```

Abrir:

```text
http://127.0.0.1:8000/
```

## Despliegue en Render con Docker

El proyecto incluye `Dockerfile`, `.dockerignore` y `render.yaml` para crear un Web Service en Render usando Docker.

Pasos:

```bash
git add .
git add -f db.sqlite3
git commit -m "Preparar despliegue en Render con Docker"
git push
```

Luego en Render:

1. Crear un nuevo Blueprint o Web Service desde el repositorio.
2. Seleccionar Docker como runtime si se crea manualmente.
3. Usar el plan Free para demo.
4. Desplegar.

Importante: `db.sqlite3` normalmente no se versiona, pero para esta demo contiene los usuarios y datos de prueba. Si no se sube con `git add -f db.sqlite3`, Render ejecutara las migraciones sobre una base vacia y las credenciales demo no funcionaran.

## Integrantes

- Alejandro Díaz.
- Juan Felipe Delgadillo.
