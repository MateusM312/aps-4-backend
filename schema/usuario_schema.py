from enum import Enum

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator


class Perfil(str, Enum):
    ADMINISTRADOR = "administrador"
    USUARIO = "usuario"


class UsuarioCreate(BaseModel):
    # Não existe campo "perfil": quem se cadastra é sempre "usuario".
    # Se alguém mandar "perfil" no JSON, o Pydantic simplesmente ignora.
    nome: str = Field(min_length=1)
    email: EmailStr
    senha: str = Field(min_length=6, description="minimo 6 caracteres")

    @field_validator("nome")
    @classmethod
    def nome_nao_pode_ser_vazio(cls, valor: str) -> str:
        valor = valor.strip()
        if not valor:
            raise ValueError("O nome não pode ser vazio")
        return valor


class UsuarioResponse(BaseModel):
    id: int
    nome: str
    email: EmailStr
    perfil: Perfil
    model_config = ConfigDict(from_attributes=True)


class LoginRequest(BaseModel):
    email: EmailStr
    senha: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"