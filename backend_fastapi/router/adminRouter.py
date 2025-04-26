from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import text
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from backend_fastapi.database import get_session
from backend_fastapi.schema.adminSchema import AdminCreate, AdminUser, CategoriaCreate, CategoriaResponse, NoticiaCreate, NoticiaResponse
from backend_fastapi.schema.usuarioSchema import Token
from backend_fastapi.security import create_access_token, get_admin, get_password_hash, verify_password

router = APIRouter()


@router.get('/Categoria', response_model=list[CategoriaResponse])
async def get_categorias(db: AsyncSession = Depends(get_session), admin=Depends(get_admin)):
    query = text('SELECT * FROM categoria')
    result = await db.execute(query)

    raw_categorias = result.fetchall()

    return [CategoriaResponse.model_validate(categoria._mapping) for categoria in raw_categorias]


@router.post('/Categoria')
async def post_categoria(categoria: CategoriaCreate, db: AsyncSession = Depends(get_session), admin=Depends(get_admin)):
    try:
        query = text(
            """
        INSERT INTO categoria (nome)
        VALUES (:nome)
        RETURNING id;
        """
        )

        result = await db.execute(query.bindparams(nome=categoria.nome))

        await db.commit()
        result = result.scalar()

        return {'Message': 'Categoria criada', 'id': result}

    except IntegrityError as e:
        if 'categoria_nome_key' in str(e.orig):
            raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail='Esta categoria já existe. Escolha um diferente.')

        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail='Erro de integridade no banco de dados.')


@router.put('/Categoria/{id}')
async def update_categoria(id: int, categoria: CategoriaCreate, db: AsyncSession = Depends(get_session), admin=Depends(get_admin)):
    try:
        query = text(
            """
            UPDATE categoria
            SET nome = :nome
            WHERE id = :id
            RETURNING id;
            """
        )
        result = await db.execute(query.bindparams(nome=categoria.nome, id=id))
        await db.commit()

        updated_id = result.scalar()

        if updated_id is None:
            raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='Categoria não encontrada')

        return {'Message': 'Categoria atualizada com sucesso', 'id': updated_id}

    except IntegrityError as e:
        if 'categoria_nome_key' in str(e.orig):
            raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail='Esta categoria já existe. Escolha um nome diferente.')

        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail='Erro de integridade no banco de dados.')


@router.delete('/Categoria/{id}')
async def delete_categoria(id: int, db: AsyncSession = Depends(get_session), admin=Depends(get_admin)):
    try:
        query = text('DELETE FROM categoria WHERE id = :id RETURNING id')
        result = await db.execute(query.bindparams(id=id))
        await db.commit()

        deleted_id = result.scalar()

        if deleted_id is None:
            raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='Categoria não encontrada')

        return {'Message': 'Categoria deletada com sucesso', 'id': deleted_id}
    except IntegrityError as e:
        if 'noticia_categoria_id_fkey' in str(e.orig):
            raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail='Não pode deletar a categoria de uma noticia existente')

        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail='Erro de integridade no banco de dados.')


@router.get('/Noticia', response_model=list[NoticiaResponse])
async def get_noticia(db: AsyncSession = Depends(get_session), admin=Depends(get_admin)):
    query = text('SELECT * FROM noticia')
    result = await db.execute(query)

    raw_noticias = result.fetchall()

    return [NoticiaResponse.model_validate(noticia._mapping) for noticia in raw_noticias]


@router.get('/Noticia/{id}', response_model=NoticiaResponse)
async def get_noticia_by_id(id: int, db: AsyncSession = Depends(get_session), admin=Depends(get_admin)):
    query = text('SELECT * FROM noticia WHERE id = :id')
    result = await db.execute(query.bindparams(id=id))

    raw_noticia = result.fetchone()

    if not raw_noticia:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=(f'Noticia ID: {id} não encontrada'))

    return NoticiaResponse.model_validate(raw_noticia._mapping)


