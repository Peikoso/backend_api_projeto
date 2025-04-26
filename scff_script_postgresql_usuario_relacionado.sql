
-- Criação do banco (opcional)
-- CREATE DATABASE scff;
-- \c scff

-- Tipos ENUM criados:
CREATE TYPE tipo_movimentacao_enum AS ENUM ('receita', 'despesa');

-- Categorias para DESPESA
CREATE TYPE categoria_despesa_enum AS ENUM (
    'alimentacao',
    'moradia',
    'transporte',
    'lazer',
    'saude',
    'educacao',
    'investimentos',
    'outros'
);

-- Categorias para RECEITA
CREATE TYPE categoria_receita_enum AS ENUM (
    'salario',
    'rendimento',
    'presente',
    'venda',
    'reembolso',
    'outros'
);

-- Categorias para Dividas
CREATE TYPE situacao_divida AS ENUM (
    'aberta',
    'quitada',
    'renegociada',
    'atrasada'
);

-- Categorias para Patrimonio
CREATE TYPE classe_patrimonio AS ENUM (
    'bem_imovel',
    'bem_movel',
    'investimento',
    'dinheiro',
    'direito_a_receber',
    'participacao_societaria',
    'propriedade_intelectual',
    'outros'
);

-- Categorias para Metas
CREATE TYPE categoria_meta_enum AS ENUM (
    'viagem',
    'casa',
    'carro',
    'educacao',
    'aposentadoria',
    'fundo_de_emergencia',
    'eletronico',
    'reforma',
    'abrir_negocio',
    'outros'
);

-- Categoria
CREATE TABLE categoria (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL UNIQUE
);

-- Imagem
CREATE TABLE imagem (
    id SERIAL PRIMARY KEY,
    imagem_url TEXT,
	imagem_path TEXT
);

--Noticia
CREATE TABLE noticia (
    id SERIAL PRIMARY KEY,
    titulo VARCHAR(255) NOT NULL,
    autor VARCHAR(100) NOT NULL,
    conteudo TEXT NOT NULL,
    imagem INTEGER,
    categoria_id INTEGER NOT NULL,
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_imagem
        FOREIGN KEY (imagem)
        REFERENCES imagem(id)
        ON DELETE SET NULL,
    CONSTRAINT fk_categoria
        FOREIGN KEY (categoria_id)
        REFERENCES categoria(id)
);


-- ADMIN
CREATE TABLE user_admin (
    id_admin SERIAL PRIMARY KEY,
    admin_login VARCHAR(100) NOT NULL UNIQUE,
    senha TEXT NOT NULL
);

-- Usuário
CREATE TABLE usuario (
    id_user SERIAL PRIMARY KEY,
    nome VARCHAR(100),
    email VARCHAR(100) UNIQUE NOT NULL,
    login VARCHAR(50) UNIQUE,
    senha VARCHAR(300)
);

-- Meta (1:N com usuário)
CREATE TABLE meta (
    id_meta SERIAL PRIMARY KEY,
    categ categoria_meta_enum,
    descri VARCHAR(200),
    data_inicio DATE,
    data_fim DATE,
    valor NUMERIC,
    valor_reservado NUMERIC DEFAULT 0,
    id_user INT REFERENCES usuario(id_user) ON DELETE CASCADE
);

-- Investimento (1:N com usuário)
CREATE TABLE investimento (
    cod SERIAL PRIMARY KEY,
    categ VARCHAR(100),
    valorini NUMERIC,
    valorfim NUMERIC,
    datainicio DATE,
    datafim DATE,
    empresa VARCHAR(100),
    proventos NUMERIC,
    id_user INT REFERENCES usuario(id_user) ON DELETE CASCADE
);

-- Patrimônio
CREATE TABLE patrimonio (
    idbem SERIAL PRIMARY KEY,
    nome VARCHAR(100),
    classe classe_patrimonio,
    valor NUMERIC,
    id_user INT REFERENCES usuario(id_user) ON DELETE CASCADE
);

-- Dívidas
CREATE TABLE dividas (
    cod_divid SERIAL PRIMARY KEY,
    natureza VARCHAR(100),
    situacao situacao_divida,
    data_inicio DATE,
    data_final DATE,
    valor NUMERIC,
    id_user INT REFERENCES usuario(id_user) ON DELETE CASCADE
);

-- Orçamento Mensal
CREATE TABLE orcamento_mensal (
    id_orcamento SERIAL PRIMARY KEY,
    mes INT NOT NULL,
    ano INT NOT NULL,
    categoria categoria_despesa_enum,
    valor_previsto NUMERIC NOT NULL,
    id_user INT REFERENCES usuario(id_user) ON DELETE CASCADE,

    CONSTRAINT unique_orcamento_usuario_mes_categoria
    UNIQUE (id_user, ano, mes, categoria)
);

