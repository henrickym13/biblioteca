from datetime import datetime
from pytz import timezone

def exibir_data():
    """Função para exibir a data e hora no fuso horario de São Paulo"""
    lista_semana = ['Segunda-feira', 'Terça-feira', 'Quarta-feira', 'Quinta-feira',
    'Sexta-feira', 'Sábado', 'Domingo']
    data_e_hora_atuais = datetime.now()
    fuso_horario = timezone('America/Sao_Paulo')
    data_e_hora_sao_paulo = data_e_hora_atuais.astimezone(fuso_horario)
    data_e_hora_sao_paulo_em_texto = data_e_hora_sao_paulo.strftime('%d/%m/%Y %H:%M')

    return f'{lista_semana[data_e_hora_atuais.weekday()]}, {data_e_hora_sao_paulo_em_texto}'


def data():
    """Função para exibir apenas a data"""

    hoje = datetime.now()
    return hoje.strftime('%d/%m%Y')
