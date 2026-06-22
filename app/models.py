from flask_appbuilder import Model
from sqlalchemy import Column, Integer, String, Date, Float, ForeignKey, Text, Boolean, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime


class Curso(Model):
    """Tabla 1: Cursos/Grados escolares"""
    __tablename__ = 'curso'
    id = Column(Integer, primary_key=True)
    nombre = Column(String(50), nullable=False)           # Ej: "1ro Primaria"
    nivel = Column(String(30), nullable=False)            # Primaria / Secundaria
    turno = Column(String(20), nullable=False)            # Mañana / Tarde
    capacidad_max = Column(Integer, default=30)
    activo = Column(Boolean, default=True)

    # Relaciones
    estudiantes = relationship('Estudiante', back_populates='curso')
    horarios = relationship('Horario', back_populates='curso')

    def __repr__(self):
        return f"{self.nombre} - {self.turno}"


class Docente(Model):
    """Tabla 2: Docentes de la unidad educativa"""
    __tablename__ = 'docente'
    id = Column(Integer, primary_key=True)
    ci = Column(String(15), unique=True, nullable=False)
    nombre = Column(String(80), nullable=False)
    apellido = Column(String(80), nullable=False)
    especialidad = Column(String(100))
    telefono = Column(String(20))
    email = Column(String(120))
    fecha_contrato = Column(Date)
    activo = Column(Boolean, default=True)

    # Relaciones
    horarios = relationship('Horario', back_populates='docente')

    def __repr__(self):
        return f"{self.apellido} {self.nombre}"

    @property
    def nombre_completo(self):
        return f"{self.apellido} {self.nombre}"


class Estudiante(Model):
    """Tabla 3: Estudiantes matriculados"""
    __tablename__ = 'estudiante'
    id = Column(Integer, primary_key=True)
    rude = Column(String(20), unique=True, nullable=False)   # Registro Único de Estudiante
    nombre = Column(String(80), nullable=False)
    apellido = Column(String(80), nullable=False)
    fecha_nacimiento = Column(Date)
    genero = Column(String(10))
    direccion = Column(String(200))
    telefono_tutor = Column(String(20))
    nombre_tutor = Column(String(150))
    fecha_matricula = Column(Date, default=datetime.today)
    activo = Column(Boolean, default=True)

    # Clave foránea
    curso_id = Column(Integer, ForeignKey('curso.id'), nullable=False)
    curso = relationship('Curso', back_populates='estudiantes')

    # Relaciones
    notas = relationship('Nota', back_populates='estudiante')
    asistencias = relationship('Asistencia', back_populates='estudiante')

    def __repr__(self):
        return f"{self.apellido} {self.nombre}"

    @property
    def nombre_completo(self):
        return f"{self.apellido} {self.nombre}"


class Materia(Model):
    """Tabla 4: Materias/Asignaturas"""
    __tablename__ = 'materia'
    id = Column(Integer, primary_key=True)
    nombre = Column(String(100), nullable=False)
    codigo = Column(String(20), unique=True, nullable=False)
    nivel = Column(String(30))          # Primaria / Secundaria
    horas_semanales = Column(Integer, default=4)
    descripcion = Column(Text)
    activo = Column(Boolean, default=True)

    # Relaciones
    notas = relationship('Nota', back_populates='materia')
    horarios = relationship('Horario', back_populates='materia')

    def __repr__(self):
        return self.nombre


class Horario(Model):
    """Tabla 5: Horario de clases (relaciona Curso, Docente y Materia)"""
    __tablename__ = 'horario'
    id = Column(Integer, primary_key=True)
    dia_semana = Column(String(15), nullable=False)     # Lunes, Martes...
    hora_inicio = Column(String(10), nullable=False)    # 08:00
    hora_fin = Column(String(10), nullable=False)       # 09:00
    aula = Column(String(20))
    gestion = Column(Integer, default=datetime.now().year)

    # Claves foráneas
    curso_id = Column(Integer, ForeignKey('curso.id'), nullable=False)
    docente_id = Column(Integer, ForeignKey('docente.id'), nullable=False)
    materia_id = Column(Integer, ForeignKey('materia.id'), nullable=False)

    # Relaciones
    curso = relationship('Curso', back_populates='horarios')
    docente = relationship('Docente', back_populates='horarios')
    materia = relationship('Materia', back_populates='horarios')

    def __repr__(self):
        return f"{self.dia_semana} {self.hora_inicio} - {self.materia}"


class Nota(Model):
    """Tabla 6: Registro de notas/calificaciones"""
    __tablename__ = 'nota'
    id = Column(Integer, primary_key=True)
    trimestre = Column(Integer, nullable=False)     # 1, 2 o 3
    ser = Column(Float, default=0.0)               # Dimensión SER (10 pts)
    saber = Column(Float, default=0.0)             # Dimensión SABER (45 pts)
    hacer = Column(Float, default=0.0)             # Dimensión HACER (35 pts)
    decidir = Column(Float, default=0.0)           # Dimensión DECIDIR (10 pts)
    nota_final = Column(Float, default=0.0)        # Suma total (100 pts)
    observacion = Column(Text)
    fecha_registro = Column(DateTime, default=datetime.now)
    gestion = Column(Integer, default=datetime.now().year)

    # Claves foráneas
    estudiante_id = Column(Integer, ForeignKey('estudiante.id'), nullable=False)
    materia_id = Column(Integer, ForeignKey('materia.id'), nullable=False)

    # Relaciones
    estudiante = relationship('Estudiante', back_populates='notas')
    materia = relationship('Materia', back_populates='notas')

    def __repr__(self):
        return f"Nota {self.nota_final} - {self.estudiante} - {self.materia}"

    def calcular_nota_final(self):
        self.nota_final = (self.ser or 0) + (self.saber or 0) + (self.hacer or 0) + (self.decidir or 0)
        return self.nota_final


class Asistencia(Model):
    """Tabla 7 (extra): Registro de asistencia diaria"""
    __tablename__ = 'asistencia'
    id = Column(Integer, primary_key=True)
    fecha = Column(Date, nullable=False, default=datetime.today)
    presente = Column(Boolean, default=True)
    justificada = Column(Boolean, default=False)
    observacion = Column(String(200))

    # Clave foránea
    estudiante_id = Column(Integer, ForeignKey('estudiante.id'), nullable=False)
    estudiante = relationship('Estudiante', back_populates='asistencias')

    def __repr__(self):
        estado = "Presente" if self.presente else ("Justificada" if self.justificada else "Ausente")
        return f"{self.fecha} - {self.estudiante} - {estado}"
