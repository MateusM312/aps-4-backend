# EVENTOS SERVICES
from fastapi import HTTPException
from sqlalchemy.orm import Session

from models.model import EventoModel, InscricaoModel
from repositories import eventos_repository, participantes_repository

def criar_evento(db: Session, dados) -> EventoModel:
    evento = EventoModel(**dados.model_dump())
    return eventos_repository.salvar(db, evento)

def listar_eventos(db: Session) -> list[EventoModel]:
    return eventos_repository.listar(db)

def buscar_evento(db: Session, evento_id:int) -> EventoModel:
    evento = eventos_repository.buscar_por_id(db, evento_id)
    if evento is None:
        raise HTTPException(status_code=404, detail="Evento não encontrado")
    return evento

def editar_evento(db:Session, evento_id:int, dados) -> EventoModel:
    evento = buscar_evento(db, evento_id)
    return eventos_repository.atualizar(db, evento, dados)

def excluir_evento(db: Session, evento_id: int) -> None:
    evento = buscar_evento(db, evento_id)
    eventos_repository.remover(db, evento)

def inscrever(db: Session, evento_id:int, participante_id:int):
    evento = buscar_evento(db, evento_id)

    participante = participantes_repository.buscar_por_id(db, participante_id)
    if participante is None:
        raise HTTPException(status_code=404, detail="Participante não encontrado")
    if eventos_repository.buscar_inscricao(db, evento_id, participante_id):
        raise HTTPException(status_code=409, detail="Participante já inscrito neste evento")
    if eventos_repository.contar_inscritos(db, evento_id) >= evento.capacidade:
        raise HTTPException(status_code=409, detail="Evento sem vagas disponíveis")

    inscricao = InscricaoModel(evento_id=evento_id, participante_id=participante_id)
    eventos_repository.inscrever(db, inscricao)
    return {"Alerta": "Inscrição realizada com sucesso"}

def listar_inscritos(db: Session, evento_id:int):
    buscar_evento(db, evento_id) # validar
    return eventos_repository.listar_inscritos(db, evento_id)