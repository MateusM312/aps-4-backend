from pydantic import BaseModel, ConfigDict, EmailStr, Field

class ParticipanteCreate(BaseModel):
    nome: str = Field(min_length=1)
    email: EmailStr
    curso: str

class ParticipanteResponse(ParticipanteCreate):
    id:int
    model_config = ConfigDict(from_attributes=True)