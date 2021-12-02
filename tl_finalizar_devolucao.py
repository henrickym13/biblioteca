from tkinter import *
from datetime import datetime
from controle_livro import buscar_livro_nome
from controle_emprestimo import atualizar_status_emprestimo
from tkinter import messagebox
import decimal

class TelaObservacao:
    """Classe que serve para colocar alguma observação sobre a devolucao"""

    def __init__(self, dados_emprestimo, master):
        """Método construtor"""

        # parametro da classe
        self.dd_emprestimo = dados_emprestimo

        # configurações da tela
        self.janela = Toplevel(master)
        self.janela.transient(master)
        self.janela.title('Finalizar Devolução')
        janela_largura = 350
        janela_altura = 390
        self.janela.maxsize(janela_largura, janela_altura)
        self.janela.minsize(janela_largura, janela_altura)

        # centralizar o frame na tela
        screen_width = self.janela.winfo_screenwidth()
        screen_height = self.janela.winfo_screenheight()
        x_cordinate = int((screen_width/2) - (janela_largura/2))
        y_cordinate = int((screen_height/2) - (janela_altura/2))
        self.janela.geometry("{}x{}+{}+{}".format(
            janela_largura, janela_altura, x_cordinate, y_cordinate))


        # adicionando as labels
        lbl_borda = Label(self.janela, borderwidth=2, relief="groove")
        lbl_borda.place(x=5, y=5, width=340, height=35)
        lbl_pergunta = Label(self.janela, text='O livro encontra-se em perfeito estado?')
        lbl_pergunta.place(x=10, y=10)
        lbl_valor_total = Label(self.janela, text='Valor Total R$: ')
        lbl_valor_total.place(x=80, y=100)

        # labels que receberam valores
        self.lbl_mostra_info = Label(self.janela, font="-weight bold -size 9")
        self.lbl_mostra_info.place(x=10, y=60, width=340)
        self.lbl_mostrar_valor = Label(self.janela, borderwidth=2,
        relief="groove", text=0.00)
        self.lbl_mostrar_valor.place(x=170, y=100, width=90)

        # adicionado entry a tela
        self.txt_obs = Entry(self.janela, state='disabled')
        self.txt_obs.place(x=10, y=150, width=330, height=180)

        # adicionando os buttons a tela
        btn_confirmar = Button(self.janela, text='Confirmar',
        command=self.realizar_devolucao)
        btn_confirmar.place(x=130, y=340, width=100, height=40)
        btn_cancelar = Button(self.janela, text='Cancelar',
         command=self.fechar_janela)
        btn_cancelar.place(x=240, y=340, width=100, height=40)

        # adicionando Radiobutton a tela e uma variavel para a escolha
        self.opcao_radio = IntVar()
        self.radio1 = Radiobutton(self.janela, value=1, text='Sim',
        variable=self.opcao_radio, command=self.validar_escolha_radion_button)
        self.radio1.place(x=230, y=10)
        self.radio2 = Radiobutton(self.janela, value=2, text='Não',
        variable=self.opcao_radio, command=self.validar_escolha_radion_button)
        self.radio2.place(x=290, y=10)

        # chamanda do método para verificar se há atraso
        self.calcular_atraso(dados_emprestimo[2])

        # loop da tela principal
        self.janela.mainloop()
    

    def validar_escolha_radion_button(self):
        """Verifica qual radiobutton foi selecionado"""

        escolha = self.opcao_radio.get()
        if escolha == 1:
            self.livro_bom_estado()
        else:
            self.livro_mal_estado()
    

    def livro_bom_estado(self):
        """Caso o livro esteja em perfeito estado"""

         # variavel global
        global quantidade_dias

        # passando a soma do valor do juros de atraso, caso tenha passado
        # da data de entrega e mostrando o valor na label
        juros = self.calcular_juros(quantidade_dias)
        self.lbl_mostrar_valor.config(text= juros)

        # passando os valores para uma lista
        dados_livro = [self.dd_emprestimo[0], juros]
        return dados_livro

    
    def livro_mal_estado(self):
        """Caso o livro esteja em pessimo estado será chamado esse
        método"""

        # variavel global
        global quantidade_dias

        # trocando a informações da label e mudando o status da entry
        self.lbl_mostra_info.config(text='Abaixo informe o estado do livro.')
        self.txt_obs.config(state='normal')

        # passando a soma do valor do juros de atraso junto com o valor
        # de perda/dano c
        livro = buscar_livro_nome(self.dd_emprestimo[8])
        juros = self.calcular_juros(quantidade_dias)
        valor_total = decimal.Decimal(juros) + livro[8]
        self.lbl_mostrar_valor.config(text= valor_total)

        # passando os valores para uma lista
        dados_livro = [self.dd_emprestimo[0], valor_total, self.txt_obs.get()]
        return dados_livro
    

    def realizar_devolucao(self):
        """Método para realizar a devolução do empréstimo"""

        # chamado dos métodos do bom estado e pessimo estado
        livro_pessimo_estado = self.livro_mal_estado()
        livro_bom_estado = self.livro_bom_estado()

        # pegando a opção selecionada do radiobutton
        if self.opcao_radio.get() == 1:
            # chamada da função da classe para realizar a devolucao do exemplar
            atualizar_status_emprestimo(livro_bom_estado[0],
            livro_bom_estado[1])

            # exibindo mensagem de devolução na tela
            messagebox.showinfo(title='Sucesso',
            message='Devolução efetuada com sucesso')

              # fechar a janela atual logo apos a finalização da devolução
            self.fechar_janela()

        elif self.opcao_radio.get() == 2:
            # chamada da função da classe para realizar a devolucao do exemplar
            atualizar_status_emprestimo(livro_pessimo_estado[0],
            livro_pessimo_estado[1], livro_pessimo_estado[2])

            # exibindo mensagem de devolução na tela
            messagebox.showinfo(title='Sucesso',
            message='Devolução efetuada com sucesso')

            # fechar a janela atual logo apos a finalização da devolução
            self.fechar_janela()

        else:
            # exibindo mensagem caso nenhum radio button seja selecionado
            messagebox.showerror(title='Erro',
            message='Selecione uma opção!')
        

    def calcular_juros(self, dias):
        """Método para realizar calculo de atraso"""

        juros = dias * 0.5

        # manda as informações para label
        self.lbl_mostrar_valor.config(text=juros)

        return juros
    
    
    def calcular_atraso(self, dt_devolucao):
        """Método que verifica se possui atraso na devolução"""

        # variavel global
        global quantidade_dias
        quantidade_dias = 0

        # converter data para string
        hoje = datetime.now()
        hoje = datetime.strftime(hoje, '%d-%m-%Y')

        # convertendo a data de hoje para string
        data_hoje = datetime.strptime(hoje,'%d-%m-%Y')

        # Data inicial de devolução do exemplar
        data_inicial = datetime.strptime(dt_devolucao, '%d/%m/%Y')

        # Realizamos o calculo da quantidade de dias e o juros
        if data_hoje > data_inicial:
            quantidade_dias = abs((data_hoje - data_inicial).days)
            self.lbl_mostra_info.config(
            text=f'Está {quantidade_dias} dias atrasado',
            foreground='red')
            self.calcular_juros(quantidade_dias)
        else:
            self.lbl_mostra_info.config(text='Dentro do prazo.')

    
    def fechar_janela(self):
        """Método para fechar a janela"""

        self.janela.destroy()
      

if __name__ == '__main__':
    TelaObservacao()