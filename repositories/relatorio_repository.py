from sqlalchemy import func
from sqlalchemy.orm import Session
from models.model import EventoModel, InscricaoModel, ParticipantesModel

def ocupacao_por_evento(db: Session):
    return (
        db.query(
            EventoModel.id,
            EventoModel.titulo,
            EventoModel.capacidade,
            func.count(InscricaoModel.id).label("total_inscritos"), # conta todos os id e cria uma coluna chamada total_inscritos para ela
        )
        .outerjoin(InscricaoModel, InscricaoModel.evento_id == EventoModel.id)
        .group_by(EventoModel.id, EventoModel.titulo, EventoModel.capacidade)
        .order_by(EventoModel.id)
        .all()
    )

def ocupacao_por_categoria(db: Session):
    inscricoes_por_evento = (
        db.query(
            InscricaoModel.evento_id.label("evento_id"),
            func.count(InscricaoModel.id).label("qtd"), 
        )
        .group_by(InscricaoModel.evento_id)
        .subquery() 
    )
    return(
        db.query(
            EventoModel.categoria,
            func.count(EventoModel.categoria).label("total_eventos"),
            func.coalesce(func.sum(EventoModel.capacidade), 0).label("capacidade_total"),
            func.coalesce(func.sum(inscricoes_por_evento.c.qtd), 0).label("total_inscricoes"),
        )
        .outerjoin(inscricoes_por_evento, inscricoes_por_evento.c.evento_id == EventoModel.id)
        .group_by(EventoModel.categoria)
        .order_by(EventoModel.categoria)
        .all()
    )

def participacao_por_curso(db: Session):
    return (
        db.query(
            ParticipantesModel.curso,
            func.count(func.distinct(ParticipantesModel.id)).label("total_participantes"),
            func.count(InscricaoModel.id).label("total_inscricoes"),
        )
        .outerjoin(InscricaoModel, InscricaoModel.participante_id == ParticipantesModel.id)
        .group_by(ParticipantesModel.curso)
        .order_by(ParticipantesModel.curso)
        .all()
    )
