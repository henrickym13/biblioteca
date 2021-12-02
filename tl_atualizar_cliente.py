from tkinter import *
from tkinter import ttk
from tkinter import messagebox as mg
import controle_cliente as cc
import estado_cidade as ec


class AtualizarCliente:
    """classe principal da tela de atualização de funcionario"""

    def __init__(self, master):
        """Método construtor"""

        # configurações da tela
        janela = Toplevel(master)
        janela.transient(master)
        janela.title('Atualizar dados Cliente')
        janela.minsize(865, 320)
        janela.maxsize(865, 320)

        # centralizar o frame na tela
        screen_width = janela.winfo_screenwidth()
        screen_height = janela.winfo_screenheight()
        x_cordinate = int((screen_width/2) - (865/2))
        y_cordinate = int((screen_height/2) - (320/2))
        janela.geometry("{}x{}+{}+{}".format(865, 320, x_cordinate, y_cordinate))

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
        lbl_uf.place(x=540, y=210)
        lbl_cidade = Label(janela, text='Cidade')
        lbl_cidade.place(x=640, y=210)
        lbl_cep = Label(janela, text='CEP')
        lbl_cep.place(x=410, y=210)
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
        self.txt_cep.place(x=410, y=230, width=110, height=20)
        self.txt_buscar_cpf = Entry(janela)
        self.txt_buscar_cpf.place(x=60, y=30, width=160, height=20)

        # adicionando o combobox a tela
        self.cbox_uf = ttk.Combobox(janela, state='readonly',
        postcommand=self.exibir_estado)
        self.cbox_uf.place(x=540, y=230, width=80)

        self.cbox_cidade = ttk.Combobox(janela, state='readonly',
        postcommand=lambda: self.exibir_cidade(self.cbox_uf.get()))
        self.cbox_cidade.place(x=640, y=230, width=210)


        # adicionando Button a tela
        btn_salvar = Button(janela, text='Atualizar Dados',
        command=self.pegar_informacoes_campos)
        btn_salvar.place(x=410, y=265, width=130, height=40)

        btn_limpar = Button(janela, text='Limpar Campos',
        command=self.limpar_campos)
        btn_limpar.place(x=565, y=265, width=130, height=40)

        btn_cancelar = Button(janela, text='Cancelar',
        command=lambda: self.fechar_janela(janela))
        btn_cancelar.place(x=720, y=265, width=130, height=40)

        btn_buscar_cpf = Button(janela, text='Buscar por CPF',
        command=self.buscar_cpf)
        btn_buscar_cpf.place(x=230, y=30, width=160, height=20)

        # colunas do treeview
        colunas = ['#1', '#2']

        # treeview na janela 
        self.tree = ttk.Treeview(janela, columns=colunas, show='headings')
        self.tree.place(x=10, y=70, width=380, height=235)

        # definindo os headings
        self.tree.heading('#1', text='CPF')
        self.tree.heading('#2', text='NOME')

        self.tree.column("#1", stretch=NO, minwidth=100, width=190)
        self.tree.column("#2", stretch=NO, minwidth=100, width=188)

        # mostra os dados do banco de dados na treeview
        self.mostrar_dados_treeview()
        
        self.tree.bind("<<TreeviewSelect>>", self.treeview_selecionado)

        # manter a janela em loop
        janela.mainloop()
    

    def mostrar_dados_treeview(self):
        """Método para mostrar os dados do banco de dados na treeview"""

        lista_cliente = cc.mostrar_cliente()
        for linha in lista_cliente:
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
        dados_cliente = cc.ler_dados_cliente(cpf)

        # envia a lista para o método 
        self.preencher_campos(dados_cliente)
    

    def buscar_cpf(self):
        """Método para buscar o cpf do funcionario"""
            
        # limpar os campos a cada consulta
        self.limpar_campos()

        if len(self.txt_buscar_cpf.get()) <= 0:
            raise mg.showerror('Vazio','Campo vazio!')
        else:
            # chamar a função do pacote controle cliente 
            dados_cliente = cc.ler_dados_cliente(self.txt_buscar_cpf.get())

            # envia a lista para o método 
            self.preencher_campos(dados_cliente)
    

    def exibir_estado(self):
        """Método para exibir os estados"""

        # limpar o campo da cidade toda vez que seleciona um estado
        self.limpar_cbox_cidade()

        #  pegar os dados da função e passa para uma variavel
        estados = ec.mostrar_estado()
        self.cbox_uf.configure(values=estados)

    
    def exibir_cidade(self, estado):
        """Método para exibir as cidades a partir do estado selecionado"""

        if len(estado) <= 0:
            raise mg.showerror('Error', 'Selecione primeiro um Estado')
        else:
            cidades = ec.mostrar_cidade(estado)
            self.cbox_cidade.config(values=cidades)
    

    def pegar_informacoes_campos(self):
        """Método para pegar todas as informações inseridas nos campos
        de texto e combobox para pode gravar no banco"""

        # instância do métodos
        id_cidade = ec.pegar_id_cidade(self.cbox_cidade.get())

        # chamar a funçao do pacote controle cliente para verificar
        # os campos
        cc.atualizar_dados_cliente(self.txt_cpf.get(), self.txt_nome.get(),
        self.txt_endereco.get(), self.txt_numero.get(), 
        self.txt_complemento.get(), self.txt_cep.get(),
        self.txt_bairro.get(), self.txt_celular.get(), self.txt_email.get(),
        id_cidade)

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
        cidade = ec.mostrar_cidade_pelo_id(lista_funcionario[11])
        self.cbox_cidade.set(cidade)
        estado = ec.exibir_estado_pela_cidade(cidade)
        self.cbox_uf.set(estado)


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
        self.cbox_cidade.set(' ')
        self.cbox_uf.set(' ')
    

    def fechar_janela(self, frame):
        """Método para fechar a janela ao pressionar o button cancelar"""

        frame.destroy()

if __name__ == '__main__':
    AtualizarCliente()