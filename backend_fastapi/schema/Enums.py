from enum import Enum


# Tipos de movimentação
class TipoMovimentacaoEnum(str, Enum):
    Receita = 'receita'
    Despesa = 'despesa'


# Categorias de despesa
class CategoriaDespesaEnum(str, Enum):
    Alimentacao = 'alimentacao'
    Moradia = 'moradia'
    Transporte = 'transporte'
    Lazer = 'lazer'
    Saude = 'saude'
    Educacao = 'educacao'
    Investimentos = 'investimentos'
    Outros = 'outros'


# Categorias de receita
class CategoriaReceitaEnum(str, Enum):
    Salario = 'salario'
    Rendimento = 'rendimento'
    Presente = 'presente'
    Venda = 'venda'
    Reembolso = 'reembolso'
    Outros = 'outros'


# Enum para Situação do Imposto de Renda
class SituacaoImprendaEnum(str, Enum):
    completa = 'completa'
    parcial = 'parcial'
    isento = 'isento'
    pendente = 'pendente'
    em_atraso = 'em_atraso'


# Enum para Situação de Dívida
class SituacaoDividaEnum(str, Enum):
    aberta = 'aberta'
    quitada = 'quitada'
    renegociada = 'renegociada'
    atrasada = 'atrasada'


# Enum para Classe do Patrimônio
class ClassePatrimonioEnum(str, Enum):
    bem_imovel = 'bem_imovel'
    bem_movel = 'bem_movel'
    investimento = 'investimento'
    dinheiro = 'dinheiro'
    direito_a_receber = 'direito_a_receber'
    participacao_societaria = 'participacao_societaria'
    propriedade_intelectual = 'propriedade_intelectual'
    outros = 'outros'
