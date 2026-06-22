from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_appbuilder import AppBuilder

db = SQLAlchemy()
appbuilder = None


def create_app():
    app = Flask(__name__, template_folder='templates', static_folder='static')
    app.config.from_object('config')
    db.init_app(app)

    with app.app_context():
        # Importar modelos ANTES de que AppBuilder inicialice (para que FAB los vea)
        from app import models  # noqa: F401

        global appbuilder
        appbuilder = AppBuilder(app, db.session)

        from app.views import (
            CursoView, DocenteView, EstudianteView, MateriaView,
            HorarioView, NotaView, AsistenciaView,
            DashboardView, ReporteView, GraficaView
        )

        appbuilder.add_view(DashboardView,   "Dashboard",      icon="fa-home",         category="")
        appbuilder.add_view(EstudianteView,  "Estudiantes",    icon="fa-users",        category="Gestión Académica", category_icon="fa-graduation-cap")
        appbuilder.add_view(NotaView,        "Calificaciones", icon="fa-star",         category="Gestión Académica")
        appbuilder.add_view(AsistenciaView,  "Asistencia",     icon="fa-check-square", category="Gestión Académica")
        appbuilder.add_view(CursoView,       "Cursos",         icon="fa-book",         category="Configuración", category_icon="fa-cog")
        appbuilder.add_view(MateriaView,     "Materias",       icon="fa-list",         category="Configuración")
        appbuilder.add_view(DocenteView,     "Docentes",       icon="fa-user-tie",     category="Configuración")
        appbuilder.add_view(HorarioView,     "Horarios",       icon="fa-calendar",     category="Configuración")
        appbuilder.add_view(ReporteView,     "Ver Reportes",   icon="fa-file-text",    category="Reportes",  category_icon="fa-bar-chart")
        appbuilder.add_view(GraficaView,     "Ver Gráficas",   icon="fa-pie-chart",    category="Gráficas",  category_icon="fa-line-chart")

        # Crear TODAS las tablas (FAB + propias)
        db.create_all()
        _seed_roles_and_data(appbuilder)

    return app


