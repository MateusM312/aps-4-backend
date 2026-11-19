# EVENTOS MODEL
from datetime import date, time
from pydantic import BaseModel, ConfigDict, Field

class EventoCreate(BaseModel):
    titulo: str = Field(min_length=1)
    descricao: str
    data: date
    horario: time
    local: str
    capacidade: int = Field(gt=0)
    categoria: str

class EventoResponse(EventoCreate):
    id:int
    model_config = ConfigDict(from_attributes=True)