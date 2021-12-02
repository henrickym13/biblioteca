from conexao import conectar_bd
from datetime import datetime
from random import randint
from tkinter import messagebox as mg
import pyodbc


def buscar_livro(codigo):
    """Funçao para buscar o livro no sistema e exibir informaçoes"""

    try:
        # instância do método conectar_bd da classe conexão
        conexao = conectar_bd()
        cursor = conexao.cursor()

        # executar comando sql e retornar os dados em uma lista
        sql = f"select LIV_NOME, LIV_VALOR, LIV_AUTOR, LIV_EXEMPLARES,\
            LIV_EMPRESTADOS from TB_LIVRO_LIV where LIV_IDENTIFICACAO =\
            '{codigo}'"
        cursor.execute(sql)
        linha = cursor.fetchone()
        linha_conv = [x for x in linha]

        return linha_conv

    
    except pyodbc.Error as ex:
        sqlstate = ex.args[0]
        if sqlstate == '08001':
            mg.showerror(title='Erro', 
            message='Nao foi possivel conectar ao banco de dados.')


def buscar_cliente(cpf):
    """Função para buscar os dados do cliente no banco de dados"""

    try:

        # instância do método conectar_bd daa classe conexão
        conexao = conectar_bd()
        cursor = conexao.cursor()

        # comando sql para retornar os dados do bf em uma lista
        sql = f"SELECT CLI_NOME, CLI_STATUS FROM TB_CLIENTE_CLI WHERE\
                CLI_CPF = '{cpf}'"
        cursor.execute(sql)
        linha = cursor.fetchone()
        linha_conv = [x for x in linha]

        return linha_conv
        
    
    except pyodbc.OperationalError:
        mg.showerror(title='Erro', 
            message='Não foi possivel conectar ao banco de dados!')


def gerar_numero_protocolo():
    """Funçao pra gerar o numero de protocolo do emprestimo"""

    ano_corrente = datetime.now()
    numeros = randint(0,10**13)
    protocolo = f'{ano_corrente.year}{numeros}'
    return str(protocolo)


def gerar_emprestimo(data_emprestimo, data_entrega, protocolo, cod_livro,
cod_cliente):
    """Função para gravar o emprestimo no banco de dados"""

    try:
        # instância do método conectar_bd da classe conexão
        conexao = conectar_bd()
        cursor = conexao.cursor()

        # comando sql para execurtar o empréstimo e gravar no bd
        sql = f"INSERT INTO TB_EMPRESTIMO_EMP (EMP_DATAEMPRESTIMO,\
        EMP_DATADEVOLUCAO, EMP_STATUS, EMP_NUMEROEMPRESTIMO, EMP_VALOR,\
        LIV_CODIGO, CLI_CODIGO) VALUES (\
        '{data_emprestimo}', '{data_entrega}', 'Emprestado',\
        '{protocolo}', '10.00', '{cod_livro}', '{cod_cliente}')"
        cursor.execute(sql)
        cursor.commit()

        # exibir mensagem de suceso
        mg.showinfo(title='Sucesso', 
        message='Emprestimo realizado com sucesso!')
    
    except pyodbc.OperationalError:
        mg.showerror(title='Erro',
        message='Não foi possivel efetuar o empréstimo!')
    
    finally:
        conexao.close()


def buscar_id_cliente(cpf):
    """Função para buscar o id do cliente, afinal o id é usado para gerar um
    novo empréstimo"""

    try:
        # instância do método conectar_bd da classe conexão
        conexao = conectar_bd()
        cursor = conexao.cursor()

        # comando sql para retornar o valor do bd em uma lista
        sql = f"select CLI_CODIGO from TB_CLIENTE_CLI where CLI_CPF=\
            '{cpf}'"
        cursor.execute(sql)
        linha = cursor.fetchone()

        if linha == None:
            raise TypeError(mg.showerror(title='Erro',
            message='Não foi possivel encontrar o CPF!'))
        else:
            return linha[0]

    except pyodbc.OperationalError:
        mg.showerror(title='Erro',
        message='Não foi possivel conectar ao banco de dados.')
        


