# 📋 Guía Completa: Subir el Proyecto a GitHub
## U.E. Profesor Elizardo Pérez G. — Sistema de Gestión Académica

---

## ✅ REQUISITOS PREVIOS

Antes de empezar, verifica que tienes instalado:

| Herramienta | Cómo verificar | Descargar si no tienes |
|-------------|----------------|------------------------|
| Git | `git --version` | https://git-scm.com |
| Python 3.10+ | `python --version` | https://python.org |
| Cuenta GitHub | Entrar a github.com | https://github.com/signup |

---

## 🌐 PASO 1: Crear el repositorio en GitHub

1. Inicia sesión en **github.com**
2. Clic en el botón **"New"** (o el ícono `+` arriba a la derecha)
3. Completa el formulario:
   - **Repository name:** `elizardo-perez-sistema`
   - **Visibility:** ✅ **Public** ← OBLIGATORIO para la rúbrica
   - **Add a README file:** ✅ marcado
4. Clic en **"Create repository"**

> ⚠️ Si el repositorio es **Private**, el docente no puede ver el historial de commits.

---

## ⚙️ PASO 2: Configurar Git en tu computadora

Abre la terminal (CMD, PowerShell o Git Bash) y ejecuta:

```bash
# Configura tu identidad (usa los datos de tu cuenta GitHub)
git config --global user.name "Tu Nombre Completo"
git config --global user.email "tucorreo@gmail.com"

# Verifica que quedó bien
git config --list
```

> ℹ️ Esto solo se hace **una vez por computadora**.

---

## 📁 PASO 3: Clonar el repositorio y copiar el proyecto

```bash
# 1. Clona el repo (reemplaza TU_USUARIO con tu usuario de GitHub)
git clone https://github.com/TU_USUARIO/elizardo-perez-sistema.git

# 2. Entra a la carpeta
cd elizardo-perez-sistema
```

Luego **descomprime** el archivo `elizardo_perez_sistema.tar.gz` y **copia** todo su contenido dentro de la carpeta `elizardo-perez-sistema/`.

La estructura final debe verse así:
```
elizardo-perez-sistema/
├── run.py
├── config.py
├── requirements.txt
├── README.md
├── .gitignore
└── app/
    ├── __init__.py
    ├── models.py
    ├── views.py
    ├── templates/
    └── static/
```

---

## 🌿 PASO 4: Crear la branch `develop`

```bash
# Desde la rama main, crea develop
git checkout -b develop

# Sube develop a GitHub
git push -u origin develop
```

---

## 👤 PASO 5: Cada integrante crea su propia branch

### Integrante 1 — Modelos de Base de Datos

```bash
# Parte desde develop
git checkout develop
git checkout -b feature/integrante1-modelos

# Agrega los archivos de tu responsabilidad
git add app/models.py
git commit -m "feat: agrega modelos Curso, Docente, Estudiante, Materia, Nota, Asistencia, Horario"

git add app/__init__.py
git commit -m "feat: configura base de datos SQLAlchemy con datos de ejemplo"

# Sube tu branch a GitHub
git push -u origin feature/integrante1-modelos
```

### Integrante 2 — Vistas y Autenticación

```bash
git checkout develop
git checkout -b feature/integrante2-vistas

git add app/views.py
git commit -m "feat: agrega vistas ModelView para Estudiante, Nota, Asistencia"

git add app/templates/dashboard.html
git commit -m "feat: dashboard con estadisticas generales de la escuela"

git push -u origin feature/integrante2-vistas
```

### Integrante 3 — Reportes y Gráficas

```bash
git checkout develop
git checkout -b feature/integrante3-reportes

git add app/templates/reportes/
git commit -m "feat: agrega reporte de estudiantes por curso, calificaciones y asistencia"

git add app/templates/graficas/
git commit -m "feat: agrega 3 graficas estadisticas con matplotlib"

git push -u origin feature/integrante3-reportes
```

> 💡 **Formato de mensajes recomendado:**
> - `feat:` para nueva funcionalidad
> - `fix:` para corrección de errores
> - `docs:` para documentación
> - `style:` para cambios de estilo/formato

---

## 🔀 PASO 6: Crear Pull Request y hacer Merge

### Opción A — Por la web de GitHub (recomendado)

