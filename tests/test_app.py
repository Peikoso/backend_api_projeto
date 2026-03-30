"""Testes básicos para a API do SCFF (Backend FastAPI).

Estes testes verificam os endpoints principais da aplicação,
garantindo que as rotas respondem corretamente com as dependências mockadas.
"""

import pytest
from fastapi.testclient import TestClient


class TestRootEndpoint:
    """Testes para o endpoint raiz da API."""

    def test_read_root_status_code(self, client: TestClient):
        """Verifica se o endpoint raiz retorna status 200."""
        response = client.get('/')
        assert response.status_code == 200

    def test_read_root_message(self, client: TestClient):
        """Verifica se o endpoint raiz retorna a mensagem de boas-vindas."""
        response = client.get('/')
        data = response.json()
        assert 'message' in data
        assert data['message'] == 'Bem Vindo a API do SCFF'


class TestSecurityModule:
    """Testes para o módulo de segurança."""

    def test_get_password_hash_returns_string(self):
        """Verifica se o hash de senha retorna uma string."""
        from backend_fastapi.security import get_password_hash
        hashed = get_password_hash('test_password')
        assert isinstance(hashed, str)
        assert hashed != 'test_password'

    def test_verify_password_correct(self):
        """Verifica se a verificação de senha funciona com senha correta."""
        from backend_fastapi.security import get_password_hash, verify_password
        password = 'minha_senha_segura'
        hashed = get_password_hash(password)
        assert verify_password(password, hashed) is True

    def test_verify_password_incorrect(self):
        """Verifica se a verificação de senha rejeita senha incorreta."""
        from backend_fastapi.security import get_password_hash, verify_password
        hashed = get_password_hash('senha_correta')
        assert verify_password('senha_errada', hashed) is False

    def test_create_access_token(self):
        """Verifica se o token JWT é criado corretamente."""
        from jwt import decode

        from backend_fastapi.security import ALGORITHM, SECRET_KEY, create_access_token
        token = create_access_token(data={'sub': 'test_user'})
        assert isinstance(token, str)
        payload = decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        assert payload['sub'] == 'test_user'
        assert 'exp' in payload

    def test_create_access_token_with_expiry(self):
        """Verifica se o token tem data de expiração."""
        from datetime import datetime, timezone

        from jwt import decode

        from backend_fastapi.security import ALGORITHM, SECRET_KEY, create_access_token
        token = create_access_token(data={'sub': 'user123'})
        payload = decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        exp = datetime.fromtimestamp(payload['exp'], tz=timezone.utc)
        now = datetime.now(tz=timezone.utc)
        assert exp > now


class TestEndpointsAuthenticated:
    """Testes para verificar que endpoints protegidos funcionam com autenticação mockada."""

    def test_usuario_endpoint_returns_ok(self, client: TestClient):
        """Verifica se o endpoint de usuário retorna 200 com mock de auth."""
        response = client.get('/Usuario/')
        assert response.status_code == 200

    def test_meta_endpoint_returns_ok(self, client: TestClient):
        """Verifica se o endpoint de meta retorna 200 com mock de auth."""
        response = client.get('/Meta/')
        assert response.status_code == 200

    def test_investimento_endpoint_returns_ok(self, client: TestClient):
        """Verifica se o endpoint de investimento retorna 200 com mock de auth."""
        response = client.get('/Investimento/')
        assert response.status_code == 200

    def test_patrimonio_endpoint_returns_ok(self, client: TestClient):
        """Verifica se o endpoint de patrimônio retorna 200 com mock de auth."""
        response = client.get('/Patrimonio/')
        assert response.status_code == 200

    def test_dividas_endpoint_returns_ok(self, client: TestClient):
        """Verifica se o endpoint de dívidas retorna 200 com mock de auth."""
        response = client.get('/Dividas/')
        assert response.status_code == 200

    def test_orcamento_endpoint_returns_ok(self, client: TestClient):
        """Verifica se o endpoint de orçamento mensal retorna 200 com mock de auth."""
        response = client.get('/OrcamentoMensal/All')
        assert response.status_code == 200

    def test_movimentacao_endpoint_returns_ok(self, client: TestClient):
        """Verifica se o endpoint de movimentação retorna 200 com mock de auth."""
        response = client.get('/Movimentacao/')
        assert response.status_code == 200

    def test_admin_categoria_endpoint_returns_ok(self, client: TestClient):
        """Verifica se o endpoint de categorias retorna 200."""
        response = client.get('/Admin/Categoria')
        assert response.status_code == 200

    def test_resumo_financeiro_endpoint_returns_ok(self, client: TestClient):
        """Verifica se o endpoint de resumo financeiro retorna 200."""
        response = client.get('/ResumoFinanceiro/')
        assert response.status_code == 200
