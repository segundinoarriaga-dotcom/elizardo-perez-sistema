from flask_appbuilder import ModelView
from flask_appbuilder.models.sqla.interface import SQLAInterface
from flask_appbuilder.views import BaseView, expose
from flask_appbuilder.security.decorators import has_access
from flask import render_template, redirect, url_for, flash, Response
from flask_login import current_user
from sqlalchemy import func, and_
from datetime import datetime, date
import io
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import base64

from app.models import Curso, Docente, Estudiante, Materia, Horario, Nota, Asistencia
from . import db


# ─────────────────────────────────────────────
# VISTAS DE MODELOS (ModelView)
# ─────────────────────────────────────────────

class CursoView(ModelView):
    datamodel = SQLAInterface(Curso)
    list_title = "Cursos"
    add_title = "Nuevo Curso"
    edit_title = "Editar Curso"

    list_columns = ['nombre', 'nivel', 'turno', 'capacidad_max', 'activo']
    add_columns = ['nombre', 'nivel', 'turno', 'capacidad_max', 'activo']
    edit_columns = ['nombre', 'nivel', 'turno', 'capacidad_max', 'activo']
    show_columns = ['nombre', 'nivel', 'turno', 'capacidad_max', 'activo']


class DocenteView(ModelView):
    datamodel = SQLAInterface(Docente)
    list_title = "Docentes"
    add_title = "Nuevo Docente"
    edit_title = "Editar Docente"

    list_columns = ['ci', 'nombre', 'apellido', 'especialidad', 'telefono', 'activo']
    add_columns = ['ci', 'nombre', 'apellido', 'especialidad', 'telefono', 'email', 'fecha_contrato', 'activo']
    edit_columns = ['ci', 'nombre', 'apellido', 'especialidad', 'telefono', 'email', 'fecha_contrato', 'activo']
    show_columns = ['ci', 'nombre', 'apellido', 'especialidad', 'telefono', 'email', 'fecha_contrato', 'activo']


class EstudianteView(ModelView):
    datamodel = SQLAInterface(Estudiante)
    list_title = "Estudiantes"
    add_title = "Nuevo Estudiante"
    edit_title = "Editar Estudiante"

    list_columns = ['rude', 'apellido', 'nombre', 'curso', 'fecha_matricula', 'activo']
    add_columns = ['rude', 'nombre', 'apellido', 'fecha_nacimiento', 'genero', 'curso',
                   'direccion', 'telefono_tutor', 'nombre_tutor', 'fecha_matricula', 'activo']
    edit_columns = ['rude', 'nombre', 'apellido', 'fecha_nacimiento', 'genero', 'curso',
                    'direccion', 'telefono_tutor', 'nombre_tutor', 'activo']
    show_columns = ['rude', 'nombre', 'apellido', 'fecha_nacimiento', 'genero', 'curso',
                    'direccion', 'telefono_tutor', 'nombre_tutor', 'fecha_matricula', 'activo']

    related_views = [type('NotaInlineView', (ModelView,), {
        'datamodel': SQLAInterface(Nota),
        'list_columns': ['materia', 'trimestre', 'nota_final', 'gestion'],
    })]


class MateriaView(ModelView):
    datamodel = SQLAInterface(Materia)
    list_title = "Materias"
    add_title = "Nueva Materia"
    edit_title = "Editar Materia"

    list_columns = ['codigo', 'nombre', 'nivel', 'horas_semanales', 'activo']
    add_columns = ['codigo', 'nombre', 'nivel', 'horas_semanales', 'descripcion', 'activo']
    edit_columns = ['codigo', 'nombre', 'nivel', 'horas_semanales', 'descripcion', 'activo']


