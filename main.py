import os

from fastapi import FastAPI
from routers import eventos_router, participantes_routers, usuario_router, auth_router, relatorios_router
from database import Base, engine, SessionLocal
from models.model import UsuarioModel
import auth

Base.metadata.create_all(bind=engine)


def preparar_usuarios():
    """Roda uma vez na inicialização:
    1) troca os perfis antigos (ADMIN/CLIENTE) pelos novos (administrador/usuario);
    2) cria o administrador inicial, se ADMIN_EMAIL e ADMIN_SENHA estiverem definidos."""
    db = SessionLocal()
    try:
        db.query(UsuarioModel).filter(UsuarioModel.perfil == "ADMIN").update({"perfil": auth.PERFIL_ADMIN})
        db.query(UsuarioModel).filter(UsuarioModel.perfil == "CLIENTE").update({"perfil": auth.PERFIL_USUARIO})
        db.commit()

        email = os.getenv("ADMIN_EMAIL")
        senha = os.getenv("ADMIN_SENHA")
        nome = os.getenv("ADMIN_NOME", "Administrador")
        if email and senha:
            ja_existe = db.query(UsuarioModel).filter(UsuarioModel.email == email).first()
            if ja_existe is None:
                admin = UsuarioModel(
                    nome=nome,
                    email=email,
                    senha_hash=auth.gerar_hash_senha(senha),
                    perfil=auth.PERFIL_ADMIN,
                )
                db.add(admin)
                db.commit()
    finally:
        db.close()


preparar_usuarios()

app = FastAPI(title="Gerenciamento de eventos acadêmicos - Santana & Mendes")


@app.get("/")
def raiz():
    return {"Alerta de Sucesso": "Hello World!"}


app.include_router(eventos_router.router)
app.include_router(participantes_routers.router)
app.include_router(usuario_router.router)
app.include_router(auth_router.router)
app.include_router(relatorios_router.router)