from datetime import date

from pydantic import BaseModel, Field, field_validator, model_validator


class MetaBase(BaseModel):
    descri: str = Field(..., min_length=3)
    data_inicio: date
    data_fim: date
    valor: float

    @model_validator(mode='after')
    def verificar_datas(cls, values):
        if values.data_fim <= values.data_inicio:
            raise ValueError('data_fim não pode ser anterior ou igual a data_inicio')
        return values

    @field_validator('valor')
    def verificar_valor(cls, v):
        if v < 0:
            raise ValueError('O valor não pode ser menor do que 0')
        return v


class MetaCreate(MetaBase):
    pass


class MetaResponse(BaseModel):
    id_meta: int
    descri: str
    data_inicio: date
    data_fim: date
    valor: float
    id_user: int
