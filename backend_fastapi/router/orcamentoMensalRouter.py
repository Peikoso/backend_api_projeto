from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import text
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from backend_fastapi.database import get_session
from backend_fastapi.schema.orcamento_mensal import OrcamentoCreate, OrcamentoResponse
from backend_fastapi.security import get_current_user

router = APIRouter()


@router.get('/', response_model=list[OrcamentoResponse])
async def get_orcamentoMensal(
    ano: int = Query(..., ge=2025, le=2100, description='Ano desejado'),
    mes: int = Query(..., ge=1, le=12, description='Mês desejado (1 a 12)'),
    db: AsyncSession = Depends(get_session),
    current_user=Depends(get_current_user),
):
    query = text('SELECT * FROM orcamento_mensal WHERE id_user = :id_user AND ano = :ano AND mes = :mes')
    result = await db.execute(query.bindparams(id_user=current_user.id_user, ano=ano, mes=mes))
    raw_orcamentos = result.fetchall()

    return [OrcamentoResponse.model_validate(orcamento._mapping) for orcamento in raw_orcamentos]


@router.get('/{id_orcamento}', response_model=OrcamentoResponse)
async def get_orcamentoMensal_by_id(id_orcamento: int, db: AsyncSession = Depends(get_session), current_user=Depends(get_current_user)):
    query = text('SELECT * FROM orcamento_mensal WHERE id_orcamento = :id_orcamento AND id_user = :id_user')
    result = await db.execute(query.bindparams(id_orcamento=id_orcamento, id_user=current_user.id_user))
    raw_orcamento = result.fetchone()

    if not raw_orcamento:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=f'Orcamento Mensal com ID: {id_orcamento} não encontrado')

    return OrcamentoResponse.model_validate(raw_orcamento._mapping)


@router.post('/')
async def create_orcamentoMensal(orcamentoMensal: OrcamentoCreate, db: AsyncSession = Depends(get_session), current_user=Depends(get_current_user)):
    try:
        query = text(
            """
            INSERT INTO orcamento_mensal(mes, ano, categoria, valor_previsto, id_user)
            VALUES (:mes, :ano, :categoria, :valor_previsto, :id_user)
            RETURNING id_orcamento
            """
        )

        query = query.bindparams(
            mes=orcamentoMensal.mes,
            ano=orcamentoMensal.ano,
            categoria=orcamentoMensal.categoria,
            valor_previsto=orcamentoMensal.valor_previsto,
            id_user=current_user.id_user,
        )

        result = await db.execute(query)
        id_orcamento = result.scalar()

        await db.commit()

        return {'message': f'Orçamento Mensal com id: {id_orcamento} criado'}

    except IntegrityError as e:
        if 'unique_orcamento_usuario_mes_categoria' in str(e.orig):
            raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail='Já existe um orçamento mensal para este mês, ano e categoria.')

        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail='Erro de integridade no banco de dados.')


@router.put('/{id_orcamento}')
async def update_orcamentoMensal(
    id_orcamento: int, orcamentoMensal: OrcamentoCreate, db: AsyncSession = Depends(get_session), current_user=Depends(get_current_user)
):
    try:
        query = text(
            """
        UPDATE orcamento_mensal
        SET mes = :mes, ano = :ano, categoria = :categoria, valor_previsto = :valor_previsto
        WHERE id_user = :id_user AND id_orcamento = :id_orcamento
        RETURNING *
        """
        )

        query = query.bindparams(
            mes=orcamentoMensal.mes,
            ano=orcamentoMensal.ano,
            categoria=orcamentoMensal.categoria,
            valor_previsto=orcamentoMensal.valor_previsto,
            id_user=current_user.id_user,
            id_orcamento=id_orcamento,
        )

        result = await db.execute(query)
        raw_orcamento = result.fetchone()

        if not raw_orcamento:
            raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=f'Orçamento Mensal com ID: {id_orcamento} não encontrado')

        await db.commit()

        return OrcamentoResponse.model_validate(raw_orcamento._mapping)

    except IntegrityError as e:
        if 'unique_orcamento_usuario_mes_categoria' in str(e.orig):
            raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail='Já existe um orçamento mensal para este mês, ano e categoria.')

        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail='Erro de integridade no banco de dados.')


@router.delete('/{id_orcamento}')
async def delete_orcamentoMensal(id_orcamento: int, db: AsyncSession = Depends(get_session), current_user=Depends(get_current_user)):
    query = text('DELETE FROM orcamento_mensal WHERE id_orcamento = :id_orcamento AND id_user = :id_user RETURNING id_orcamento')
    result = await db.execute(query.bindparams(id_orcamento=id_orcamento, id_user=current_user.id_user))
    deleted_id_orcamento = result.scalar()

    if not deleted_id_orcamento:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=f'Orçamento Mensal com ID: {id_orcamento} não encontrado')

    await db.commit()
    return {'message': f'Orçamento Mensal com ID: {id_orcamento} deletado'}
