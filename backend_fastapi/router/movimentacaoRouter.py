import os
import shutil
from datetime import datetime
from http import HTTPStatus
from pathlib import Path
from typing import Optional

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from fastapi.responses import FileResponse
from pydantic import Json
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from backend_fastapi.database import get_session
from backend_fastapi.schema.movimentacaoSchema import MovimentacaoCreate, MovimentacaoResponse
from backend_fastapi.security import get_current_user

router = APIRouter()


UPLOAD_DIR = 'comprovantes_pdfs/'

os.makedirs(UPLOAD_DIR, exist_ok=True)

MAX_FILE_SIZE = 10 * 1024 * 1024


@router.get('/', response_model=list[MovimentacaoResponse])
async def get_movimentacoes(db: AsyncSession = Depends(get_session), current_user=Depends(get_current_user)):
    query = text(
        'SELECT valor, descricao, mes, ano, tipo_mov, categoria_receita, categoria_despesa, idmov, id_user FROM movimentacao WHERE id_user = :id_user'
    )
    result = await db.execute(query.bindparams(id_user=current_user.id_user))
    raw_movimentacoes = result.fetchall()

    return [MovimentacaoResponse.model_validate(movimentacao._mapping) for movimentacao in raw_movimentacoes]


@router.get('/{idmov}', response_model=MovimentacaoResponse)
async def get_movimentacao_by_id(idmov: int, db: AsyncSession = Depends(get_session), current_user=Depends(get_current_user)):
    query = text('SELECT * FROM movimentacao WHERE id_user = :id_user AND idmov = :idmov')
    result = await db.execute(query.bindparams(id_user=current_user.id_user, idmov=idmov))
    raw_movimentacao = result.fetchone()

    if not raw_movimentacao:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=f'Movimentação com ID: {idmov} não encontrada')

    return MovimentacaoResponse.model_validate(raw_movimentacao._mapping)


@router.get('/download_comprovante/{idmov}')
async def get_pdf_downlaod(idmov: int, db: AsyncSession = Depends(get_session), current_user=Depends(get_current_user)):
    query = text('SELECT comprovante_pdf FROM movimentacao WHERE idmov = :idmov AND id_user = :id_user')
    result = await db.execute(query.bindparams(idmov=idmov, id_user=current_user.id_user))

    row = result.fetchone()

    if row is None or row[0] is None:
        return {'PDF não encontrado'}

    comprovante_pdf = row[0]

    pdf_path = Path(comprovante_pdf)

    if pdf_path.exists():
        return FileResponse(
            path=pdf_path, media_type='application/pdf', filename=pdf_path.name, headers={'Content-Disposition': f'inline; filename={pdf_path.name}'}
        )

    return {'PDF não encontrado'}


@router.post('/')
async def create_movimentacao(
    movimentacao: Json[MovimentacaoCreate],
    comprovante_pdf: Optional[UploadFile] = File(None),
    db: AsyncSession = Depends(get_session),
    current_user=Depends(get_current_user),
):
    pdf_path = None

    if comprovante_pdf:
        if comprovante_pdf.content_type != 'application/pdf':
            raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail='O arquivo não é um PDF.')

        file_size = comprovante_pdf.size
        if file_size > MAX_FILE_SIZE:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail=f'O arquivo é muito grande. O tamanho máximo permitido é {MAX_FILE_SIZE / (1024 * 1024)} MB.',
            )

        pdf_filename = 'movimentacao'
        pdf_filename = f'{datetime.now().strftime("%Y%m%d%H%M%S%f")}_{pdf_filename}'
        pdf_path = os.path.join(UPLOAD_DIR, pdf_filename)

        with open(pdf_path, 'wb') as f:
            shutil.copyfileobj(comprovante_pdf.file, f)

    query = text(
        """
        INSERT INTO movimentacao(valor, descricao, mes, ano, tipo_mov, categoria_receita, categoria_despesa, comprovante_pdf, id_user)
        VALUES(:valor, :descricao, :mes, :ano, :tipo_mov, :categoria_receita, :categoria_despesa, :comprovante_pdf, :id_user)
        RETURNING idmov
        """
    )

    query = query.bindparams(
        valor=movimentacao.valor,
        descricao=movimentacao.descricao,
        mes=movimentacao.mes,
        ano=movimentacao.ano,
        tipo_mov=movimentacao.tipo_mov,
        categoria_receita=movimentacao.categoria_receita,
        categoria_despesa=movimentacao.categoria_despesa,
        comprovante_pdf=pdf_path,
        id_user=current_user.id_user,
    )

    result = await db.execute(query)
    idmov = result.scalar()

    if not idmov:
        raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail='Error ao criar movimentação')

    await db.commit()

    return {'message': f'Movimentação com ID: {idmov} criada com sucesso'}