-- Movimentação
CREATE TABLE movimentacao (
    idmov SERIAL PRIMARY KEY,
    valor NUMERIC,
    descricao TEXT,
    mes INT NOT NULL ,
    ano INT NOT NULL,
    tipo_mov tipo_movimentacao_enum,
    categoria_receita categoria_receita_enum,
    categoria_despesa categoria_despesa_enum,
    comprovante_pdf TEXT,
    id_user INT REFERENCES usuario(id_user) ON DELETE CASCADE
);



-- Inserção de dados

-- Usuário
INSERT INTO usuario (nome, email, login, senha)
VALUES 
('Carlos Andrade', 'carlos@email.com', 'carlos123', '$argon2id$v=19$m=65536,t=3,p=4$Di6+ciMdHJWKAvlGXyg0uw$40zmaP3agxedN/RTld4rRvdfaNThIiRu/KHgNSpVWaM'),
('Fernanda Lima', 'fernanda@email.com', 'ferlima', '$argon2id$v=19$m=65536,t=3,p=4$hS1LW8g2Dtp4cEPPh92qVA$KNoWe1Uke14JNOUwGs9cxi9e1wrDt+9F9K2n7nE6vvA');

-- Meta
INSERT INTO meta (categ, descri, data_inicio, data_fim, valor, valor_reservado, id_user)
VALUES 
('carro', 'Comprar um carro novo', '2025-01-01', '2025-12-31', 100000, 3500, 1),
('viagem', 'Fazer intercâmbio', '2025-06-01', '2026-06-01', 15000, 7500, 2);

-- Investimento
INSERT INTO investimento (categ, valorini, valorfim, datainicio, datafim, empresa, proventos, id_user)
VALUES 
('CDB', 10000, 10500, '2025-01-10', '2025-12-10', 'Banco XPTO', 500, 1),
('Tesouro Direto', 5000, 5500, '2025-02-01', '2026-02-01', 'Tesouro Nacional', 500, 2);

-- Patrimônio
INSERT INTO patrimonio (nome, classe, valor, id_user)
VALUES 
('Carro', 'bem_movel', 30000, 1),
('Apartamento', 'bem_imovel', 200000, 2);

-- Dívidas
INSERT INTO dividas (natureza, situacao, data_inicio, data_final, valor, id_user)
VALUES 
('CartaoCredito', 'aberta', '2025-03-01', '2025-04-01', 1500, 1),
('EmprestimoPessoal', 'quitada', '2024-01-01', '2025-01-01', 8000, 2);

-- Orçamento mensal para o usuário 1
INSERT INTO orcamento_mensal (mes, ano, categoria, valor_previsto, id_user)
VALUES
(4, 2025, 'alimentacao', 500, 1),
(4, 2025, 'moradia', 1200, 1),
(4, 2025, 'transporte', 300, 1),
(4, 2025, 'lazer', 250, 1),
(4, 2025, 'saude', 150, 1),
(4, 2025, 'educacao', 200, 1),
(4, 2025, 'investimentos', 400, 1);

-- Orçamento mensal para o usuário 2
INSERT INTO orcamento_mensal (mes, ano, categoria, valor_previsto, id_user)
VALUES
(4, 2025, 'alimentacao', 450, 2),
(4, 2025, 'moradia', 1000, 2),
(4, 2025, 'transporte', 350, 2),
(4, 2025, 'lazer', 200, 2),
(4, 2025, 'saude', 180, 2),
(4, 2025, 'educacao', 300, 2),
(4, 2025, 'investimentos', 500, 2);


-- Movimentação (1 Receita e 1 Despesa para cada usuário)
INSERT INTO movimentacao (valor, descricao, mes, ano, tipo_mov, categoria_receita, categoria_despesa, id_user)
VALUES 
(5000, 'Salário mensal', 4, 2025, 'receita', 'salario', NULL, 1),
(200, 'Jantar fora', 4, 2025, 'despesa', NULL, 'lazer', 1),
(300, 'Venda online', 4, 2025, 'receita', 'venda', NULL, 2),
(150, 'Remédio',  4, 2025, 'despesa', NULL, 'saude', 2);

-- Movimentações adicionais para usuário 1
INSERT INTO movimentacao (valor, descricao, mes, ano, tipo_mov, categoria_receita, categoria_despesa, id_user)
VALUES
(120, 'Reembolso de transporte', 4, 2025, 'receita', 'reembolso', NULL, 1),
(800, 'Aluguel pago',  4, 2025, 'despesa', NULL, 'moradia', 1),
(90, 'Supermercado',  4, 2025, 'despesa', NULL, 'alimentacao', 1),
(60, 'Cinema',  4, 2025, 'despesa', NULL, 'lazer', 1),
(150, 'Curso online',  4, 2025, 'despesa', NULL, 'educacao', 1);

