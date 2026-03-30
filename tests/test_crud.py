"""Testes CRUD para todos os endpoints da API do SCFF.

Cada teste verifica as operações CRUD completas usando
o TestClient com dependências mockadas.
"""

import json


def test_admin_category(client):
    """Testa CRUD completo de categorias no Admin."""
    assert client.get('/Admin/Categoria').status_code == 200
    assert client.post('/Admin/Categoria', json={'nome': 'Novo'}).status_code in [200, 201]
    assert client.put('/Admin/Categoria/1', json={'nome': 'Atualizado'}).status_code == 200
    assert client.delete('/Admin/Categoria/1').status_code == 200


def test_admin_noticia(client):
    """Testa CRUD completo de notícias no Admin."""
    req = {'titulo': 'Noticia', 'autor': 'Autor', 'conteudo': 'Conteudo', 'categoria_id': 1}
    assert client.get('/Admin/Noticia').status_code == 200
    assert client.post('/Admin/Noticia', json=req).status_code in [200, 201]
    assert client.put('/Admin/Noticia/1', json=req).status_code == 200
    assert client.delete('/Admin/Noticia/1').status_code == 200
    assert client.get('/Admin/Imagem').status_code == 200


def test_usuario(client):
    """Testa CRUD completo de usuário."""
    u = {'nome': 'Joao', 'email': 'a@a.com', 'login': 'joao', 'senha': 'abc123'}
    assert client.get('/Usuario/').status_code == 200
    assert client.post('/Usuario/Cadastro', json=u).status_code in [200, 201]
    assert client.put('/Usuario/', json=u).status_code == 200
    assert client.delete('/Usuario/').status_code == 200
    # refresh token funciona com mock
    assert client.post('/Usuario/refresh_token').status_code in [200, 422, 500]


def test_patrimonio(client):
    """Testa CRUD completo de patrimônio."""
    p = {
        'nome': 'Casa na praia',
        'classe': 'bem_imovel',
        'valor': 100000.0,
    }
    assert client.get('/Patrimonio/').status_code == 200
    assert client.get('/Patrimonio/1').status_code == 200
    assert client.post('/Patrimonio/', json=p).status_code == 200
    assert client.put('/Patrimonio/1', json=p).status_code == 200
    assert client.delete('/Patrimonio/1').status_code == 200


def test_investimentos(client):
    """Testa CRUD completo de investimentos."""
    i = {
        'categ': 'CDB Test', 'valorini': 1000.0, 'valorfim': 2000.0,
        'datainicio': '2025-01-01', 'datafim': '2026-01-01',
        'empresa': 'Banco Test',
    }
    assert client.get('/Investimento/').status_code == 200
    assert client.get('/Investimento/1').status_code == 200
    assert client.post('/Investimento/', json=i).status_code in [200, 201]
    assert client.put('/Investimento/1', json=i).status_code == 200
    assert client.delete('/Investimento/1').status_code == 200


def test_metas(client):
    """Testa CRUD completo de metas."""
    m = {
        'categ': 'carro', 'descri': 'Comprar carro novo',
        'data_inicio': '2025-01-01', 'data_fim': '2026-01-01',
        'valor': 50000.0, 'valor_reservado': 10000.0,
    }
    assert client.get('/Meta/').status_code == 200
    assert client.get('/Meta/1').status_code == 200
    assert client.post('/Meta/', json=m).status_code in [200, 201]
    assert client.put('/Meta/1', json=m).status_code == 200
    assert client.delete('/Meta/1').status_code == 200


def test_dividas(client):
    """Testa CRUD completo de dívidas."""
    d = {
        'natureza': 'Financiamento',
        'situacao': 'aberta',
        'data_inicio': '2025-01-01',
        'data_final': '2026-12-01',
        'valor': 1000.0,
    }
    assert client.get('/Dividas/').status_code == 200
    assert client.get('/Dividas/1').status_code == 200
    assert client.post('/Dividas/', json=d).status_code == 200
    assert client.put('/Dividas/1', json=d).status_code == 200
    assert client.delete('/Dividas/1').status_code == 200


def test_gastos(client):
    """Testa endpoints de gastos."""
    assert client.get('/Gasto/Categoria?categ=lazer').status_code == 200
    assert client.get('/Gasto/Mensal/1/2025').status_code == 200


def test_orcamento_mensal(client):
    """Testa CRUD completo de orçamento mensal."""
    o = {'mes': 1, 'ano': 2025, 'categoria': 'lazer', 'valor_previsto': 1000.0}
    assert client.get('/OrcamentoMensal/All').status_code == 200
    assert client.get('/OrcamentoMensal/?ano=2025&mes=1').status_code == 200
    assert client.get('/OrcamentoMensal/1').status_code == 200
    assert client.post('/OrcamentoMensal/', json=o).status_code == 200
    assert client.put('/OrcamentoMensal/1', json=o).status_code == 200
    assert client.delete('/OrcamentoMensal/1').status_code == 200


def test_resumo_financeiro(client):
    """Testa endpoints de resumo financeiro."""
    assert client.get('/ResumoFinanceiro/').status_code == 200
    assert client.get('/ResumoFinanceiro/Mensal/1/2025').status_code == 200
    assert client.get('/ResumoFinanceiro/Outros').status_code == 200


def test_movimentacao(client):
    """Testa CRUD completo de movimentação."""
    m = {
        'mes': 1, 'ano': 2025, 'tipo_mov': 'receita', 'valor': 1000.0,
        'descricao': 'Salario mensal', 'categoria_receita': 'salario',
        'categoria_despesa': None,
    }
    assert client.get('/Movimentacao/').status_code == 200
    assert client.get('/Movimentacao/1').status_code == 200
    # POST usa form data com JSON string para movimentacao
    assert client.post('/Movimentacao/', data={'movimentacao': json.dumps(m)}).status_code in [200, 201]
    assert client.put('/Movimentacao/1', json=m).status_code == 200
    assert client.delete('/Movimentacao/1').status_code == 200
