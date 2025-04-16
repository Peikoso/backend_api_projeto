from typing import Optional

from pydantic import BaseModel

from backend_fastapi.schema.Enums import CategoriaDespesaEnum, CategoriaReceitaEnum, TipoMovimentacaoEnum


class MovimentacaoBase(BaseModel):
    valor: float
    descricao: str
    data: str
    tipo_mov: TipoMovimentacaoEnum
    categoria_receita: Optional[CategoriaReceitaEnum] = None
    categoria_despesa: Optional[CategoriaDespesaEnum] = None
    data_renov: Optional[str] = None


class MovimentacaoCreate(MovimentacaoBase):
    pass


class MovimentacaoResponse(MovimentacaoBase):
    idmov: int
    id_user: int
