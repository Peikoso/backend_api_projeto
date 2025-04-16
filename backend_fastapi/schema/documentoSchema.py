from typing import Optional

from pydantic import BaseModel


class DocumentoBase(BaseModel):
    nome_arquivo: str
    tipo_arquivo: Optional[str] = None
    arquivo: bytes
    data_upload: Optional[str] = None


class DocumentoCreate(DocumentoBase):
    pass


class DocumentoResponse(DocumentoBase):
    id: int
    idmov: int
