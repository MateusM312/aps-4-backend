from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from auth import exigir_admin
from database import get_db
from models.model import UsuarioModel
from schema.relatorio_schema import OcupacaoEventoResponse, CategoriaResponse, CursoResponse
from services import relatorio_services

# Todos os relatórios são só para administrador
router = APIRouter(prefix="/relatorios", tags=["Relatórios"])


@router.get("/eventos/ocupacao", response_model=list[OcupacaoEventoResponse])
def relatorio_por_ocupacao(db: Session = Depends(get_db), usuario_logado: UsuarioModel = Depends(exigir_admin)):
    return relatorio_services.buscar_por_capacidade(db)


@router.get("/eventos/categorias", response_model=list[CategoriaResponse])
def relatorio_por_categoria(db: Session = Depends(get_db), usuario_logado: UsuarioModel = Depends(exigir_admin)):
    return relatorio_services.relatorio_categorias(db)


@router.get("/participantes/cursos", response_model=list[CursoResponse])
def relatorio_por_curso(db: Session = Depends(get_db), usuario_logado: UsuarioModel = Depends(exigir_admin)):
    return relatorio_services.relatorio_cursos(db)