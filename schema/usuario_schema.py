from pydantic import BaseModel, Field
from enum import Enum

class Perfil(str, Enum):
    ADMIN = "ADMIN"
    CLIENTE = "CLIENTE"

class UsuarioCreate(BaseModel):
    email: str
    nome: str = Field(min_length=1)
    senha: str = Field(min_length=6, description="minimo 6 caracteres")
    perfil: Perfil = Perfil.CLIENTE

class UsuarioResponse(BaseModel):
    id: int
    email: str
    perfil: Perfil

class LoginRequest(BaseModel):
    email:str
    senha:str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
