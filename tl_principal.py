from tkinter import *
from PIL import Image, ImageTk
from horario import exibir_data
from tkinter import messagebox as mg
from tl_devolucao import TelaDevolucao
from tl_emprestimo import Emprestimo
from tela_cad_cliente import Cliente
from tela_cad_funcionario import Funcionario
from tela_cad_livro import Livro
from tl_atualizar_cliente import AtualizarCliente
from tl_atualizar_funcionario import ConsultaFuncionario
from tl_atualizar_livro import AtualizarLivro


class TelaPrincipal:
    """Classe da tela principal da aplicação"""

    def __init__(self, master, usuario):
        """Método construtor da classe"""
        
        # configurações da tela
        janela = Toplevel(master)
        janela.transient(master)
        janela.title('Biblioteca')
        janela_largura = janela.winfo_screenwidth()
        janela_altura = janela.winfo_screenheight()
        janela.maxsize(janela_largura, janela_altura)
        janela.minsize(janela_largura, janela_altura)
        janela.state('zoomed')
    
        # centralizar o frame na tela
        screen_width = janela.winfo_screenwidth()
        screen_height = janela.winfo_screenheight()
        x_cordinate = int((screen_width/2) - (janela_largura/2))
        y_cordinate = int((screen_height/2) - (janela_altura/2))
        janela.geometry("{}x{}+{}+{}".format(
            janela_largura, janela_altura, x_cordinate, y_cordinate))

        # adicionando menubar a tela
        menubar = Menu(tearoff=False)
        janela.config(menu=menubar)

        # adicionando o menu cadastro e seus submenus
        cadastro_menubar = Menu(tearoff=False)
        menubar.add_cascade(label='Cadastro',
        menu=cadastro_menubar)
        cadastro_menubar.add_command(label='Cliente',
        command=lambda: Cliente(janela))
        cadastro_menubar.add_command(label='Funcionario',
        command=lambda: Funcionario(janela))
        cadastro_menubar.add_command(label='Livro', 
        command=lambda: Livro(janela))

        # adicionando menubar de consultar e seus submenus
        atualizar_menubar = Menu(tearoff=False)
        menubar.add_cascade(label='Atualizar cadastro',
        menu=atualizar_menubar)
        atualizar_menubar.add_command(label='Cliente', 
        command=lambda: AtualizarCliente(janela))
        atualizar_menubar.add_command(label='Funcionario', 
        command=lambda: ConsultaFuncionario(janela))
        atualizar_menubar.add_command(label='Livro', 
        command=lambda: AtualizarLivro(janela))

        # adicionando menubar de empréstimo, devolução e sair
        emprestimo_devolucao_menubar = Menu(tearoff=False)
        menubar.add_cascade(label='Empréstimo/Devolução', 
        menu=emprestimo_devolucao_menubar)
        emprestimo_devolucao_menubar.add_command(label='Empréstimo',
        command=lambda: Emprestimo(janela))
        emprestimo_devolucao_menubar.add_command(label='Devolução',
        command=lambda: TelaDevolucao(janela))
        
        # adicionado menubar sair
        opcoes_menubar = Menu(tearoff=False)
        menubar.add_cascade(label='Opções', menu=opcoes_menubar)
        opcoes_menubar.add_command(label='Sair', command=self.fechar_janela)

        # adicionando label que terá imagem de fundo
        image = Image.open("imagem\\biblioteca.jpg")
        photo = ImageTk.PhotoImage(image)
        self.imagem = Label(janela, image = photo, 
        borderwidth=2, relief="groove")
        self.imagem.place(x=0, y=0, relwidth=1, height=(janela_altura-110))

        # label para exibir usuario logado no sistema e data
        lbl_mostra_usuario = Label(janela, text=
        f'Usuário: {usuario}\t{exibir_data()}', borderwidth=2, relief=
        "groove", anchor='w')
        lbl_mostra_usuario.place(x=0, y=(janela_altura-111),
        width=janela_largura)

        # manter a tela em loop
        janela.mainloop()
    

    def fechar_janela(self):
        """Método para exibir mensagem se o usuario deseja sair"""

        mensagem = mg.askquestion(title='Sair do Aplicativo', 
        message='Tem certeza que deseja sair do aplicativo?')
        
        # validando escolha do usuario
        if mensagem == 'yes':
            exit()
    

if __name__== '__main__':
    TelaPrincipal()