-- Movimentações adicionais para usuário 2
INSERT INTO movimentacao (valor, descricao, mes, ano, tipo_mov, categoria_receita, categoria_despesa, id_user)
VALUES
(1000, 'Freelance',  4, 2025, 'receita', 'rendimento', NULL, 2),
(400, 'Prestação do carro',  4, 2025, 'despesa', NULL, 'transporte', 2),
(250, 'Consulta médica',  4, 2025, 'despesa', NULL, 'saude', 2),
(70, 'Internet mensal',  4, 2025, 'despesa', NULL, 'moradia', 2),
(50, 'Presente para amigo',  4, 2025, 'despesa', NULL, 'outros', 2);

--Admin
INSERT INTO user_admin (admin_login, senha) VALUES
('admin1', '$argon2id$v=19$m=65536,t=3,p=4$fxBzbn0x72/GfoV/uqsUMA$eai9tFzhAsNOLwle3eMYEJ6UFp50Ju2MDX5CONNkZhI');

-- Categorias
INSERT INTO categoria (nome) VALUES
('Investimentos'),
('Mercado de Ações'),
('Economia Nacional'),
('Criptomoedas'),
('Educação Financeira'),
('Política Monetária');

-- Noticias
INSERT INTO noticia (titulo, autor, conteudo, imagem, categoria_id)
VALUES
(
  'Selic é mantida em 10,75%: o que isso significa para seus investimentos?',
  'João Elias',
  '<p>O Comitê de Política Monetária decidiu manter a taxa Selic em 10,75% ao ano...</p><p>Isso impacta diretamente a renda fixa e o crédito.</p>',
  NULL,
  6
),
(
  'Bolsa fecha em alta após anúncio de estímulo nos EUA',
  'Maria Senna',
  '<p>O índice Ibovespa fechou em alta de 1,2% nesta terça-feira...</p><p>Analistas apontam otimismo após medidas anunciadas pelo FED.</p>',
  NULL,
  2
),
(
  'Bitcoin ultrapassa US$ 70 mil pela primeira vez em 2025',
  'João Martins',
  '<p>A criptomoeda mais conhecida do mundo atingiu uma nova máxima histórica...</p>',
  NULL,
  4
),
(
  'Entenda o que são fundos imobiliários e como começar a investir',
  'Camila Costa',
  '<p>Fundos Imobiliários (FIIs) são uma excelente porta de entrada para quem deseja investir em imóveis...</p>',
  NULL,
  1
),
(
  'Inflação desacelera em março e anima o mercado',
  'Lucas Ribeiro',
  '<p>O IPCA registrou uma alta de 0,21% em março, abaixo das expectativas...</p>',
  NULL,
  3
),
(
  'Como montar uma reserva de emergência sólida em 2025',
  'Ana Paula',
  '<p>Especialistas recomendam que a reserva de emergência cubra de 6 a 12 meses de despesas...</p>',
  NULL,
  5
);

