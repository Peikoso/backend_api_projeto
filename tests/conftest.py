import pytest
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock
import datetime

from backend_fastapi.app import app
from backend_fastapi.database import get_session
from backend_fastapi.security import get_current_user, get_admin
from backend_fastapi.schema.usuarioSchema import UsuarioBase
from backend_fastapi.schema.adminSchema import AdminUser

class MockResult:
    def __init__(self, data=None, scalar_val=None):
        self._data = data or []
        self._scalar = scalar_val

    def fetchall(self):
        class Row:
            def __init__(self, d):
                self._mapping = d
        return [Row(d) for d in self._data]

    def fetchone(self):
        res = self.fetchall()
        return res[0] if res else None

    def scalar(self):
        return self._scalar


class MockSession:
    async def execute(self, query, *args, **kwargs):
        q = str(query).lower()
        if 'select' in q:
            if 'admin' in q:
                return MockResult([{'id_admin': 1, 'admin_login': 'admin', 'senha': 'hashed_password'}], 1)
            elif 'usuario' in q:
                return MockResult([{'id_user': 1, 'nome': 'User', 'email': 'user@user.com', 'login': 'user', 'senha': 'hashed_password'}], 1)
            elif 'categoria' in q:
                return MockResult([{'id': 1, 'nome': 'Lazer'}], 1)
            elif 'noticia' in q:
                return MockResult([{'id':1, 'titulo':'Teste', 'imagem':None, 'autor':'Auto', 'conteudo':'Cont', 'categoria_id':1}], 1)
            elif 'imagem' in q:
                return MockResult([{'id':1, 'imagem_url':'abc', 'imagem_path':'abc'}], 1)
            elif 'movimentacao' in q:
                return MockResult([{
                    'idmov': 1, 'tipo_mov': 'RECEITA', 'id_user': 1, 'data': datetime.date.today(),
                    'valor': 100.0, 'descricao': 'T', 'categoria': 'T', 'conta': 'T', 'comprovante_pdf': None
                }], 1)
            elif 'patrimonio' in q:
                return MockResult([{
                    'idbem': 1, 'tipo_bem': 'T', 'nome_bem': 'T', 'valor_estimado': 100.0,
                    'data_aquisicao': datetime.date.today(), 'descricao': 'T', 'id_user':1
                }], 1)
            elif 'investimento' in q:
                return MockResult([{
                    'cod': 1, 'id_user':1, 'nome': 'T', 'descricao':'T', 'tipo_inv': 'T', 'valor_mensal':10,
                    'valor_investido': 100, 'meta_inv': 1000, 'tempo_estimado': 10, 'rentabilidade': 0.1,
                    'data_inicio': datetime.date.today()
                }], 1)
            elif 'meta' in q:
                return MockResult([{
                    'id_meta': 1, 'id_user': 1, 'nome_meta': 'T', 'valor_total': 1000, 
                    'saldo_atual': 100, 'valor_mes': 10, 'prazo_meses': 10
                }], 1)
            elif 'dividas' in q:
                return MockResult([{
                    'cod_divid': 1, 'id_user': 1, 'nome': 'T', 'descricao':'T',
                    'vencimento': datetime.date.today(), 'status_divid': 'PAGO', 
                    'valor_original': 100, 'juros': 0.1, 'valor_pago': 0
                }], 1)
            elif 'orcamento_mensal' in q:
                return MockResult([{
                    'id_orcamento': 1, 'id_user': 1, 'mes': 1, 'ano': 2025,
                    'categoria': 'LAZER', 'valor_previsto': 100
                }], 1)
            
            # fallback
            return MockResult([{'id':1}], 1)
        else:
             # inserts/deletes/updates
             return MockResult([], 1)
             
    async def commit(self):
        pass

async def override_get_session_mock():
    yield MockSession()

def override_get_current_user():
    return UsuarioBase(id_user=1, nome='Teste', email='teste@test.com', login='teste', senha='abc')

def override_get_admin():
    return AdminUser(id_admin=1, admin_login='admin', senha='abc')

app.dependency_overrides[get_session] = override_get_session_mock
app.dependency_overrides[get_current_user] = override_get_current_user
app.dependency_overrides[get_admin] = override_get_admin

@pytest.fixture
def client():
    with TestClient(app) as test_client:
        yield test_client
