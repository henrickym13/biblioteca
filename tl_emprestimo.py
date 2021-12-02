from tkinter import *
from tkinter import messagebox as mg
from tkcalendar import DateEntry
from datetime import datetime
from horario import data
import controle_emprestimo as ce


class Emprestimo:
    """Classe da tela de realizar emprestimo"""

    def __init__(self, master):
        """Método construtor"""
        
        # configurações da tela
        janela = Toplevel(master)
        janela.transient(master)
        janela.title('Emprestimo')
        janela_largura = 565
        janela_altura = 460
        janela.maxsize(janela_largura, janela_altura)
        janela.minsize(janela_largura, janela_altura)
    
        # centralizar o frame na tela
        screen_width = janela.winfo_screenwidth()
        screen_height = janela.winfo_screenheight()
        x_cordinate = int((screen_width/2) - (janela_largura/2))
        y_cordinate = int((screen_height/2) - (janela_altura/2))
        janela.geometry("{}x{}+{}+{}".format(janela_largura, janela_altura,
        x_cordinate, y_cordinate))

        # adicionado as labels na tela
        lbl_cod_livro = Label(janela, text='Código do livro:')
        lbl_cod_livro.place(x=10, y=20)
        lbl_borda_dados_livro = Label(janela, borderwidth=2, relief="groove")
        lbl_borda_dados_livro.place(x=10, y=70, width=540, height=100)
        lbl_dados_livro = Label(janela, text='Dados do Livro')
        lbl_dados_livro.place(x=20, y=60)
        lbl_nome_livro = Label(janela, text='Nome do Livro')
        lbl_nome_livro.place(x=20, y=80)
        lbl_valor_dano = Label(janela, text='Valor Perda/Dano R$')
        lbl_valor_dano.place(x=410, y=80)
        lbl_nome_autor = Label(janela, text='Autor')
        lbl_nome_autor.place(x=20, y=120)
        lbl_status_livro = Label(janela, text='Status')
        lbl_status_livro.place(x=380, y=120)
        lbl_cpf_cliente = Label(janela, text='CPF do Cliente:')
        lbl_cpf_cliente.place(x=10, y=180)
        lbl_borda_dados_cliente = Label(janela, borderwidth=2, relief="groove")
        lbl_borda_dados_cliente.place(x=10, y=215, width=540, height=62)
        lbl_dados_cliente = Label(janela, text='Dados do Cliente')
        lbl_dados_cliente.place(x=20, y=205)
        lbl_nome_cliente = Label(janela, text='Nome')
        lbl_nome_cliente.place(x=20, y=225)
        lbl_status_cliente = Label(janela, text='Status')
        lbl_status_cliente.place(x=410, y=225)
        lbl_dt_emprestimo = Label(janela, text='Data de Empréstimo')
        lbl_dt_emprestimo.place(x=10, y=280)
        lbl_dt_devolucao = Label(janela, text='Data de Devolução')
        lbl_dt_devolucao.place(x=260, y=280)
        lbl_borda_obs = Label(janela, borderwidth=2, relief="groove")
        lbl_borda_obs.place(x=10, y=330, width=540, height=75)
        lbl_obs = Label(janela, text='Observações')
        lbl_obs.place(x=20, y=320)
        lbl_txt_obs = Label(janela, text='CASO OCORRA ATRASO NA DEVOLUCÃO \
SERÁ COBRADO MULTA E JUROS DIARIAMENTE \nDE R$ 0,50 OU CASO HAJA PERCA \
OU DANO AO EXEMPLAR,\n SERÁ COBRADO O VALOR DO MESMO.', font="-weight bold -size 9")
        lbl_txt_obs.place(x=20, y=350)
        lbl_emprestimo_n = Label(janela, text='Empréstimo Nº')
        lbl_emprestimo_n.place(x=10, y=405)
        self.lbl_numero_emp = Label(janela, borderwidth=2, relief="groove")
        self.lbl_numero_emp.place(x=10, y=425, width=140)
        self.lbl_numero_emp.config(text=ce.gerar_numero_protocolo())

        # labels que irão receber dados da consulta do banco de dados
        self.lbl_mostra_nome_livro = Label(janela, borderwidth=2, relief="groove")
        self.lbl_mostra_nome_livro.place(x=20, y=100, width=380, height=20)
        self.lbl_mostrar_valor_dano = Label(janela, borderwidth=2, relief="groove")
        self.lbl_mostrar_valor_dano.place(x=410, y=100, width=130, height=20)
        self.lbl_nome_autor = Label(janela, borderwidth=2, relief="groove")
        self.lbl_nome_autor.place(x=20, y=140, width=350, height=20)
        self.lbl_mostrar_status_livro = Label(janela, borderwidth=2, relief="groove")
        self.lbl_mostrar_status_livro.place(x=380, y=140, width=160, height=20)
        self.lbl_mostrar_nome_cliente = Label(janela, borderwidth=2, relief="groove")
        self.lbl_mostrar_nome_cliente.place(x=20, y=245, width=380, height=20)
        self.lbl_mostrar_status_cliente = Label(janela, borderwidth=2, relief="groove")
        self.lbl_mostrar_status_cliente.place(x=410, y=245, width=128, height=20)
        self.lbl_mostra_dt_emprestimo = Label(janela, borderwidth=2, relief="groove")
        self.lbl_mostra_dt_emprestimo.place(x=10, y=300, width=240)
        self.lbl_mostra_dt_emprestimo.config(text=data(), bg='white')
        
        # adicionando as entry na tela
        self.txt_cod_livro = Entry(janela)
        self.txt_cod_livro.place(x=110, y=20, width=270, height=20)
        self.txt_cpf_cliente = Entry(janela)
        self.txt_cpf_cliente.place(x=110, y=180, width=130, height=20)

        # adicionando botões a tela
        btn_buscar_livro = Button(janela, text='Buscar',
        command=self.preencher_campos_livro)
        btn_buscar_livro.place(x=390, y=20, width=160, height=20)

        btn_buscar_cpf_cliente = Button(janela, text='Buscar',
        command=self.preencher_campos_cliente)
        btn_buscar_cpf_cliente.place(x=255, y=180, width=125, height=20)

        btn_concluir = Button(janela, text='Concluir Empréstimo',
        command=self.pegar_valores_campos)
        btn_concluir.place(x=260, y=405, width=140 , height=40)

        btn_cancelar = Button(janela, text='Cancelar',
        command=lambda: self.fechar_janela(janela))
        btn_cancelar.place(x=410, y=405, width=140 , height=40)

        # adicionado um dateEntry na tela e pegando a data atual
        data_hoje = datetime.now()
        self.calendario_devolucao = DateEntry(janela, year=data_hoje.year,
        month=data_hoje.month, day=data_hoje.day)
        self.calendario_devolucao.place(x=260, y=300, width=250)


        janela.mainloop()
    
    
    def preencher_campos_livro(self):
        """Método para preencher as labels com dados do livro do bd"""
        
        try:
            lista_livro = ce.buscar_livro(self.txt_cod_livro.get())

            # enviar os dados para label
            self.lbl_mostra_nome_livro.config(text=lista_livro[0])
            self.mostrar_valor_dano.config(text=lista_livro[1])
            self.lbl_nome_autor.config(text=lista_livro[2])

            # chamado do método para mostrar se o livro esta disponivel
            self.status_livro(lista_livro[3], lista_livro[4])
        
        except TypeError:
            mg.showerror('Erro', 'Livro não encontrado!')


    def preencher_campos_cliente(self):

        try:
            lista_cliente = ce.buscar_cliente(self.txt_cpf_cliente.get())

            # enviar os dados para label
            self.mostrar_nome_cliente.config(text=lista_cliente[0])

            # chamada do métdo para mostrar se o cliente está ativo
            self.status_cliente(lista_cliente[1])
        
        except TypeError:
            mg.showerror('Erro', 'Cliente não encontrado!')

    
    def status_livro(self, qtd_exemplares, qtd_emprestados):
        """Método para exibir na label se o livro está disponivel"""

        if int(qtd_emprestados) >= int(qtd_exemplares):
            self.lbl_mostrar_status_livro.config(bg='red', text='Indisponivel')
        else:
            self.lbl_mostrar_status_livro.config(bg='green', text='Disponivel')
    

    def status_cliente(self, status_cliente):
        """Método para exibir na label se o cliente esta ativo ou não"""

        if status_cliente is True:
            self.lbl_mostrar_status_cliente.config(bg='green', text='Ativo')
        else:
            self.lbl_mostrar_status_cliente.config(bg='red', text='Inativo')
    

    def comparar_data_calendario(self):
        """Método para fazer a validação da data de emprestimo com a
        de devolução"""
        
        # pegando o valor do DateEntry e a data atual
        cal_devolucao = self.calendario_devolucao.get_date()
        data_atual = datetime.now()

        # fazendo as validações
        if cal_devolucao.month > data_atual.month:
            pass
        elif cal_devolucao.month == data_atual.month:
            if cal_devolucao.day > data_atual.day:
                pass
            else:
                mg.showwarning('Atenção', 'dia anterior ou igual a data de hoje')      
        else:
           mg.showwarning('Atenção', 'mês anterior ao mês atual')
    

    def formatando_data(self, data):
        """Método para formatar a saida do datetime no formato dd/mm/yyyy"""

        data_convertida = data.strftime('%d/%m/%Y')
        return data_convertida
    

    def pegar_valores_campos(self):
        """Método pra pegar os valores preenchidos no campo"""

        # comparar as data de emprestimo
        self.comparar_data_calendario()

        # pegar os id de livro e cliente
        id_cliente = ce.buscar_id_cliente(self.txt_cpf_cliente.get())
        id_livro = ce.buscar_id_livro(self.txt_cod_livro.get())

        # fazendo a convençao das datas para formato brasileiro
        data_emp = self.formatando_data(datetime.now())
        data_devolucao = self.formatando_data(self.calendario_devolucao.get_date())

        # chamada da função para gerar emprestimo
        ce.gerar_emprestimo(data_emp, data_devolucao, 
        self.lbl_numero_emp.cget('text'), id_livro, id_cliente)

        # limpar os campos apos o emprestimo
        self.limpar_campos()
    

    def limpar_campos(self):
        """Método para limpar os campos depois de te sido feito o emprestimo"""

        # campos do livro
        self.txt_cod_livro.delete(0, END)
        self.lbl_mostra_nome_livro.config(text=' ')
        self.lbl_mostrar_valor_dano.config(text=' ')
        self.lbl_nome_autor.config(text=' ')
        self.lbl_mostrar_status_livro.config(bg='gray', text=' ')

        self.txt_cpf_cliente.delete(0, END)
        self.mostrar_nome_cliente.config(text=' ')
        self.lbl_mostrar_status_cliente.config(bg='gray', text= ' ')

        # gerar um novo numero de emprestimo
        self.lbl_numero_emp.config(text=ce.gerar_numero_protocolo)
        self.calendario_devolucao.configure(validate='none')
    

    def fechar_janela(self, frame):
        """Método para fechar a janela ao clicar no botão cancelar"""

        frame.destroy()
        

if __name__ == '__main__':
    Emprestimo()