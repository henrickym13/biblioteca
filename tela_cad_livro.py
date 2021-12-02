from tkinter import *
from tkinter import ttk
from controle_livro import verificar_campos_vazios, exibir_genero_livro


class Livro:
    """classe principal da tela de cadastro de funcionario"""

    def __init__(self, master):
        """Método construtor"""

        # configurações da tela
        janela = Toplevel(master)
        janela.transient(master)
        janela.title('Cadastro de Livro')
        janela.minsize(465, 235)
        janela.maxsize(465, 235)

        # centralizar o frame na tela
        screen_width = janela.winfo_screenwidth()
        screen_height = janela.winfo_screenheight()
        x_cordinate = int((screen_width/2) - (465/2))
        y_cordinate = int((screen_height/2) - (235/2))
        janela.geometry("{}x{}+{}+{}".format(465, 235, x_cordinate, y_cordinate))

        # add as labels a tela
        lbl_nome = Label(janela, text='Nome do Livro')
        lbl_nome.place(x=10, y=10)
        lbl_autor = Label(janela, text='Autor')
        lbl_autor.place(x=10, y=50)
        lbl_genero = Label(janela, text='Gênero')
        lbl_genero.place(x=10, y=90)
        lbl_editora = Label(janela, text='Editora')
        lbl_editora.place(x=180, y=90)
        lbl_exemplares = Label(janela, text='Exemplares')
        lbl_exemplares.place(x=350, y=90) 
        lbl_codigo = Label(janela, text='Código (ISBN)')
        lbl_codigo.place(x=10, y=130)
        lbl_ano = Label(janela, text='Ano')
        lbl_ano.place(x=210, y=130)
        lbl_valor = Label(janela, text='Valor Perda/Dano R$')
        lbl_valor.place(x=330, y=130)   
      
        # adicionando os campos entry a janela
        self.txt_nome = Entry(janela)
        self.txt_nome.place(x=10, y=30, width=440, height=20)
        self.txt_autor = Entry(janela)
        self.txt_autor.place(x=10, y=70, width=440, height=20)
        self.txt_editora = Entry(janela)
        self.txt_editora.place(x=180, y=110, width=160, height=20)
        self.txt_exemplares = Entry(janela)
        self.txt_exemplares.place(x=350, y=110, width=100, height=20)
        self.txt_codigo = Entry(janela)
        self.txt_codigo.place(x=10, y=150, width=190, height=20)
        self.txt_ano = Entry(janela)
        self.txt_ano.place(x=210, y=150, width=110, height=20)
        self.txt_valor = Entry(janela)
        self.txt_valor.place(x=330, y=150, width=120, height=20)

        # adicionando o combobox a tela
        self.cbox_genero = ttk.Combobox(janela, state='readonly',
        postcommand=self.exibir_generos)
        self.cbox_genero.place(x=10, y=110, width=160)

        # adicionando Button a tela
        btn_salvar = Button(janela, text='Gravar Dados',
        command=self.pegar_informacoes_campos)
        btn_salvar.place(x=10, y=180, width=130, height=40)

        btn_limpar = Button(janela, text='Limpar Campos',
        command=self.limpar_campos)
        btn_limpar.place(x=165, y=180, width=130, height=40)

        btn_cancelar = Button(janela, text='Cancelar',
        command=lambda: self.fechar_janela(janela))
        btn_cancelar.place(x=320, y=180, width=130, height=40)
    
        janela.mainloop()
    

    def exibir_generos(self):
        """Método para exibir os gêneros de lirvos"""

        generos = exibir_genero_livro()
        self.cbox_genero.configure(values=generos)


    def pegar_informacoes_campos(self):
        """Método para pegar todas as informações inseridas nos campos
        de texto e combobox para pode gravar no banco"""

        # chama a função do pacote controle livro para fazer verificação
        # dos campos
        verificar_campos_vazios(self.txt_nome.get(), self.txt_ano.get(),
        self.txt_exemplares.get(), self.txt_codigo.get(),
        self.txt_autor.get(), self.txt_editora.get(),
        self.txt_valor.get(), self.cbox_genero.get())

        # chamada do método para apagar os campos logos apos o cadastro
        # ser feito
        self.limpar_campos()
    

    def limpar_campos(self):
        """Método para limpar os campos preenchidos"""

        self.txt_nome.delete(0, END)
        self.txt_ano.delete(0, END)
        self.txt_exemplares.delete(0, END)
        self.txt_codigo.delete(0, END)
        self.txt_editora.delete(0, END)
        self.txt_autor.delete(0, END)
        self.txt_valor.delete(0, END)
        self.cbox_genero.set(' ')
    

    def fechar_janela(self, frame):
        """Método para fechar a janela ao pressionar o button cancelar"""

        frame.destroy()
        

if __name__ == '__main__':
    Livro()