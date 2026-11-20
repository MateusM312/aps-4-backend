from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from schema.usuario_schema import LoginRequest, TokenResponse
from database import get_db
from services import usuario_services

router = APIRouter(tags=["Login"])

@router.post("/login", response_model=TokenResponse)
def login(dados: LoginRequest, db: Session = Depends(get_db)):
    token = usuario_services.autenticar(db, dados)
    return TokenResponse(access_token=token)