def _seed_roles_and_data(ab):
    from app.models import Curso, Docente, Estudiante, Materia, Horario, Nota, Asistencia
    from datetime import date, timedelta
    import random

    # ─── Roles ──────────────────────────────────
    for rol in ["Admin", "Supervisor", "Usuario"]:
        if not ab.sm.find_role(rol):
            ab.sm.add_role(rol)

    # ─── Usuarios de prueba ──────────────────────
    if not ab.sm.find_user(username='admin'):
        ab.sm.add_user(username='admin', first_name='Administrador', last_name='Sistema',
                       email='admin@elizardoperez.edu.bo', role=ab.sm.find_role('Admin'), password='admin123')
    if not ab.sm.find_user(username='supervisor'):
        ab.sm.add_user(username='supervisor', first_name='María', last_name='Flores',
                       email='supervisor@elizardoperez.edu.bo', role=ab.sm.find_role('Supervisor'), password='super123')
    if not ab.sm.find_user(username='usuario'):
        ab.sm.add_user(username='usuario', first_name='Carlos', last_name='Mamani',
                       email='usuario@elizardoperez.edu.bo', role=ab.sm.find_role('Usuario'), password='user123')

    # ─── Datos de ejemplo ────────────────────────
    if db.session.query(Curso).count() == 0:
        cursos = [
            Curso(nombre="1ro A Primaria",   nivel="Primaria",   turno="Mañana", capacidad_max=30),
            Curso(nombre="2do A Primaria",   nivel="Primaria",   turno="Mañana", capacidad_max=30),
            Curso(nombre="3ro A Primaria",   nivel="Primaria",   turno="Tarde",  capacidad_max=28),
            Curso(nombre="4to A Primaria",   nivel="Primaria",   turno="Tarde",  capacidad_max=28),
            Curso(nombre="1ro A Secundaria", nivel="Secundaria", turno="Mañana", capacidad_max=35),
            Curso(nombre="2do A Secundaria", nivel="Secundaria", turno="Tarde",  capacidad_max=35),
            Curso(nombre="3ro A Secundaria", nivel="Secundaria", turno="Mañana", capacidad_max=33),
            Curso(nombre="4to A Secundaria", nivel="Secundaria", turno="Tarde",  capacidad_max=32),
        ]
        db.session.add_all(cursos)
        db.session.commit()

    if db.session.query(Materia).count() == 0:
        materias = [
            Materia(codigo="MAT01", nombre="Matemática",            nivel="Ambos",      horas_semanales=5),
            Materia(codigo="LEN01", nombre="Lenguaje y Literatura", nivel="Ambos",      horas_semanales=5),
            Materia(codigo="CN01",  nombre="Ciencias Naturales",    nivel="Primaria",   horas_semanales=4),
            Materia(codigo="CS01",  nombre="Ciencias Sociales",     nivel="Primaria",   horas_semanales=4),
            Materia(codigo="FIS01", nombre="Física",                nivel="Secundaria", horas_semanales=4),
            Materia(codigo="QUI01", nombre="Química",               nivel="Secundaria", horas_semanales=4),
            Materia(codigo="BIO01", nombre="Biología",              nivel="Secundaria", horas_semanales=3),
            Materia(codigo="EDF01", nombre="Educación Física",      nivel="Ambos",      horas_semanales=2),
        ]
        db.session.add_all(materias)
        db.session.commit()

    if db.session.query(Docente).count() == 0:
        docentes = [
            Docente(ci="1234567", nombre="Juan",   apellido="Quispe Mamani",    especialidad="Matemática",         telefono="70012345", email="jquispe@elizardoperez.edu.bo",  fecha_contrato=date(2018,2,1)),
            Docente(ci="2345678", nombre="Rosa",   apellido="Condori Flores",   especialidad="Lenguaje",           telefono="70023456", email="rcondori@elizardoperez.edu.bo", fecha_contrato=date(2019,2,1)),
            Docente(ci="3456789", nombre="Pedro",  apellido="Vargas López",     especialidad="Ciencias Naturales", telefono="70034567", email="pvargas@elizardoperez.edu.bo",  fecha_contrato=date(2020,2,1)),
            Docente(ci="4567890", nombre="Carmen", apellido="Torrez Gutiérrez", especialidad="Física y Química",   telefono="70045678", email="ctorrez@elizardoperez.edu.bo",  fecha_contrato=date(2017,2,1)),
            Docente(ci="5678901", nombre="Miguel", apellido="Salinas Rojas",    especialidad="Educación Física",   telefono="70056789", email="msalinas@elizardoperez.edu.bo", fecha_contrato=date(2021,2,1)),
        ]
        db.session.add_all(docentes)
        db.session.commit()

    if db.session.query(Estudiante).count() == 0:
        nombres_m = ["Andrés","Bryan","Carlos","Diego","Erick","Franco","Gabriel","Hugo","Ivan","Jorge","Kevin","Luis"]
        nombres_f = ["Ana","Beatriz","Carla","Diana","Elena","Fabiola","Gabriela","Hilda","Iris","Julia","Karen","Luisa"]
        apells = ["Quispe","Mamani","Condori","Flores","Vargas","Torrez","Salinas","Rojas","Mendoza","Cruz","Pinto","Huanca"]
        cursos = db.session.query(Curso).all()
        rude = 80000001
        for i, curso in enumerate(cursos):
            for _ in range(random.randint(18, 25)):
                g = random.choice(["M", "F"])
                db.session.add(Estudiante(
                    rude=str(rude),
                    nombre=random.choice(nombres_m if g == "M" else nombres_f),
                    apellido=random.choice(apells) + " " + random.choice(apells),
                    fecha_nacimiento=date(2015 - i - random.randint(0, 1), random.randint(1, 12), random.randint(1, 28)),
                    genero=g, curso_id=curso.id,
                    direccion="Villa Pagador, Cochabamba",
                    nombre_tutor=random.choice(apells) + " (Tutor)",
                    telefono_tutor=f"7{random.randint(1000000, 9999999)}",
                    fecha_matricula=date(2025, 2, random.randint(1, 15)),
                ))
                rude += 1
        db.session.commit()

    if db.session.query(Nota).count() == 0:
        estudiantes = db.session.query(Estudiante).all()
        materias = db.session.query(Materia).all()
        for est in estudiantes:
            for mat in materias[:6]:
                for trim in [1, 2, 3]:
                    s = round(random.uniform(7, 10), 1)
                    sa = round(random.uniform(30, 45), 1)
                    h = round(random.uniform(22, 35), 1)
                    d = round(random.uniform(7, 10), 1)
                    db.session.add(Nota(
                        estudiante_id=est.id, materia_id=mat.id, trimestre=trim,
                        ser=s, saber=sa, hacer=h, decidir=d,
                        nota_final=round(s + sa + h + d, 1), gestion=2025,
                    ))
        db.session.commit()

    if db.session.query(Asistencia).count() == 0:
        from datetime import date as ddate
        hoy = ddate.today()
        inicio = ddate(hoy.year, hoy.month, 1)
        dias = []
        d = inicio
        while d <= hoy:
            if d.weekday() < 5:
                dias.append(d)
            d += timedelta(days=1)
        for est in db.session.query(Estudiante).all():
            for dia in dias:
                presente = random.random() > 0.1
                justif = (not presente) and (random.random() > 0.5)
                db.session.add(Asistencia(estudiante_id=est.id, fecha=dia, presente=presente, justificada=justif))
        db.session.commit()

    if db.session.query(Horario).count() == 0:
        dias_sem = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes"]
        horas = [("07:30","08:30"),("08:30","09:30"),("09:45","10:45"),("10:45","11:45")]
        cursos = db.session.query(Curso).all()
        docentes = db.session.query(Docente).all()
        materias = db.session.query(Materia).all()
        for curso in cursos:
            for i, dia in enumerate(dias_sem):
                for j, (hi, hf) in enumerate(horas):
                    db.session.add(Horario(
                        dia_semana=dia, hora_inicio=hi, hora_fin=hf,
                        aula=f"Aula {curso.id}", curso_id=curso.id,
                        docente_id=docentes[(i + j) % len(docentes)].id,
                        materia_id=materias[(i * 4 + j) % len(materias)].id,
                        gestion=2025,
                    ))
        db.session.commit()
