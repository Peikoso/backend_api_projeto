from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class AdminCreate(BaseModel):
    admin_login: str
    senha: str


class AdminUser(AdminCreate):
    id_admin: int


class NoticiaCreate(BaseModel):
    titulo: str
    autor: str
    conteudo: str
    categoria_id: int


class NoticiaResponse(NoticiaCreate):
    imagem: Optional[str]
    criado_em: datetime
    id: int


class Imagem(BaseModel):
    imagem: Optional[str]


class CategoriaCreate(BaseModel):
    nome: str


class CategoriaResponse(CategoriaCreate):
    id: int