class HorarioView(ModelView):
    datamodel = SQLAInterface(Horario)
    list_title = "Horarios"
    add_title = "Nuevo Horario"
    edit_title = "Editar Horario"

    list_columns = ['dia_semana', 'hora_inicio', 'hora_fin', 'curso', 'materia', 'docente', 'aula']
    add_columns = ['dia_semana', 'hora_inicio', 'hora_fin', 'aula', 'curso', 'materia', 'docente', 'gestion']
    edit_columns = ['dia_semana', 'hora_inicio', 'hora_fin', 'aula', 'curso', 'materia', 'docente', 'gestion']


class NotaView(ModelView):
    datamodel = SQLAInterface(Nota)
    list_title = "Calificaciones"
    add_title = "Registrar Calificación"
    edit_title = "Editar Calificación"

    list_columns = ['estudiante', 'materia', 'trimestre', 'ser', 'saber', 'hacer', 'decidir', 'nota_final', 'gestion']
    add_columns = ['estudiante', 'materia', 'trimestre', 'ser', 'saber', 'hacer', 'decidir', 'nota_final', 'observacion', 'gestion']
    edit_columns = ['estudiante', 'materia', 'trimestre', 'ser', 'saber', 'hacer', 'decidir', 'nota_final', 'observacion', 'gestion']


class AsistenciaView(ModelView):
    datamodel = SQLAInterface(Asistencia)
    list_title = "Registro de Asistencia"
    add_title = "Registrar Asistencia"
    edit_title = "Editar Asistencia"

    list_columns = ['fecha', 'estudiante', 'presente', 'justificada', 'observacion']
    add_columns = ['fecha', 'estudiante', 'presente', 'justificada', 'observacion']
    edit_columns = ['fecha', 'estudiante', 'presente', 'justificada', 'observacion']


# ─────────────────────────────────────────────
# DASHBOARD PRINCIPAL
# ─────────────────────────────────────────────

class DashboardView(BaseView):
    default_view = 'index'
    route_base = "/"

    @expose('/dashboard')
    @has_access
    def index(self):
        total_estudiantes = db.session.query(func.count(Estudiante.id)).filter_by(activo=True).scalar() or 0
        total_docentes = db.session.query(func.count(Docente.id)).filter_by(activo=True).scalar() or 0
        total_cursos = db.session.query(func.count(Curso.id)).filter_by(activo=True).scalar() or 0
        total_materias = db.session.query(func.count(Materia.id)).filter_by(activo=True).scalar() or 0

        # Promedio general de notas
        promedio = db.session.query(func.avg(Nota.nota_final)).scalar()
        promedio = round(promedio, 1) if promedio else 0

        # Estudiantes por curso (para mini-tabla)
        por_curso = db.session.query(
            Curso.nombre, func.count(Estudiante.id)
        ).join(Estudiante).filter(Estudiante.activo == True).group_by(Curso.nombre).all()

        return self.render_template(
            'dashboard.html',
            total_estudiantes=total_estudiantes,
            total_docentes=total_docentes,
            total_cursos=total_cursos,
            total_materias=total_materias,
            promedio=promedio,
            por_curso=por_curso,
        )


# ─────────────────────────────────────────────
# REPORTES
# ─────────────────────────────────────────────

