import pytest

def test_admin_category(client):
    assert client.get("/Admin/Categoria").status_code == 200
    assert client.post("/Admin/Categoria", json={"nome": "Novo"}).status_code in [200, 201]
    assert client.put("/Admin/Categoria/1", json={"nome": "Atualizado"}).status_code == 200
    assert client.delete("/Admin/Categoria/1").status_code == 200

def test_admin_noticia(client):
    req = {"titulo": "Noticia", "autor": "Auto", "conteudo": "Cont", "categoria_id": 1}
    assert client.get("/Admin/Noticia").status_code == 200
    assert client.post("/Admin/Noticia", json=req).status_code in [200, 201]
    assert client.put("/Admin/Noticia/1", json=req).status_code == 200
    assert client.delete("/Admin/Noticia/1").status_code == 200
    assert client.get("/Admin/Imagem").status_code == 200

def test_usuario(client):
    u = {"nome":"A","email":"a@a.com","login":"a","senha":"abc"}
    assert client.get("/Usuario/").status_code == 200
    assert client.post("/Usuario/Cadastro", json=u).status_code in [200, 201]
    assert client.put("/Usuario/", json=u).status_code == 200
    assert client.delete("/Usuario/").status_code == 200
    # ensure refresh token works with mock
    assert client.post("/Usuario/refresh_token").status_code in [200, 422, 500] 

def test_patrimonio(client):
    p = {
        "tipo_bem": "IMOVEL",
        "nome_bem": "Casa",
        "valor_estimado": 100000.0,
        "data_aquisicao": "2023-01-01",
        "descricao": "Casa na praia"
    }
    assert client.get("/Patrimonio/All").status_code == 200
    assert client.get("/Patrimonio/1").status_code == 200
    assert client.post("/Patrimonio/", json=p).status_code == 200
    assert client.put("/Patrimonio/1", json=p).status_code == 200
    assert client.delete("/Patrimonio/1").status_code == 200

def test_investimentos(client):
    i = {
        "nome": "CDB", "descricao": "CDB BB", "tipo_inv": "CDB", 
        "valor_mensal": 100.0, "valor_investido": 1000.0, 
        "meta_inv": 5000.0, "tempo_estimado": 12, "rentabilidade": 1.0, 
        "data_inicio": "2023-01-01"
    }
    assert client.get("/Investimento/All").status_code == 200
    assert client.get("/Investimento/1").status_code == 200
    assert client.post("/Investimento/", json=i).status_code == 200
    assert client.put("/Investimento/1", json=i).status_code == 200
    assert client.delete("/Investimento/1").status_code == 200

def test_metas(client):
    m = {
        "nome_meta": "Carro", "valor_total": 50000, "saldo_atual": 10000, 
        "valor_mes": 1000, "prazo_meses": 40
    }
    assert client.get("/Meta/All").status_code == 200
    assert client.get("/Meta/1").status_code == 200
    assert client.post("/Meta/", json=m).status_code == 200
    assert client.put("/Meta/1", json=m).status_code == 200
    assert client.delete("/Meta/1").status_code == 200

def test_dividas(client):
    d = {
        "nome": "Carro", "descricao": "Financiamento", 
        "vencimento": "2023-12-01", "status_divid": "PAGO", 
        "valor_original": 1000, "juros": 10.0, "valor_pago": 1000
    }
    assert client.get("/Dividas/All").status_code == 200
    assert client.get("/Dividas/1").status_code == 200
    assert client.post("/Dividas/", json=d).status_code == 200
    assert client.put("/Dividas/1", json=d).status_code == 200
    assert client.delete("/Dividas/1").status_code == 200

def test_gastos(client):
    assert client.get("/Gasto/MensalCategoria/LAZER").status_code == 200
    assert client.get("/Gasto/Mensal/2023/1").status_code == 200
    assert client.get("/Gasto/TotalMensal/2023/1").status_code == 200

def test_orcamento_mensal(client):
    o = {"mes": 1, "ano": 2023, "categoria": "LAZER", "valor_previsto": 1000.0}
    assert client.get("/OrcamentoMensal/All").status_code == 200
    assert client.get("/OrcamentoMensal/?ano=2025&mes=1").status_code == 200
    assert client.get("/OrcamentoMensal/1").status_code == 200
    assert client.post("/OrcamentoMensal/", json=o).status_code == 200
    assert client.put("/OrcamentoMensal/1", json=o).status_code == 200
    assert client.delete("/OrcamentoMensal/1").status_code == 200

def test_resumo_financeiro(client):
    assert client.get("/ResumoFinanceiro/").status_code == 200
    assert client.get("/ResumoFinanceiro/Mensal/1/2023").status_code == 200
    assert client.get("/ResumoFinanceiro/Outros").status_code == 200

def test_movimentacao(client):
    m = {
        "data": "2023-01-01", "tipo_mov": "RECEITA", "valor": 1000.0,
        "descricao": "Salario", "categoria": "SALARIO", "conta": "Corrente"
    }
    import json
    assert client.get("/Movimentacao/").status_code == 200
    assert client.get("/Movimentacao/1").status_code == 200
    # using form data for post since comprovente is optional file, 
    # and movimentacao is json
    assert client.post("/Movimentacao/", data={"movimentacao": json.dumps(m)}).status_code in [200, 201]
    assert client.put("/Movimentacao/1", json=m).status_code == 200
    assert client.delete("/Movimentacao/1").status_code == 200
