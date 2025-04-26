from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class AdminResponse(BaseModel):
    admin_login: str
    id_admin: int


class AdminCreate(BaseModel):
    admin_login: str = Field(..., min_length=3)
    senha: str = Field(..., min_length=3)


class AdminUser(AdminCreate):
    id_admin: int


class NoticiaCreate(BaseModel):
    titulo: str
    autor: str
    conteudo: str
    categoria_id: int


class NoticiaResponse(NoticiaCreate):
    imagem_id: Optional[int]
    criado_em: datetime
    id: int


class CategoriaCreate(BaseModel):
    nome: str


class CategoriaResponse(CategoriaCreate):
    id: int


class ImagemCreate(BaseModel):
    imagem_url: str


class ImagemResponse(ImagemCreate):
    id: int