class ReporteView(BaseView):
    route_base = "/reportes"
    default_view = 'index'

    @expose('/')
    @has_access
    def index(self):
        return self.render_template('reportes/index.html')

    # ── REPORTE 1: Estudiantes por curso ──────
    @expose('/estudiantes_por_curso')
    @has_access
    def estudiantes_por_curso(self):
        datos = db.session.query(
            Curso.nombre,
            Curso.turno,
            Curso.nivel,
            func.count(Estudiante.id).label('total')
        ).outerjoin(Estudiante, and_(Estudiante.curso_id == Curso.id, Estudiante.activo == True)) \
         .filter(Curso.activo == True) \
         .group_by(Curso.id) \
         .order_by(Curso.nivel, Curso.nombre).all()

        return self.render_template('reportes/estudiantes_por_curso.html', datos=datos)

    # ── REPORTE 2: Calificaciones por materia ─
    @expose('/calificaciones_materia')
    @has_access
    def calificaciones_materia(self):
        gestion = datetime.now().year
        datos = db.session.query(
            Materia.nombre,
            func.count(Nota.id).label('total_notas'),
            func.avg(Nota.nota_final).label('promedio'),
            func.min(Nota.nota_final).label('minima'),
            func.max(Nota.nota_final).label('maxima'),
        ).join(Nota).filter(Nota.gestion == gestion) \
         .group_by(Materia.id) \
         .order_by(Materia.nombre).all()

        return self.render_template('reportes/calificaciones_materia.html', datos=datos, gestion=gestion)

    # ── REPORTE 3: Asistencia mensual ─────────
    @expose('/asistencia_mensual')
    @has_access
    def asistencia_mensual(self):
        hoy = date.today()
        datos = db.session.query(
            Estudiante.apellido,
            Estudiante.nombre,
            Curso.nombre.label('curso'),
            func.count(Asistencia.id).label('total_dias'),
            func.sum(
                db.case((Asistencia.presente == True, 1), else_=0)
            ).label('dias_presente'),
            func.sum(
                db.case((Asistencia.justificada == True, 1), else_=0)
            ).label('dias_justificados'),
        ).join(Estudiante, Estudiante.id == Asistencia.estudiante_id) \
         .join(Curso, Curso.id == Estudiante.curso_id) \
         .filter(
             Asistencia.fecha >= date(hoy.year, hoy.month, 1),
             Estudiante.activo == True
         ) \
         .group_by(Estudiante.id) \
         .order_by(Curso.nombre, Estudiante.apellido).all()

        return self.render_template(
            'reportes/asistencia_mensual.html',
            datos=datos,
            mes=hoy.strftime("%B %Y")
        )


# ─────────────────────────────────────────────
# GRÁFICAS
# ─────────────────────────────────────────────

def _fig_to_base64(fig):
    buf = io.BytesIO()
    fig.savefig(buf, format='png', bbox_inches='tight', dpi=100)
    buf.seek(0)
    img_b64 = base64.b64encode(buf.read()).decode('utf-8')
    plt.close(fig)
    return img_b64


