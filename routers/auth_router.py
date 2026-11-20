from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from auth import get_usuario_atual
from schema.usuario_schema import LoginRequest, TokenResponse, UsuarioResponse
from database import get_db
from services import usuario_services
from models.model import UsuarioModel

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/login", response_model=TokenResponse)
def login(dados: LoginRequest, db: Session = Depends(get_db)):
    token = usuario_services.autenticar(db, dados)
    return TokenResponse(access_token=token)

@router.get("/me", response_model=UsuarioResponse)
def me(usuario: UsuarioModel = Depends(get_usuario_atual)):
    return usuario