from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from backend_fastapi.database import get_session
from backend_fastapi.schema.patrimonioSchema import PatrimonioCreate, PatrimonioResponse
from backend_fastapi.security import get_current_user

router = APIRouter()


@router.get('/', response_model=list[PatrimonioResponse])
async def get_patrimonio(db: AsyncSession = Depends(get_session)):
    query = text('SELECT * FROM patrimonio')
    result = await db.execute(query)
    raw_patrimonio = result.fetchall()

    return [PatrimonioResponse.model_validate(patrimonio._mapping) for patrimonio in raw_patrimonio]


@router.get('/{idbem}', response_model=PatrimonioResponse)
async def get_patrimonio_idbem(idbem: int, db: AsyncSession = Depends(get_session)):
    query = text('SELECT * FROM patrimonio WHERE idbem = :idbem')
    result = await db.execute(query.bindparams(idbem=idbem))
    raw_patrimonio = result.fetchone()

    if not raw_patrimonio:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=f'Patrimonio ID:{idbem} não encontrado')

    return PatrimonioResponse.model_validate(raw_patrimonio._mapping)


@router.post('/')
async def create_patrimonio(patrimonio: PatrimonioCreate, db: AsyncSession = Depends(get_session), current_user=Depends(get_current_user)):
    query = text(
        """
        INSERT INTO patrimonio(nome, classe, valor, id_user)
        VALUES (:nome, :classe, :valor, :id_user)
        RETURNING idbem
        """
    )

    query = query.bindparams(nome=patrimonio.nome, classe=patrimonio.classe, valor=patrimonio.valor, id_user=current_user.id_user)
    result = await db.execute(query)
    idbem = result.scalar()

    if not idbem:
        HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail='Error ao criar a patrimonio')

    await db.commit()

    return {'message': f'Patrimonio ID: {idbem} criado'}


@router.put('/{idbem}')
async def update_patrimonio(
    patrimonio: PatrimonioCreate, idbem: int, db: AsyncSession = Depends(get_session), current_user=Depends(get_current_user)
):
    query = text(
        """
        UPDATE patrimonio
        SET nome = :nome, classe = :classe, valor = :valor
        WHERE idbem = :idbem AND id_user = :id_user
        RETURNING *
        """
    )

    query = query.bindparams(nome=patrimonio.nome, classe=patrimonio.classe, valor=patrimonio.valor, idbem=idbem, id_user=current_user.id_user)

    result = await db.execute(query)
    raw_patrimonio = result.fetchone()

    if not raw_patrimonio:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=f'patrimonio ID:{idbem} não encontrado')

    await db.commit()

    return PatrimonioResponse.model_validate(raw_patrimonio._mapping)


@router.delete('/{idbem}')
async def delete_patrimonio(idbem: int, db: AsyncSession = Depends(get_session), current_user=Depends(get_current_user)):
    query = text('DELETE FROM patrimonio WHERE idbem = :idbem AND id_user = :id_user RETURNING idbem').bindparams(
        idbem=idbem, id_user=current_user.id_user
    )
    result = await db.execute(query)
    deleted_idbem = result.scalar()

    if not deleted_idbem:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=f'patrimonio ID:{idbem} não encontrado')

    await db.commit()

    return {'message': f'patrimonio ID:{idbem} deletado com sucesso'}
