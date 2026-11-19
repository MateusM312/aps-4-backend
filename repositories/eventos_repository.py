#  EVENTOS REPOSITORY

from sqlalchemy.orm import Session
from models.model import ParticipantesModel, EventoModel, InscricaoModel

def salvar(db:Session, evento:EventoModel) -> EventoModel:
    db.add(evento)
    db.commit()
    db.refresh(evento)
    return evento

def listar(db:Session) -> list[EventoModel]:
    return db.query(EventoModel).all()

def buscar_por_id(db: Session, evento_id: int) -> EventoModel | None:
    return db.query(EventoModel).filter(EventoModel.id == evento_id).first()

def remover(db: Session, evento: EventoModel) -> None:
    db.delete(evento)
    db.commit()

def atualizar(db: Session, evento: EventoModel, dados) -> EventoModel:
    evento.titulo = dados.titulo
    evento.descricao = dados.descricao
    evento.data = dados.data
    evento.horario = dados.horario
    evento.local = dados.local
    evento.capacidade = dados.capacidade
    evento.categoria = dados.categoria
    db.commit()
    db.refresh(evento)
    return evento

def inscrever(db: Session, inscricao: InscricaoModel) -> InscricaoModel:
    db.add(inscricao)
    db.commit()
    db.refresh(inscricao)
    return inscricao

def listar_inscritos(db: Session, evento_id: int) -> list[ParticipantesModel]:
    return (
        db.query(ParticipantesModel)
        .join(InscricaoModel, InscricaoModel.participante_id == ParticipantesModel.id)
        .filter(InscricaoModel.evento_id == evento_id)
        .all()
    )

def contar_inscritos(db: Session, evento_id: int) -> int:
    return db.query(InscricaoModel).filter(InscricaoModel.evento_id == evento_id).count()

def buscar_inscricao(db: Session, evento_id: int, participante_id: int) -> InscricaoModel | None:
    return (db.query(InscricaoModel).filter(InscricaoModel.evento_id == evento_id, InscricaoModel.participante_id == participante_id,).first())