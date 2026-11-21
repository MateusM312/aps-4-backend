import os
from datetime import datetime, timedelta, timezone

import jwt
from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from database import get_db
from models.model import UsuarioModel

# A chave vem de uma variável de ambiente (nunca escrita no código)
SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    raise RuntimeError("Defina a variável de ambiente SECRET_KEY antes de iniciar a API.")

ALGORITHM = "HS256"
EXPIRACAO_TOKEN_MINUTOS = 60

PERFIL_ADMIN = "administrador"
PERFIL_USUARIO = "usuario"

MSG_CREDENCIAIS = "Não foi possível validar as credenciais."

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# auto_error=False: quando não vem token, nós mesmos devolvemos 401
security = HTTPBearer(auto_error=False)


def gerar_hash_senha(senha: str) -> str:
    return pwd_context.hash(senha)


def verificar_senha(senha: str, hash_senha: str) -> bool:
    return pwd_context.verify(senha, hash_senha)


def criar_token(usuario_id: int) -> str:
    payload = {
        "sub": str(usuario_id),  # o padrão do JWT pede string
        "exp": datetime.now(timezone.utc) + timedelta(minutes=EXPIRACAO_TOKEN_MINUTOS),
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def decodificar_token(token: str) -> int:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return int(payload["sub"])
    except (jwt.InvalidTokenError, KeyError, ValueError):
        # InvalidTokenError já cobre token expirado e token inválido
        raise HTTPException(
            status_code=401,
            detail=MSG_CREDENCIAIS,
            headers={"WWW-Authenticate": "Bearer"},
        )


def get_usuario_atual(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
) -> UsuarioModel:
    if credentials is None:
        raise HTTPException(
            status_code=401,
            detail=MSG_CREDENCIAIS,
            headers={"WWW-Authenticate": "Bearer"},
        )

    usuario_id = decodificar_token(credentials.credentials)

    usuario = db.query(UsuarioModel).filter(UsuarioModel.id == usuario_id).first()
    if usuario is None:
        raise HTTPException(
            status_code=401,
            detail=MSG_CREDENCIAIS,
            headers={"WWW-Authenticate": "Bearer"},
        )

    return usuario


def exigir_admin(usuario: UsuarioModel = Depends(get_usuario_atual)) -> UsuarioModel:
    if usuario.perfil != PERFIL_ADMIN:
        raise HTTPException(
            status_code=403,
            detail="Apenas usuários administradores podem realizar essa ação",
        )
    return usuario