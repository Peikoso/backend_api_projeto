from datetime import date

from pydantic import BaseModel, Field, field_validator, model_validator


class InvestimentoBase(BaseModel):
    categ: str = Field(..., min_length=3)
    valorini: float
    valorfim: float
    datainicio: date
    datafim: date
    empresa: str = Field(..., min_length=3)

    @field_validator('valorini', 'valorfim')
    def validar_positivo(cls, v):
        if v < 0:
            raise ValueError('O campo não pode ser um número negativo')
        return v

    @model_validator(mode='after')
    def verificar_datas(cls, values):
        if values.datafim <= values.datainicio:
            raise ValueError('data_fim não pode ser anterior ou igual a data_inicio')
        return values


class InvestimentoCreate(InvestimentoBase):
    pass


class InvestimentoResponse(BaseModel):
    categ: str
    valorini: float
    valorfim: float
    datainicio: date
    datafim: date
    empresa: str
    proventos: float = 0.0
    cod: int
    id_user: int
