from pydantic import BaseModel


class resumoFinanceiroMensalResponse(BaseModel):
    mes: int
    ano: int
    total_movimentacoes: int
    total_receitas: float
    total_despesas: float
    saldo: float


class resumoFinanceiroOutrosResponse(BaseModel):
    progresso_medio_metas: float
    total_patrimonio: float
    total_investido_final: float
    total_proventos: float
    total_dividas: float