def buscar_id_livro(identificacao):
    """Função para buscar o id do cliente, afinal o id é usado para gerar um
    novo empréstimo"""

    try:
        # instância do método conectar_bd da classe conexão
        conexao = conectar_bd()
        cursor = conexao.cursor()

        # comando sql para retornar os valores do bd em uma lista
        sql = f"select LIV_CODIGO from TB_LIVRO_LIV where LIV_IDENTIFICACAO =\
            '{identificacao}'"
        cursor.execute(sql)
        linha = cursor.fetchone()

        if linha == None:
            raise TypeError(mg.showerror('Erro', 'Livro não encontrado!'))
        else:
            return linha[0]

    except pyodbc.OperationalError:
        mg.showerror(title='Erro',
        message='Não foi possivel conectar ao banco de dados.')


def exibir_emprestimos():
    """Função para exibir dados da tabela emprestimo"""

    try:
        # instância do método conectar_bd da classe conexão
        conexao = conectar_bd()
        cursor = conexao.cursor()

        # comando sql para retornar os valoresdo bd em uma lista
        sql = 'select e.EMP_NUMEROEMPRESTIMO, e.EMP_DATAEMPRESTIMO,\
        e.EMP_DATADEVOLUCAO, e.EMP_STATUS, e.EMP_OBSERVACAO,\
        c.CLI_CPF, c.CLI_NOME, l.LIV_IDENTIFICACAO, l.LIV_NOME,\
        e.EMP_VALOR from TB_EMPRESTIMO_EMP e \
        inner join TB_CLIENTE_CLI c on e.CLI_CODIGO = c.CLI_CODIGO \
        inner join TB_LIVRO_LIV l on e.LIV_CODIGO = l.LIV_CODIGO'
    
        # comando para executar a consultar
        cursor.execute(sql)
        linha = cursor.fetchall()
        return [valor for valor in linha]
    
    except pyodbc.OperationalError:
        mg.showerror(title='Erro',
        message='Não foi possivel conectar ao banco de dados.')


def exibir_emprestimo_opcao(escolha):
    """Função para mostrar o o livros emprestados por uma escolha
    entre Emprestado e Devolvido"""

    try:
        # instância do método conectar_bd da classe conexão
        conexao = conectar_bd()
        cursor = conexao.cursor()

        # variavel do comando para consulta no bd
        sql = f"select e.EMP_NUMEROEMPRESTIMO, e.EMP_DATAEMPRESTIMO,\
        e.EMP_DATADEVOLUCAO, e.EMP_STATUS, e.EMP_OBSERVACAO,\
        c.CLI_CPF, c.CLI_NOME, l.LIV_IDENTIFICACAO, l.LIV_NOME,\
        e.EMP_VALOR from TB_EMPRESTIMO_EMP e \
        inner join TB_CLIENTE_CLI c on e.CLI_CODIGO = c.CLI_CODIGO \
        inner join TB_LIVRO_LIV l on e.LIV_CODIGO = l.LIV_CODIGO \
        where e.EMP_STATUS = '{escolha}'"
    
        # comando para executar a consultar e retornar em uma lista
        cursor.execute(sql)
        linha = cursor.fetchall()
        return [valor for valor in linha]
    
    except pyodbc.OperationalError:
        mg.showerror(title='Erro',
        message='Não foi possivel conectar ao banco de dados.')


def atualizar_status_emprestimo(num_emprestimo, valor, obs= ' '):
    """Função para atualizar o status do emprestimo com o livro em
    perfeito estado"""

    try:
        # instância do método conectar_bd da classe conexão
        conexao = conectar_bd()
        cursor = conexao.cursor()

        # comando sql para executar o update na tabela do bd
        sql = f"update TB_EMPRESTIMO_EMP set \
        EMP_STATUS = 'Devolvido',\
        EMP_OBSERVACAO = '{obs}',\
        EMP_VALOR = '{valor}' \
        where EMP_NUMEROEMPRESTIMO = '{num_emprestimo}'"
    
        # commit para que não ocorra um erro quando varias pessoas
        # estiverem tentando grava os dados no mesmo banco
        cursor.execute(sql)
        conexao.commit()

        # mensagem de operação realizada com sucesso
        mg.showinfo(title='Sucesso',
        message='Devolução realizada com sucesso!')

    except pyodbc.OperationalError:
        mg.showerror(title='Erro',
        message='Não foi possivel conectar ao banco de dados.')


