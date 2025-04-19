from pydantic import BaseModel

from backend_fastapi.schema.enums import CategoriaDespesaEnum


class GastoMensalResponse(BaseModel):
    ano: int
    mes: int
    categoria_despesa: CategoriaDespesaEnum
    total_gasto: float
    percentual: float


class GastoMensalComparativo(BaseModel):
    ano: int
    mes: int
    categoria_despesa: CategoriaDespesaEnum
    orcamento_previsto: float
    gasto_real: float
    diferenca: float
    percentual_gasto: float
