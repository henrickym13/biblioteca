from tkinter import messagebox as mg

def validar_email(email):
    """Função para verificar se o email é valido"""
    
    letras_maiusculas = [chr(x) for x in range(ord('a'), ord('z') + 1)]
    simbolos_permitidos = [i for i in email if i not in letras_maiusculas]

    if simbolos_permitidos != ['@', '.']:
        raise mg.showerror(title='Erro', 
                message='E-mail inválido')