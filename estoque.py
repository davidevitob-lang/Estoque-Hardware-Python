import sqlite3
import tkinter as tk
import unicodedata
from tkinter import ttk
from tkinter import messagebox

# Conexão com banco de dados através de SQLite
def conectar_db():
    conn = sqlite3.connect("estoque_hardware.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS pecas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tipo TEXT NOT NULL,
            marca TEXT,
            modelo TEXT,
            quantidade INTEGER,
            preco REAL
        )
    """)
    conn.commit()
    conn.close()

def inserir_peca(tipo, marca, modelo, quantidade, preco):
    conn = sqlite3.connect("estoque_hardware.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO pecas VALUES (NULL, ?, ?, ?, ?, ?)", (tipo, marca, modelo, quantidade, preco))
    conn.commit()
    conn.close()

def visualizar_pecas():
    conn = sqlite3.connect("estoque_hardware.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM pecas")
    linhas = cursor.fetchall()
    conn.close()
    return linhas

def remover_acentos(texto):
    if not texto:
        return ""
    texto = unicodedata.normalize('NFD', texto)
    return texto.encode('ascii', 'ignore').decode("utf-8")

def buscar_por_tipo(tipo):
    conn = sqlite3.connect("estoque_hardware.db")
    cursor = conn.cursor()
    # Puxa todas as peças do banco
    cursor.execute("SELECT * FROM pecas")
    todas_pecas = cursor.fetchall()
    conn.close()

    termo_limpo = remover_acentos(tipo).lower()
    
    linhas_filtradas = []
    for peca in todas_pecas:
        tipo_banco = remover_acentos(peca[1]).lower()
        
        if termo_limpo in tipo_banco:
            linhas_filtradas.append(peca)
            
    return linhas_filtradas

def atualizar_peca(id_peca, tipo, marca, modelo, quantidade, preco):
    conn = sqlite3.connect("estoque_hardware.db")
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE pecas SET tipo=?, marca=?, modelo=?, quantidade=?, preco=? WHERE id=?
    """, (tipo, marca, modelo, quantidade, preco, id_peca))
    conn.commit()
    conn.close()

def deletar_peca(id_peca):
    conn = sqlite3.connect("estoque_hardware.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM pecas WHERE id=?", (id_peca,))
    conn.commit()
    conn.close()


