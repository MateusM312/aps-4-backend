from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from auth import exigir_admin, get_usuario_atual
from database import get_db
from schema.eventos_model import EventoCreate, EventoResponse
from schema.participantes_model import ParticipanteResponse
from services import eventos_services
from models.model import UsuarioModel

router = APIRouter(prefix="/eventos", tags=["Eventos"])


# Cadastrar evento (somente administrador)
# POST /eventos
@router.post("/", response_model=EventoResponse, status_code=201)
def cadastrar_evento(evento: EventoCreate, db: Session = Depends(get_db), usuario_logado: UsuarioModel = Depends(exigir_admin)):
    return eventos_services.criar_evento(db, evento)


# Listar eventos (público)
# GET /eventos
@router.get("/", response_model=list[EventoResponse])
def listar_eventos(db: Session = Depends(get_db)):
    return eventos_services.listar_eventos(db)


# Consultar evento (público)
# GET /eventos/{id}
@router.get("/{id}", response_model=EventoResponse)
def consultar_evento(id: int, db: Session = Depends(get_db)):
    return eventos_services.buscar_evento(db, id)


# Atualizar evento (somente administrador)
# PUT /eventos/{id}
@router.put("/{id}", response_model=EventoResponse)
def atualizar_evento(id: int, evento: EventoCreate, db: Session = Depends(get_db), usuario_logado: UsuarioModel = Depends(exigir_admin)):
    return eventos_services.editar_evento(db, id, evento)


# Excluir evento (somente administrador)
# DELETE /eventos/{id}
@router.delete("/{id}")
def excluir_evento(id: int, db: Session = Depends(get_db), usuario_logado: UsuarioModel = Depends(exigir_admin)):
    eventos_services.excluir_evento(db, id)
    return {"mensagem": "Evento removido"}


# Inscrever participante (precisa estar autenticado)
# POST /eventos/{evento_id}/inscricoes/{participante_id}
@router.post("/{evento_id}/inscricoes/{participante_id}", status_code=201)
def inscrever_participante(evento_id: int, participante_id: int, db: Session = Depends(get_db), usuario_logado: UsuarioModel = Depends(get_usuario_atual)):
    return eventos_services.inscrever(db, evento_id, participante_id)


# Listar participantes inscritos em um evento (precisa estar autenticado)
# GET /eventos/{evento_id}/inscricoes
@router.get("/{evento_id}/inscricoes", response_model=list[ParticipanteResponse])
def listar_inscritos(evento_id: int, db: Session = Depends(get_db), usuario_logado: UsuarioModel = Depends(get_usuario_atual)):
    return eventos_services.listar_inscritos(db, evento_id)