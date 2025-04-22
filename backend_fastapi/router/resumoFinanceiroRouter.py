from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from backend_fastapi.database import get_session
from backend_fastapi.schema.resumoFinanceiroSchema import resumoFinanceiroMensalResponse, resumoFinanceiroOutrosResponse
from backend_fastapi.security import get_current_user

router = APIRouter()


@router.get('/', response_model=list[resumoFinanceiroMensalResponse])
async def get_resumos_financeiros(db: AsyncSession = Depends(get_session), current_user=Depends(get_current_user)):
    query = text(
        """
        SELECT mes, ano, total_movimentacoes, total_receitas, total_despesas, saldo
        FROM resumo_financeiro_mensal
        WHERE id_user = :id_user
        """
    )

    result = await db.execute(query.bindparams(id_user=current_user.id_user))
    raw_resumos = result.fetchall()

    return [resumoFinanceiroMensalResponse.model_validate(resumo._mapping) for resumo in raw_resumos]


@router.get('/Mensal/{mes}/{ano}', response_model=resumoFinanceiroMensalResponse)
async def get_resumo_financeiro_mensal(mes: int, ano: int, db: AsyncSession = Depends(get_session), current_user=Depends(get_current_user)):
    query = text(
        """
        SELECT mes, ano, total_movimentacoes, total_receitas, total_despesas, saldo
        FROM resumo_financeiro_mensal
        WHERE id_user = :id_user AND mes = :mes AND ano = :ano
        """
    )

    result = await db.execute(query.bindparams(id_user=current_user.id_user, mes=mes, ano=ano))
    raw_resumo = result.fetchone()

    if not raw_resumo:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='Resumo Financeiro Mensal para esse periodo não existe')

    return resumoFinanceiroMensalResponse.model_validate(raw_resumo._mapping)


@router.get('/Outros', response_model=resumoFinanceiroOutrosResponse)
async def get_resumo_financeiro_outros(db: AsyncSession = Depends(get_session), current_user=Depends(get_current_user)):
    query = text(
        """
        SELECT progresso_medio_metas, total_patrimonio, total_investido_final, total_proventos, total_dividas
        FROM resumo_financeiro_outros
        WHERE id_user = :id_user
        """
    )

    result = await db.execute(query.bindparams(id_user=current_user.id_user))
    raw_resumo = result.fetchone()

    if not raw_resumo:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='Resumo Financeiro Fixo para esse periodo não existe')

    return resumoFinanceiroOutrosResponse.model_validate(raw_resumo._mapping)
