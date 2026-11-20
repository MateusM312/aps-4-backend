from fastapi import HTTPException
from sqlalchemy.orm import Session

import repositories.usuario_repository
import auth
from models.model import UsuarioModel
from schema.usuario_schema import UsuarioCreate, LoginRequest

repository = repositories.usuario_repository

# ----- Usuários / Login -----
def cadastrar_usuario(db: Session, dados: UsuarioCreate) -> UsuarioModel:
    if repository.buscar_usuario_por_email(db,dados.email):
        raise HTTPException(status_code=400, detail="E-mail já cadastrado")

    usuario = UsuarioModel(
        email=dados.email,
        nome=dados.nome,
        senha_hash=auth.gerar_hash_senha(dados.senha),
        perfil=dados.perfil.value
    )
    return repository.salvar_usuario(db, usuario)

def autenticar(db: Session, dados: LoginRequest) -> str:
    usuario = repository.buscar_usuario_por_email(db, dados.email)

    if usuario is None or not auth.verificar_senha(dados.senha, usuario.senha_hash):
        raise HTTPException(status_code=401,detail="E-mail ou senha inválidos")

    return auth.criar_token(usuario.email)