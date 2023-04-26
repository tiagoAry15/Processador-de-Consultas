# arquivo: constantes_tabelas.py

class Usuario:
    TABLE_NAME = "Usuario"
    ID_USUARIO = "idUsuario"
    NOME = "Nome"
    LOGRADOURO = "Logradouro"
    NUMERO = "Número"
    BAIRRO = "Bairro"
    CEP = "CEP"
    UF = "UF"
    DATA_NASCIMENTO = "DataNascimento"


class TipoConta:
    TABLE_NAME = "TipoConta"
    ID_TIPO_CONTA = "idTipoConta"
    DESCRICAO = "Descrição"


class Contas:
    TABLE_NAME = "Contas"
    ID_CONTA = "idConta"
    DESCRICAO = "Descricao"
    TIPO_CONTA_ID_TIPO_CONTA = "TipoConta_idTipoConta"
    USUARIO_ID_USUARIO = "Usuario_idUsuario"
    SALDO_INICIAL = "SaldoInicial"


class TipoMovimento:
    TABLE_NAME = "TipoMovimento"
    ID_TIPO_MOVIMENTO = "idTipoMovimento"
    DESC_MOVIMENTACAO = "DescMovimentacao"


class Categoria:
    TABLE_NAME = "Categoria"
    ID_CATEGORIA = "idCategoria"
    DESC_CATEGORIA = "DescCategoria"


class Movimentacao:
    TABLE_NAME = "Movimentacao"
    ID_MOVIMENTACAO = "idMovimentacao"
    DATA_MOVIMENTACAO = "DataMovimentacao"
    DESCRICAO = "Descricao"
    TIPO_MOVIMENTO_ID_TIPO_MOVIMENTO = "TipoMovimento_idTipoMovimento"
    CATEGORIA_ID_CATEGORIA = "Categoria_idCategoria"
    CONTAS_ID_CONTA = "Contas_idConta"
    VALOR = "Valor"


def verifica_atributo(atributo):
    classes = [Usuario, TipoConta, Contas,
               TipoMovimento, Categoria, Movimentacao]

    for classe in classes:
        if atributo in vars(classe).values():
            return f"O atributo '{atributo}' pertence à classe {classe.__name__}"
    return f"O atributo '{atributo}' não pertence a nenhuma das classes"


def verifica_atributo(atributo, classe):
    return atributo in vars(classe).values()
