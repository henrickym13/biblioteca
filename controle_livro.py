import pyodbc
from conexao import conectar_bd
from tkinter import messagebox as mg


def verificar_campos_vazios(nome, ano, exemplares, identificacao,
autor, editora, valor, genero):
    """Verifica sem ha algum campo vazio"""

    # passando os parametros da função para um dict
    # para exibir para o usuario o campo que estive vazio
    campos_obrigatorios = [nome, ano, exemplares, identificacao, autor,
    editora, valor, genero]

    for item in campos_obrigatorios:
        if item == ' ':
            raise mg.showerror(title='Error', message='Campos obrigatórios vazio')
    else:
        validar_dados_livro(nome, ano, exemplares, identificacao,
        autor, editora, valor, genero)


def validar_dados_livro(nome, ano, exemplares, identificacao, autor,
editora, valor, genero):
    """Verificar se os dados estão corretos"""

    try:
        # verificar se o livro ja esta no sistema
        verificar_cadastro_livro(identificacao)

        # pegar o id do genero do livro
        id_genero = busca_id_genero(genero)

        gravar_dados_livro(str(nome), str(ano), str(exemplares), 
        str(identificacao), str(autor), str(editora),
        float(valor), id_genero)

    except TypeError:
        mg.showerror(title='Erro', message='Formato de dado inválido!')
    
    except ValueError:
        mg.showerror(title='Erro', message='Valor inválido!')


def gravar_dados_livro(nome, ano, exemplares, identificacao, autor,
editora, valor, genero):
    """Função para gravar os dados obrigatorios no banco de dados"""

    try:

        # instância da classe conectar_bd
        conexao = conectar_bd()
        cursor = conexao.cursor()

        sql = f"INSERT INTO TB_LIVRO_LIV VALUES ('{nome}', '{ano}',\
                '{exemplares}', '{'0'}','{identificacao}',\
                '{autor}','{editora}','{valor}','{genero}')"

        # commit para que não ocorra um erro quando varias pessoas
        # estiverem tentando grava os dados no mesmo banco
        cursor.execute(sql)
        conexao.commit()

        # exibir mensagem de sucesso
        mg.showinfo(title='Sucesso', message='Dados gravados com sucesso!')

    except pyodbc.DataError:
        mg.showerror(title='Erro', message='Formato de dado inválido!')
    
    except pyodbc.OperationalError:
        raise mg.showerror(title='Erro',
        message='Não foi possivel conectar ao banco de dados.')
    
    finally:
        conexao.close()


def atualizar_dados_livro(nome, ano, exemplares, identificacao, autor,
editora, valor, codigo):
    """Função para atualizar os dados"""

    try:

        # instância da classe conectar_bd
        conexao = conectar_bd()
        cursor = conexao.cursor()

        sql = f"update TB_LIVRO_LIV set \
            LIV_ANO = '{ano}',\
            LIV_EXEMPLARES = '{exemplares}',\
            LIV_IDENTIFICACAO = '{identificacao}',\
            LIV_AUTOR = '{autor}',\
            LIV_EDITORA = '{editora}',\
            LIV_VALOR = '{valor}',\
            GEN_CODIGO = '{codigo}' \
            where LIV_NOME = '{nome}'"

        # commit para que não ocorra um erro quando varias pessoas
        # estiverem tentando grava os dados no mesmo banco
        cursor.execute(sql)
        conexao.commit()
        
        # exibir mensagem na tela
        mg.showinfo(title='Sucesso',
        message='Dados atualizados com sucesso!')
    
    except TypeError:
        mg.showerror('Erro', 'Formato de dado inválido!')

    except pyodbc.DataError:
        mg.showerror(title='Erro', message='Formato de dado inválido!')
    
    except pyodbc.OperationalError:
        raise mg.showerror(title='Erro',
        message='Não foi possivel conectar ao banco de dados.')
    
    finally:
        conexao.close()


def verificar_cadastro_livro(indetificacao):
    """Verificar se o livro ja está cadastrado no sistema"""

    try:
        # instância do método conectar_bd da classe conexão
        conexao = conectar_bd()
        cursor = conexao.cursor()

        sql = f"select LIV_IDENTIFICACAO from TB_LIVRO_LIV\
            where LIV_IDENTIFICACAO = '{indetificacao}'"
        cursor.execute(sql)
        linha = cursor.fetchone()

        # verifica se o cliente está cadastro no sistema
        # caso não esteja a variavel linha retorna None
        if linha == None:
            pass
        else:
            if linha[0] == indetificacao:
                raise mg.showerror(title='Erro', 
                message='Livro já está cadastrado no sistema!')
    
    except pyodbc.OperationalError:
        raise mg.showerror(title='Erro',
        message='Não foi possivel conectar ao banco de dados.')


