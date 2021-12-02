from conexao import conectar_bd
from tkinter import messagebox as mg
import pyodbc


def mostrar_estado():
    """Função para mostrar todos os estados gravados no banco de dados"""

    try:
        # instância do método conectar_bd
        conexao = conectar_bd()
        cursor = conexao.cursor()

        sql = f"select EST_ESTADO from TB_ESTADO_EST "

        cursor.execute(sql)
        estados = cursor.fetchall()
        return [estado[0] for estado in estados]
    
    except pyodbc.OperationalError:
        mg.showerror(title='Erro',
        message='Não foi possivel conectar ao banco de dados.')


def mostrar_cidade(estado):
    """Função para mostrar todas as cidades de um determinado estado"""
    try:

        # instância do método conectar_bd
        conexao = conectar_bd()
        cursor = conexao.cursor()

        # comando para executar o script do banco de dados
        sql = f"select CID_CIDADE from TB_CIDADE_CID where EST_CODIGO IN(\
            select EST_CODIGO from TB_ESTADO_EST where EST_ESTADO = \
                '{estado}')"
        cursor.execute(sql)
        cidades = cursor.fetchall()

        return [cidade[0] for cidade in cidades]
    
    except pyodbc.OperationalError:
        mg.showerror(title='Erro',
        message='Não foi possivel conectar ao banco de dados.')


def pegar_id_cidade(cidade):
    """Função para pegar o id da cidade"""

    try:

        # instância do método conectar_bd
        conexao = conectar_bd()
        cursor = conexao.cursor()

        # comando para executar o script do banco de dados
        sql = f"select CID_CODIGO from TB_CIDADE_CID where CID_CIDADE=\
            '{cidade}'"
        cursor.execute(sql)
        id_cidade = cursor.fetchone()
        
        return id_cidade[0]
    
    except pyodbc.OperationalError:
        mg.showerror(title='Erro',
        message='Não foi possivel conectar ao banco de dados.')


def exibir_estado_pela_cidade(cidade):
    """Exibir o estado a partir do id da cidade gravado no banco
    de dados"""

    try:

        # instância do método conectar_bd
        conexao = conectar_bd()
        cursor = conexao.cursor()

        # comando para executar o script do banco de dados
        sql = f"select EST_ESTADO from TB_ESTADO_EST where EST_CODIGO in(\
            select EST_CODIGO from TB_CIDADE_CID where CID_CIDADE =\
            '{cidade}')"
        cursor.execute(sql)
        estado = cursor.fetchone()
        
        return estado[0]
    
    except pyodbc.OperationalError:
        mg.showerror(title='Erro',
        message='Não foi possivel conectar ao banco de dados.')


def mostrar_cidade_pelo_id(id_cidade):
    """Função para exibir a cidade a partir do id"""

    try:

        # instância do método conectar_bd
        conexao = conectar_bd()
        cursor = conexao.cursor()

        # comando para executar o script do banco de dados
        sql = f"select CID_CIDADE from TB_CIDADE_CID where CID_CODIGO=\
            '{id_cidade}'"
        cursor.execute(sql)
        cidade = cursor.fetchone()
        
        return cidade[0]
    
    except pyodbc.OperationalError:
        mg.showerror(title='Erro',
        message='Não foi possivel conectar ao banco de dados.')
