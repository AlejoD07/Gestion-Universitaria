"""
Management command para configurar roles y usuarios de prueba
para el sistema de Gestión Universitaria.

Uso: python manage.py setup_roles_usuarios
"""

from django.core.management.base import BaseCommand
from django.db import transaction
from gestionAcademica.models import (
    Rol, Usuario, TipoDocumento, Facultad, Programa,
    PeriodoAcademico, Estudiante
)
from datetime import date, timedelta


class Command(BaseCommand):
    help = 'Configura roles simplificados y crea usuarios de prueba con credenciales'

    @transaction.atomic
    def handle(self, *args, **options):
        # 1. Limpiar datos anteriores
        self.stdout.write(self.style.WARNING('🗑️  Limpiando datos anteriores...'))
        Usuario.objects.all().delete()
        Estudiante.objects.all().delete()

        # 1. Crear/Limpiar Roles simplificados
        self.stdout.write(self.style.SUCCESS('🔧 Configurando roles...'))

        roles_simplificados = {
            1: 'Administrador',
            2: 'Profesor',
            3: 'Estudiante',
            4: 'Recursos Humanos',
            5: 'Contador',
            6: 'Inventario',
        }

        # Limpiar roles anteriores
        Rol.objects.all().delete()

        # Crear nuevos roles
        roles_creados = {}
        for id_rol, nombre in roles_simplificados.items():
            rol, created = Rol.objects.get_or_create(
                id_rol=id_rol,
                defaults={'nombre_rol': nombre}
            )
            roles_creados[nombre] = rol
            status = "✅ Creado" if created else "📌 Existente"
            self.stdout.write(f"  {status}: {nombre}")

        # 2. Crear TipoDocumento
        self.stdout.write(self.style.SUCCESS('\n📝 Configurando tipos de documento...'))
        TipoDocumento.objects.all().delete()

        tipos_doc = {
            1: 'Cédula',
            2: 'Pasaporte',
            3: 'Carnet Extranjero',
        }

        tipos_doc_creados = {}
        for id_tipo, nombre in tipos_doc.items():
            tipo, created = TipoDocumento.objects.get_or_create(
                id_tipo_doc=id_tipo,
                defaults={'nombre_tipo_doc': nombre}
            )
            tipos_doc_creados[nombre] = tipo
            self.stdout.write(f"  ✅ {nombre}")

        # 3. Crear Facultades
        self.stdout.write(self.style.SUCCESS('\n🏛️  Configurando facultades...'))
        facultades_nombres = [
            'Ingeniería',
            'Medicina',
            'Derecho',
            'Administración',
            'Educación',
        ]
        facultades = {}
        for nombre in facultades_nombres:
            fac, _ = Facultad.objects.get_or_create(nombre=nombre)
            facultades[nombre] = fac
            self.stdout.write(f"  ✅ {nombre}")

        # 4. Crear Programas (Carreras)
        self.stdout.write(self.style.SUCCESS('\n📚 Configurando programas académicos...'))
        programas_data = [
            ('Ingeniería Sistemas', facultades['Ingeniería']),
            ('Ingeniería Civil', facultades['Ingeniería']),
            ('Medicina General', facultades['Medicina']),
            ('Derecho', facultades['Derecho']),
            ('Administración Empresarial', facultades['Administración']),
        ]

        for nombre, facultad in programas_data:
            Programa.objects.get_or_create(
                nombre=nombre,
                defaults={'facultad': facultad}
            )
            self.stdout.write(f"  ✅ {nombre}")

        # 5. Crear Período Académico
        self.stdout.write(self.style.SUCCESS('\n📅 Configurando períodos académicos...'))
        hoy = date.today()
        PeriodoAcademico.objects.get_or_create(
            nombre='2024-1',
            defaults={
                'fecha_inicio': hoy,
                'fecha_fin': hoy + timedelta(days=180),
            }
        )
        self.stdout.write('  ✅ Período 2024-1')

        # 6. Crear Usuarios de Prueba
        self.stdout.write(self.style.SUCCESS('\n👥 Creando usuarios de prueba...'))
        Usuario.objects.all().delete()

        usuarios_data = [
            {
                'id_usuario': 1001,
                'nombre_usuario': 'Administrador Sistema',
                'rol': 'Administrador',
                'facultad': None,
            },
            {
                'id_usuario': 2001,
                'nombre_usuario': 'Juan Pérez López',
                'rol': 'Profesor',
                'facultad': facultades['Ingeniería'],
            },
            {
                'id_usuario': 2002,
                'nombre_usuario': 'María García Rodríguez',
                'rol': 'Profesor',
                'facultad': facultades['Medicina'],
            },
            {
                'id_usuario': 3001,
                'nombre_usuario': 'Carlos Martínez',
                'rol': 'Estudiante',
                'facultad': facultades['Ingeniería'],
            },
            {
                'id_usuario': 3002,
                'nombre_usuario': 'Ana López Jiménez',
                'rol': 'Estudiante',
                'facultad': facultades['Medicina'],
            },
            {
                'id_usuario': 4001,
                'nombre_usuario': 'Director RRHH',
                'rol': 'Recursos Humanos',
                'facultad': None,
            },
            {
                'id_usuario': 5001,
                'nombre_usuario': 'Contador Sistema',
                'rol': 'Contador',
                'facultad': None,
            },
            {
                'id_usuario': 6001,
                'nombre_usuario': 'Jefe Inventario',
                'rol': 'Inventario',
                'facultad': None,
            },
        ]

        usuarios_creados = {}
        for datos in usuarios_data:
            usuario, created = Usuario.objects.get_or_create(
                id_usuario=datos['id_usuario'],
                defaults={
                    'nombre_usuario': datos['nombre_usuario'],
                    'id_rol': roles_creados[datos['rol']],
                    'id_tipo_documento': tipos_doc_creados['Cédula'],
                    'facultad': datos['facultad'],
                    'activo': True,
                }
            )
            usuarios_creados[datos['id_usuario']] = usuario
            status = "✅ Creado" if created else "📌 Existente"
            self.stdout.write(
                f"  {status}: {datos['nombre_usuario']} ({datos['rol']})"
            )

        # 7. Crear Estudiantes
        self.stdout.write(self.style.SUCCESS('\n🎓 Registrando estudiantes...'))
        for est_id in [3001, 3002]:
            usuario = usuarios_creados[est_id]
            estudiante, created = Estudiante.objects.get_or_create(
                usuario=usuario,
                defaults={
                    'codigo_estudiante': f'EST-{est_id}',
                    'semestre': 3,
                    'promedio': 3.8,
                }
            )
            status = "✅ Creado" if created else "📌 Existente"
            self.stdout.write(f"  {status}: {usuario.nombre_usuario}")

        # 8. Mostrar Credenciales
        self.stdout.write(self.style.SUCCESS('\n' + '='*60))
        self.stdout.write(self.style.SUCCESS('🔐 CREDENCIALES DE PRUEBA'))
        self.stdout.write(self.style.SUCCESS('='*60))
        self.stdout.write('\nFormato: Documento | Clave\n')

        for datos in usuarios_data:
            documento = datos['id_usuario']
            clave = datos['nombre_usuario']
            rol = datos['rol']
            self.stdout.write(
                f"👤 {rol.ljust(20)} | Doc: {documento:5d} | Clave: {clave}"
            )

        self.stdout.write('\n' + '='*60)
        self.stdout.write(self.style.SUCCESS('✅ Configuración completada exitosamente'))
        self.stdout.write('='*60 + '\n')

        self.stdout.write(self.style.WARNING(
            '⚠️  IMPORTANTE:\n'
            '- Las credenciales son para DESARROLLO ÚNICAMENTE\n'
            '- En PRODUCCIÓN cambiar contraseñas y usar hash\n'
            '- Documento = id_usuario, Clave = nombre_usuario\n'
        ))
