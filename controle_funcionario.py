from os import execlpe
from conexao import conectar_bd
from estado_cidade import pegar_id_cidade
from validar_email import validar_email
from tkinter import messagebox as mg
import pyodbc


def verificar_campos_vazios(nome, celular, cpf, email, endereco,
    numero, complemento, bairro, cidade, cep, cargo, login, senha, ativo):
    """Verifica sem ha algum campo vazio"""

    # passando os parametros da função para uma lista
    # para exibir para o se o usuario se tiver algum campo vazio
    campos_obrigatorios = [nome, celular, cpf, email, endereco,
    numero, complemento, bairro, cidade, cep, cargo, login, senha, ativo]

    for valor in campos_obrigatorios:
        if valor == ' ':
            raise mg.showerror(title='Error', message='Campos obrigatórios vazio')
    else:
        validar_dados_funcionario(nome, celular, cpf, email, endereco,
    numero, complemento, bairro, cidade, cep, cargo, login, senha, ativo)


def validar_dados_funcionario(nome, celular, cpf, email, endereco, numero,
    complemento, bairro, cidade, cep, cargo, login, senha, ativo):
    """Verificar se os dados estão corretos"""

    try:
        # chamada da função para verificar o email
        validar_email(email)

        # chamada das funções para pegar o id
        id_cidade = pegar_id_cidade(cidade)
        id_cargo = pegar_id_cargo(cargo)

        # chama o metodo para gravar dados
        gravar_dados_funcionario(str(nome), str(celular), str(cpf), 
        str(email), str(endereco), str(numero), str(complemento),
        str(bairro), id_cidade, str(cep), id_cargo, str(login),
        str(senha), bool(ativo))

    except TypeError:
        raise TypeError(mg.showerror(title='Erro', message='Formato de dado inválido!'))
    
    except ValueError:
        raise ValueError(mg.showerror(title='Erro', message='Valor inválido'))


def gravar_dados_funcionario(nome, celular, cpf, email, endereco,
    numero, complemento, bairro, cidade, cep, cargo, login, senha, ativo):
    """Função para gravar os dados no banco de dados"""

    # instancia da classe conexão
    conexao = conectar_bd()
    cursor = conexao.cursor()

    try:
        sql = f"INSERT INTO TB_FUNCIONARIO_FUN  VALUES \
            ('{cpf}', '{nome}','{endereco}', '{numero}',\
            '{complemento}', '{cep}', '{bairro}', '{celular}', '{email}',\
            '{ativo}', '{login}', '{senha}', '{cidade}', '{cargo}')"
        
        # commit para que não ocorra um erro quando varias pessoas
        # estiverem tentando grava os dados ao mesmo momento
        cursor.execute(sql)
        conexao.commit()

        # exibir mensagem de sucesso na atualização de dados
        mg.showinfo(title='Sucesso', message='Cadastro efetuado com sucesso!') 

    except pyodbc.DataError:
        mg.showerror(title='Erro', message='Formato de dado Inválido')
    
    except pyodbc.IntegrityError:
        mg.showerror(title='Erro', message='Funcionario já cadastrado.')
    
    finally:
        conexao.close()


def atualizar_dados_funcionario(nome, celular, cpf, email, endereco,
    numero, complemento, bairro, uf, cep, cargo, login, senha, ativo):
    """Função para atualizar os dados no banco de dados"""

    try:

        # instancia da classe conexão
        conexao = conectar_bd()
        cursor = conexao.cursor()

        sql = f"update TB_FUNCIONARIO_FUN set \
            FUN_NOME = '{nome}',\
            FUN_ENDEREÇO = '{endereco}',\
            FUN_NUMERO = '{numero}',\
            FUN_COMPLEMENTO = '{complemento}',\
            FUN_CEP = '{cep}',\
            FUN_BAIRRO = '{bairro}',\
            FUN_CELULAR = '{celular}',\
            FUN_EMAIL = '{email}',\
            FUN_ATIVO = '{ativo}',\
            FUN_LOGIN = '{login}',\
            FUN_SENHA = '{senha}',\
            CID_CODIGO = '{uf}',\
            CAR_CODIGO = '{cargo}' \
            where FUN_CPF = '{cpf}'"
        
        # commit para que não ocorra um erro quando varias pessoas
        # estiverem tentando grava os dados no mesmo banco
        cursor.execute(sql)
        conexao.commit()

        # exibir mensagem de dados atualizados com sucesso
        mg.showinfo(title='Sucesso',
        message='Dados Atualizados com sucesso')

    
    except pyodbc.DataError:
        mg.showerror(title='Erro', message='Formato inválido!')
    
    except pyodbc.Error as ex:
        sqlstate = ex.args[0]
        if sqlstate == '23000':
            mg.showerror(title='Erro', message='Campos obrigatórios vazio!')
            print('campos obrigatorios vazio:')
    
    finally:
        conexao.close()


