import re

from pydantic import BaseModel, EmailStr, Field, field_validator


class UsuarioBase(BaseModel):
    id_user: int
    nome: str
    email: EmailStr
    login: str
    senha: str


class UsuarioCreate(BaseModel):
    nome: str = Field(..., min_length=3)
    email: EmailStr
    login: str = Field(..., min_length=3)
    senha: str = Field(..., min_length=3)

    @field_validator('nome')
    def validar_nome(cls, v):
        if not re.match(r'^[A-Za-zÀ-ÿ\s]+$', v):
            raise ValueError('O nome deve conter apenas letras e espaços')
        return v

    @field_validator('login')
    def validar_login(cls, v):
        if re.match(r'^\d', v):
            raise ValueError('O login não pode começar com números.')
        return v


class UsuarioResponse(BaseModel):
    id_user: int
    nome: str
    email: EmailStr
    login: str


class Token(BaseModel):
    access_token: str
    token_type: str
