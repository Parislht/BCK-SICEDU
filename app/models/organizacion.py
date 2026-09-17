from datetime import date
from typing import Optional

from sqlmodel import Field, SQLModel


class PeriodoAcademico(SQLModel, table=True):
    __tablename__ = "periodo_academico"

    id_periodo: Optional[int] = Field(default=None, primary_key=True)
    nombre: str
    fecha_inicio: date
    fecha_fin: date


class PeriodoEvaluacion(SQLModel, table=True):
    __tablename__ = "periodo_evaluacion"

    id_periodo_evaluacion: Optional[int] = Field(default=None, primary_key=True)
    id_periodo: int = Field(foreign_key="periodo_academico.id_periodo")
    numero: int
    fecha_inicio: date
    fecha_fin: date


class Colegio(SQLModel, table=True):
    __tablename__ = "colegio"

    id_colegio: Optional[int] = Field(default=None, primary_key=True)
    nombre: str
    zona: Optional[str] = Field(default=None)


class CicloEbr(SQLModel, table=True):
    __tablename__ = "ciclo_ebr"

    id_ciclo: Optional[int] = Field(default=None, primary_key=True)
    nombre: str


class Grado(SQLModel, table=True):
    __tablename__ = "grado"

    id_grado: Optional[int] = Field(default=None, primary_key=True)
    nombre: str
    id_ciclo: int = Field(foreign_key="ciclo_ebr.id_ciclo")


class Programa(SQLModel, table=True):
    __tablename__ = "programa"

    id_programa: Optional[int] = Field(default=None, primary_key=True)
    nombre: str


class Docente(SQLModel, table=True):
    __tablename__ = "docente"

    id_docente: Optional[int] = Field(default=None, primary_key=True)
    nombres: str
    apellidos: str
    activo: bool = Field(default=True)


class Rol(SQLModel, table=True):
    __tablename__ = "rol"

    id_rol: Optional[int] = Field(default=None, primary_key=True)
    nombre: str


class Usuario(SQLModel, table=True):
    __tablename__ = "usuario"

    id_usuario: Optional[int] = Field(default=None, primary_key=True)
    id_rol: int = Field(foreign_key="rol.id_rol")
    correo: str = Field(unique=True, index=True)
    password_hash: str
    id_docente: Optional[int] = Field(default=None, foreign_key="docente.id_docente")
    nombres: str
    apellidos: str
    activo: bool = Field(default=True)


class Alumno(SQLModel, table=True):
    __tablename__ = "alumno"

    id_alumno: Optional[int] = Field(default=None, primary_key=True)
    nombres: str
    apellidos: str
    id_colegio: int = Field(foreign_key="colegio.id_colegio")
    id_grado: int = Field(foreign_key="grado.id_grado")
    id_programa_actual: int = Field(foreign_key="programa.id_programa")
    classroom_razkids: Optional[str] = Field(default=None)
    fecha_registro: date
    activo: bool = Field(default=True)


class DocenteColegioGrado(SQLModel, table=True):
    __tablename__ = "docente_colegio_grado"

    id: Optional[int] = Field(default=None, primary_key=True)
    id_docente: int = Field(foreign_key="docente.id_docente")
    id_colegio: int = Field(foreign_key="colegio.id_colegio")
    id_grado: int = Field(foreign_key="grado.id_grado")
    id_periodo_evaluacion: int = Field(foreign_key="periodo_evaluacion.id_periodo_evaluacion")


class AlumnoProgramaHistorial(SQLModel, table=True):
    __tablename__ = "alumno_programa_historial"

    id: Optional[int] = Field(default=None, primary_key=True)
    id_alumno: int = Field(foreign_key="alumno.id_alumno")
    id_programa: int = Field(foreign_key="programa.id_programa")
    id_periodo_evaluacion: int = Field(foreign_key="periodo_evaluacion.id_periodo_evaluacion")
