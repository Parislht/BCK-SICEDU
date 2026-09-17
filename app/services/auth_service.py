from typing import Optional

from sqlmodel import Session, select

from app.core.security import verify_password
from app.models.organizacion import Usuario


def authenticate_user(db: Session, correo: str, password: str) -> Optional[Usuario]:
    usuario = db.exec(select(Usuario).where(Usuario.correo == correo)).first()
    if usuario is None or not usuario.activo:
        return None
    if not verify_password(password, usuario.password_hash):
        return None
    return usuario
