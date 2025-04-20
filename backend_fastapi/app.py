from http import HTTPStatus

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend_fastapi.router.dividasRouter import router as divida_router
from backend_fastapi.router.gastoRouter import router as gasto_router
from backend_fastapi.router.investimentoRouter import router as investimento_router
from backend_fastapi.router.metaRouter import router as meta_router
from backend_fastapi.router.movimentacaoRouter import router as movimentacao_router
from backend_fastapi.router.orcamentoMensalRouter import router as orcamentoMensal_router
from backend_fastapi.router.patrimonioRouter import router as patrimonio_router
from backend_fastapi.router.resumoFinanceiroRouter import router as resumo_financeiro_router
from backend_fastapi.router.usuarioRouter import router as usuario_router
from backend_fastapi.router.emailRouter import router as email_router


app = FastAPI()

origins = [
    'http://localhost:5173',
    'http://127.0.0.1:5173',
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)


app.include_router(usuario_router, prefix='/Usuario', tags=['Usuario'])
app.include_router(meta_router, prefix='/Meta', tags=['Meta'])
app.include_router(investimento_router, prefix='/Investimento', tags=['Investimento'])
app.include_router(patrimonio_router, prefix='/Patrimonio', tags=['Patrimonio'])
app.include_router(divida_router, prefix='/Dividas', tags={'Dividas'})
app.include_router(orcamentoMensal_router, prefix='/OrcamentoMensal', tags=['Orcamento Mensal'])
app.include_router(movimentacao_router, prefix='/Movimentacao', tags=['Movimetacao'])
app.include_router(resumo_financeiro_router, prefix='/ResumoFinanceiro', tags=['Resumo Financeiro'])
app.include_router(gasto_router, prefix='/Gasto', tags=['Gasto'])
app.include_router(email_router, prefix='/EnviarEmail', tags=['Enviar Email'])


@app.get('/', status_code=HTTPStatus.OK)
def read_root():
    return {'message': 'Bem Vindo a API do SCFF'}