1. Ve a tu repositorio en **github.com**
2. Haz clic en la pestaña **"Pull requests"**
3. Clic en **"New pull request"**
4. Selecciona:
   - **base:** `develop`
   - **compare:** `feature/integrante1-modelos`
5. Título: `feat: modelos de base de datos - Integrante 1`
6. Clic en **"Create pull request"**
7. Clic en **"Merge pull request"** → **"Confirm merge"**

Repite para cada integrante.

### Opción B — Por terminal

```bash
# Asegúrate de estar en develop y actualizado
git checkout develop
git pull origin develop

# Merge de cada integrante (--no-ff mantiene el historial visible)
git merge --no-ff feature/integrante1-modelos -m "merge: feature/integrante1-modelos -> develop"
git merge --no-ff feature/integrante2-vistas  -m "merge: feature/integrante2-vistas -> develop"
git merge --no-ff feature/integrante3-reportes -m "merge: feature/integrante3-reportes -> develop"

# Sube develop con todos los merges
git push origin develop
```

> ✅ Usar `--no-ff` (no fast-forward) hace que el gráfico de GitHub muestre claramente quién hizo cada aporte.

---

## 🚀 PASO 7: Merge final develop → main

```bash
# Cambia a main
git checkout main

# Integra todo desde develop
git merge --no-ff develop -m "release: v1.0.0 - sistema academico U.E. Elizardo Perez G."

# Sube el resultado final
git push origin main

# Verifica el historial completo antes de entregar
git log --oneline --graph --all
```

---

## 🔗 PASO 8: Entregar el link al docente

El link de tu repositorio es:
```
https://github.com/TU_USUARIO/elizardo-perez-sistema
```

Reemplaza `TU_USUARIO` con tu nombre de usuario de GitHub.

---

## 📊 Checklist de entrega (Rúbrica GitHub — 6 pts)

| Requisito | ¿Cómo verificarlo? | ✓ |
|-----------|-------------------|---|
| Repositorio **público** | Ve al repo → debe decir "Public" arriba | ☐ |
| Branch `main` | Visible en la lista de branches | ☐ |
| Branch `develop` | Visible en la lista de branches | ☐ |
| Branch personal de cada integrante | 3 branches `feature/...` visibles | ☐ |
| Commits con mensajes claros | Pestaña "Commits" — mensajes descriptivos | ☐ |
| Mínimo 3 commits por integrante | Filtrar por autor en el historial | ☐ |
| Pull Requests realizados | Pestaña "Pull requests" — cerrados y mergeados | ☐ |
| Merge a `develop` | Gráfico de red en Insights → Network | ☐ |
| README.md completo | Visible en la página principal del repo | ☐ |

---

## ❓ Problemas frecuentes

### "Permission denied" al hacer push

```bash
# Solución: usa token de acceso personal
# Ve a GitHub → Settings → Developer settings → Personal access tokens
# Genera un token con permisos de repo
# Úsalo como contraseña cuando Git lo pida
```

### "failed to push some refs"

```bash
# Alguien subió cambios antes que tú — primero descarga
git pull origin develop --rebase
git push origin develop
```

### Conflicto de merge

```bash
# Git te indica el archivo en conflicto
# Ábrelo, busca los marcadores <<<<<<< y >>>>>>>
# Edita hasta que quede correcto
git add archivo_con_conflicto.py
git commit -m "fix: resuelve conflicto de merge"
```

### No puedo ver el historial de ramas en GitHub

```bash
# Verifica que todas las branches estén subidas
git push origin feature/integrante1-modelos
git push origin feature/integrante2-vistas
git push origin feature/integrante3-reportes
git push origin develop
git push origin main
```

---

## 🌐 Ver el gráfico de ramas en GitHub

Para verificar que todo el trabajo en equipo es visible:

1. Ve a tu repositorio en GitHub
2. Clic en **"Insights"** (pestaña superior)
3. Clic en **"Network"**

Deberás ver las 5 ramas con sus merges hacia `develop` y el merge final hacia `main`.

---

*U.E. Profesor Elizardo Pérez G. · Villa Pagador · Av. La Joya y Bella Vista · Cochabamba, Bolivia*
*2do Parcial — Gestión 2025*
