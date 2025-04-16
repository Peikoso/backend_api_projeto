from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from backend_fastapi.database import get_session
from backend_fastapi.schema.dividasSchema import DividasCreate, DividasResponse
from backend_fastapi.security import get_current_user

router = APIRouter()


@router.get('/', response_model=list[DividasResponse])
async def get_dividas(db: AsyncSession = Depends(get_session)):
    query = text('SELECT * FROM dividas')
    result = await db.execute(query)
    raw_dividas = result.fetchall()

    return [DividasResponse.model_validate(divida._mapping) for divida in raw_dividas]


@router.get('/{cod_divid}', response_model=DividasResponse)
async def get_divida_by_cod_divid(cod_divid: int, db: AsyncSession = Depends(get_session)):
    query = text('SELECT * FROM dividas WHERE cod_divid = :cod_divid')
    result = await db.execute(query.bindparams(cod_divid=cod_divid))
    raw_divida = result.fetchone()

    if not raw_divida:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=f'Divida com cod_divid: {cod_divid} não encontrada')

    return DividasResponse.model_validate(raw_divida._mapping)


@router.post('/')
async def create_divida(divida: DividasCreate, db: AsyncSession = Depends(get_session), current_user=Depends(get_current_user)):
    query = text(
        """
    INSERT INTO dividas (natureza, situacao, data_inicio, data_final, valor, id_user)
    VALUES (:natureza, :situacao, :data_inicio, :data_final, :valor, :id_user)
    RETURNING cod_divid
    """
    )

    query = query.bindparams(
        natureza=divida.natureza,
        situacao=divida.situacao,
        data_inicio=divida.data_inicio,
        data_final=divida.data_final,
        valor=divida.valor,
        id_user=current_user.id_user,
    )

    result = await db.execute(query)
    cod_divid = result.scalar()

    if not cod_divid:
        HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail='Error ao criar a divida')

    await db.commit()

    return {'message': f'Divida com cod_divid: {cod_divid} criada'}


@router.put('/{cod_divid}')
async def update_divida(cod_divid: int, divida: DividasCreate, db: AsyncSession = Depends(get_session), current_user=Depends(get_current_user)):
    query = text(
    """
    UPDATE dividas
    SET natureza = :natureza, situacao = :situacao, data_inicio = :data_inicio, data_final = :data_final, valor = :valor
    WHERE id_user = :id_user AND cod_divid = :cod_divid
    RETURNING *
    """
    )

    query = query.bindparams(
        natureza=divida.natureza,
        situacao=divida.situacao,
        data_inicio=divida.data_inicio,
        data_final=divida.data_final,
        valor=divida.valor,
        id_user=current_user.id_user,
        cod_divid=cod_divid
    )

    result = await db.execute(query)
    raw_divida = result.fetchone()

    if not raw_divida:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=f'Divida com cod: {cod_divid} não encontrada')

    await db.commit()

    return DividasResponse.model_validate(raw_divida._mapping)

@router.delete('/{cod_divid}')
async def delete_divida(cod_divid: int, db: AsyncSession = Depends(get_session), current_user = Depends(get_current_user)):
    query = text('DELETE FROM dividas WHERE id_user = :id_user AND cod_divid = :cod_divid RETURNING cod_divid')
    result = await db.execute(query.bindparams(id_user=current_user.id_user, cod_divid=cod_divid))
    deleted_cod = result.scalar()
    
    if not deleted_cod:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=f'Divida com cod: {cod_divid} não encontrada')
    
    await db.commit()
    
    return{'message': f'Divida com cod: {cod_divid} deletada'}

