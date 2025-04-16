from pydantic import BaseModel


class ImprendaBase(BaseModel):
    ano: int
    situacao: str
    valdiara: float
    valrest: float


class ImprendaCreate(ImprendaBase):
    pass


class ImprendaResponse(ImprendaBase):
    id_imprenda: int
    id_user: int
