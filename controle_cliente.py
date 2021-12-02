from conexao import conectar_bd
from validar_email import validar_email
from estado_cidade import pegar_id_cidade
from tkinter import messagebox as mg
import pyodbc


def verificar_campos_vazios(cpf, nome, endereco, numero, complemento, cep,
    bairro, celular, email, cidade):
    """Verifica sem ha algum campo obrigatorio vazio"""

    # passando os parametros da função para um dict
    # para exibir para o usuario o campo que estive vazio
    campos_obrigatorios = [cpf, nome, endereco, numero, complemento, cep,
    bairro, celular, email, cidade]

    for valor in campos_obrigatorios:
        if valor == ' ':
            raise mg.showerror(title='Error', message='Campos obrigatórios vazio')
    else:
        validar_dados_cliente(cpf, nome, endereco, numero, complemento, cep,
    bairro, celular, email, cidade)


def validar_dados_cliente(cpf, nome, endereco, numero, complemento, cep,
    bairro, celular, email, cidade):
    """Verificar se os dados estão corretos"""

    try:
        # ja esta cadastrado no sistema verificar se o cliente
        verificar_cadastro_cliente(cpf)

        # chamada da função para verificar o email
        validar_email(email)

        # chamada das funções para pegar o id e 
        id_cidade = pegar_id_cidade(cidade)

        gravar_dados_cliente(str(cpf), str(nome), str(endereco), 
        str(numero), str(complemento), str(cep), str(bairro), str(celular),
        str(email), id_cidade)

    except TypeError:
        mg.showerror(title='ERRO', message='Formato de dado inválido!')
    
    except ValueError:
        mg.showerror(title='ERRO', message='Valor inválido!')


def gravar_dados_cliente(cpf, nome, endereco, numero, complemento, cep,
    bairro, celular, email, cidade):
    """Função para gravar os dados no banco de dados"""

    try:
        # instancia da classe conexão
        conexao = conectar_bd()
        cursor = conexao.cursor()

        sql = f"INSERT INTO TB_CLIENTE_CLI  VALUES \
            ('{cpf}', '{nome}','{endereco}', '{numero}',\
            '{complemento}', '{cep}', '{bairro}', '{celular}',\
            '{email}','{True}', '{cidade}')"
        
        # commit para que não ocorra um erro quando varias pessoas
        # estiverem tentando grava os dados ao mesmo momento
        cursor.execute(sql)
        conexao.commit()

        # exibir mensagem de sucesso
        mg.showinfo(title='Sucesso', message='Dados gravados com sucesso!')
    
    except pyodbc.DataError:
        mg.showerror(title='ERRO', message='Formato inválido!')

    except pyodbc.Error as ex:
        sqlstate = ex.args[0]
        if sqlstate == '23000':
            mg.showerror(title='ERRO', message='Campos obrigatórios vazio!')
    
    finally:
        conexao.close()


def atualizar_dados_cliente(cpf, nome, endereco, numero, complemento, cep,
    bairro, celular, email, cidade):
    """Função para atualizar os dados no banco de dados"""

    try:

        # instancia da classe conexão
        conexao = conectar_bd()
        cursor = conexao.cursor()
    
        sql = f"update TB_CLIENTE_CLI set \
            CLI_NOME = '{nome}',\
            CLI_ENDEREÇO = '{endereco}',\
            CLI_NUMERO = '{numero}',\
            CLI_COMPLEMENTO = '{complemento}',\
            CLI_CEP = '{cep}',\
            CLI_BAIRRO = '{bairro}',\
            CLI_CELULAR = '{celular}',\
            CLI_EMAIL = '{email}',\
            CID_CODIGO = '{cidade}' \
            where CLI_CPF = '{cpf}'"
        
        # commit para que não ocorra um erro quando varias pessoas
        # estiverem tentando grava os dados no mesmo banco
        cursor.execute(sql)
        conexao.commit()

        # exibir mensagem de sucesso
        mg.showinfo(title='Sucesso', 
        message='Cadastro atualizado com sucesso!')
    
    except pyodbc.DataError:
        mg.showerror(title='ERRO', message='Formato inválido!')
    
    except pyodbc.Error as ex:
        sqlstate = ex.args[0]
        if sqlstate == '23000':
            mg.showerror(title='ERRO', message='Campos obrigatórios vazio!')
    
    finally:
        conexao.close()


def ler_dados_cliente(cpf):
    """Função para buscar os dados do funcionario no banco de dados"""

    try:

        # instância do método conectar_bd daa classe conexão
        conexao = conectar_bd()
        cursor = conexao.cursor()

        sql = f"SELECT * FROM TB_CLIENTE_CLI WHERE CLI_CPF = '{cpf}'"
        
        cursor.execute(sql)
        linha = cursor.fetchone()

        if linha == None:
            mg.showerror('Erro', 'Cliente não encontrado!')
        else:
            return linha
    
    except pyodbc.OperationalError:
        mg.showerror(title='ERRO', 
        message='Não foi possivel conectar ao banco de dados!')


def verificar_cadastro_cliente(cpf):
    """Verificar se o cliente ja está cadastrado no sistema"""

    try:
        # instância do método conectar_bd da classe conexão
        conexao = conectar_bd()
        cursor = conexao.cursor()

        sql = f"select CLI_CPF from TB_CLIENTE_CLI\
            where CLI_CPF = '{cpf}'"
        cursor.execute(sql)
        linha = cursor.fetchone()

        # verifica se o cliente está cadastro no sistema
        # caso não esteja a variavel linha retorna None
        if linha == None:
            pass
        else:
            if linha[0] == cpf:
                raise mg.showerror(title='Erro',
                message='Cliente já está cadastrado no sistema!')
    
    except pyodbc.OperationalError:
        mg.showerror(title='ERRO', 
        message='Não foi possivel conectar ao banco de dados!')


def mostrar_cliente():
    """Função para mostra todos os dados da tabela cliente"""

    try:

        # instância do método conectar_bd daa classe conexão
        conexao = conectar_bd()
        cursor = conexao.cursor()

        # executar o script e passar os dados para uma lista
        sql = "select * from TB_CLIENTE_CLI"

        cursor.execute(sql)
        linha = cursor.fetchall()
        return [valor for valor in linha]
    
    except pyodbc.OperationalError:
        mg.showerror(title='ERRO', 
        message='Não foi possivel conectar ao banco de dados!')