# Interface gráfica com tkinter
class SistemaHardware:
    def __init__(self, root):
        self.root = root
        self.root.title("Gerenciamento de Peças de Computador")
        self.root.geometry("850x600")
        self.root.configure(padx=20, pady=20)

        style = ttk.Style()
        style.theme_use('clam')
        style.configure("TLabel", font=("Arial", 10))
        style.configure("TButton", font=("Arial", 10, "bold"))
        style.configure("Treeview.Heading", font=("Arial", 10, "bold"))

        self.id_selecionado = tk.StringVar()
        self.tipo_var = tk.StringVar()
        self.marca_var = tk.StringVar()
        self.modelo_var = tk.StringVar()
        self.quantidade_var = tk.StringVar()
        self.preco_var = tk.StringVar()
        self.busca_tipo_var = tk.StringVar()

        self.criar_widgets()
        conectar_db()
        self.carregar_dados()

    def criar_widgets(self):
        # Frame Entradas (Formulário)
        frame_form = ttk.LabelFrame(self.root, text="Dados da Peça", padding=15)
        frame_form.pack(fill="x", pady=10)

        # Combobox para Tipo (facilita e padroniza, mas permite digitar novos)
        ttk.Label(frame_form, text="Tipo da Peça:").grid(row=0, column=0, sticky="w", pady=5)
        combo_tipo = ttk.Combobox(frame_form, textvariable=self.tipo_var, width=23, 
                                  values=["Processador (CPU)", "Placa de Vídeo (GPU)", "Placa-Mãe", "Memória RAM", "Armazenamento (SSD/HDD)", "Fonte", "Gabinete"])
        combo_tipo.grid(row=0, column=1, padx=10)

        ttk.Label(frame_form, text="Marca:").grid(row=0, column=2, sticky="w")
        ttk.Entry(frame_form, textvariable=self.marca_var, width=25).grid(row=0, column=3, padx=10)

        ttk.Label(frame_form, text="Modelo:").grid(row=0, column=4, sticky="w")
        ttk.Entry(frame_form, textvariable=self.modelo_var, width=25).grid(row=0, column=5, padx=10)

        ttk.Label(frame_form, text="Quantidade:").grid(row=1, column=0, sticky="w", pady=10)
        ttk.Entry(frame_form, textvariable=self.quantidade_var, width=25).grid(row=1, column=1, padx=10)

        ttk.Label(frame_form, text="Preço (R$):").grid(row=1, column=2, sticky="w")
        ttk.Entry(frame_form, textvariable=self.preco_var, width=25).grid(row=1, column=3, padx=10)

        # Frame Botões CRUD
        frame_botoes = tk.Frame(self.root)
        frame_botoes.pack(fill="x", pady=5)

        ttk.Button(frame_botoes, text="Adicionar", command=self.adicionar).pack(side="left", padx=5)
        ttk.Button(frame_botoes, text="Atualizar", command=self.atualizar).pack(side="left", padx=5)
        ttk.Button(frame_botoes, text="Deletar", command=self.deletar).pack(side="left", padx=5)
        ttk.Button(frame_botoes, text="Limpar Campos", command=self.limpar_campos).pack(side="left", padx=5)

        # Frame Busca
        frame_busca = ttk.LabelFrame(self.root, text="Buscar no Estoque", padding=10)
        frame_busca.pack(fill="x", pady=10)

        ttk.Label(frame_busca, text="Buscar por Tipo de Peça:").pack(side="left", padx=5)
        ttk.Entry(frame_busca, textvariable=self.busca_tipo_var, width=30).pack(side="left", padx=5)
        ttk.Button(frame_busca, text="Pesquisar", command=self.buscar).pack(side="left", padx=5)
        ttk.Button(frame_busca, text="Mostrar Todos", command=self.carregar_dados).pack(side="left", padx=5)

        # Frame Tabela
        frame_tabela = tk.Frame(self.root)
        frame_tabela.pack(fill="both", expand=True)

        colunas = ("ID", "Tipo", "Marca", "Modelo", "Quantidade", "Preço (R$)")
        self.tabela = ttk.Treeview(frame_tabela, columns=colunas, show="headings")

        # Configurar cabeçalhos e tamanhos das colunas
        larguras = [30, 150, 100, 200, 80, 80]
        for col, larg in zip(colunas, larguras):
            self.tabela.heading(col, text=col)
            self.tabela.column(col, width=larg, anchor="center")

        # Barra de rolagem
        scroll = ttk.Scrollbar(frame_tabela, orient="vertical", command=self.tabela.yview)
        self.tabela.configure(yscrollcommand=scroll.set)
        scroll.pack(side="right", fill="y")
        self.tabela.pack(side="left", fill="both", expand=True)

        # Evento de clique na tabela
        self.tabela.bind("<ButtonRelease-1>", self.selecionar_linha)

    # Interação com o banco de dados
    def carregar_dados(self):
        for linha in self.tabela.get_children():
            self.tabela.delete(linha)
        for row in visualizar_pecas():
            # Formatando o preço com 2 casas decimais
            linha_formatada = list(row)
            linha_formatada[5] = f"R$ {row[5]:.2f}"
            self.tabela.insert("", "end", values=linha_formatada)

    def adicionar(self):
        if not self.tipo_var.get() or not self.modelo_var.get():
            messagebox.showerror("Erro", "Os campos 'Tipo' e 'Modelo' são obrigatórios!")
            return
        try:
            qtd = int(self.quantidade_var.get()) if self.quantidade_var.get() else 0
            preco = float(self.preco_var.get().replace(',','.')) if self.preco_var.get() else 0.0
            
            inserir_peca(self.tipo_var.get(), self.marca_var.get(), self.modelo_var.get(), qtd, preco)
            self.carregar_dados()
            self.limpar_campos()
            messagebox.showinfo("Sucesso", "Peça adicionada com sucesso!")
        except ValueError:
            messagebox.showerror("Erro", "Quantidade e Preço devem ser números!")

    def selecionar_linha(self, event):
        item_selecionado = self.tabela.focus()
        if not item_selecionado:
            return
        valores = self.tabela.item(item_selecionado, "values")
        
        self.id_selecionado.set(valores[0])
        self.tipo_var.set(valores[1])
        self.marca_var.set(valores[2])
        self.modelo_var.set(valores[3])
        self.quantidade_var.set(valores[4])
        # Limpar o "R$ " do preço para voltar pro input numérico limpo
        preco_limpo = valores[5].replace("R$ ", "").strip()
        self.preco_var.set(preco_limpo)

    def atualizar(self):
        if not self.id_selecionado.get():
            messagebox.showerror("Erro", "Selecione uma peça na tabela para atualizar.")
            return
        try:
            qtd = int(self.quantidade_var.get())
            preco = float(self.preco_var.get().replace(',','.'))
            atualizar_peca(self.id_selecionado.get(), self.tipo_var.get(), self.marca_var.get(), 
                           self.modelo_var.get(), qtd, preco)
            self.carregar_dados()
            self.limpar_campos()
            messagebox.showinfo("Sucesso", "Peça atualizada!")
        except ValueError:
            messagebox.showerror("Erro", "Quantidade e Preço devem ser números!")

    def deletar(self):
        if not self.id_selecionado.get():
            messagebox.showerror("Erro", "Selecione uma peça na tabela para deletar.")
            return
        if messagebox.askyesno("Confirmar", "Tem certeza que deseja deletar esta peça?"):
            deletar_peca(self.id_selecionado.get())
            self.carregar_dados()
            self.limpar_campos()

    def buscar(self):
        termo = self.busca_tipo_var.get()
        for linha in self.tabela.get_children():
            self.tabela.delete(linha)
            
        resultados = buscar_por_tipo(termo)
        for row in resultados:
            linha_formatada = list(row)
            linha_formatada[5] = f"R$ {row[5]:.2f}"
            self.tabela.insert("", "end", values=linha_formatada)

    def limpar_campos(self):
        self.id_selecionado.set("")
        self.tipo_var.set("")
        self.marca_var.set("")
        self.modelo_var.set("")
        self.quantidade_var.set("")
        self.preco_var.set("")
        self.busca_tipo_var.set("")


if __name__ == "__main__":
    root = tk.Tk()
    app = SistemaHardware(root)
    root.mainloop()