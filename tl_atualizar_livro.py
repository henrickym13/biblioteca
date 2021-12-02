from tkinter import *
from tkinter import ttk
from tkinter import messagebox as mg
import controle_livro as cl


class AtualizarLivro:
    """Classe principal da tela de atualização de livro"""

    def __init__(self, master):
        """método construtor da classe"""

        # configurações da tela
        janela = Toplevel(master)
        janela.transient(master)
        janela.title('Consultar Livro')
        largura = 880
        altura = 490
        janela.minsize()
        janela.minsize(largura, altura)
        janela.maxsize(largura, altura)

        # centralizar o frame na tela
        screen_width = janela.winfo_screenwidth()
        screen_height = janela.winfo_screenheight()
        x_cordinate = int((screen_width/2) - (largura/2))
        y_cordinate = int((screen_height/2) - (altura/2))
        janela.geometry("{}x{}+{}+{}".format(largura, altura, x_cordinate, y_cordinate))

        # add as labels a tela
        lbl_buscar_nome = Label(janela, text='Nome do Livro')
        lbl_buscar_nome.place(x=10, y=10)
        lbl_buscar_codigo = Label(janela, text='Código')
        lbl_buscar_codigo.place(x=10, y=50)
        lbl_buscar_autor = Label(janela, text='Autor')
        lbl_buscar_autor.place(x=10, y=90)
        lbl_nome = Label(janela, text='Nome do Livro')
        lbl_nome.place(x=430, y=10)
        lbl_autor = Label(janela, text='Autor')
        lbl_autor.place(x=430, y=50)
        lbl_genero = Label(janela, text='Gênero')
        lbl_genero.place(x=430, y=90)
        lbl_editora = Label(janela, text='Editora')
        lbl_editora.place(x=600, y=90)
        lbl_exemplares = Label(janela, text='Exemplares')
        lbl_exemplares.place(x=770, y=90) 
        lbl_codigo = Label(janela, text='Código (ISBN)')
        lbl_codigo.place(x=430, y=130)
        lbl_ano = Label(janela, text='Ano')
        lbl_ano.place(x=630, y=130)
        lbl_valor = Label(janela, text='Valor Perda/Dano R$')
        lbl_valor.place(x=750, y=130) 

        # adicionando os campos entry a janela
        self.txt_buscar_nome = Entry(janela)
        self.txt_buscar_nome.place(x=10, y=30, width=400, height=20)
        self.txt_buscar_codigo = Entry(janela)
        self.txt_buscar_codigo.place(x=10, y=70, width=400, height=20)
        self.txt_buscar_autor = Entry(janela)
        self.txt_buscar_autor.place(x=10, y=110, width=400)
        self.txt_nome = Entry(janela)
        self.txt_nome.place(x=430, y=30, width=440, height=20)
        self.txt_autor = Entry(janela)
        self.txt_autor.place(x=430, y=70, width=440, height=20)
        self.txt_editora = Entry(janela)
        self.txt_editora.place(x=600, y=110, width=160, height=20)
        self.txt_exemplares = Entry(janela)
        self.txt_exemplares.place(x=770, y=110, width=100, height=20)
        self.txt_codigo = Entry(janela)
        self.txt_codigo.place(x=430, y=150, width=190, height=20)
        self.txt_ano = Entry(janela)
        self.txt_ano.place(x=630, y=150, width=110, height=20)
        self.txt_valor = Entry(janela)
        self.txt_valor.place(x=750, y=150, width=120, height=20)

        # adicionando button a janela
        btn_consultar = Button(janela, text='Consultar',
        command=self.consultar_livro)
        btn_consultar.place(x=10, y=140, width=400, height=30)

        btn_salvar = Button(janela, text='Atualizar Dados',
        command=self.pegar_informacoes_campos)
        btn_salvar.place(x=430, y=440, width=130, height=40)

        btn_limpar = Button(janela, text='Limpar Campos',
        command=self.limpar_campos)
        btn_limpar.place(x=585, y=440, width=130, height=40)

        btn_cancelar = Button(janela, text='Cancelar',
        command=lambda: self.fechar_janela(janela))
        btn_cancelar.place(x=740, y=440, width=130, height=40)

        # adicionando o combobox a tela
        self.cbox_genero = ttk.Combobox(janela, state='readonly',
        postcommand=self.mostrar_genero_livro)
        self.cbox_genero.place(x=430, y=110, width=160)

        # colunas do treeview
        colunas = ['#1', '#2', '#3', '#4', '#5', '#6', '#7', '#8', '#9']

        # treeview na janela 
        self.tree = ttk.Treeview(janela, columns=colunas, show='headings')
        self.tree.place(x=10, y=190, width=860, height=235)

        # definindo os headings
        self.tree.heading('#1', text='NOME DO LIVRO')
        self.tree.heading('#2', text='ANO')
        self.tree.heading('#3', text='EXEMPLARES')
        self.tree.heading('#4', text='EMPRESTADOS')
        self.tree.heading('#5', text='IDENTIFICAÇÃO')
        self.tree.heading('#6', text='AUTOR')
        self.tree.heading('#7', text='EDITORA')
        self.tree.heading('#8', text='VALOR')
        self.tree.heading('#9', text='GÊNERO')

        self.tree.column("#1", stretch=NO, minwidth=100, width=178)
        self.tree.column("#2", stretch=NO, minwidth=100, width=50)
        self.tree.column("#3", stretch=NO, minwidth=100, width=90)
        self.tree.column("#4", stretch=NO, minwidth=100, width=90)
        self.tree.column("#5", stretch=NO, minwidth=100, width=100)
        self.tree.column("#6", stretch=NO, minwidth=100, width=100)
        self.tree.column("#7", stretch=NO, minwidth=100, width=90)
        self.tree.column("#8", stretch=NO, minwidth=100, width=70)
        self.tree.column("#9", stretch=NO, minwidth=100, width=90)

        # mostra os dados do banco de dados na treeview
        self.mostrar_dados_treeview()
        self.tree.bind("<<TreeviewSelect>>", self.treeview_selecionado)

        janela.mainloop()
    

    def mostrar_dados_treeview(self):
        """Método para mostrar os dados do banco de dados na treeview"""

        # chamado do metodo para mostrar o genero do livro
        lista_livro = cl.mostrar_livro()

        for linha in lista_livro:
            self.tree.insert('', 'end', values=(linha[1], linha[2], linha[3],
            linha[4], linha[5], linha[6], linha[7], linha[8], 
            cl.busca_genero_pelo_id(linha[9])))


    def mostrar_dados_treeview_autor(self, lista_autor):
        """Método para mostrar os dados do banco de dados na treeview
        fazendo busca atraves do nome do autor"""

        # limpar os campos de pesquisa
        self.limpar_campos_pesquisa()

        for linha in lista_autor:
            self.tree.insert('', 'end', values=(linha[1], linha[2], linha[3],
            linha[4], linha[5], linha[6], linha[7], linha[8], 
            self.buscar_genero(linha[9])))


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
            nome = item_texto['values'][0]
        
        # enviando a variavel cpf para o método
        self.buscar_livro_treeview(nome)
    

    def buscar_livro_treeview(self, nome):
        """Método para buscar o nome do livro pela treeview
        selecionada"""
            
        # limpar os campos a cada consulta
        self.limpar_campos()

        # instância do método para realizar a busca do livro
        # e preencher os campos
        livro = cl.buscar_livro_nome(nome)
        self.preencher_campos(livro)
    

    def mostrar_genero_livro(self):
        """Método para exibir os generos dos livros"""

        # chamando a função e passando seu valor para uma variavel
        generos = cl.exibir_genero_livro()
        self.cbox_genero.configure(values=generos)


    def consultar_livro(self):
        """Método para fazer a busca no banco de dados pelo valor informado
        pelo usuario"""

        if len(self.txt_buscar_autor.get()) > 0:
            # chamar a função para retornar os dados do item pesquisado
            autor = cl.buscar_livro_nome_autor(self.txt_buscar_autor.get())
            self.mostrar_dados_treeview_autor(autor)

        elif len(self.txt_buscar_codigo.get()) > 0:
            # chamar a função para retornar os dados do item pesquisado
            livro_cod = cl.buscar_livro_codigo(self.txt_buscar_codigo.get())
            self.preencher_campos(livro_cod)

        elif len(self.txt_buscar_nome.get()) > 0:
            # chamar a função para retornar os dados do item pesquisado
            livro_nome = cl.buscar_livro_nome(self.txt_buscar_nome.get())
            self.preencher_campos(livro_nome)
        else:
            mg.showerror(title='Erro',
            message='Preencha algum dos campos')


    def pegar_informacoes_campos(self):
        """Método para pegar todas as informações inseridas nos campos
        de texto e combobox para pode gravar no banco"""

        # instância do método para pegar o id do genero
        id_genero = cl.busca_id_genero(self.cbox_genero.get())

        # formatando string para float
        valor_real = float(self.txt_valor.get())

        # chamar a funçao do pacote controle cliente para verificar
        # os campos
        cl.atualizar_dados_livro(self.txt_nome.get(), self.txt_ano.get(),
        self.txt_exemplares.get(), self.txt_codigo.get(),self.txt_autor.get(),
        self.txt_editora.get(), valor_real, id_genero)

        # chamada dos metodos para apagar a treeview os mostrar os dados
        # atualizados
        self.limpar_treeview()
        self.mostrar_dados_treeview()

        # chamada do método para apagar os campos logos apos o cadastro
        # ser feito
        self.limpar_campos()


    def preencher_campos(self, lista_livro):
        """Método para mostrar os dados do livro nos campos da tela"""

        self.limpar_campos_pesquisa()
        # passando os valores da lista para os respectivos campos
        self.txt_nome.insert(0, lista_livro[1])
        self.txt_ano.insert(0, lista_livro[2])
        self.txt_exemplares.insert(0, lista_livro[3])
        self.txt_codigo.insert(0, lista_livro[5])
        self.txt_autor.insert(0, lista_livro[6])
        self.txt_editora.insert(0, lista_livro[7])
        self.txt_valor.insert(0, lista_livro[8])
        genero = cl.busca_genero_pelo_id(lista_livro[9])
        self.cbox_genero.set(genero)
    

    def limpar_campos(self):
        """Método para limpar os campos preenchidos"""

        self.txt_nome.delete(0, END)
        self.txt_ano.delete(0, END)
        self.txt_exemplares.delete(0, END)
        self.txt_codigo.delete(0, END)
        self.txt_autor.delete(0, END)
        self.txt_editora.delete(0, END)
        self.txt_valor.delete(0, END)
        self.cbox_genero.set(' ')
    

    def limpar_campos_pesquisa(self):
        """Método para limpar os campos de pesquisar apos se realizado
        a pesquisa"""

        self.txt_buscar_autor.delete(0, END)
        self.txt_buscar_codigo.delete(0, END)
        self.txt_buscar_nome.delete(0, END)


    def fechar_janela(self, frame):
        """Método para fechar a janela ao pressionar o button cancelar"""

        frame.destroy()


if __name__ == '__main__':
    AtualizarLivro()