def buscar_emprestimo_numero(n_emprestimo):
    """Função para buscar o dado do emprestimo por numero de
    protocolo"""

    try:
        # instância do método conectar_bd da classe conexão
        conexao = conectar_bd()
        cursor = conexao.cursor()

        # comando sql para exibir os dados da tabela do bd
        sql = f"select e.EMP_NUMEROEMPRESTIMO, e.EMP_DATAEMPRESTIMO,\
            e.EMP_DATADEVOLUCAO, e.EMP_STATUS, e.EMP_OBSERVACAO,\
            c.CLI_CPF, c.CLI_NOME, l.LIV_IDENTIFICACAO, l.LIV_NOME,\
            e.EMP_VALOR from TB_EMPRESTIMO_EMP e \
            inner join TB_CLIENTE_CLI c on e.CLI_CODIGO = c.CLI_CODIGO \
            inner join TB_LIVRO_LIV l on e.LIV_CODIGO = l.LIV_CODIGO \
            where e.EMP_NUMEROEMPRESTIMO = '{n_emprestimo}'"

        # executar o comando e passar para uma lista
        cursor.execute(sql)
        linha = cursor.fetchone()
        
        if linha == None:
            raise TypeError(mg.showerror('Error', 'Não encontrado!')) 
        else:
            return linha
    
    except pyodbc.Error as ex:
        sqlstate = ex.args[0]
        if sqlstate == '22018':
            mg.showerror(title='Erro', message='Falha ao converter os dados')
    
    except pyodbc.OperationalError:
        mg.showerror(title='Erro',
        message='Não foi possivel conectar ao banco de dados.')


def buscar_emprestimo_codigo_livro(cod_livro):
    """Função para buscar o emprestimo pelo codigo do livro"""

    try:
        # instância do método conectar_bd da classe conexão
        conexao = conectar_bd()
        cursor = conexao.cursor()

        # chamada da função para pegar o id do livro
        id_livro = buscar_id_livro(cod_livro)

        # comando sql para realizar a consultar no bd
        sql = f"select e.EMP_NUMEROEMPRESTIMO, e.EMP_DATAEMPRESTIMO,\
            e.EMP_DATADEVOLUCAO, e.EMP_STATUS, e.EMP_OBSERVACAO,\
            c.CLI_CPF, c.CLI_NOME, l.LIV_IDENTIFICACAO, l.LIV_NOME,\
            e.EMP_VALOR from TB_EMPRESTIMO_EMP e \
            inner join TB_CLIENTE_CLI c on e.CLI_CODIGO = c.CLI_CODIGO \
            inner join TB_LIVRO_LIV l on e.LIV_CODIGO = l.LIV_CODIGO \
            where e.LIV_CODIGO = '{id_livro}'"

        # executar o comando e passar para uma lista
        cursor.execute(sql)
        linha = cursor.fetchall()

        # caso não encontre o livro ele retorna None
        if len(linha) <= 0:
            raise TypeError(mg.showerror('Error', 'Não encontrado!')) 
        else:
            return [valor for valor in linha]   
    
    except pyodbc.Error as ex:
        sqlstate = ex.args[0]
        if sqlstate == '22018':
            mg.showerror(title='Erro', message='Falha ao converter os dados!')
        

def buscar_emprestimo_cpf_cliente(cpf):
    """Função para buscar o emprestimo pelo codigo do livro"""

    try:
        # instância do método conectar_bd da classe conexão
        conexao = conectar_bd()
        cursor = conexao.cursor()

        # comando sql para realizar a consultar no bd
        sql = f"select e.EMP_NUMEROEMPRESTIMO, e.EMP_DATAEMPRESTIMO,\
        e.EMP_DATADEVOLUCAO, e.EMP_STATUS, e.EMP_OBSERVACAO,\
        c.CLI_CPF, c.CLI_NOME, l.LIV_IDENTIFICACAO, l.LIV_NOME,\
        e.EMP_VALOR from TB_EMPRESTIMO_EMP e \
        inner join TB_CLIENTE_CLI c on e.CLI_CODIGO = c.CLI_CODIGO \
        inner join TB_LIVRO_LIV l on e.LIV_CODIGO = l.LIV_CODIGO \
        where c.CLI_CPF = '{cpf}'"

        # executar o comando e passar para uma lista
        cursor.execute(sql)
        linha = cursor.fetchall()

        # para caso retorne None, se não achar o cpf
        if len(linha) <= 0:
            raise TypeError(mg.showerror('Error', 'Não encontrado!')) 
        else:
            return [valor for valor in linha]
    
    except pyodbc.Error as ex:
        sqlstate = ex.args[0]
        if sqlstate == '22018':
            mg.showerror(title='Erro', message='Falha ao converter os dados')
