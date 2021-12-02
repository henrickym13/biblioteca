from tkinter import *
from tkinter import ttk
from conexao import conectar_bd
import controle_funcionario as cf
import estado_cidade as ec
from tkinter import messagebox as mg
import pyodbc


class Funcionario:
    """classe principal da tela de cadastro de funcionario"""

    def __init__(self, master):
        """Método construtor"""       

        # configurações da tela
        janela = Toplevel(master)
        janela.transient(master)
        janela.title('Cadastro de Funcionário')
        janela.maxsize(465, 495)
        janela.minsize(465, 495)

        # centralizar o frame na tela
        screen_width = janela.winfo_screenwidth()
        screen_height = janela.winfo_screenheight()
        x_cordinate = int((screen_width/2) - (465/2))
        y_cordinate = int((screen_height/2) - (495/2))
        janela.geometry("{}x{}+{}+{}".format(465, 495, x_cordinate, y_cordinate))

        # add as labels a tela
        lbl_nome = Label(janela, text='Nome')
        lbl_nome.place(x=10, y=10)
        lbl_celular = Label(janela, text='Celular')
        lbl_celular.place(x=10, y=50)
        lbl_cpf = Label(janela, text='CPF')
        lbl_cpf.place(x=230, y=50)
        lbl_email = Label(janela, text='E-mail')
        lbl_email.place(x=10, y=90)
        lbl_endereco = Label(janela, text='Endereço')
        lbl_endereco.place(x=10, y=130)
        lbl_numero = Label(janela, text='Nº')
        lbl_numero.place(x=350, y=130)
        lbl_complemento = Label(janela, text='Complemento')
        lbl_complemento.place(x=10, y=170)
        lbl_bairro = Label(janela, text='Bairro')
        lbl_bairro.place(x=230, y=170)
        lbl_uf = Label(janela, text='UF')
        lbl_uf.place(x=10, y=210)
        lbl_cidade = Label(janela, text='Cidade')
        lbl_cidade.place(x=120, y=210)
        lbl_cep = Label(janela, text='CEP')
        lbl_cep.place(x=10, y=250)
        lbl_cargo = Label(janela, text='Cargo')
        lbl_cargo.place(x=160, y=250)        
        lbl_borda = Label(janela, borderwidth=2, relief="groove")
        lbl_borda.place(x=10, y=310, width=440, height=120)
        lbl_campo_usuario = Label(janela, text='Cadastro de usuário')
        lbl_campo_usuario.place(x=15, y=300)
        lbl_login_usuario = Label(janela, text='Login')
        lbl_login_usuario.place(x=30, y=330)
        lbl_senha_usuario = Label(janela, text='Senha')
        lbl_senha_usuario.place(x=30, y=360)
        lbl_confirmar_usuario = Label(janela, text='Confirmar')
        lbl_confirmar_usuario.place(x=30, y=390)
        lbl_status_borda = Label(janela, borderwidth=2, relief="groove")
        lbl_status_borda.place(x=335, y=330, width=100, height=80)
        lbl_status = Label(janela, text='Status')
        lbl_status.place(x=340, y=320)

        # adicionando os campos entry a janela
        self.txt_nome = Entry(janela)
        self.txt_nome.place(x=10, y=30, width=440, height=20)
        self.txt_celular = Entry(janela)
        self.txt_celular.place(x=10, y=70, width=200, height=20)
        self.txt_cpf = Entry(janela)
        self.txt_cpf.place(x=230, y=70, width=220, height=20)
        self.txt_email = Entry(janela)
        self.txt_email.place(x=10, y=110, width=440, height=20)
        self.txt_endereco = Entry(janela)
        self.txt_endereco.place(x=10, y=150, width=320, height=20)
        self.txt_numero = Entry(janela)
        self.txt_numero.place(x=350, y=150, width=100, height=20)
        self.txt_complemento = Entry(janela)
        self.txt_complemento.place(x=10, y=190, width=200, height=20)
        self.txt_bairro = Entry(janela)
        self.txt_bairro.place(x=230, y=190, width=220, height=20)
        self.txt_cep = Entry(janela)
        self.txt_cep.place(x=10, y=270, width=130, height=20)
        self.txt_login_usuario = Entry(janela)
        self.txt_login_usuario.place(x=100, y=330, width=210, height=20)
        self.txt_senha_usuario = Entry(janela)
        self.txt_senha_usuario.place(x=100, y=360, width=210, height=20)
        self.txt_confirmar_usuario = Entry(janela)
        self.txt_confirmar_usuario.place(x=100, y=390, width=210, height=20)

        # adicionando o combobox a tela
        self.cbox_uf = ttk.Combobox(janela, state='readonly',
        postcommand=self.exibir_estado)
        self.cbox_uf.place(x=10, y=230, width=90)

        self.cbox_cidade = ttk.Combobox(janela, state='readonly',
        postcommand=lambda: self.exibir_cidade(self.cbox_uf.get()))
        self.cbox_cidade.place(x=120, y=230, width=330)

        self.cbox_cargo = ttk.Combobox(janela, state='readonly',
        postcommand=self.exibir_cargo)
        self.cbox_cargo.place(x=160, y=270, width=290)


        # adicionando Button a tela
        btn_salvar = Button(janela, text='Gravar Dados',
        command=self.pegar_informacoes_campos)
        btn_salvar.place(x=10, y=440, width=130, height=40)

        btn_limpar = Button(janela, text='Limpar Campos',
        command=self.limpar_campos)
        btn_limpar.place(x=165, y=440, width=130, height=40)

        btn_cancelar = Button(janela, text='Cancelar',
        command=lambda: self.fechar_janela(janela))
        btn_cancelar.place(x=320, y=440, width=130, height=40)

        # adicionando Radiobutton a tela e uma variavel para a escolha
        self.opcao = IntVar()
        self.radio1 = Radiobutton(janela, text='Ativo', value=1,
        var=self.opcao)
        self.radio1.place(x=355, y=340)
        self.radio2 = Radiobutton(janela, text='Inativo', value=2,
        var=self.opcao)
        self.radio2.place(x=355, y=370)

        # manter a janela em loop
        janela.mainloop()


    def limpar_cbox_cidade(self):
        """Método para limpar a cbox_cidade"""
        self.cbox_cidade.set(' ')


    def exibir_estado(self):
        """Método para exibir os estados"""

        # chamar o método limprar cbox toda vez que
        # o usuario for selecionar um estado
        self.limpar_cbox_cidade()

        # chamar a unção e passar o valor para o cbox
        estados = ec.mostrar_estado()
        self.cbox_uf.configure(values=estados)

    
    def exibir_cidade(self, estado):
        """Método para exibir as cidades a partir do estado selecionado"""

        if len(estado) <= 0:
            raise mg.showerror('Error', 'Selecione primeiro um Estado')
        else:
            cidades = ec.mostrar_cidade(estado)
            self.cbox_cidade.config(values=cidades)
    

    def exibir_cargo(self):
        """Método para exibir os cargos"""

        cargos = cf.mostrar_cargo()
        self.cbox_cargo.configure(values=cargos)


    def verificar_senha(self):
        """Verifica se a senha são as mesmas"""

        if self.txt_senha_usuario.get() == self.txt_confirmar_usuario.get():
            return self.txt_senha_usuario.get()
        else:
            raise mg.showerror(title='Erro', 
            message='Senha e confirmação de senha são diferentes!')
    
    
    def varidar_escolha_ativo_inativo(self):
        """Verifica qual radiobutton foi selecionado"""

        escolha = self.opcao.get()
        if escolha == 1:
            return True
        else:
            return False
    

    def pegar_informacoes_campos(self):
        """Método para pegar todas as informações inseridas nos campos
        de texto e combobox para pode gravar no banco"""

        # instância do métodos
        confirma_senha = self.verificar_senha()
        escolha = self.varidar_escolha_ativo_inativo()

        # chamar o metodo do pacote controle_funcionario para fazer a
        # verificação dos campos
        cf.verificar_campos_vazios(self.txt_nome.get(), self.txt_celular.get(),
        self.txt_cpf.get(), self.txt_email.get(), self.txt_endereco.get(),
        self.txt_numero.get(), self.txt_complemento.get(), self.txt_bairro.get(),
        self.cbox_cidade.get(), self.txt_cep.get(), self.cbox_cargo.get(),
        self.txt_login_usuario.get(), confirma_senha, escolha)

        # chamada do método para apagar os campos logos apos o cadastro
        # ser feito
        self.limpar_campos()
    

    def limpar_campos(self):
        """Método para limpar os campos preenchidos"""

        self.txt_nome.delete(0, END)
        self.txt_celular.delete(0, END)
        self.txt_cpf.delete(0, END)
        self.txt_email.delete(0, END)
        self.txt_endereco.delete(0, END)
        self.txt_numero.delete(0, END)
        self.txt_complemento.delete(0, END)
        self.txt_bairro.delete(0, END)
        self.txt_cep.delete(0, END)
        self.txt_login_usuario.delete(0,END)
        self.txt_senha_usuario.delete(0, END)
        self.txt_confirmar_usuario.delete(0, END)
        self.cbox_cargo.set(' ')
        self.cbox_cidade.set(' ')
        self.cbox_uf.set(' ')
        self.opcao.set(False)
    

    def fechar_janela(self, frame):
        """Método para fechar a janela ao pressionar o button cancelar"""

        frame.destroy()

if __name__ == '__main__':
    Funcionario()