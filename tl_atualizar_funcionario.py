from tkinter import *
from tkinter import ttk
import controle_funcionario as cf
from tkinter import messagebox as mg
import estado_cidade as ec


class ConsultaFuncionario:
    """Classe da tela de consultar e alterar cadastro de funcionario"""

    def __init__(self, master):
        """Método construtor"""

        # configurações da tela
        janela = Toplevel(master)
        janela.transient(master)
        janela.title('Atualizar dados Funcionário')
        janela.maxsize(865, 495)
        janela.minsize(865, 495)
    
        # centralizar o frame na tela
        screen_width = janela.winfo_screenwidth()
        screen_height = janela.winfo_screenheight()
        x_cordinate = int((screen_width/2) - (865/2))
        y_cordinate = int((screen_height/2) - (495/2))
        janela.geometry("{}x{}+{}+{}".format(865, 495, x_cordinate, y_cordinate))

        # add as labels a tela
        lbl_nome = Label(janela, text='Nome')
        lbl_nome.place(x=410, y=10)
        lbl_celular = Label(janela, text='Celular')
        lbl_celular.place(x=410, y=50)
        lbl_cpf = Label(janela, text='CPF')
        lbl_cpf.place(x=630, y=50)
        lbl_email = Label(janela, text='E-mail')
        lbl_email.place(x=410, y=90)
        lbl_endereco = Label(janela, text='Endereço')
        lbl_endereco.place(x=410, y=130)
        lbl_numero = Label(janela, text='Nº')
        lbl_numero.place(x=750, y=130)
        lbl_complemento = Label(janela, text='Complemento')
        lbl_complemento.place(x=410, y=170)
        lbl_bairro = Label(janela, text='Bairro')
        lbl_bairro.place(x=630, y=170)
        lbl_uf = Label(janela, text='UF')
        lbl_uf.place(x=410, y=210)
        lbl_cidade = Label(janela, text='Cidade')
        lbl_cidade.place(x=520, y=210)
        lbl_cep = Label(janela, text='CEP')
        lbl_cep.place(x=410, y=250)
        lbl_cargo = Label(janela, text='Cargo')
        lbl_cargo.place(x=560, y=250)        
        lbl_borda = Label(janela, borderwidth=2, relief="groove")
        lbl_borda.place(x=410, y=310, width=440, height=120)
        lbl_campo_usuario = Label(janela, text='Cadastro de usuário')
        lbl_campo_usuario.place(x=415, y=300)
        lbl_login_usuario = Label(janela, text='Login')
        lbl_login_usuario.place(x=430, y=330)
        lbl_senha_usuario = Label(janela, text='Senha')
        lbl_senha_usuario.place(x=430, y=360)
        lbl_confirmar_usuario = Label(janela, text='Confirmar')
        lbl_confirmar_usuario.place(x=430, y=390)
        lbl_status_borda = Label(janela, borderwidth=2, relief="groove")
        lbl_status_borda.place(x=735, y=330, width=100, height=80)
        lbl_status = Label(janela, text='Status')
        lbl_status.place(x=740, y=320)
        lbl_buscar_cpf = Label(janela,text='CPF:')
        lbl_buscar_cpf.place(x=10, y=30)

        # adicionando os campos entry a janela
        self.txt_nome = Entry(janela)
        self.txt_nome.place(x=410, y=30, width=440, height=20)
        self.txt_celular = Entry(janela)
        self.txt_celular.place(x=410, y=70, width=200, height=20)
        self.txt_cpf = Entry(janela)
        self.txt_cpf.place(x=630, y=70, width=220, height=20)
        self.txt_email = Entry(janela)
        self.txt_email.place(x=410, y=110, width=440, height=20)
        self.txt_endereco = Entry(janela)
        self.txt_endereco.place(x=410, y=150, width=320, height=20)
        self.txt_numero = Entry(janela)
        self.txt_numero.place(x=750, y=150, width=100, height=20)
        self.txt_complemento = Entry(janela)
        self.txt_complemento.place(x=410, y=190, width=200, height=20)
        self.txt_bairro = Entry(janela)
        self.txt_bairro.place(x=630, y=190, width=220, height=20)
        self.txt_cep = Entry(janela)
        self.txt_cep.place(x=410, y=270, width=130, height=20)
        self.txt_login_usuario = Entry(janela)
        self.txt_login_usuario.place(x=500, y=330, width=210, height=20)
        self.txt_senha_usuario = Entry(janela)
        self.txt_senha_usuario.place(x=500, y=360, width=210, height=20)
        self.txt_confirmar_usuario = Entry(janela)
        self.txt_confirmar_usuario.place(x=500, y=390, width=210, height=20)
        self.txt_buscar_cpf = Entry(janela)
        self.txt_buscar_cpf.place(x=60, y=30, width=160, height=20)

        # adicionando o combobox a tela
        self.cbox_uf = ttk.Combobox(janela, state='readonly',
        postcommand=self.exibir_estado)
        self.cbox_uf.place(x=410, y=230, width=90)

        self.cbox_cidade = ttk.Combobox(janela, state='readonly',
        postcommand=lambda: self.exibir_cidade(self.cbox_uf.get()))
        self.cbox_cidade.place(x=520, y=230, width=330)

        self.cbox_cargo = ttk.Combobox(janela, state='readonly',
        postcommand=self.exibir_cargo)
        self.cbox_cargo.place(x=560, y=270, width=290)

        # adicionando os botões a tela
        btn_salvar = Button(janela, text='Atualizar Dados',
        command=self.pegar_informacoes_campos)
        btn_salvar.place(x=410, y=440, width=130, height=40)

        btn_limpar = Button(janela, text='Limpar Campos',
        command=self.limpar_campos)
        btn_limpar.place(x=565, y=440, width=130, height=40)

        btn_cancelar = Button(janela, text='Cancelar',
        command=lambda: self.fechar_janela(janela))
        btn_cancelar.place(x=720, y=440, width=130, height=40)

        btn_buscar_cpf = Button(janela, text='Buscar por CPF',
        command=self.buscar_cpf)
        btn_buscar_cpf.place(x=230, y=30, width=160, height=20)

        # adicionando Radiobutton a tela e uma variavel para a escolha
        self.opcao = IntVar()
        self.radio1 = Radiobutton(janela, text='Ativo', value=1,
        var=self.opcao)
        self.radio1.place(x=755, y=340)
        self.radio2 = Radiobutton(janela, text='Inativo', value=2,
        var=self.opcao)
        self.radio2.place(x=755, y=370)

        # colunas do treeview
        colunas = ['#1', '#2']

        # treeview na janela 
        self.tree = ttk.Treeview(janela, columns=colunas, show='headings')
        self.tree.place(x=10, y=70, width=380, height=410)

        # definindo os headings
        self.tree.heading('#1', text='CPF')
        self.tree.heading('#2', text='NOME')

        self.tree.column("#1", stretch=NO, minwidth=100, width=190)
        self.tree.column("#2", stretch=NO, minwidth=100, width=188)

        # mostra os dados do banco de dados na treeview
        self.mostrar_dados_treeview()
        
        self.tree.bind("<<TreeviewSelect>>", self.treeview_selecionado)
        
        janela.mainloop()


    def mostrar_dados_treeview(self):
        """Método para mostrar os dados do banco de dados na treeview"""

        lista_funcionario = cf.mostrar_funcionario()
        for linha in lista_funcionario:
            self.tree.insert('', 'end', values=(linha[1], linha[2]))


    def limpar_treeview(self):
        """Método para apagar os dados da treeview"""

        valor = self.tree.get_children()
        for item in valor:
            self.tree.delete(item)


    def treeview_selecionado(self, event):
        """Método para pegar o valor selecionado na treeview
        pelo mouse"""
      
        for item in self.tree.selection():
            item_texto = self.tree.item(item)
            cpf = item_texto['values'][0]
        
        # enviando a variavel cpf para o método
        self.buscar_cpf_treeview(cpf)
    
   
    def limpar_cbox_cidade(self):
        """Método para limpar a cbox_cidade"""
        self.cbox_cidade.set(' ')
        
         
    def buscar_cpf_treeview(self, cpf):
        """Método para buscar o cpf do funcionario pela treeview
        selecionada"""
            
        # limpar os campos a cada consulta
        self.limpar_campos()

        # chamar a função do pacote controle cliente
        dados_funcionario = cf.ler_dados_funcionario(cpf)

        # envia a lista para o método 
        self.preencher_campos(dados_funcionario)
    

    def buscar_cpf(self):
        """Método para buscar o cpf do funcionario"""
            
        # limpar os campos a cada consulta
        self.limpar_campos()

        if len(self.txt_buscar_cpf.get()) <= 0:
            raise mg.showerror('Vazio','Campo vazio!')
        else:
            # chamar a função do pacote controle cliente 
            dados_funcionario = cf.ler_dados_funcionario(
                self.txt_buscar_cpf.get())

            # envia a lista para o método 
            self.preencher_campos(dados_funcionario)
    

    def exibir_estado(self):
        """Método para exibir os estados"""

        # limpar o cbox cidade toda vez que seleciona um estado
        self.limpar_cbox_cidade()

        # pegar os dados da função e passa para uma variavel
        estados = ec.mostrar_estado()
        self.cbox_uf.configure(values=estados)

    
    def exibir_cidade(self, estado):
        """Método para exibir as cidades a partir do estado selecionado"""

        if len(estado) <= 0:
            raise mg.showerror('Error', 'Selecione primeiro um Estado')
        else:
            # pegar os dados da função e passa para uma variavel
            cidades = ec.mostrar_cidade(estado)
            self.cbox_cidade.configure(values=cidades)
    

    def exibir_cargo(self):
        """Método para exibir todos os cargos"""

        cargos = cf.mostrar_cargo()
        self.cbox_cargo.config(values=cargos)

    def verificar_senha(self):
        """Verifica se a senha são as mesmas"""

        if self.txt_senha_usuario != self.txt_confirmar_usuario:
            return self.txt_senha_usuario
        else:
            raise mg.showerror(title='Erro', 
            message='Senhas não conferem')
    
    
    def validar_escolha_ativo_inativo(self):
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
        id_cargo = cf.pegar_id_cargo(self.cbox_cargo.get())
        confirma_senha = self.verificar_senha()
        escolha = self.validar_escolha_ativo_inativo()
        id_cidade = ec.pegar_id_cidade(self.cbox_cidade.get())

        # chamar o metodo do pacote controle_funcionario para fazer a
        # verificação dos campos
        cf.atualizar_dados_funcionario(self.txt_nome.get(), self.txt_celular.get(),
        self.txt_cpf.get(), self.txt_email.get(), self.txt_endereco.get(),
        self.txt_numero.get(), self.txt_complemento.get(), self.txt_bairro.get(),
        id_cidade, self.txt_cep.get(), id_cargo, self.txt_login_usuario.get(),
        confirma_senha.get(), escolha)

        # chamada dos metodos para apagar a treeview os mostrar os dados
        # atualizados
        self.limpar_treeview()
        self.mostrar_dados_treeview()

        # chamada do método para apagar os campos logos apos o cadastro
        # ser feito
        self.limpar_campos()
    

    def preencher_campos(self, lista_funcionario):
        """Método para mostrar os dados do funcionario nos campos da tela"""

        # passando os valores da lista para os respectivos campos
        self.txt_cpf.insert(0, lista_funcionario[1])
        self.txt_nome.insert(0, lista_funcionario[2])
        self.txt_endereco.insert(0, lista_funcionario[3])
        self.txt_numero.insert(0, lista_funcionario[4])
        self.txt_complemento.insert(0, lista_funcionario[5])
        self.txt_cep.insert(0, lista_funcionario[6])
        self.txt_bairro.insert(0, lista_funcionario[7])
        self.txt_celular.insert(0, lista_funcionario[8])
        self.txt_email.insert(0, lista_funcionario[9])
        self.opcao.set(lista_funcionario[10])
        self.txt_login_usuario.insert(0, lista_funcionario[11])
        self.txt_senha_usuario.insert(0, lista_funcionario[12])
        self.txt_confirmar_usuario.insert(0, lista_funcionario[12])
        cidade = ec.mostrar_cidade_pelo_id(lista_funcionario[13])
        cargo = cf.mostrar_cargo_pelo_id(lista_funcionario[14])
        estado = ec.exibir_estado_pela_cidade(cidade)
        self.cbox_cidade.set(cidade)
        self.cbox_uf.set(estado)
        self.cbox_cargo.set(cargo)


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
    ConsultaFuncionario()