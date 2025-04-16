from http import HTTPStatus

from fastapi import FastAPI

from backend_fastapi.router.dividasRouter import router as divida_router
from backend_fastapi.router.investimentoRouter import router as investimento_router
from backend_fastapi.router.metaRouter import router as meta_router
from backend_fastapi.router.patrimonioRouter import router as patrimonio_router
from backend_fastapi.router.usuarioRouter import router as usuario_router

app = FastAPI()


app.include_router(usuario_router, prefix='/Usuario', tags=['Usuario'])
app.include_router(meta_router, prefix='/Meta', tags=['Meta'])
app.include_router(investimento_router, prefix='/Investimento', tags=['Investimento'])
app.include_router(patrimonio_router, prefix='/Patrimonio', tags=['Patrimonio'])
app.include_router(divida_router, prefix='/Dividas', tags={'Dividas'})


@app.get('/', status_code=HTTPStatus.OK)
def read_root():
    return {'message': 'Bem Vindo a API do SCFF'}
