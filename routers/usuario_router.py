from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from schema.usuario_schema import UsuarioCreate, UsuarioResponse
from database import get_db
from services import usuario_services

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])

@router.post("", response_model=UsuarioResponse, status_code=201)
def cadastrar_usuario(dados: UsuarioCreate, db: Session = Depends(get_db)):
    return usuario_services.cadastrar_usuario(db, dados)