@router.put('/{idmov}', response_model=MovimentacaoResponse)
async def update_movimentacao(
    movimentacao: MovimentacaoCreate, idmov: int, db: AsyncSession = Depends(get_session), current_user=Depends(get_current_user)
):
    query = text(
        """
        UPDATE movimentacao
        SET valor = :valor, descricao = :descricao, mes = :mes, ano = :ano,
        tipo_mov = :tipo_mov, categoria_receita = :categoria_receita,
        categoria_despesa = :categoria_despesa
        WHERE idmov = :idmov AND id_user = :id_user
        RETURNING *
        """
    )

    query = query.bindparams(
        valor=movimentacao.valor,
        descricao=movimentacao.descricao,
        mes=movimentacao.mes,
        ano=movimentacao.ano,
        tipo_mov=movimentacao.tipo_mov,
        categoria_receita=movimentacao.categoria_receita,
        categoria_despesa=movimentacao.categoria_despesa,
        idmov=idmov,
        id_user=current_user.id_user,
    )

    result = await db.execute(query)
    raw_movimentacao = result.fetchone()

    if not raw_movimentacao:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=f'Movimentação com ID: {idmov} não encontrada')

    await db.commit()

    return MovimentacaoResponse.model_validate(raw_movimentacao._mapping)


@router.put('/update_comprovante/{idmov}')
async def update_movimentacao_file(
    idmov: int, comprovante_pdf: Optional[UploadFile] = File(None), db: AsyncSession = Depends(get_session), current_user=Depends(get_current_user)
):
    query = text('SELECT comprovante_pdf FROM movimentacao WHERE idmov = :idmov AND id_user = :id_user')

    result_select = await db.execute(query.bindparams(idmov=idmov, id_user=current_user.id_user))
    pdf_path = result_select.scalar()

    if pdf_path:
        os.remove(pdf_path)
        pdf_path = None

    if comprovante_pdf:
        if comprovante_pdf.content_type != 'application/pdf':
            raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail='O arquivo não é um PDF.')

        file_size = comprovante_pdf.size
        if file_size > MAX_FILE_SIZE:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail=f'O arquivo é muito grande. O tamanho máximo permitido é {MAX_FILE_SIZE / (1024 * 1024)} MB.',
            )

        pdf_filename = 'movimentacao'
        pdf_filename = f'{datetime.now().strftime("%Y%m%d%H%M%S%f")}_{pdf_filename}'
        pdf_path = os.path.join(UPLOAD_DIR, pdf_filename)

    query = text(
        """
        UPDATE movimentacao
        SET comprovante_pdf = :comprovante_pdf
        WHERE idmov = :idmov AND id_user = :id_user
        RETURNING idmov
        """
    )

    query = query.bindparams(comprovante_pdf=pdf_path, idmov=idmov, id_user=current_user.id_user)

    result_update = await db.execute(query)
    id_movimentacao = result_update.scalar()

    if not id_movimentacao:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=f'Movimentacao com ID: {idmov} não encontrada')

    await db.commit()

    with open(pdf_path, 'wb') as f:
        shutil.copyfileobj(comprovante_pdf.file, f)

    return {'Comprovante atualizado com sucesso'}


@router.delete('/{idmov}')
async def delete_movimentacao(idmov: int, db: AsyncSession = Depends(get_session), current_user=Depends(get_current_user)):
    query = text('SELECT comprovante_pdf FROM movimentacao WHERE idmov = :idmov AND id_user = :id_user')
    result_select = await db.execute(query.bindparams(idmov=idmov, id_user=current_user.id_user))
    pdf_path = result_select.scalar()

    query = text('DELETE FROM movimentacao WHERE idmov = :idmov AND id_user = :id_user RETURNING idmov')
    result = await db.execute(query.bindparams(idmov=idmov, id_user=current_user.id_user))
    deleted_idmov = result.scalar()

    if not deleted_idmov:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=f'Movimentação com ID: {idmov} não encontrada')

    await db.commit()

    if pdf_path:
        os.remove(pdf_path)

    return {'message': f'Movimentacao com ID: {deleted_idmov} Deletada'}
