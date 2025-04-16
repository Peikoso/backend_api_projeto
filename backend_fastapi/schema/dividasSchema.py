from datetime import date

from pydantic import BaseModel, Field, field_validator, model_validator

from backend_fastapi.schema.Enums import SituacaoDividaEnum


class DividasBase(BaseModel):
    natureza: str = Field(..., min_length=3)
    situacao: SituacaoDividaEnum
    data_inicio: date
    data_final: date
    valor: float

    @field_validator('valor')
    def validar_valor(cls, v):
        if v < 0:
            raise ValueError('O valor não pode ser menor que 0')
        return v

    @model_validator(mode='after')
    def verificar_datas(cls, values):
        if values.data_final <= values.data_inicio:
            raise ValueError('data_fim não pode ser anterior ou igual a data_inicio')
        return values


class DividasCreate(DividasBase):
    pass


class DividasResponse(BaseModel):
    natureza: str
    situacao: SituacaoDividaEnum
    data_inicio: date
    data_final: date
    valor: float
    cod_divid: int
    id_user: int
