from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from backend_fastapi.database import get_session
from backend_fastapi.schema.enums import CategoriaDespesaEnum
from backend_fastapi.schema.gastoMensalSchema import GastoMensalComparativo, GastoMensalResponse
from backend_fastapi.security import get_current_user

router = APIRouter()


@router.get('/Categoria', response_model=list[GastoMensalResponse])
async def get_gasto_mensal_categoria(categ: CategoriaDespesaEnum, db: AsyncSession = Depends(get_session), current_user=Depends(get_current_user)):
    query = text(
        """
        SELECT ano, mes, categoria_despesa, total_gasto, percentual
        FROM gasto_mensal_por_categoria
        WHERE id_user = :id_user AND categoria_despesa = :categoria_despesa
        """
    )

    result = await db.execute(query.bindparams(id_user=current_user.id_user, categoria_despesa=categ))
    raw_gastos = result.fetchall()

    return [GastoMensalResponse.model_validate(gasto._mapping) for gasto in raw_gastos]


@router.get('/Mensal', response_model=list[GastoMensalResponse])
async def get_gasto_mensal(ano: int, mes: int, db: AsyncSession = Depends(get_session), current_user=Depends(get_current_user)):
    query = text(
        """
        SELECT ano, mes, categoria_despesa, total_gasto, percentual
        FROM gasto_mensal_por_categoria
        WHERE id_user = :id_user AND mes = :mes AND ano = :ano
        """
    )

    result = await db.execute(query.bindparams(id_user=current_user.id_user, mes=mes, ano=ano))
    raw_gastos = result.fetchall()

    return [GastoMensalResponse.model_validate(gasto._mapping) for gasto in raw_gastos]


@router.get('/Comparativo/Categoria', response_model=list[GastoMensalComparativo])
async def get_gasto_comparativo_categoria(
    categ: CategoriaDespesaEnum, db: AsyncSession = Depends(get_session), current_user=Depends(get_current_user)
):
    query = text(
        """
        SELECT ano, mes, categoria_despesa, orcamento_previsto, gasto_real, diferenca, percentual_gasto
        FROM comparativo_orcamento_gasto
        WHERE id_user = :id_user AND categoria_despesa = :categoria_despesa
        """
    )

    result = await db.execute(query.bindparams(id_user=current_user.id_user, categoria_despesa=categ))
    raw_gastos = result.fetchall()

    return [GastoMensalComparativo.model_validate(gasto._mapping) for gasto in raw_gastos]


@router.get('/Comparativo/Mensal', response_model=list[GastoMensalComparativo])
async def get_gasto_comparativo_mensal(ano: int, mes: int, db: AsyncSession = Depends(get_session), current_user=Depends(get_current_user)):
    query = text(
        """
        SELECT ano, mes, categoria_despesa, orcamento_previsto, gasto_real, diferenca, percentual_gasto
        FROM comparativo_orcamento_gasto
        WHERE id_user = :id_user AND mes = :mes AND ano = :ano
        """
    )

    result = await db.execute(query.bindparams(id_user=current_user.id_user, mes=mes, ano=ano))
    raw_gastos = result.fetchall()

    return [GastoMensalComparativo.model_validate(gasto._mapping) for gasto in raw_gastos]
