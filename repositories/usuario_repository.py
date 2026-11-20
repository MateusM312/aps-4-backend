from sqlalchemy.orm import Session
from models import UsuarioModel

def salvar_usuario(db:Session, usuario: UsuarioModel) -> UsuarioModel:
    db.add(usuario)
    db.commit()
    db.refresh(usuario)
    return usuario

def buscar_usuario_por_email(db:Session, email:str) -> UsuarioModel | None:
    return db.query(UsuarioModel).filter(UsuarioModel.email == email).first()