def ler_dados_funcionario(cpf):
    """Função para buscar os dados do funcionario no banco de dados"""

    try:

        # instância do método conectar_bd daa classe conexão
        conexao = conectar_bd()
        cursor = conexao.cursor()

        # variavel com o script do banco, pra executar e retornar os dados
        # em uma lista
        sql = f"SELECT * FROM TB_FUNCIONARIO_FUN WHERE FUN_CPF = '{cpf}'"
        
        cursor.execute(sql)
        linha = cursor.fetchone()
        lista = [valor for valor in linha]
        return lista
    
    except pyodbc.OperationalError:
        mg.showerror(title='Erro',
        message='Não foi possivel conectar ao banco de dados.')


def mostrar_funcionario():
    """Função para mostra todos os dados da tabela funcionario"""

    try:
        # instância do método conectar_bd daa classe conexão
        conexao = conectar_bd()
        cursor = conexao.cursor()

        # variavel com o script do banco, pra executar e retornar os dados
        # em uma lista
        sql = "select * from TB_FUNCIONARIO_FUN"

        cursor.execute(sql)
        linha = cursor.fetchall()
        return [valor for valor in linha]
    
    except pyodbc.OperationalError:
        mg.showerror(title='Erro',
        message='Não foi possivel conectar ao banco de dados.')


def buscar_login_funcionario(login):
    """Função para buscar os dado do login do usuario"""

    try:
        # instância do método conectar_bd da classe conexão
        conexao = conectar_bd()
        cursor = conexao.cursor()

        # variavel com o script do banco, pra executar e retornar os dados
        # em uma lista
        sql = f"select FUN_NOME, FUN_LOGIN, FUN_SENHA from TB_FUNCIONARIO_FUN\
            where FUN_LOGIN = '{login}'"

        cursor.execute(sql)
        linha = cursor.fetchone()
        #return [valor for valor in linha]

        if linha == None:
            raise mg.showerror('Erro','Usuário não encontrado!')
        else:
            return [dado for dado in linha]

    except pyodbc.OperationalError:
        raise mg.showerror(title='Erro',
        message='Não foi possivel conectar ao banco de dados.')


def mostrar_cargo():
    """Função para exibir do banco de dados os cargos do funcionarios"""

    try:     
        # instância do método conectar_bd
        conexao = conectar_bd()
        cursor = conexao.cursor()

        # variavel com o script do banco, pra executar e retornar os dados
        # em uma lista
        sql = f"select CAR_CARGO from TB_CARGO_CAR"
        cursor.execute(sql)
        cargos = cursor.fetchall()
        return [cargo[0] for cargo in cargos]
    
    except pyodbc.OperationalError:
        mg.showerror(title='Erro',
        message='Não foi possivel conectar ao banco de dados.')


def pegar_id_cargo(cargo):
    """Função para pegar o id do cargo"""

    try:

        # instância do método conectar_bd
        conexao = conectar_bd()
        cursor = conexao.cursor()

        # comando para executar o script do banco de dados
        sql = f"select CAR_CODIGO from TB_CARGO_CAR where CAR_CARGO=\
            '{cargo}'"
        cursor.execute(sql)
        id_cargo = cursor.fetchone()

        return id_cargo[0]
    
    except pyodbc.OperationalError:
        mg.showerror(title='Erro',
        message='Não foi possivel conectar ao banco de dados.')


def mostrar_cargo_pelo_id(id_cargo):
    """Função para pegar o id do cargo"""

    try:

        # instância do método conectar_bd
        conexao = conectar_bd()
        cursor = conexao.cursor()

        # comando para executar o script do banco de dados
        sql = f"select CAR_CARGO from TB_CARGO_CAR where CAR_CODIGO=\
            '{id_cargo}'"
        cursor.execute(sql)
        id_cargo = cursor.fetchone()

        return id_cargo[0]
    
    except pyodbc.OperationalError:
        mg.showerror(title='Erro',
        message='Não foi possivel conectar ao banco de dados.')