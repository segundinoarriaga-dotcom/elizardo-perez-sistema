# 🏫 Sistema de Gestión Académica
## U.E. Profesor Elizardo Pérez G.
### Villa Pagador · Av. La Joya y Bella Vista · Cochabamba, Bolivia

---

## 📋 Descripción
Sistema web académico desarrollado con **Flask-AppBuilder** para gestionar estudiantes, docentes, cursos, calificaciones y asistencia de la Unidad Educativa Profesor Elizardo Pérez G.

---

## 🗄️ Base de Datos (7 Tablas)

| Tabla        | Descripción                          | Relaciones               |
|--------------|--------------------------------------|--------------------------|
| `curso`      | Cursos/grados escolares              | → estudiantes, horarios  |
| `docente`    | Personal docente                     | → horarios               |
| `estudiante` | Estudiantes matriculados             | → notas, asistencias     |
| `materia`    | Asignaturas / materias               | → notas, horarios        |
| `horario`    | Horario de clases                    | FK: curso, docente, mat. |
| `nota`       | Calificaciones (SER/SABER/HACER/DEC) | FK: estudiante, materia  |
| `asistencia` | Registro de asistencia diaria        | FK: estudiante           |

---

## 👥 Roles y Accesos

| Rol         | Accesos                                                       |
|-------------|---------------------------------------------------------------|
| **Admin**   | Acceso total: CRUD de todo, usuarios, roles, seguridad        |
| **Supervisor** | Gestión académica + reportes + gráficas (sin seguridad) |
| **Usuario** | Solo lectura de estudiantes, notas, asistencia y reportes     |

### Credenciales de prueba
| Usuario      | Contraseña | Rol         |
|-------------|------------|-------------|
| `admin`      | `admin123` | Admin       |
| `supervisor` | `super123` | Supervisor  |
| `usuario`    | `user123`  | Usuario     |

---

## 📊 Reportes (3)
1. **Estudiantes por Curso** – Matrícula agrupada por curso, nivel y turno
2. **Calificaciones por Materia** – Promedio, mínima y máxima por asignatura (gestión actual)
3. **Asistencia Mensual** – % de asistencia por estudiante en el mes en curso

## 📈 Gráficas (3)
1. **Estudiantes por Nivel** – Gráfico de torta: Primaria vs Secundaria
2. **Promedio por Materia** – Barras horizontales con línea de nota mínima
3. **Asistencia por Curso** – Barras por curso con meta del 80%

---

## 🚀 Instalación y ejecución

```bash
# 1. Clonar repositorio
git clone https://github.com/TU_USUARIO/elizardo-perez-sistema.git
cd elizardo-perez-sistema

# 2. Crear entorno virtual
python -m venv venv
source venv/bin/activate        # Linux/Mac
venv\Scripts\activate           # Windows

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Ejecutar
python run.py
```

Abrir en el navegador: **http://localhost:5000/dashboard**

---

## 🌿 Flujo de trabajo con GitHub

```bash
# Cada integrante trabaja en su branch
git checkout -b feature/nombre-integrante

# Commits con mensajes claros
git add .
git commit -m "feat: agrega reporte de calificaciones por materia"

# Subir branch
git push origin feature/nombre-integrante

# Crear Pull Request → develop → revisión → merge
```

### Branches sugeridas
- `main` – producción estable
- `develop` – integración del equipo
- `feature/integrante1` – trabajo individual
- `feature/integrante2`
- `feature/integrante3`

---

## 🗂️ Estructura del proyecto
```
elizardo-perez-sistema/
├── run.py                    # Punto de entrada
├── config.py                 # Configuración Flask
├── requirements.txt
├── README.md
└── app/
    ├── __init__.py           # Fábrica + registro de vistas + datos semilla
    ├── models.py             # 7 modelos SQLAlchemy
    ├── views.py              # Vistas ModelView + Reportes + Gráficas
    ├── static/
    └── templates/
        ├── dashboard.html
        ├── reportes/
        │   ├── index.html
        │   ├── estudiantes_por_curso.html
        │   ├── calificaciones_materia.html
        │   └── asistencia_mensual.html
        └── graficas/
            ├── index.html
            └── grafica.html
```

---

## 🔑 Tecnologías
- **Python 3.10+**
- **Flask 3.x** + **Flask-AppBuilder 5.x**
- **SQLAlchemy** (ORM) · SQLite (desarrollo)
- **Matplotlib** (gráficas)
- **Bootstrap 3** (UI via FAB)

---
*Desarrollado para el 2do Parcial · Cochabamba, Bolivia · 2025*
