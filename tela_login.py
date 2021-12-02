from tkinter import *
from tkinter import messagebox as mg
from PIL import Image, ImageTk
from controle_funcionario import buscar_login_funcionario
from tl_principal import TelaPrincipal


class TelaLogin:
    """Tela de login e tela principal da aplicação, atraves dela
    que sera feito o acesso a aplicação"""

    def __init__(self):
        """Método construtor da classe"""
        
        # configurações da tela
        self.janela = Tk()
        self.janela.title('Login')
        janela_largura = 350
        janela_altura = 200
        self.janela.maxsize(janela_largura, janela_altura)
        self.janela.minsize(janela_largura, janela_altura)
    
        # centralizar o frame na tela
        screen_width = self.janela.winfo_screenwidth()
        screen_height = self.janela.winfo_screenheight()
        x_cordinate = int((screen_width/2) - (janela_largura/2))
        y_cordinate = int((screen_height/2) - (janela_altura/2))
        self.janela.geometry("{}x{}+{}+{}".format(
            janela_largura, janela_altura, x_cordinate, y_cordinate))
        
        # adicionando icones que serão exibidos na label e button
        imagem_login = Image.open("imagem\\login.png")
        imagem_login.thumbnail((50,50))
        photo_login = ImageTk.PhotoImage(imagem_login)
        imagem_entrar = Image.open("imagem\\enter.png")
        imagem_entrar.thumbnail((25,25))
        photo_entrar = ImageTk.PhotoImage(imagem_entrar)
        imagem_sair = Image.open("imagem\\power-off.png")
        imagem_sair.thumbnail((25,25))
        photo_sair = ImageTk.PhotoImage(imagem_sair)
        

        # adicionando label que terá imagem
        lbl_imagem = Label(self.janela, image = photo_login)
        lbl_imagem.place(x=145, y=10, width=50, height=50)

        # adicionando labels de login e senha
        lbl_login = Label(self.janela, text='Login', font='arial 10')
        lbl_login.place(x= 70, y=80)
        lbl_senha = Label(self.janela, text='Senha', font='arial 10')
        lbl_senha.place(x=70, y=110)

        # adicionando entry de login e senha a tela
        self.txt_login = Entry(self.janela)
        self.txt_login.place(x=115, y=80, width=140)
        self.txt_senha = Entry(self.janela, show='*')
        self.txt_senha.place(x=115, y=110, width=140)

        # adicionado os buttons a tela
        btn_confirmar = Button(self.janela, text='Confirmar', image=photo_entrar,
        compound=LEFT, font='arial', command=self.verificar_administrador)
        btn_confirmar.place(x=10, y=150, width=130, height=40)
        btn_sair = Button(self.janela, text='Sair', image=photo_sair,
        compound=LEFT, font='arial', command=self.fechar_aplicação)
        btn_sair.place(x=207, y=150, width=130, height=40)
        
        # manter a janela em loop
        self.janela.mainloop()
    

    def verificar_administrador(self):
        """Método para verificar se o login é de administrador"""

        if self.txt_login.get() == 'admin' and self.txt_senha.get() == '123':
            mg.showinfo(message=f'Bem-vindo Administrador!')
            self.realizar_login('Administrador')
        else:
            self.verificar_login()


    def verificar_login(self):
        """Método para verificar se o login está correto e loga no
        sistema"""

        # pegando os dados do usuario e passando para string
        dados_funcionario = buscar_login_funcionario(self.txt_login.get())

        # fazendo as verificações
        if dados_funcionario[1] == self.txt_login.get() and\
            dados_funcionario[2] == self.txt_senha.get():
            mg.showinfo(message=f'Bem-vindo {dados_funcionario[0]}!')
            self.realizar_login(dados_funcionario[0])
        else:
            mg.showwarning('Usuário Inválido!')
            

    def realizar_login(self, usuario):
        """Método para efetuar login e mudar de tela"""
        
        Tk(TelaPrincipal(self.janela, usuario))


    def fechar_aplicação(self):
        """Método para fechar aplicação ao clicar no botão cancelar"""

        exit()
    

if __name__ == '__main__':
    TelaLogin()