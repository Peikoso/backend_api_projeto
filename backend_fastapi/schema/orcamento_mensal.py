from pydantic import BaseModel, Field

from backend_fastapi.schema.Enums import CategoriaDespesaEnum


class OrcamentoBase(BaseModel):
    mes: int = Field(..., ge=1, le=12)
    ano: int = Field(..., ge=2025, le=2100)
    categoria: CategoriaDespesaEnum
    valor_previsto: float = Field(..., ge=0)


class OrcamentoCreate(OrcamentoBase):
    pass

    
class OrcamentoResponse(BaseModel):
    mes: int
    ano: int
    categoria: CategoriaDespesaEnum
    valor_previsto: float
    id_orcamento: int
    id_user: int
