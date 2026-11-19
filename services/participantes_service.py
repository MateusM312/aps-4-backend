# PARTICIPANTES SERVICES
from fastapi import HTTPException
from sqlalchemy.orm import Session

from models.model import ParticipantesModel
from repositories import eventos_repository, participantes_repository

def criar_participante(db: Session, dados):
    participante = ParticipantesModel(**dados.model_dump())
    return participantes_repository.salvar(db, participante)

def listar_participantes(db:Session):
    return participantes_repository.listar_participantes(db)

def buscar_participante(db:Session, participante_id:int):
    participante = participantes_repository.buscar_por_id(db, participante_id)
    if participante is None:
        raise HTTPException(status_code=404, detail="Participante não encontrado")
    return participante

def editar_participante(db:Session, participante_id:int, dados):
    participante = buscar_participante(db, participante_id)
    return participantes_repository.atualizar(db, participante, dados)

def excluir_participante(db: Session, participante_id:int):
    participante = buscar_participante(db, participante_id)
    participantes_repository.excluir(db, participante)
    return {"Alerta":"Participante excluido do Data Base"}