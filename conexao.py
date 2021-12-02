import pyodbc

def conectar_bd():
    """Função para se conectar ao BD"""

    string_conexao = ('Driver={SQL Server Native Client 11.0};'
                      'Server=DESKTOP-UD03IMO\SQLEXPRESS2;'
                      'Database=Biblioteca;'
                      'Trusted_Connection=yes;')

    return pyodbc.connect(string_conexao)