-- Auditoria
CREATE TABLE auditoria_movimentacao (
    id SERIAL PRIMARY KEY,
    idmov INT,
    operacao VARCHAR(10),
    data_operacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE OR REPLACE FUNCTION log_auditoria_movimentacao()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO auditoria_movimentacao (idmov, operacao)
    VALUES (OLD.idmov, TG_OP);
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_audit_mov
AFTER UPDATE OR DELETE ON movimentacao
FOR EACH ROW EXECUTE FUNCTION log_auditoria_movimentacao();


-- Função: Conta itens na tabela
CREATE OR REPLACE FUNCTION contar_linhas_tabelas()
RETURNS TABLE (
    tabela TEXT,
    total_linhas BIGINT
)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT 'usuario', COUNT(*) FROM usuario
    UNION ALL
    SELECT 'meta', COUNT(*) FROM meta
    UNION ALL
    SELECT 'investimento', COUNT(*) FROM investimento
    UNION ALL
    SELECT 'patrimonio', COUNT(*) FROM patrimonio
    UNION ALL
    SELECT 'dividas', COUNT(*) FROM dividas
    UNION ALL
    SELECT 'orcamento_mensal', COUNT(*) FROM orcamento_mensal
    UNION ALL
    SELECT 'movimentacao', COUNT(*) FROM movimentacao
    UNION ALL
    SELECT 'auditoria_movimentacao', COUNT(*) FROM auditoria_movimentacao;
END;
$$;



-- View gerencial 
CREATE OR REPLACE VIEW resumo_financeiro_mensal AS
WITH 
movs AS (
    SELECT 
        id_user,
        mes,
        ano,
        COUNT(*) AS total_mov,
        SUM(CASE WHEN tipo_mov = 'receita' THEN valor ELSE 0 END) AS total_receitas,
        SUM(CASE WHEN tipo_mov = 'despesa' THEN valor ELSE 0 END) AS total_despesas
    FROM movimentacao
    GROUP BY id_user, mes, ano
)

SELECT 
    u.id_user,
    u.nome,
    m.mes,
    m.ano,
    COALESCE(m.total_mov, 0) AS total_movimentacoes,
    COALESCE(m.total_receitas, 0) AS total_receitas,
    COALESCE(m.total_despesas, 0) AS total_despesas,
    COALESCE(m.total_receitas, 0) - COALESCE(m.total_despesas, 0) AS saldo

FROM usuario u
LEFT JOIN movs m ON u.id_user = m.id_user;


CREATE OR REPLACE VIEW resumo_financeiro_outros AS
WITH metas AS (
    SELECT 
        id_user,
        ROUND(COALESCE(AVG(
            CASE 
                WHEN valor > 0 AND valor_reservado IS NOT NULL THEN (valor_reservado / valor) * 100
                ELSE NULL
            END
        ), 0), 2) AS progresso_medio_metas
    FROM meta
    GROUP BY id_user
),
patrimonios AS (
    SELECT 
        id_user,
        SUM(valor) AS total_patrimonio
    FROM patrimonio
    GROUP BY id_user
),
investimentos AS (
    SELECT 
        id_user,
        SUM(valorfim) AS total_investido_final,
        SUM(proventos) AS total_proventos
    FROM investimento
    GROUP BY id_user
),
dividas AS (
    SELECT 
        id_user,
        SUM(valor) AS total_dividas
    FROM dividas
    WHERE situacao != 'quitada'
    GROUP BY id_user
)

SELECT 
    u.id_user,
    u.nome,
    COALESCE(m.progresso_medio_metas, 0) AS progresso_medio_metas,
    COALESCE(p.total_patrimonio, 0) AS total_patrimonio,
    COALESCE(i.total_investido_final, 0) AS total_investido_final,
    COALESCE(i.total_proventos, 0) AS total_proventos,
    COALESCE(d.total_dividas, 0) AS total_dividas

FROM usuario u
LEFT JOIN metas m ON u.id_user = m.id_user
LEFT JOIN patrimonios p ON u.id_user = p.id_user
LEFT JOIN investimentos i ON u.id_user = i.id_user
LEFT JOIN dividas d ON u.id_user = d.id_user;


--- view Gasto mensal por categoria
CREATE OR REPLACE VIEW gasto_mensal_por_categoria AS
WITH total_mes AS (
    SELECT 
        m.id_user,
        m.ano,
        m.mes,
        SUM(m.valor) AS total_gasto_mes
    FROM movimentacao m
    WHERE m.tipo_mov = 'despesa'
    GROUP BY m.id_user, m.ano, m.mes
)
SELECT 
    m.id_user,
    m.ano,
    m.mes,
    m.categoria_despesa,
    SUM(m.valor) AS total_gasto,
    ROUND(SUM(m.valor) / NULLIF(tm.total_gasto_mes, 0) * 100, 2) AS percentual
FROM movimentacao m
JOIN total_mes tm 
    ON m.id_user = tm.id_user
    AND m.ano = tm.ano
    AND m.mes = tm.mes
WHERE m.tipo_mov = 'despesa'
GROUP BY m.id_user, m.categoria_despesa, m.ano, m.mes, tm.total_gasto_mes;



CREATE OR REPLACE VIEW comparativo_orcamento_gasto AS
SELECT 
    o.id_user,
    o.ano,
    o.mes,
    o.categoria AS categoria_despesa,
    COALESCE(o.valor_previsto, 0) AS orcamento_previsto,
    COALESCE(g.total_gasto, 0) AS gasto_real,
    (COALESCE(o.valor_previsto, 0) - COALESCE(g.total_gasto, 0)) AS diferenca,
    ROUND(
        CASE 
            WHEN o.valor_previsto > 0 THEN 
                (COALESCE(g.total_gasto, 0) / o.valor_previsto) * 100
            ELSE 0
        END, 2
    ) AS percentual_gasto
FROM orcamento_mensal o
LEFT JOIN gasto_mensal_por_categoria g 
    ON o.id_user = g.id_user 
    AND o.categoria = g.categoria_despesa
    AND o.ano = g.ano
    AND o.mes = g.mes;
