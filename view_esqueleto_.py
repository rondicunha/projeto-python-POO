from tkinter import messagebox
import tkinter as tk
from tkinter import ttk
from model_esqueleto_ import BDImagens, Imagem
import tkintermapview as tkmv
from PIL import Image, ImageTk
from datetime import datetime
from tkinter.messagebox import showerror

class AplicativoFiltroMapa:
    def __init__(self, root):
        self.root = root
        self.root.title("Aplicativo de Filtro de Mapa")

        self.frame_principal = ttk.Frame(root, padding="10")
        self.frame_principal.pack()

        self.frame_secundario = ttk.Frame(root, padding="5")
        self.frame_secundario.pack()

        self.imagens_tk = []

        self.bd = BDImagens('dataset1/index')
        self.bd.processa()

        self.num_fotos_listadas = len(self.bd.todas())

        self.criar_filtros_busca()

        self.criar_botao_busca()

        self.criar_tabela(self.bd.todas())

        self.criar_exibicao_fotos()

        self.criar_mapa()

        self.inserindo_marcadores()


    def criar_filtros_busca(self):
        frame_filtros = ttk.LabelFrame(self.frame_principal, text="Filtros de Busca")
        frame_filtros.pack(padx=10, pady=10, fill="x")

        ttk.Label(frame_filtros, text="Data Inicial (AAAA-MM-DD):").grid(row=0, column=0, padx=5, pady=5)
        self.entry_data_inicial = ttk.Entry(frame_filtros)
        self.entry_data_inicial.grid(row=0, column=1, padx=5, pady=5)

        self.checkbox_data_inicial_var = tk.IntVar()
        self.checkbox_data_inicial = tk.Checkbutton(frame_filtros, variable=self.checkbox_data_inicial_var)
        self.checkbox_data_inicial.grid(row=0, column=2, padx=5, pady=5)

        ttk.Label(frame_filtros, text="Data Final (AAAA-MM-DD):").grid(row=0, column=3, padx=5, pady=5)
        self.entry_data_final = ttk.Entry(frame_filtros)
        self.entry_data_final.grid(row=0, column=4, padx=5, pady=5)

        self.checkbox_data_final_var = tk.IntVar()
        self.checkbox_data_final = tk.Checkbutton(frame_filtros, variable=self.checkbox_data_final_var)
        self.checkbox_data_final.grid(row=0, column=5, padx=5, pady=5)

        ttk.Label(frame_filtros, text="Nome:").grid(row=0, column=6, padx=5, pady=5)
        self.entry_nome = ttk.Entry(frame_filtros)
        self.entry_nome.grid(row=0, column=7, padx=5, pady=5)

        self.checkbox_nome_var = tk.IntVar()
        self.checkbox_nome = tk.Checkbutton(frame_filtros, variable=self.checkbox_nome_var)
        self.checkbox_nome.grid(row=0, column=8, padx=5, pady=5)

        ttk.Label(frame_filtros, text="Cidade:").grid(row=1, column=0, padx=5, pady=5)
        self.entry_cidade = ttk.Entry(frame_filtros)
        self.entry_cidade.grid(row=1, column=1, padx=5, pady=5)

        self.checkbox_cidade_var = tk.IntVar()
        self.checkbox_cidade = tk.Checkbutton(frame_filtros, variable=self.checkbox_cidade_var)
        self.checkbox_cidade.grid(row=1, column=2, padx=5, pady=5)

        ttk.Label(frame_filtros, text="País:").grid(row=1, column=3, padx=5, pady=5)
        self.entry_pais = ttk.Entry(frame_filtros)
        self.entry_pais.grid(row=1, column=4, padx=5, pady=5)

        self.checkbox_pais_var = tk.IntVar()
        self.checkbox_pais = tk.Checkbutton(frame_filtros, variable=self.checkbox_pais_var)
        self.checkbox_pais.grid(row=1, column=5, padx=5, pady=5)



    def criar_botao_busca(self):
        botao_busca = ttk.Button(self.frame_principal, text="Buscar", command=(self.buscar_fotos))
        botao_busca.pack(pady=10)
    

    def criar_exibicao_fotos(self):
        

        for img_tk in self.bd.todas():
            img_tk = ImageTk.PhotoImage(img_tk._img.resize(size=(100, 80)))
            self.imagens_tk.append(img_tk)

        for img_tk in self.imagens_tk:
            lbl_img = tk.Label(self.frame_principal, image=img_tk)
            lbl_img.pack(side=tk.RIGHT)


    def criar_mapa(self):
        self.mapa = tkmv.TkinterMapView(self.frame_secundario, width=800, height=600)
        self.mapa.pack(padx=10, pady=10)
        self.mapa.set_tile_server("https://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=22)
        self.mapa.set_address('MARACANÂ, RIO DE JANEIRO')
        self.mapa.set_zoom(1)
    
    def buscar_fotos(self):
        data_inicial = self.entry_data_inicial.get()
        data_final = self.entry_data_final.get()
        nome = self.entry_nome.get()
        cidade = self.entry_cidade.get()
        pais = self.entry_pais.get()

        usar_data_inicial = self.checkbox_data_inicial_var.get()
        usar_data_final = self.checkbox_data_final_var.get()
        usar_nome = self.checkbox_nome_var.get()
        usar_cidade = self.checkbox_cidade_var.get()
        usar_pais = self.checkbox_pais_var.get()

        
        if usar_data_inicial == 1 and usar_data_final == 1:
            try:
                resultados = self.bd.busca_por_data(datetime.strptime(data_inicial, "%Y-%m-%d"), datetime.strptime(data_final, "%Y-%m-%d"))
            except:
                showerror('Título do Erro',\
                            'Formato de data inválido!')
        if usar_nome == 1:
            resultados = self.bd.busca_por_nome(nome)

        if usar_cidade == 1:
            resultados = self.bd.busca_por_cidade(cidade)

        if usar_pais == 1:
            resultados = self.bd.busca_por_pais(pais)

    
        self.limpar_tabela()

        if not resultados:
            self.tv.insert('', tk.END, values=['Não há itens disponíval para sua consulta'])
        else:
            for imagem in resultados:
                self.adicionar_item_tabela(imagem)
        
        self.num_fotos_listadas = len(resultados)
        self.label_num_fotos.config(text=f"Número de Fotos: {self.num_fotos_listadas}")

    def limpar_tabela(self):
        
        self.tv.delete(*self.tv.get_children())

    def adicionar_item_tabela(self, imagem):
        
        self.tv.insert("", tk.END, values=[imagem.nome, imagem.data, imagem.latitude, imagem.longitude, imagem.cidade, imagem.pais])
    
    def inserindo_marcadores(self):
        
        for img_tk in self.bd.todas():  
            marcador = self.mapa.set_marker(img_tk.latitude, img_tk.longitude, text=img_tk.nome)

    def criar_tabela(self, lista_imagens):
        self.label_num_fotos = ttk.Label(self.frame_principal, text=f"Número de Fotos: {self.num_fotos_listadas}")
        self.label_num_fotos.pack()

        nomes_colunas = ['nome', 'data', 'lat', 'lon', 'cidade', 'pais'] 
        self.tv = ttk.Treeview(self.frame_principal, columns=nomes_colunas, show='headings')

     
        self.tv.heading('nome', text='Nome') 
        self.tv.heading('data', text='Data')
        self.tv.heading('lat', text='Latitude')
        self.tv.heading('lon', text='Longitude')
        self.tv.heading('cidade', text='Cidade')
        self.tv.heading('pais', text='País')

        self.tv.column('nome', width=120, minwidth=130)
        self.tv.column('data', width=75, minwidth=100)
        self.tv.column('lat', width=75, minwidth=100)
        self.tv.column('lon', width=75, minwidth=100)
        self.tv.column('cidade', width=75, minwidth=100)
        self.tv.column('pais', width=75, minwidth=100)

        sb_y = ttk.Scrollbar(self.frame_principal, orient=tk.VERTICAL, command=self.tv.yview) 
        self.tv.configure(yscroll=sb_y.set) 
        sb_y.pack(side=tk.RIGHT, fill=tk.Y)

        sb_x = ttk.Scrollbar(self.frame_principal, orient=tk.HORIZONTAL, command=self.tv.xview)
        self.tv.configure(xscroll=sb_x.set)
        sb_x.pack(side=tk.BOTTOM, fill=tk.X)

        self.tv.pack(fill=tk.BOTH, expand=True)

        for i in lista_imagens:
            self.tv.insert('', tk.END, values=[i.nome, i.data, i.latitude, i.longitude, i.cidade, i.pais])    


root = tk.Tk()

app = AplicativoFiltroMapa(root)

root.mainloop()
