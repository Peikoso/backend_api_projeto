from datetime import date

from pydantic import BaseModel, Field, field_validator, model_validator

from backend_fastapi.schema.Enums import CategoriaMetaEnum


class MetaBase(BaseModel):
    categ: CategoriaMetaEnum
    descri: str = Field(..., min_length=3, max_length=200)
    data_inicio: date
    data_fim: date
    valor: float
    valor_reservado: float

    @model_validator(mode='after')
    def verificar_datas(cls, values):
        if values.data_fim <= values.data_inicio:
            raise ValueError('data_fim não pode ser anterior ou igual a data_inicio')
        return values

    @field_validator('valor', 'valor_reservado')
    def verificar_valor(cls, v):
        if v < 0:
            raise ValueError('O valor não pode ser menor do que 0')
        return v

    @model_validator(mode='after')
    def verificar_valor_reservado(cls, values):
        if values.valor_reservado > values.valor:
            raise ValueError('O valor Reservado não pode exceder o valor da meta')
        return values
    
    
class MetaCreate(MetaBase):
    pass


class MetaResponse(BaseModel):
    categ: CategoriaMetaEnum
    descri: str
    data_inicio: date
    data_fim: date
    valor: float
    valor_reservado: float
    id_meta: int
    id_user: int
