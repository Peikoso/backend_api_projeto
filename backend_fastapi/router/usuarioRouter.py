from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import text
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from backend_fastapi.database import get_session
from backend_fastapi.schema.usuarioSchema import Token, UsuarioBase, UsuarioCreate, UsuarioResponse
from backend_fastapi.security import create_access_token, get_current_user, get_password_hash, optional_oauth2_scheme, verify_password

router = APIRouter()


@router.get('/', response_model=UsuarioResponse)
async def get_usuarios(db: AsyncSession = Depends(get_session), current_user=Depends(get_current_user)):
    query = text('SELECT id_user, nome, email, login FROM usuario WHERE id_user = :id_user')
    result = await db.execute(query.bindparams(id_user=current_user.id_user))
    raw_user = result.fetchone()
    return UsuarioResponse.model_validate(raw_user._mapping)


@router.post('/Cadastro', status_code=HTTPStatus.CREATED)
async def create_usuario(usuario: UsuarioCreate, db: AsyncSession = Depends(get_session), token: str = Depends(optional_oauth2_scheme)):
    if token:
        raise HTTPException(status_code=HTTPStatus.FORBIDDEN, detail='Usuários autenticados não podem criar nova conta.')

    try:
        query = text(
            """
            INSERT INTO usuario (nome, email, login, senha)
            VALUES (:nome, :email, :login, :senha)
            RETURNING id_user;
            """
        )
        query = query.bindparams(nome=usuario.nome, email=usuario.email, login=usuario.login, senha=get_password_hash(usuario.senha))

        result = await db.execute(query)
        await db.commit()

        return {'Message': 'Usuario criado', 'id_user': result.scalar()}

    except IntegrityError as e:
        if 'usuario_login_key' in str(e.orig) or 'usuario_email_key' in str(e.orig):
            raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail='Este login ou e-mail já está em uso. Escolha um diferente.')

        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail='Erro de integridade no banco de dados.')


@router.put('/', response_model=UsuarioResponse)
async def update_usuario(usuario: UsuarioCreate, db: AsyncSession = Depends(get_session), current_user=Depends(get_current_user)):
    try:
        query = text(
            """
            UPDATE usuario
            SET nome = :nome, email = :email, login = :login, senha = :senha
            WHERE id_user = :id_user
            RETURNING id_user, nome, email, login;
            """
        )
        query = query.bindparams(
            nome=usuario.nome, email=usuario.email, login=usuario.login, senha=get_password_hash(usuario.senha), id_user=current_user.id_user
        )

        result = await db.execute(query)
        raw_usuario = result.fetchone()

        await db.commit()

        return UsuarioResponse.model_validate(raw_usuario._mapping)

    except IntegrityError as e:
        if 'usuario_login_key' in str(e.orig) or 'usuario_email_key' in str(e.orig):
            raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail='Este login ou e-mail já está em uso. Escolha um diferente.')

        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail='Erro de integridade no banco de dados.')


@router.delete('/', status_code=HTTPStatus.OK)
async def delete_usuario(db: AsyncSession = Depends(get_session), current_user=Depends(get_current_user)):
    query = text('DELETE FROM usuario WHERE id_user = :id_user RETURNING id_user')
    result = await db.execute(query.bindparams(id_user=current_user.id_user))
    deleted_id = result.scalar()

    if not deleted_id:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='Usuario não encontrado')

    await db.commit()

    return {'message': 'Usuario deletado'}


@router.post('/token', response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_session),
):
    result = await db.execute(text('SELECT * FROM usuario WHERE login = :login').bindparams(login=form_data.username))
    raw_usuario = result.fetchone()

    if not raw_usuario:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Incorrect login or password',
        )

    usuario = UsuarioBase.model_validate(raw_usuario._mapping)

    if not usuario or not verify_password(form_data.password, usuario.senha):
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Incorrect login or password',
        )
    access_token = create_access_token(data={'sub': usuario.login})

    return {'access_token': access_token, 'token_type': 'Bearer'}
