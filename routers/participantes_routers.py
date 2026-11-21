from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from auth import get_usuario_atual
from database import get_db
from models.model import UsuarioModel
from schema.participantes_model import ParticipanteCreate, ParticipanteResponse
from services import participantes_service

router = APIRouter(prefix="/participantes", tags=["Participante"])


# Cadastrar participante (precisa estar autenticado)
# POST /participantes
@router.post("/", response_model=ParticipanteResponse, status_code=201)
def cadastrar_participante(
    dados: ParticipanteCreate,
    db: Session = Depends(get_db),
    usuario_logado: UsuarioModel = Depends(get_usuario_atual),
):
    return participantes_service.criar_participante(db, dados)


# Listar participantes (precisa estar autenticado)
# GET /participantes
@router.get("/", response_model=list[ParticipanteResponse])
def listar_participantes(
    db: Session = Depends(get_db),
    usuario_logado: UsuarioModel = Depends(get_usuario_atual),
):
    return participantes_service.listar_participantes(db)


# Consultar participante (precisa estar autenticado)
# GET /participantes/{id}
@router.get("/{id}", response_model=ParticipanteResponse)
def consultar_participante(
    id: int,
    db: Session = Depends(get_db),
    usuario_logado: UsuarioModel = Depends(get_usuario_atual),
):
    return participantes_service.buscar_participante(db, id)


# Atualizar participante (precisa estar autenticado)
# PUT /participantes/{id}
# Obs.: o corpo agora é ParticipanteCreate (antes era ParticipanteResponse, que exigia "id" no JSON)
@router.put("/{id}", response_model=ParticipanteResponse)
def atualizar_participantes(
    id: int,
    dado: ParticipanteCreate,
    db: Session = Depends(get_db),
    usuario_logado: UsuarioModel = Depends(get_usuario_atual),
):
    return participantes_service.editar_participante(db, id, dado)


# Excluir participante (precisa estar autenticado)
# DELETE /participantes/{id}
@router.delete("/{id}")
def excluir_participantes(
    id: int,
    db: Session = Depends(get_db),
    usuario_logado: UsuarioModel = Depends(get_usuario_atual),
):
    participantes_service.excluir_participante(db, id)
    return {"mensagem": "Participante removido"}