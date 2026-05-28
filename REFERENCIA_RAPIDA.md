# 🎓 Sistema de Calificación - Referencia Rápida

## 🚀 Inicio Rápido (Para Profesores)

### 1. Acceder al Sistema
```
URL: http://127.0.0.1:8000/academica/profesor/materias/
Login: 2001 (Profesor de Demo)
```

### 2. Crear Primera Actividad
```
1. Clic en "Nueva Actividad" de tu materia
2. Llena el formulario:
   - Nombre: "Quiz 1"
   - Tipo: QUIZ
   - Porcentaje: 15.00
   - Período: 2026-1
3. Clic en "Crear Actividad"
```

### 3. Calificar Estudiantes
```
1. Desde Actividades → Clic en "Calificar"
2. Para cada estudiante ingresa nota (0.0 - 5.0)
3. Opcionalmente escribe observaciones
4. Clic en "Guardar Calificaciones"
```

### 4. Ver Resultado
```
1. Clic en "Ver Reporte" después de guardar
2. Verás:
   - Promedio de clase
   - Notas finales (si todas actividades completas)
   - Desglose por estudiante
```

---

## 📊 Fórmula de Cálculo

```
Nota Final = (Nota₁ × Peso₁ + Nota₂ × Peso₂ + ... + Notₙ × Pesₙ) / 100

Ejemplo:
4.5×15 + 4.0×20 + 3.8×35 + 4.2×30 = 406 / 100 = 4.06
```

---

## 🔑 Credenciales de Prueba

| Rol | Documento | Contraseña | URL |
|-----|-----------|-----------|-----|
| Profesor | 2001 | Juan Pérez López | /academica/profesor/materias/ |
| Estudiante | 3001 | Carlos Martínez | /academica/ (lectura) |
| Admin | 1001 | Administrador Sistema | /admin/ |

---

## 📝 Tipos de Actividad

```
📝 QUIZ           Evaluación corta
📋 TALLER         Trabajo práctico
📊 PARCIAL        Examen intermedio
🎓 FINAL          Examen final
🚀 PROYECTO       Trabajo integrador
🙋 PARTICIPACION  Clase y aportes
📌 OTRO           Cualquier otra
```

---

## ✅ Validaciones Automáticas

| Validación | Regla | Acción |
|-----------|-------|--------|
| **Porcentajes** | Suma debe = 100% | Error si > 100% |
| **Notas** | 0.0 - 5.0 | Rechaza fuera de rango |
| **Completitud** | Todas actividades calificadas | Nota final = NULL si incompleto |
| **Integridad** | Una nota por estudiante/actividad | unique_together enforced |

---

## 🎯 Estados de Nota

```
🟢 Excelente    4.5 - 5.0
🟢 Muy Bueno    4.0 - 4.4
🟡 Bueno        3.5 - 3.9
🟡 Aceptable    3.0 - 3.4
🔴 Deficiente   0.0 - 2.9
⚪ Sin Calificar Pendiente
```

---

## 🔗 URLs Principales

```
/academica/profesor/materias/                          Dashboard
/academica/profesor/actividad/crear/<materia_id>/      Crear actividad
/academica/profesor/actividad/calificar/<actividad_id>/ Calificar
/academica/profesor/reporte/corte/<actividad_id>/       Ver reportes
/academica/profesor/actividades/<materia_id>/           Gestionar
```

---

## 💾 Modelos de Base de Datos

### Actividad
```python
- nombre           # Ej: "Quiz 1"
- tipo             # QUIZ, TALLER, PARCIAL, etc
- porcentaje       # 15.00
- materia          # FK a Materia
- periodo          # FK a PeriodoAcademico
```

### CalificacionActividad
```python
- inscripcion      # FK a Inscripcion (estudiante+materia)
- actividad        # FK a Actividad
- calificacion     # 0.0 - 5.0
- observaciones    # Retroalimentación
```

### Corte (Calificación por Período)
```python
- inscripcion      # FK
- numero_corte     # 1, 2, 3
- fecha_inicio
- fecha_fin
- calcular_nota_final() # Suma ponderada
```

---

## ⚡ Atajos Útiles

```
Crear múltiples actividades: 5 minutos
Calificar una clase (25 est): 15-20 minutos
Generar reporte: 1 minuto
Ver estadísticas: 30 segundos
```

---

## 🆘 Problemas Comunes

| Problema | Solución |
|----------|----------|
| "Suma > 100%" | Reduce porcentajes de otras actividades |
| "No veo nota final" | Completa todas las actividades |
| "No puedo editar" | Solo profesores de la materia pueden |
| "¿Cómo cambio una nota?" | Ve a Calificar y edita el campo |

---

## 📈 Ejemplo Completo

```
MATERIA: Cálculo I | PERÍODO: 2026-1

ACTIVIDADES CREADAS:
✓ Quiz 1 (15%) → 25 estudiantes calificados
✓ Quiz 2 (15%) → 25 estudiantes calificados
✓ Parcial (35%) → 20 estudiantes calificados
✓ Proyecto (35%) → 18 estudiantes calificados

NOTAS FINALES CALCULADAS:
• Carlos Martínez: 4.07 (Muy Bueno) ✓
• Pedro González: INCOMPLETO (falta Proyecto)
• María Rodríguez: 3.52 (Bueno) ✓

ESTADÍSTICAS:
• Promedio: 3.78
• Máxima: 4.8
• Mínima: 2.6
```

---

## 📞 Contacto

```
Admin: 1001 / Administrador
Soporte: [Tu equipo TI]
```

---

**Versión:** 3.0
**Actualizado:** 27/05/2026
**Estado:** ✅ Funcional
