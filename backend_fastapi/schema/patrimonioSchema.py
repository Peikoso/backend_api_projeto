from pydantic import BaseModel, Field, field_validator

from backend_fastapi.schema.Enums import ClassePatrimonioEnum


class PatrimonioBase(BaseModel):
    nome: str = Field(..., min_length=3)
    classe: ClassePatrimonioEnum = Field(..., min_length=3)
    valor: float

    @field_validator('valor')
    def valida_valor(cls, v):
        if v < 0:
            raise ValueError('O valor não pode ser menor que 0')
        return v


class PatrimonioCreate(PatrimonioBase):
    pass


class PatrimonioResponse(BaseModel):
    idbem: int
    nome: str
    classe: ClassePatrimonioEnum
    valor: float
    id_user: int
