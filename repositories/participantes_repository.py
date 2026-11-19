# REPOSITORIO PARTICIPANTES

from sqlalchemy.orm import Session
from models.model import ParticipantesModel, EventoModel, InscricaoModel

def salvar(db: Session, participante: ParticipantesModel) -> ParticipantesModel:
    db.add(participante)
    db.commit()
    db.refresh(participante)
    return participante

def listar_participantes(db: Session):
    return db.query(ParticipantesModel).all()

def buscar_por_id(db: Session, id: int) -> ParticipantesModel | None:
    return db.query(ParticipantesModel).filter(ParticipantesModel.id == id).first()

def excluir(db: Session, participante: ParticipantesModel) -> None:
    db.delete(participante)
    db.commit()

def atualizar(db: Session, participante: ParticipantesModel, dados) -> ParticipantesModel:
    participante.nome = dados.nome
    participante.email = dados.email
    participante.curso = dados.curso
    db.commit()
    db.refresh(participante)
    return participante