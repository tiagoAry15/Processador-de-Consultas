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
    DESCRICAO = "descricao"
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
    DESCRICAO = "Descrição"
    TIPO_MOVIMENTO_ID_TIPO_MOVIMENTO = "TipoMovimento_idTipoMovimento"
    CATEGORIA_ID_CATEGORIA = "Categoria_idCategoria"
    CONTAS_ID_CONTA = "Contas_idConta"
    VALOR = "Valor"


dict_classes = {
    'usuario': Usuario,
    'tipoconta': TipoConta,
    'contas': Contas,
    'tipomovimento': TipoMovimento,
    'categoria': Categoria,
    'movimentacao': Movimentacao

}


def find_class_for_attribute(attribute):
    for class_name, class_obj in dict_classes.items():
        if any(val.lower() == attribute.lower() for val in vars(class_obj).values() if isinstance(val, str)):
            return class_name
    return None


def is_attribute_in_class(attribute, class_name):
    class_obj = dict_classes[class_name]
    return any(val.lower() == attribute.lower() for val in vars(class_obj).values() if isinstance(val, str))
