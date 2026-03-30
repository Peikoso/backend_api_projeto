import datetime

import pytest
from fastapi.testclient import TestClient

from backend_fastapi.app import app
from backend_fastapi.database import get_session
from backend_fastapi.schema.adminSchema import AdminUser
from backend_fastapi.schema.usuarioSchema import UsuarioBase
from backend_fastapi.security import get_current_user, get_admin


class MockResult:
    """Resultado simulado que imita o retorno de session.execute()."""

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


# Dados mock alinhados com os schemas atuais
MOCK_DATA = {
    'admin': [{'id_admin': 1, 'admin_login': 'admin', 'senha': 'hashed'}],
    'usuario': [{'id_user': 1, 'nome': 'User', 'email': 'user@user.com', 'login': 'user', 'senha': 'hashed'}],
    'categoria': [{'id': 1, 'nome': 'Lazer'}],
    'noticia': [{'id': 1, 'titulo': 'Teste', 'imagem': None, 'autor': 'Auto', 'conteudo': 'Conteudo', 'categoria_id': 1, 'criado_em': datetime.datetime.now()}],
    'imagem': [{'id': 1, 'imagem_url': 'http://test/img.png'}],
    'movimentacao': [{
        'idmov': 1, 'tipo_mov': 'receita', 'id_user': 1,
        'mes': 1, 'ano': 2025,
        'valor': 100.0, 'descricao': 'Salario',
        'categoria_receita': 'salario', 'categoria_despesa': None,
        'conta': 'Corrente', 'comprovante_pdf': None,
    }],
    'patrimonio': [{
        'idbem': 1, 'nome': 'Casa', 'classe': 'bem_imovel',
        'valor': 100000.0, 'id_user': 1,
    }],
    'investimento': [{
        'cod': 1, 'id_user': 1, 'categ': 'CDB', 'valorini': 1000.0,
        'valorfim': 2000.0, 'datainicio': datetime.date(2025, 1, 1),
        'datafim': datetime.date(2026, 1, 1), 'empresa': 'Banco',
        'proventos': 1000.0,
    }],
    'meta': [{
        'id_meta': 1, 'id_user': 1, 'categ': 'carro',
        'descri': 'Comprar carro', 'data_inicio': datetime.date(2025, 1, 1),
        'data_fim': datetime.date(2026, 1, 1),
        'valor': 50000.0, 'valor_reservado': 10000.0,
    }],
    'dividas': [{
        'cod_divid': 1, 'id_user': 1, 'natureza': 'Financiamento',
        'situacao': 'aberta', 'data_inicio': datetime.date(2025, 1, 1),
        'data_final': datetime.date(2026, 1, 1), 'valor': 1000.0,
    }],
    'orcamento_mensal': [{
        'id_orcamento': 1, 'id_user': 1, 'mes': 1, 'ano': 2025,
        'categoria': 'lazer', 'valor_previsto': 100.0,
    }],
    'resumo_financeiro_mensal': [{
        'mes': 1, 'ano': 2025, 'total_movimentacoes': 5,
        'total_receitas': 5000.0, 'total_despesas': 3000.0, 'saldo': 2000.0,
    }],
    'resumo_financeiro_outros': [{
        'progresso_medio_metas': 50.0, 'total_patrimonio': 100000.0,
        'total_investido_final': 50000.0, 'total_proventos': 5000.0,
        'total_dividas': 1000.0,
    }],
    'gasto_mensal': [{
        'ano': 2025, 'mes': 1, 'categoria_despesa': 'lazer',
        'total_gasto': 500.0, 'percentual': 25.0,
    }],
}


class MockSession:
    """Sessão mock que retorna dados baseados no conteúdo da query SQL."""

    def _match_data(self, q):
        """Retorna os dados mock apropriados para a query."""
        if 'select comprovante_pdf' in q:
            return [{'comprovante_pdf': None}], None
        
        # Ordem importa: verificar termos mais específicos primeiro
        if 'resumo_financeiro_mensal' in q:
            return MOCK_DATA['resumo_financeiro_mensal'], 1
        if 'resumo_financeiro_outros' in q:
            return MOCK_DATA['resumo_financeiro_outros'], 1
        if 'gasto_mensal' in q or 'comparativo_orcamento_gasto' in q:
            return MOCK_DATA['gasto_mensal'], 1
        if 'orcamento_mensal' in q:
            return MOCK_DATA['orcamento_mensal'], 1
        if 'movimentacao' in q:
            return MOCK_DATA['movimentacao'], 1
        if 'user_admin' in q:
            return MOCK_DATA['admin'], 1
        if 'noticia' in q:
            return MOCK_DATA['noticia'], 1
        if 'imagem' in q:
            return MOCK_DATA['imagem'], 1
        if 'usuario' in q:
            return MOCK_DATA['usuario'], 1
        if 'categoria' in q:
            return MOCK_DATA['categoria'], 1
        if 'patrimonio' in q:
            return MOCK_DATA['patrimonio'], 1
        if 'investimento' in q:
            return MOCK_DATA['investimento'], 1
        if 'meta' in q:
            return MOCK_DATA['meta'], 1
        if 'dividas' in q:
            return MOCK_DATA['dividas'], 1
        # fallback
        return [{'id': 1}], 1

    async def execute(self, query, *args, **kwargs):
        q = str(query).lower()
        data, scalar = self._match_data(q)
        return MockResult(data, scalar)

    async def commit(self):
        pass

    async def rollback(self):
        pass





async def override_get_session_mock():
    """Gera uma MockSession para injeção de dependência."""
    yield MockSession()


def override_get_current_user():
    """Retorna um UsuarioBase mock para testes autenticados."""
    return UsuarioBase(id_user=1, nome='Teste', email='teste@test.com', login='teste', senha='abc')


def override_get_admin():
    """Retorna um AdminUser mock para testes autenticados como admin."""
    return AdminUser(id_admin=1, admin_login='admin', senha='abc')


app.dependency_overrides[get_session] = override_get_session_mock
app.dependency_overrides[get_current_user] = override_get_current_user
app.dependency_overrides[get_admin] = override_get_admin


@pytest.fixture
def client():
    """Fixture que cria um TestClient com as dependências mockadas."""
    with TestClient(app) as test_client:
        yield test_client
