# 📚 Sistema Mejorado de Calificación - Guía Completa

**Versión:** 3.0
**Fecha:** 27 de Mayo de 2026
**Estado:** ✅ Implementado y Funcional

---

## 📋 Tabla de Contenidos

1. [Descripción General](#descripción-general)
2. [Características Principales](#características-principales)
3. [Modelos de Base de Datos](#modelos-de-base-de-datos)
4. [Guía de Uso por Rol](#guía-de-uso-por-rol)
5. [Flujo de Trabajo del Profesor](#flujo-de-trabajo-del-profesor)
6. [Cálculo de Notas](#cálculo-de-notas)
7. [Rutas y URLs](#rutas-y-urls)
8. [Ejemplos Prácticos](#ejemplos-prácticos)
9. [Troubleshooting](#troubleshooting)

---

## 🎯 Descripción General

El sistema de calificación mejorado permite a los profesores:

✅ **Crear actividades** con porcentajes específicos (Quiz, Taller, Examen Parcial, etc.)
✅ **Registrar notas** de estudiantes en cada actividad (escala 0.0 - 5.0)
✅ **Calcular automáticamente** la nota final como suma ponderada
✅ **Ver reportes detallados** con estadísticas de clase
✅ **Proporcionar retroalimentación** a cada estudiante

### Ventajas del Sistema

| Aspecto | Beneficio |
|--------|----------|
| **Transparencia** | Los estudiantes ven exactamente cómo se calcula su nota |
| **Flexibilidad** | Profesores pueden ajustar porcentajes según necesidades |
| **Precisión** | Sistema automático evita errores de cálculo manual |
| **Reportes** | Estadísticas por clase (promedio, máxima, mínima) |
| **Trazabilidad** | Registro completo de todas las calificaciones |

---

## ⭐ Características Principales

### 1. Tipos de Actividades
```
📝 Quiz           - Evaluación corta y rápida
📋 Taller         - Trabajo práctico colaborativo
📊 Examen Parcial - Evaluación intermedia
🎓 Examen Final   - Evaluación final del período
🚀 Proyecto       - Trabajo integrador largo plazo
🙋 Participación  - Asistencia y participación en clase
📌 Otro           - Cualquier otro tipo de evaluación
```

### 2. Cálculo Inteligente
```
Fórmula: Nota Final = Σ(Nota Actividad × Porcentaje / 100)

Ejemplo:
- Quiz 1 (15%):        4.5 → 4.5 × 0.15 = 0.675
- Taller (20%):        4.0 → 4.0 × 0.20 = 0.800
- Examen Parcial (35%): 3.8 → 3.8 × 0.35 = 1.330
- Proyecto (30%):      4.2 → 4.2 × 0.30 = 1.260
───────────────────────────────────────────────
Nota Final:                                4.065
```

### 3. Validación de Porcentajes
- El sistema valida que el total de porcentajes = 100%
- Si no suma 100%, no se puede calcular la nota final
- Aviso visual si faltan actividades o porcentajes

### 4. Estados de Calificación
```
🟢 Excelente    (4.5 - 5.0)
🟢 Muy Bueno    (4.0 - 4.4)
🟡 Bueno        (3.5 - 3.9)
🟡 Aceptable    (3.0 - 3.4)
🔴 Deficiente   (0.0 - 2.9)
⚪ Sin Calificar (Pendiente)
```

---

## 📊 Modelos de Base de Datos

### Actividad
```
- id (PK)
- nombre (CharField)          # Ej: "Quiz 1"
- descripcion (TextField)      # Detalles opcionales
- tipo (CharField)             # QUIZ, TALLER, PARCIAL, FINAL, PROYECTO, PARTICIPACION, OTRO
- porcentaje (DecimalField)    # 0.00 - 100.00
- materia (FK → Materia)       # Qué materia es
- periodo (FK → PeriodoAcademico) # Cuándo es
- fecha_creacion (DateTimeField)  # Registro automático
- activa (BooleanField)        # Activada/desactivada
```

**Métodos útiles:**
- `get_tipo_display_icon()` - Retorna emoji según tipo
- `__str__()` - Muestra "nombre (porcentaje%)"

### CalificacionActividad
```
- id (PK)
- inscripcion (FK → Inscripcion)
- actividad (FK → Actividad)
- calificacion (DecimalField)   # 0.00 - 5.00 (null si no se calificó)
- observaciones (TextField)     # Retroalimentación del profesor
- fecha_calificacion (DateTimeField) # Auto-actualiza
- unique_together = (inscripcion, actividad) # Un estudiante, una actividad, una nota
```

**Métodos útiles:**
- `get_aporte_nota_final()` - Calcula cuánto aporta a la nota final
- `obtener_estado()` - Retorna estado de la nota

### Corte
```
- id (PK)
- inscripcion (FK → Inscripcion)
- numero_corte (IntegerField)   # 1, 2 o 3
- fecha_inicio (DateField)
- fecha_fin (DateField)
- activo (BooleanField)
- unique_together = (inscripcion, numero_corte)
```

**Métodos útiles:**
- `calcular_nota_final()` - Calcula suma ponderada (retorna None si incompleto)
- `obtener_detalles_calificacion()` - Desglose completo para reportes

---

## 👨‍🏫 Guía de Uso por Rol

### Para PROFESOR

#### 1️⃣ Acceder al módulo
```
http://127.0.0.1:8000/academica/profesor/materias/
```
✅ Muestra todas tus materias asignadas

#### 2️⃣ Crear una actividad
```
URL: /academica/profesor/actividad/crear/<materia_id>/
```
**Formulario:**
- Nombre: "Quiz 1"
- Tipo: Selecciona de lista
- Porcentaje: 15.00
- Descripción: Opcional
- Período: Selecciona período académico

**Validaciones:**
- El nombre es obligatorio
- El porcentaje debe estar entre 0 y 100
- La suma total no puede exceder 100%

**Después de crear:**
- Se crea automáticamente una entrada CalificacionActividad para cada estudiante inscrito
- Puedes ver un resumen de actividades creadas por período

#### 3️⃣ Calificar estudiantes
```
URL: /academica/profesor/actividad/calificar/<actividad_id>/
```
**Proceso:**
1. Ves tabla con todos los estudiantes
2. Para cada uno, ingresas:
   - **Calificación**: 0.0 a 5.0
   - **Observaciones**: Retroalimentación (opcional)
3. Haces clic en "Guardar Calificaciones"

**Características:**
- Las filas de completadas se resaltan en verde
- Ves progreso (N de N estudiantes)
- Puedes volver a editar en cualquier momento

#### 4️⃣ Ver reportes
```
URL: /academica/profesor/reporte/corte/<actividad_id>/
```
**Muestra:**
- Estadísticas generales (promedio, máximo, mínimo)
- Desglose por estudiante de todas las actividades
- Nota final calculada automáticamente (si está completa)
- Estado de cada estudiante (Excelente, Bueno, etc.)
- Detalles de observaciones dadas

**Opción de impresión:**
- Botón "Imprimir Reporte" para formato papel

#### 5️⃣ Gestionar actividades
```
URL: /academica/profesor/actividades/<materia_id>/
```
**Características:**
- Agrupa actividades por período
- Muestra validación de porcentajes
- Acceso rápido a calificar y ver reportes
- Información de cuántos estudiantes se han calificado

---

### Para ESTUDIANTE
Los estudiantes pueden ver sus notas en el módulo académico (funcionalidad de lectura).

---

### Para ADMINISTRADOR
El administrador tiene acceso completo a:
- Django Admin: `/admin/`
- Ver/editar todas las Actividades
- Ver/editar todas las CalificacionesActividades
- Ver Cortes y validar datos

---

## 🔄 Flujo de Trabajo del Profesor

### Semana 1: Planificación
```
1. Ingresa al módulo de Gestión de Calificaciones
2. Revisa sus materias
3. Define actividades:
   - Quiz continuo: 20%
   - Talleres: 20%
   - Examen Parcial: 30%
   - Examen Final: 30%
   (Total: 100%) ✓
```

### Semana 2-4: Aplicación de Evaluaciones
```
1. Crea la actividad en el sistema
2. Después de calificar en papel:
   - Ingresa notas en el sistema
   - Añade observaciones si es necesario
3. Verifica progreso en reporte
```

### Semana 5: Revisión y Análisis
```
1. Ve el reporte de corte
2. Analiza estadísticas:
   - Si promedio < 3.0, considera refuerzo
   - Si estudiante tiene < 3.0 en parcial, atiende
3. Proporciona retroalimentación personalizada
```

### Semana 6: Presentación de Notas
```
1. Genera reporte imprimible
2. Publica notas a estudiantes
3. Atiende reclamos/consultas
```

---

## 📐 Cálculo de Notas

### Fórmula General
```
NotaFinal = Σ(CalificacionActividad[i] × Porcentaje[i] / 100)

Condiciones:
- Σ(Porcentaje[i]) DEBE SER 100%
- 0 ≤ CalificacionActividad ≤ 5.0
- Si alguna CalificacionActividad = NULL → NotaFinal = NULL
```

### Ejemplo Paso a Paso
**Materia: Algoritmos | Período: 2026-1**

**Actividades Creadas:**
```
1. Quiz 1        (10%) - calificación: 4.5
2. Quiz 2        (10%) - calificación: 5.0
3. Taller        (20%) - calificación: 4.0
4. Parcial       (30%) - calificación: 3.5
5. Proyecto      (30%) - calificación: 4.2
─────────────────────────────────────
Total:          (100%) ✓
```

**Cálculo:**
```
= (4.5 × 10 + 5.0 × 10 + 4.0 × 20 + 3.5 × 30 + 4.2 × 30) / 100
= (45 + 50 + 80 + 105 + 126) / 100
= 406 / 100
= 4.06
```

**Resultado:** Nota Final = **4.06** → Estado: **Muy Bueno** 🟢

---

## 🔗 Rutas y URLs

### URLs del Sistema de Calificaciones

| Función | URL | Método | Rol Requerido |
|---------|-----|--------|---------------|
| Dashboard de Materias | `/academica/profesor/materias/` | GET | Profesor |
| Crear Actividad | `/academica/profesor/actividad/crear/<materia_id>/` | GET/POST | Profesor |
| Calificar Actividad | `/academica/profesor/actividad/calificar/<actividad_id>/` | GET/POST | Profesor |
| Reporte de Corte | `/academica/profesor/reporte/corte/<actividad_id>/` | GET | Profesor |
| Gestionar Actividades | `/academica/profesor/actividades/<materia_id>/` | GET | Profesor |

### URLs Utilizadas Internamente
```python
# gestionAcademica/urls.py
path('profesor/materias/', views_calificaciones.materias_profesor, name='profesor_materias'),
path('profesor/actividad/crear/<int:materia_id>/', views_calificaciones.crear_actividad, name='profesor_crear_actividad'),
path('profesor/actividad/calificar/<int:actividad_id>/', views_calificaciones.calificar_actividad, name='profesor_calificar_actividad'),
path('profesor/reporte/corte/<int:actividad_id>/', views_calificaciones.reporte_corte, name='profesor_reporte_corte'),
path('profesor/actividades/<int:materia_id>/', views_calificaciones.gestionar_actividades, name='profesor_gestionar_actividades'),
```

---

## 💡 Ejemplos Prácticos

### Ejemplo 1: Crear Primer Corte de Algoritmos

**Paso 1:** Acceder al sistema
```
Login: 2001 / Juan Pérez López (Profesor)
URL: /academica/profesor/materias/
```

**Paso 2:** Crear actividades
```
Actividad 1: Quiz 1 (QUIZ, 15%)
Actividad 2: Taller 1 (TALLER, 15%)
Actividad 3: Examen Parcial (PARCIAL, 35%)
Actividad 4: Proyecto (PROYECTO, 35%)
──────────────────────────────────────
Total: 100% ✓
```

**Paso 3:** Calificar Quiz 1
```
URL: /academica/profesor/actividad/calificar/<quiz_id>/
```
Ingresa las notas:
- Carlos Martínez: 4.5
- Estudiante 2: 3.8
- Etc.

**Paso 4:** Ver reporte
```
URL: /academica/profesor/reporte/corte/<quiz_id>/
```
Verás:
- 2 estudiantes completos
- Promedio: 4.15
- Máxima: 4.5
- Mínima: 3.8

---

### Ejemplo 2: Calificación Completa de un Estudiante

**Estudiante:** Carlos Martínez (código: 3001)

**Notas registradas:**
```
| Actividad      | Peso | Nota | Aporte |
|----------------|------|------|--------|
| Quiz 1         | 15%  | 4.5  | 0.675  |
| Taller 1       | 15%  | 4.0  | 0.600  |
| Examen Parcial | 35%  | 3.8  | 1.330  |
| Proyecto       | 35%  | 4.2  | 1.470  |
|────────────────────────────────────────|
| TOTAL          | 100% | -    | 4.075  |
```

**Sistema automáticamente:**
1. ✓ Valida que 15+15+35+35 = 100%
2. ✓ Calcula 4.5×0.15 + 4.0×0.15 + 3.8×0.35 + 4.2×0.35
3. ✓ Redondea a 4.08
4. ✓ Clasifica como "Muy Bueno"
5. ✓ Genera reporte con todos los datos

---

## 🆘 Troubleshooting

### Problema: "La suma de porcentajes no es 100%"

**Causa:** Intentas crear una actividad que hace que el total no sea 100%

**Solución:**
```
1. Revisa qué porcentajes ya tienes asignados
2. Suma actual + nueva actividad = 100%?
3. Si no, ajusta los porcentajes
4. O elimina una actividad existente
```

**Ejemplo:**
```
Tienes:
- Quiz: 20%
- Taller: 20%
- Examen: 40%
(Total: 80%)

Quieres agregar:
- Proyecto: 25% → 80 + 25 = 105% ❌

Solución: Proyecto debe ser máximo 20%
```

---

### Problema: "No veo la nota final calculada"

**Causa:** No todas las actividades del estudiante están calificadas

**Solución:**
```
1. Ve a Gestionar Actividades
2. Revisa qué está "Sin Calificar" para ese estudiante
3. Califica todas las actividades
4. La nota final aparecerá automáticamente
```

---

### Problema: "¿Cómo edito una calificación ya guardada?"

**Solución:**
```
1. Ve a la vista de Calificar (misma URL)
2. Localiza al estudiante
3. Cambia el valor en el campo
4. Haz clic en "Guardar Calificaciones"
5. Los cambios se aplican inmediatamente
```

---

### Problema: "¿Puedo eliminar una actividad?"

**Solución:**
Para eliminar una actividad:
```
1. Opción manual: Django Admin → /admin/gestionacademica/actividad/
2. Busca la actividad
3. Haz clic en ella y marca como inactiva (o elimina si no hay calificaciones)

NOTA: Si ya hay estudiantes calificados,
es mejor marcar como inactiva que eliminar
```

---

### Problema: "¿Qué pasa si cambio el porcentaje de una actividad?"

**Importante:**
```
⚠️ Si cambias el porcentaje de una actividad después de calificar:
- Las calificaciones previas se RECALCULAN automáticamente
- La nota final se actualiza con la nueva fórmula

Ejemplo:
- Antes: Quiz 15%, nota: 4.5 → aporte: 0.675
- Después: Quiz 20%, nota: 4.5 → aporte: 0.900
- Nota final sube automáticamente
```

---

## 📱 Interfaz de Usuario

### Dashboard Principal
```
┌─────────────────────────────────────────────┐
│   Gestión de Calificaciones                 │
│   Crea actividades y califica estudiantes   │
├─────────────────────────────────────────────┤
│ Mis Materias (2)                            │
│                                             │
│ ┌─ Algoritmos y Estructuras de Datos ─┐   │
│ │ Programa: Ingeniería de Sistemas     │   │
│ │ ├─ 25 Estudiantes inscritos          │   │
│ │ ├─ 4 Actividades creadas             │   │
│ │ └─ [Ver Actividades] [Nueva Actividad] │
│ └─────────────────────────────────────┘   │
│                                             │
│ ┌─ Cálculo Diferencial ────────────────┐   │
│ │ ... más materias ...                  │   │
│ └──────────────────────────────────────┘   │
└─────────────────────────────────────────────┘
```

### Tabla de Calificación
```
┌────────────────────────────────────────────────────────┐
│ Calificar "Quiz 1" - Algoritmos                       │
├────────────────────────────────────────────────────────┤
│ Progreso: ████████░░ 80%                             │
│ (20 de 25 estudiantes calificados)                    │
├────────────────────────────────────────────────────────┤
│ Estudiante          │ Código  │ Nota  │ Observaciones │
├─────────────────────┼─────────┼───────┼───────────────┤
│ Carlos Martínez     │ 3001    │ [4.5] │ Muy bien      │
│ Pedro González      │ 3002    │ [____]│ Pendiente     │
│ ... más estudiantes                                   │
└────────────────────────────────────────────────────────┘
[Guardar] [Ver Reporte] [Volver]
```

### Reporte de Notas
```
┌──────────────────────────────────────────────────┐
│ Reporte de Notas - Algoritmos                   │
├──────────────────────────────────────────────────┤
│ Estadísticas:                                    │
│ ├─ Promedio clase: 3.85                        │
│ ├─ Máxima nota: 4.8                            │
│ ├─ Mínima nota: 2.5                            │
│ └─ Completos: 23/25 estudiantes                │
├──────────────────────────────────────────────────┤
│ Carlos Martínez (3001)           NOTA FINAL: 4.07
│ └─ Desglose:                                    │
│    📝 Quiz 1 (15%): 4.5 → +0.675                │
│    📋 Taller (15%): 4.0 → +0.600                │
│    📊 Parcial (35%): 3.8 → +1.330               │
│    🚀 Proyecto (35%): 4.2 → +1.470              │
│    Estado: 🟢 Muy Bueno                         │
├──────────────────────────────────────────────────┤
│ Pedro González (3002)            INCOMPLETO
│ └─ Falta: 📊 Parcial                           │
└──────────────────────────────────────────────────┘
```

---

## 📞 Soporte Técnico

### Para Problemas del Sistema
1. Verifica que hayas iniciado sesión como Profesor
2. Asegúrate de estar en una materia que te fue asignada
3. Revisa que el período académico esté activo

### Contacto
```
Administrador del Sistema: 1001 / Administrador Sistema
Soporte Técnico: [Tu equipo de TI]
```

---

## 📝 Notas Importantes

1. **Validación automática:** El sistema previene sumas de porcentajes > 100%
2. **Retroalimentación:** Las observaciones son cruciales para estudiantes
3. **Reportes:** Genera antes de publicar notas oficiales
4. **Seguridad:** Solo profesores pueden calificar sus propias materias
5. **Auditoría:** Toda actividad queda registrada con fecha y hora

---

## ✨ Mejoras Futuras Sugeridas

- [ ] Exportar reportes a Excel
- [ ] Estadísticas avanzadas (desviación estándar, curva de distribución)
- [ ] Ponderación por sección de clase
- [ ] Calificador por rúbrica
- [ ] Notificaciones a estudiantes cuando se publica nota
- [ ] Historial de cambios en calificaciones
- [ ] Integración con email para enviar reportes

---

**Última actualización:** 27 de Mayo de 2026
**Versión:** 3.0 - Producción
**Estado:** ✅ Funcional y Probado
