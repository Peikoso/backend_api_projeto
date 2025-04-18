from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from backend_fastapi.database import get_session
from backend_fastapi.schema.metaSchema import MetaCreate, MetaResponse
from backend_fastapi.security import get_current_user

router = APIRouter()


@router.get('/', response_model=list[MetaResponse])
async def get_metas(db: AsyncSession = Depends(get_session), current_user = Depends(get_current_user)):
    query = text('SELECT * FROM meta WHERE id_user = :id_user')
    result = await db.execute(query.bindparams(id_user=current_user.id_user))
    raw_metas = result.fetchall()
    
    return [MetaResponse.model_validate(meta._mapping) for meta in raw_metas]


@router.get('/{id_meta}', response_model=MetaResponse)
async def get_meta_by_id(id_meta: int, db: AsyncSession = Depends(get_session), current_user = Depends(get_current_user)):
    query = text('SELECT * FROM meta WHERE id_meta = :id_meta AND id_user = :id_user')
    result = await db.execute(query.bindparams(id_meta=id_meta, id_user=current_user.id_user))
    raw_meta = result.fetchone()
    if not raw_meta:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='Meta não encontrada')
    
    return MetaResponse.model_validate(raw_meta._mapping)


@router.post('/', status_code=HTTPStatus.CREATED)
async def create_meta(meta: MetaCreate, db: AsyncSession = Depends(get_session), current_user=Depends(get_current_user)):
    query = text(
        """
        INSERT INTO meta (categ, descri, data_inicio, data_fim, valor, valor_reservado, id_user)
        VALUES (:categ, :descri, :data_inicio, :data_fim, :valor, :valor_reservado, :id_user)
        RETURNING id_meta;
        """
    )

    query = query.bindparams(
        categ=meta.categ,
        descri=meta.descri,
        data_inicio=meta.data_inicio,
        data_fim=meta.data_fim,
        valor=meta.valor,
        valor_reservado=meta.valor_reservado,
        id_user=current_user.id_user,
    )

    result = await db.execute(query)
    id_meta = result.scalar()

    if not id_meta:
        HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail='Error ao criar a meta')

    await db.commit()
    return {'message': f'Meta com ID: {id_meta} criada'}


@router.put('/{id_meta}', response_model=MetaResponse)
async def update_meta(id_meta: int, meta: MetaCreate, db: AsyncSession = Depends(get_session), current_user=Depends(get_current_user)):
    query = text(
        """
        UPDATE meta
        SET categ = :categ, descri = :descri, data_inicio = :data_inicio, data_fim = :data_fim, valor = :valor, valor_reservado = :valor_reservado
        WHERE id_user = :id_user AND id_meta = :id_meta
        RETURNING *;
        """
    )
    result = await db.execute(
        query.bindparams(
            categ=meta.categ,
            descri=meta.descri,
            data_inicio=meta.data_inicio,
            data_fim=meta.data_fim,
            valor=meta.valor,
            valor_reservado=meta.valor_reservado,
            id_user=current_user.id_user,
            id_meta=id_meta,
        )
    )

    raw_meta = result.fetchone()

    if not raw_meta:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=f'Meta ID: {id_meta} nao encontrada')

    await db.commit()

    return MetaResponse.model_validate(raw_meta._mapping)


@router.delete('/{id_meta}')
async def delete_meta(id_meta: int, db: AsyncSession = Depends(get_session), current_user=Depends(get_current_user)):
    query = text('DELETE FROM meta WHERE id_meta = :id_meta AND id_user = :id_user RETURNING id_meta')
    result = await db.execute(query.bindparams(id_meta=id_meta, id_user=current_user.id_user))
    deleted_id = result.scalar()

    if not deleted_id:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=f'Meta ID: {id_meta} não encontrada')

    await db.commit()

    return {'message': f'Meta ID: {deleted_id} deletada com sucesso'}
