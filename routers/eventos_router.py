from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from schema.eventos_model import EventoCreate, EventoResponse
from schema.participantes_model import ParticipanteResponse
from services import eventos_services

router = APIRouter(prefix="/eventos", tags=["Eventos"])

# Cadastrar evento
# POST /eventos
# Deverá receber os dados do evento em formato JSON e retornar o evento cadastrado.
@router.post("/", response_model=EventoResponse, status_code=201)
def cadastrar_evento(evento: EventoCreate, db: Session = Depends(get_db)):
    return eventos_services.criar_evento(db, evento)


# Listar eventos
# GET /eventos
# Deverá retornar a lista de eventos cadastrados.
@router.get("/", response_model=list[EventoResponse])
def listar_eventos(db: Session = Depends(get_db)):
    return eventos_services.listar_eventos(db)


# Consultar evento
# GET /eventos/{id}
# Deverá retornar os dados de um evento específico.
# Caso o evento não exista, a API deverá retornar um código HTTP adequado e uma
# mensagem informando o problema.
@router.get("/{id}", response_model=EventoResponse)
def consultar_evento(id: int, db: Session = Depends(get_db)):
    return eventos_services.buscar_evento(db, id)


# Atualizar evento
# PUT /eventos/{id}
# Deverá permitir a atualização dos dados de um evento existente.
@router.put("/{id}", response_model=EventoResponse)
def atualizar_evento(id: int, evento: EventoCreate, db: Session = Depends(get_db)):
    return eventos_services.editar_evento(db, id, evento)


# Excluir evento
# DELETE /eventos/{id}
# Deverá remover um evento existente.
@router.delete("/{id}")
def excluir_evento(id: int, db: Session = Depends(get_db)):
    eventos_services.excluir_evento(db, id)
    return {"mensagem": "Evento removido"}


# Inscrever participante:
# POST /eventos/{evento_id}/inscricoes/{participante_id}
@router.post("/{evento_id}/inscricoes/{participante_id}", status_code=201)
def inscrever_participante(evento_id: int, participante_id: int, db: Session = Depends(get_db)):
    return eventos_services.inscrever(db, evento_id, participante_id)


# Listar participantes inscritos em um evento
# GET /eventos/{evento_id}/inscricoes
@router.get("/{evento_id}/inscricoes", response_model=list[ParticipanteResponse])
def listar_inscritos(evento_id: int, db:Session = Depends(get_db)):
    return eventos_services.listar_inscritos(db, evento_id)