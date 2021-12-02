from tkinter import *
from tkinter import messagebox as mg
import controle_emprestimo as ce
import tl_finalizar_devolucao as fd
from tkinter import ttk


class TelaDevolucao:
    """classe da tela de devoluçao de livros"""

    def __init__(self, master):
        """Método construtor da classe"""

        # configurações da tela
        self.janela = Toplevel(master)
        self.janela.transient(master)
        self.janela.title('Devolução de Livro')
        janela_largura = 965
        janela_altura = 495
        self.janela.maxsize(janela_largura, janela_altura)
        self.janela.minsize(janela_largura, janela_altura)
    
        # centralizar o frame na tela
        screen_width = self.janela.winfo_screenwidth()
        screen_height = self.janela.winfo_screenheight()
        x_cordinate = int((screen_width/2) - (janela_largura/2))
        y_cordinate = int((screen_height/2) - (janela_altura/2))
        self.janela.geometry("{}x{}+{}+{}".format(
            janela_largura, janela_altura, x_cordinate, y_cordinate))

        # adicionando as labels a tela
        lbl_n_emprestimo = Label(self.janela,text='Empréstimo Nº')
        lbl_n_emprestimo.place(x=10, y=10)
        lbl_ou_1 = Label(self.janela, text='ou')
        lbl_ou_1.place(x=140, y=30)
        lbl_cod_livro = Label(self.janela, text='Código do Livro')
        lbl_cod_livro.place(x=165, y=10)
        lbl_ou_2 = Label(self.janela, text='ou')
        lbl_ou_2.place(x=295, y=30)
        lbl_cpf = Label(self.janela, text='CPF')
        lbl_cpf.place(x=320, y=10)
        lbl_exibir = Label(self.janela, text='Exibir:')
        lbl_exibir.place(x=810, y=10)

        # adicionando entry na tela
        self.txt_n_emprestimo = Entry(self.janela)
        self.txt_n_emprestimo.place(x=10, y=30)
        self.txt_cod_livro = Entry(self.janela)
        self.txt_cod_livro.place(x=165, y=30)
        self.txt_cpf = Entry(self.janela)
        self.txt_cpf.place(x=320, y=30)

        # adicionando combobox na tela
        self.cbox_exibir_opcoes = ttk.Combobox(self.janela, state='readonly',
        values=['Tudo', 'Emprestado', 'Devolvido'])
        self.cbox_exibir_opcoes.place(x=810, y=30)
        self.cbox_exibir_opcoes.bind("<<ComboboxSelected>>", self.opcao_cbox)

        # adicionando button na janela
        btn_buscar = Button(self.janela, text='Buscar',
        command=self.buscar_emprestimo_pelos_campos_entry)
        btn_buscar.place(x=475, y=30, width=130, height=20)
        btn_devolver = Button(self.janela, text='Devolver',
        command=self.realizar_devolucao)
        btn_devolver.place(x=674, y=455, width=130, height=30)
        btn_cancelar = Button(self.janela, text='Cancelar',
        command=lambda: self.fechar_janela(self.janela))
        btn_cancelar.place(x=824, y=455, width=130, height=30)

        # adicinando treeview na tela
        # colunas do treeview
        colunas = ['#1', '#2', '#3', '#4', '#5', '#6', '#7', '#8', '#9',
        '#10']

        # treeview na janela 
        self.tree = ttk.Treeview(self.janela, columns=colunas, show='headings')
        self.tree.place(x=10, y=60, width=944, height=385)

        # definindo os nomes da headings 
        self.tree.heading('#1', text='Empréstimo nº')
        self.tree.heading('#2', text='Data Empréstimo')
        self.tree.heading('#3', text='Data Devolução')
        self.tree.heading('#4', text='Status')
        self.tree.heading('#5', text='Observação')
        self.tree.heading('#6', text='CPF')
        self.tree.heading('#7', text='Cliente')
        self.tree.heading('#8', text='Cód.Livro')
        self.tree.heading('#9', text='Livro')
        self.tree.heading('#10', text='Valor Pago')

        # definindo colunas e tamanhos
        self.tree.column("#1", stretch=NO, minwidth=100, width=129)
        self.tree.column("#2", stretch=NO, minwidth=100, width=99)
        self.tree.column("#3", stretch=NO, minwidth=100, width=90)
        self.tree.column("#4", stretch=NO, minwidth=100, width=90)
        self.tree.column("#5", stretch=NO, minwidth=100, width=100)
        self.tree.column("#6", stretch=NO, minwidth=100, width=100)
        self.tree.column("#7", stretch=NO, minwidth=100, width=90)
        self.tree.column("#8", stretch=NO, minwidth=100, width=70)
        self.tree.column("#9", stretch=NO, minwidth=100, width=90)
        self.tree.column("#10", stretch=NO, minwidth=100, width=84)

        # chamada do método para mostrar dados na treeview e pegar
        # o valor selecionado
        self.mostrar_dados_treeview()
        self.tree.bind("<<TreeviewSelect>>", self.treeview_selecionado)
        
        # manter a janela em loop
        self.janela.mainloop()
    

    def mostrar_dados_treeview(self):
        """Método para exibir os dados da tabela do banco na treeview"""

        # limpar os dados da treeview
        self.limpar_treeview()

        # chamado do metodo para mostrar o genero do livro
        lista_emprestimo = ce.exibir_emprestimos()

        for linha in lista_emprestimo:
            self.tree.insert('', 'end', values=(linha[0], linha[1], linha[2],
            linha[3], linha[4], linha[5], linha[6], linha[7], linha[8],
            linha[9] ))


    def mostrar_treeview_escolha(self, valores):
        """Método pra mostrar os dados na treeview a partir da escolha
        no combobox de todos, emprestado ou devolvidos"""

        # limpar os dados da treeview
        self.limpar_treeview()

        emprestimo = ce.exibir_emprestimo_opcao(valores)

        for linha in emprestimo:
            self.tree.insert('', 'end', values=(linha[0], linha[1], linha[2],
            linha[3], linha[4], linha[5], linha[6], linha[7], linha[8],
            linha[9] ))
    

    def mostrar_treeview_escolha_da_entry(self, valores):
        """Método pra mostrar os dados na treeview a partir da escolha
        nos campos entry de emprestimo, cod.livro ou cpf"""
        try:
            # limpar os dados da treeview e entry
            self.limpar_treeview()
            self.limpar_entry()

            for linha in valores:
                self.tree.insert('', 'end', values=(linha[0], linha[1], linha[2],
                linha[3], linha[4], linha[5], linha[6], linha[7], linha[8],
                linha[9]))
        
        except TypeError:
            mg.showerror(title='Erro',
            message='Não foi possivel localizar os dados solicitados.')
    

    def opcao_cbox(self, event):
        """Método para aplicar  filtro na treeview a partir da escolha no
        cbox"""
        
        entrada = self.cbox_exibir_opcoes.get()

        if entrada == 'Tudo':
            self.mostrar_dados_treeview()
        else:
            self.mostrar_treeview_escolha(self.cbox_exibir_opcoes.get())   


    def limpar_treeview(self):
        """Método para limpar os dados da treeview"""

        valor = self.tree.get_children()
        for item in valor:
            self.tree.delete(item)
    

    def treeview_selecionado(self, event):
        """Método para pegar o valor selecionado na treeview
        pelo mouse"""
        global lista

        for item in self.tree.selection():
            item_texto = self.tree.item(item)
            
        lista = item_texto['values']
    

    def limpar_entry(self):
        """Método para limpar os entry logo apos uma consulta"""

        self.txt_cod_livro.delete(0, END)
        self.txt_cpf.delete(0, END)
        self.txt_n_emprestimo.delete(0, END)
    
    
    def buscar_emprestimo_pelos_campos_entry(self):
        """Método para buscar o empréstimo pelo entry do cpf,
        numero emprestimo ou cpf do cliente"""

        if len(self.txt_n_emprestimo.get()) > 0:
            # passa o texto da entry para a função e mostrar os resultados
            # em uma lista e enviar para treeview
            lista_emp = ce.buscar_emprestimo_numero(self.txt_n_emprestimo.get())
            self.mostrar_treeview_escolha_da_entry(lista_emp)
        
        elif len(self.txt_cod_livro.get()) > 0:
            # passa o texto da entry para a função e mostrar os resultados
            # em uma lista e enviar para treeview
            lista_emp = ce.buscar_emprestimo_codigo_livro(
                self.txt_cod_livro.get())
            self.mostrar_treeview_escolha_da_entry(lista_emp)
        
        elif len(self.txt_cpf.get()) > 0:
            # passa o texto da entry para a função e mostrar os resultados
            # em uma lista e enviar para treeview
            lista_emp = ce.buscar_emprestimo_cpf_cliente(self.txt_cpf.get())
            self.mostrar_treeview_escolha_da_entry(lista_emp)
        
        else:
            mg.showerror(title='Error',
                message='Preenchar algum dos campos acima')
        
    
    def realizar_devolucao(self):
        """Método para fazer a devolução do Emprestimo"""

        global lista

        if lista[3] == 'Emprestado':
            fd.TelaObservacao(lista, self.janela)
            self.mostrar_dados_treeview()
        else:
            mg.showinfo(
            title='Atenção', message='Devolução já efetuada')
    

    def fechar_janela(self, frame):
        """Método para fechar a janela ao clicar no botão cancelar"""

        frame.destroy()


if __name__ == '__main__':
    TelaDevolucao()