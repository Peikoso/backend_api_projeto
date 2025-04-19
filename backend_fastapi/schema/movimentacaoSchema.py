from typing import Optional

from pydantic import BaseModel, Field, model_validator

from backend_fastapi.schema.enums import CategoriaDespesaEnum, CategoriaReceitaEnum, TipoMovimentacaoEnum


class MovimentacaoBase(BaseModel):
    valor: float = Field(..., ge=0)
    descricao: str = Field(..., min_length=3)
    mes: int = Field(..., ge=1, le=12)
    ano: int = Field(..., ge=2025, le=2100)
    tipo_mov: TipoMovimentacaoEnum
    categoria_receita: Optional[CategoriaReceitaEnum] = None
    categoria_despesa: Optional[CategoriaDespesaEnum] = None

    @model_validator(mode='after')
    def check_tipo_mov(cls, values):
        tipo_mov = values.tipo_mov
        categoria_receita = values.categoria_receita
        categoria_despesa = values.categoria_despesa

        if tipo_mov == 'receita' and categoria_despesa is not None:
            raise ValueError('Categoria despesa deve ser None para movimentações do tipo receita')
        if tipo_mov == 'despesa' and categoria_receita is not None:
            raise ValueError('Categoria receita deve ser None para movimentação do tipo despesa')

        return values


class MovimentacaoCreate(MovimentacaoBase):
    pass


class MovimentacaoResponse(BaseModel):
    valor: float
    descricao: str
    mes: int
    ano: int
    tipo_mov: TipoMovimentacaoEnum
    categoria_receita: Optional[CategoriaReceitaEnum] = None
    categoria_despesa: Optional[CategoriaDespesaEnum] = None
    idmov: int
    id_user: int
