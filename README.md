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

- Súper administrador: `9000` / `Super Administrador`
- Administrador: `1001` / `Admin Academico`
- Profesor: `9500` / `Profesor Demo`
- Contabilidad: `9100` / `Usuario Contabilidad`
- Recursos Humanos: `9200` / `Usuario Recursos Humanos`
- inventario: `9300` / `Usuario inventario`
- Solicitudes: `9400` / `Usuario Solicitudes`
- Estudiante: `9600` / `Estudiante Demo`

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

## Integrantes

- Alejandro Díaz.
- Juan Felipe Delgadillo.
