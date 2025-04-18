from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from backend_fastapi.database import get_session
from backend_fastapi.schema.investimentoSchema import InvestimentoCreate, InvestimentoResponse
from backend_fastapi.security import get_current_user

router = APIRouter()


@router.get('/', response_model=list[InvestimentoResponse])
async def get_investimentos(db: AsyncSession = Depends(get_session), current_user = Depends(get_current_user)):
    query = text('SELECT * FROM investimento WHERE id_user = :id_user')
    result = await db.execute(query.bindparams(id_user=current_user.id_user))
    raw_investimentos = result.fetchall()

    return [InvestimentoResponse.model_validate(investimento._mapping) for investimento in raw_investimentos]


@router.get('/{cod}', response_model=InvestimentoResponse)
async def get_investimento_by_id(cod: int, db: AsyncSession = Depends(get_session), current_user = Depends(get_current_user)):
    query = text('SELECT * FROM investimento WHERE cod = :cod AND id_user = :id_user')
    result = await db.execute(query.bindparams(cod=cod, id_user=current_user.id_user))
    raw_investimento = result.fetchone()

    if not raw_investimento:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='investimento não encontrado')

    return InvestimentoResponse.model_validate(raw_investimento._mapping)


@router.post('/', status_code=HTTPStatus.CREATED)
async def create_investimento(investimento: InvestimentoCreate, db: AsyncSession = Depends(get_session), current_user=Depends(get_current_user)):
    query = text(
        """
    INSERT INTO investimento (categ, valorini, valorfim, datainicio, datafim, empresa, proventos, id_user)
    VALUES (:categ, :valorini, :valorfim, :datainicio, :datafim, :empresa, :proventos, :id_user)
    RETURNING cod
    """
    )

    query = query.bindparams(
        categ=investimento.categ,
        valorini=investimento.valorini,
        valorfim=investimento.valorfim,
        datainicio=investimento.datainicio,
        datafim=investimento.datafim,
        empresa=investimento.empresa,
        proventos=investimento.valorfim - investimento.valorini,
        id_user=current_user.id_user,
    )

    result = await db.execute(query)
    cod = result.scalar()

    if not cod:
        HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail='Error ao criar a patrimonio')

    await db.commit()

    return {'message': 'Investimento Criado', 'cod': result.scalar()}


@router.put('/{cod}', response_model=InvestimentoResponse)
async def update_investimento(
    cod: int, investimento: InvestimentoCreate, db: AsyncSession = Depends(get_session), current_user=Depends(get_current_user)
):
    query = text(
        """
    UPDATE investimento
    SET categ = :categ, valorini = :valorini, valorfim = :valorfim, datainicio = :datainicio,
    datafim = :datafim, empresa = :empresa, proventos = :proventos
    WHERE id_user = :id_user AND cod = :cod
    RETURNING *;
    """
    )

    query = query.bindparams(
        categ=investimento.categ,
        valorini=investimento.valorini,
        valorfim=investimento.valorfim,
        datainicio=investimento.datainicio,
        datafim=investimento.datafim,
        empresa=investimento.empresa,
        proventos=investimento.valorfim - investimento.valorini,
        id_user=current_user.id_user,
        cod=cod,
    )

    result = await db.execute(query)
    raw_investimento = result.fetchone()

    if not raw_investimento:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=f'Investimento cod: {cod} nao encontrado')

    await db.commit()

    return InvestimentoResponse.model_validate(raw_investimento._mapping)


@router.delete('/{cod}')
async def delete_investimento(cod: int, db: AsyncSession = Depends(get_session), current_user=Depends(get_current_user)):
    query = text('DELETE FROM investimento WHERE cod = :cod AND id_user = :id_user RETURNING cod')
    result = await db.execute(query.bindparams(cod=cod, id_user=current_user.id_user))
    deleted_cod = result.scalar()

    if not deleted_cod:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=f'investimento cod: {cod} não encontrado')

    await db.commit()

    return {'message': f'Investimento cod: {deleted_cod} deletado'}