def mostrar_livro():
    """Função para mostra todos os dados da tabela livro"""

    try:
        # instância do método conectar_bd daa classe conexão
        conexao = conectar_bd()
        cursor = conexao.cursor()

        # executar comando sql e retorna os dados em uma lista
        sql = "select * from TB_LIVRO_LIV"
        cursor.execute(sql)
        linha = cursor.fetchall()
        return [valor for valor in linha]
    
    except pyodbc.OperationalError:
        raise mg.showerror(title='Erro',
        message='Não foi possivel conectar ao banco de dados.')


def buscar_livro_codigo(identificacao):
    """Função para buscar o livro no banco de dados pelo seu ISRB"""

    try:
        # instância do método conectar_bd daa classe conexão
        conexao = conectar_bd()
        cursor = conexao.cursor()

        # executar os comando do sql e retorna os valores em lista
        sql = f"select * from TB_LIVRO_LIV where LIV_IDENTIFICACAO =\
         '{identificacao}'"
        cursor.execute(sql)
        linha = cursor.fetchone()

        # verificar se retornou algum dado ou none
        if linha == None:
            raise TypeError(mg.showerror('Erro', 'Livro não encontrado!'))
        else:
            return linha

    except pyodbc.OperationalError:
        raise mg.showerror(title='Erro',
        message='Não foi possivel conectar ao banco de dados.')


def buscar_livro_nome(nome):
    """Função para buscar o livro no banco de dados pelo seu nome"""

    try:
        # instância do método conectar_bd daa classe conexão
        conexao = conectar_bd()
        cursor = conexao.cursor()

        # executar o comando do sql e retornar os dados e uma lista
        sql = f"select * from TB_LIVRO_LIV where LIV_NOME =\
         '{nome}'"
        cursor.execute(sql)
        linha = cursor.fetchone()
        
        # verificar se retornou algum dado ou none
        if linha == None:
            raise TypeError(mg.showerror('Erro', 'Livro não encontrado!'))
        else:
            return linha
    
    except pyodbc.OperationalError:
        raise mg.showerror(title='Erro',
        message='Não foi possivel conectar ao banco de dados.')


def buscar_livro_nome_autor(nome_autor):
    """Função para buscar o livro no banco de dados pelo seu nome"""

    try:
        # instância do método conectar_bd daa classe conexão
        conexao = conectar_bd()
        cursor = conexao.cursor()

        # executar comando sql e retornar os valores em uma lista
        sql = f"select * from TB_LIVRO_LIV where LIV_AUTOR =\
        '{nome_autor}'"
        cursor.execute(sql)
        linha = cursor.fetchall()

        if len(linha) <= 0:
            raise TypeError(mg.showerror('Error', 'Não encontrado!')) 
        else:
            return [valor for valor in linha]

    except pyodbc.OperationalError:
        raise mg.showerror(title='Erro',
        message='Não foi possivel conectar ao banco de dados.')


def exibir_genero_livro():
    """Função para exibir todos os generos de livro gravado no bd"""

    try:
        # instancia da classe conexão
        conexao = conectar_bd()
        cursor = conexao.cursor()

        # chamando a query do banco de dados, passando para uma variavel
        # e executando o comando para trazer os dados do banco
        sql = f"select GEN_GENERO from TB_GENERO_GEN "
        cursor.execute(sql)
        generos = cursor.fetchall()

        # passando os dados para cbox_cidade
        return [genero[0] for genero in generos]
        
    except pyodbc.OperationalError:
        raise mg.showerror(title='Erro',
        message='Não foi possivel conectar ao banco de dados.')
        

def busca_id_genero(genero):
    """Método para buscar o id do genero no banco de dados"""

    try:
        # instância do método conectar_bd do pacote conexão
        conexao = conectar_bd()
        cursor = conexao.cursor()
        
        # comando para buscar e retornar o id do estado
        sql = f"select GEN_CODIGO from TB_GENERO_GEN where GEN_GENERO =\
        '{genero}'"
        cursor.execute(sql)
        id_genero = cursor.fetchone()

        # chamada do método para converter o tipo de dado e retornar o valor
        return id_genero[0]
        
    except pyodbc.OperationalError:
        raise mg.showerror(title='Erro',
        message='Não foi possivel conectar ao banco de dados.')


def busca_genero_pelo_id(genero):
    """Método para buscar o genero do livro pelo id no banco de dados"""

    try:
        # instância do método conectar_bd do pacote conexão
        conexao = conectar_bd()
        cursor = conexao.cursor()
        
        # comando para buscar e retornar o id do estado
        sql = f"select GEN_GENERO from TB_GENERO_GEN where GEN_CODIGO =\
        '{genero}'"
        cursor.execute(sql)
        id_genero = cursor.fetchone()

        # chamada do método para converter o tipo de dado e retornar o valor
        return id_genero[0]
        
    except pyodbc.OperationalError:
        raise mg.showerror(title='Erro',
        message='Não foi possivel conectar ao banco de dados.')