@router.post('/Noticia')
async def create_noticia(noticia: NoticiaCreate, db: AsyncSession = Depends(get_session), admin=Depends(get_admin)):
    categoria = await db.execute(text('SELECT * FROM categoria WHERE id = :id').bindparams(id=noticia.categoria_id))
    raw_categoria = categoria.fetchone()

    if not raw_categoria:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=('Categoria não encontrada'))

    query = text(
        """
    INSERT INTO noticia (titulo, autor, conteudo, imagem, categoria_id)
    VALUES (:titulo, :autor, :conteudo, :imagem, :categoria_id)
    RETURNING id
    """
    )

    query = query.bindparams(titulo=noticia.titulo, autor=noticia.autor, conteudo=noticia.conteudo, imagem=None, categoria_id=noticia.categoria_id)

    result = await db.execute(query)
    await db.commit()

    return {'Message': 'Noticia criado', 'id': result.scalar()}


@router.put('/Noticia/{id}')
async def update_noticia(id: int, noticia: NoticiaCreate, db: AsyncSession = Depends(get_session), admin=Depends(get_admin)):
    categoria = await db.execute(text('SELECT * FROM categoria WHERE id = :id').bindparams(id=noticia.categoria_id))
    raw_categoria = categoria.fetchone()

    if not raw_categoria:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=('Categoria não encontrada'))

    query = text(
        """
        UPDATE noticia
        SET titulo = :titulo, autor = :autor, conteudo = :conteudo, imagem = :imagem, categoria_id = :categoria_id
        WHERE id = :id
        RETURNING id
        """
    )

    query = query.bindparams(
        id=id, titulo=noticia.titulo, autor=noticia.autor, conteudo=noticia.conteudo, imagem=None, categoria_id=noticia.categoria_id
    )

    result = await db.execute(query)
    await db.commit()

    updated_id = result.scalar()

    if updated_id is None:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=f'Notícia ID: {id} não encontrada')

    return {'Message': 'Notícia atualizada com sucesso', 'id': updated_id}


@router.delete('/Noticia/{id}')
async def delete_noticia(id: int, db: AsyncSession = Depends(get_session), admin=Depends(get_admin)):
    query = text('DELETE FROM noticia WHERE id = :id RETURNING id')
    result = await db.execute(query.bindparams(id=id))
    await db.commit()

    deleted_id = result.scalar()

    if deleted_id is None:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=f'Notícia ID: {id} não encontrada')

    return {'Message': 'Notícia deletada com sucesso', 'id': deleted_id}


@router.post('/Cadastro', status_code=HTTPStatus.CREATED)
async def create_usuario(admin: AdminCreate, db: AsyncSession = Depends(get_session), token: str = Depends(get_admin)):
    try:
        query = text(
            """
            INSERT INTO user_admin (admin_login, senha)
            VALUES (:admin_login, :senha)
            RETURNING id_admin;
            """
        )
        query = query.bindparams(admin_login=admin.admin_login, senha=get_password_hash(admin.senha))

        result = await db.execute(query)
        await db.commit()

        return {'Message': 'Admin criado', 'id_admin': result.scalar()}

    except IntegrityError as e:
        if 'user_admin_admin_login_key' in str(e.orig):
            raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail='Este admin_login já está em uso. Escolha um diferente.')

        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail='Erro de integridade no banco de dados.')


@router.delete('/{id_admin}', status_code=HTTPStatus.OK)
async def delete_admin(id_admin: int, db: AsyncSession = Depends(get_session), token: str = Depends(get_admin)):
    query = text('DELETE FROM user_admin WHERE id_admin = :id_admin RETURNING id_admin;')
    result = await db.execute(query.bindparams(id_admin=id_admin))
    deleted_id = result.scalar()

    if deleted_id is None:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='Admin não encontrado.')

    await db.commit()
    return {'message': 'Admin deletado com sucesso', 'id_admin': deleted_id}


@router.post('/token', response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_session),
):
    result = await db.execute(text('SELECT * FROM user_admin WHERE admin_login = :admin_login').bindparams(admin_login=form_data.username))
    raw_admin = result.fetchone()

    if not raw_admin:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Incorrect login or password',
        )

    admin = AdminUser.model_validate(raw_admin._mapping)

    if not admin or not verify_password(form_data.password, admin.senha):
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Incorrect login or password',
        )
    access_token = create_access_token(data={'sub': admin.admin_login})

    return {'access_token': access_token, 'token_type': 'Bearer'}
