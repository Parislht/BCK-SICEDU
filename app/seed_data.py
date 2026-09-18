"""
Datos de prueba para HU14 (autenticacion). Ficticios, no son informacion
real de Mision Huascaran. Correr manualmente con:

    python -m app.seed_data
"""
from sqlmodel import Session, select

from app.core.database import engine
from app.core.security import hash_password
from app.models.organizacion import Colegio, Docente, Rol, Usuario

ROLES = ["Profesor", "Jefa_Profesores", "Directivos"]

PROFESOR_CORREO = "profesor.prueba@sicedu.test"
PROFESOR_PASSWORD = "ProfesorTest123"

JEFA_CORREO = "jefa.prueba@sicedu.test"
JEFA_PASSWORD = "JefaTest123"

DIRECTIVO_CORREO = "directivo.prueba@sicedu.test"
DIRECTIVO_PASSWORD = "DirectivoTest123"


def get_or_create_rol(session: Session, nombre: str) -> Rol:
    rol = session.exec(select(Rol).where(Rol.nombre == nombre)).first()
    if rol is None:
        rol = Rol(nombre=nombre)
        session.add(rol)
        session.commit()
        session.refresh(rol)
    return rol


def seed() -> None:
    with Session(engine) as session:
        roles = {nombre: get_or_create_rol(session, nombre) for nombre in ROLES}

        colegio = session.exec(
            select(Colegio).where(Colegio.nombre == "Colegio de Prueba")
        ).first()
        if colegio is None:
            colegio = Colegio(nombre="Colegio de Prueba", zona="Zona de Prueba")
            session.add(colegio)
            session.commit()
            session.refresh(colegio)

        docente = session.exec(
            select(Docente).where(
                Docente.nombres == "Docente", Docente.apellidos == "de Prueba"
            )
        ).first()
        if docente is None:
            docente = Docente(nombres="Docente", apellidos="de Prueba", activo=True)
            session.add(docente)
            session.commit()
            session.refresh(docente)

        usuario_profesor = session.exec(
            select(Usuario).where(Usuario.correo == PROFESOR_CORREO)
        ).first()
        if usuario_profesor is None:
            usuario_profesor = Usuario(
                id_rol=roles["Profesor"].id_rol,
                correo=PROFESOR_CORREO,
                password_hash=hash_password(PROFESOR_PASSWORD),
                id_docente=docente.id_docente,
                nombres="Docente",
                apellidos="de Prueba",
                activo=True,
            )
            session.add(usuario_profesor)

        usuario_jefa = session.exec(
            select(Usuario).where(Usuario.correo == JEFA_CORREO)
        ).first()
        if usuario_jefa is None:
            usuario_jefa = Usuario(
                id_rol=roles["Jefa_Profesores"].id_rol,
                correo=JEFA_CORREO,
                password_hash=hash_password(JEFA_PASSWORD),
                id_docente=None,
                nombres="Jefa",
                apellidos="de Prueba",
                activo=True,
            )
            session.add(usuario_jefa)

        usuario_directivo = session.exec(
            select(Usuario).where(Usuario.correo == DIRECTIVO_CORREO)
        ).first()
        if usuario_directivo is None:
            usuario_directivo = Usuario(
                id_rol=roles["Directivos"].id_rol,
                correo=DIRECTIVO_CORREO,
                password_hash=hash_password(DIRECTIVO_PASSWORD),
                id_docente=None,
                nombres="Directivo",
                apellidos="de Prueba",
                activo=True,
            )
            session.add(usuario_directivo)

        session.commit()

        print("Seed completado.")
        print(f"Profesor         -> correo: {PROFESOR_CORREO}  password: {PROFESOR_PASSWORD}")
        print(f"Jefa_Profesores  -> correo: {JEFA_CORREO}  password: {JEFA_PASSWORD}")
        print(f"Directivos       -> correo: {DIRECTIVO_CORREO}  password: {DIRECTIVO_PASSWORD}")


if __name__ == "__main__":
    seed()