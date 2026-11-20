from fastapi import HTTPException
from sqlalchemy.orm import Session
from repositories import relatorio_repository

def buscar_por_capacidade(db: Session) -> list[dict]:
    resultado = []
    for i in relatorio_repository.ocupacao_por_evento(db):
        percentual = (i.total_inscritos / i.capacidade * 100) if i.capacidade else 0.0
        resultado.append({
            "evento_id" : i.id,
            "titulo": i.titulo,
            "capacidade": i.capacidade,
            "total_inscritos": i.total_inscritos,
            "vagas_disponiveis": max(i.capacidade - i.total_inscritos, 0),
            "percentual_ocupacao": round(percentual, 2),
        })
    return resultado

def relatorio_categorias(db: Session) -> list[dict]:
    return [
        {
            "categoria": l.categoria,
            "total_eventos": l.total_eventos,
            "capacidade_total": int(l.capacidade_total),
            "total_inscricoes": int(l.total_inscricoes),
        }
        for l in relatorio_repository.ocupacao_por_categoria(db)
    ]

def relatorio_cursos(db: Session) -> list[dict]:
    return [
        {
            "curso": l.curso,
            "total_participantes": l.total_participantes,
            "total_inscricoes": l.total_inscricoes,
        }
        for l in relatorio_repository.participacao_por_curso(db)
    ]