class GraficaView(BaseView):
    route_base = "/graficas"
    default_view = 'index'

    @expose('/')
    @has_access
    def index(self):
        return self.render_template('graficas/index.html')

    # ── GRÁFICA 1: Estudiantes por Nivel ──────
    @expose('/estudiantes_nivel')
    @has_access
    def estudiantes_nivel(self):
        datos = db.session.query(
            Curso.nivel,
            func.count(Estudiante.id).label('total')
        ).join(Estudiante, Estudiante.curso_id == Curso.id) \
         .filter(Estudiante.activo == True) \
         .group_by(Curso.nivel).all()

        niveles = [d[0] for d in datos]
        totales = [d[1] for d in datos]

        fig, ax = plt.subplots(figsize=(7, 5))
        colores = ['#1B4F72', '#2980B9', '#85C1E9', '#D6EAF8']
        wedges, texts, autotexts = ax.pie(
            totales, labels=niveles, autopct='%1.1f%%',
            colors=colores[:len(niveles)], startangle=90,
            wedgeprops=dict(edgecolor='white', linewidth=2)
        )
        for at in autotexts:
            at.set_fontsize(12)
            at.set_color('white')
            at.set_fontweight('bold')
        ax.set_title('Distribución de Estudiantes por Nivel', fontsize=14, fontweight='bold', pad=15)
        img = _fig_to_base64(fig)

        return self.render_template('graficas/grafica.html',
                                    titulo='Estudiantes por Nivel',
                                    imagen=img,
                                    descripcion='Distribución porcentual de estudiantes entre nivel Primario y Secundario.')

    # ── GRÁFICA 2: Promedio de notas por materia
    @expose('/promedios_materia')
    @has_access
    def promedios_materia(self):
        gestion = datetime.now().year
        datos = db.session.query(
            Materia.nombre,
            func.avg(Nota.nota_final).label('promedio')
        ).join(Nota).filter(Nota.gestion == gestion) \
         .group_by(Materia.id) \
         .order_by(func.avg(Nota.nota_final).desc()).all()

        materias = [d[0][:15] for d in datos]
        promedios = [round(d[1], 1) for d in datos]

        fig, ax = plt.subplots(figsize=(9, 5))
        bars = ax.barh(materias, promedios, color='#1B4F72', edgecolor='white', linewidth=0.5)
        ax.axvline(x=51, color='#E74C3C', linestyle='--', linewidth=1.5, label='Nota mínima (51)')
        for bar, val in zip(bars, promedios):
            ax.text(bar.get_width() + 0.5, bar.get_y() + bar.get_height() / 2,
                    f'{val}', va='center', fontsize=10, fontweight='bold', color='#1B4F72')
        ax.set_xlabel('Promedio de Nota', fontsize=11)
        ax.set_title(f'Promedio de Calificaciones por Materia – Gestión {gestion}', fontsize=13, fontweight='bold')
        ax.set_xlim(0, 105)
        ax.legend(fontsize=9)
        ax.grid(axis='x', linestyle=':', alpha=0.5)
        fig.tight_layout()
        img = _fig_to_base64(fig)

        return self.render_template('graficas/grafica.html',
                                    titulo='Promedios por Materia',
                                    imagen=img,
                                    descripcion=f'Promedio general de calificaciones por materia en la gestión {gestion}.')

    # ── GRÁFICA 3: Asistencia del mes ─────────
    @expose('/asistencia_mes')
    @has_access
    def asistencia_mes(self):
        hoy = date.today()
        datos = db.session.query(
            Curso.nombre,
            func.count(Asistencia.id).label('total'),
            func.sum(db.case((Asistencia.presente == True, 1), else_=0)).label('presentes')
        ).join(Estudiante, Estudiante.id == Asistencia.estudiante_id) \
         .join(Curso, Curso.id == Estudiante.curso_id) \
         .filter(Asistencia.fecha >= date(hoy.year, hoy.month, 1)) \
         .group_by(Curso.nombre).all()

        cursos = [d[0] for d in datos]
        pct_asistencia = [
            round((d[2] / d[1] * 100), 1) if d[1] > 0 else 0
            for d in datos
        ]

        fig, ax = plt.subplots(figsize=(9, 5))
        colores_barra = ['#1B4F72' if p >= 80 else '#E74C3C' for p in pct_asistencia]
        bars = ax.bar(cursos, pct_asistencia, color=colores_barra, edgecolor='white', linewidth=0.5)
        ax.axhline(y=80, color='#F39C12', linestyle='--', linewidth=1.5, label='Meta 80%')
        for bar, val in zip(bars, pct_asistencia):
            ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 1,
                    f'{val}%', ha='center', va='bottom', fontsize=9, fontweight='bold')
        ax.set_ylim(0, 110)
        ax.set_ylabel('% Asistencia', fontsize=11)
        ax.set_title(f'Porcentaje de Asistencia por Curso – {hoy.strftime("%B %Y")}', fontsize=13, fontweight='bold')
        plt.xticks(rotation=30, ha='right', fontsize=9)

        bueno = mpatches.Patch(color='#1B4F72', label='≥ 80% asistencia')
        malo = mpatches.Patch(color='#E74C3C', label='< 80% asistencia')
        ax.legend(handles=[bueno, malo, plt.Line2D([0], [0], color='#F39C12', linestyle='--', label='Meta 80%')],
                  fontsize=9)
        ax.grid(axis='y', linestyle=':', alpha=0.5)
        fig.tight_layout()
        img = _fig_to_base64(fig)

        return self.render_template('graficas/grafica.html',
                                    titulo='Asistencia por Curso',
                                    imagen=img,
                                    descripcion=f'Porcentaje de asistencia por curso durante {hoy.strftime("%B %Y")}.')
