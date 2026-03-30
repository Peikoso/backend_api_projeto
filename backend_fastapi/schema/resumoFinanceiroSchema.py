from typing import Optional

from pydantic import BaseModel


class ResumoFinanceiroMensalResponse(BaseModel):
    mes: Optional[int] = None
    ano: Optional[int] = None
    total_movimentacoes: int
    total_receitas: float
    total_despesas: float
    saldo: float


class ResumoFinanceiroOutrosResponse(BaseModel):
    progresso_medio_metas: float
    total_patrimonio: float
    total_investido_final: float
    total_proventos: float
    total_dividas: float
