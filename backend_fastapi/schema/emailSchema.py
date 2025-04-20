import re

from pydantic import BaseModel, EmailStr, Field, field_validator


class ContactForm(BaseModel):
    nome: str
    email: EmailStr
    menssagem: str = Field(..., min_length=5)

    @field_validator('nome')
    def validar_nome(cls, v):
        if not re.match(r'^[A-Za-zÀ-ÿ\s]+$', v):
            raise ValueError('O nome deve conter apenas letras e espaços')
        return v
