import tkinter as tk
from tkinter import ttk, messagebox

from app_database import Database


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Barbearia Vintage - Sistema de Gestao")
        self.geometry("1000x650")
        self.configure(bg="#FAF3E8")

        self.db = Database()

        estilo = ttk.Style(self)
        estilo.theme_use("clam")
        estilo.configure("TNotebook.Tab", padding=(16, 8), font=("Segoe UI", 10, "bold"))
        estilo.configure("TButton", padding=6)
        estilo.configure("Treeview", rowheight=24)
        estilo.configure("Treeview.Heading", font=("Segoe UI", 9, "bold"))

        titulo = tk.Label(
            self, text="Barbearia Vintage", bg="#8B2E2E", fg="white",
            font=("Segoe UI", 18, "bold"), pady=10,
        )
        titulo.pack(fill="x")

        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)

        self.aba_clientes = ttk.Frame(self.notebook)
        self.aba_barbeiros = ttk.Frame(self.notebook)
        self.aba_servicos = ttk.Frame(self.notebook)
        self.aba_produtos = ttk.Frame(self.notebook)
        self.aba_agendamentos = ttk.Frame(self.notebook)
        self.aba_vendas = ttk.Frame(self.notebook)

        self.notebook.add(self.aba_clientes, text="Clientes")
        self.notebook.add(self.aba_barbeiros, text="Barbeiros")
        self.notebook.add(self.aba_servicos, text="Servicos")
        self.notebook.add(self.aba_produtos, text="Produtos")
        self.notebook.add(self.aba_agendamentos, text="Agendamentos")
        self.notebook.add(self.aba_vendas, text="Vendas")

        self.itens_venda_servico_temp = []
        self.itens_venda_produto_temp = []

        self.montar_aba_clientes()
        self.montar_aba_barbeiros()
        self.montar_aba_servicos()
        self.montar_aba_produtos()
        self.montar_aba_agendamentos()
        self.montar_aba_vendas()

        self.atualizar_tudo()

    def montar_aba_clientes(self):
        painel = self.aba_clientes
        formulario = ttk.LabelFrame(painel, text="Novo cliente")
        formulario.pack(fill="x", padx=10, pady=10)

        ttk.Label(formulario, text="Nome").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.cli_nome = ttk.Entry(formulario, width=30)
        self.cli_nome.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(formulario, text="Telefone").grid(row=0, column=2, padx=5, pady=5, sticky="w")
        self.cli_telefone = ttk.Entry(formulario, width=20)
        self.cli_telefone.grid(row=0, column=3, padx=5, pady=5)

        ttk.Label(formulario, text="Email").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.cli_email = ttk.Entry(formulario, width=30)
        self.cli_email.grid(row=1, column=1, padx=5, pady=5)

        ttk.Button(formulario, text="Cadastrar", command=self.cadastrar_cliente).grid(
            row=1, column=3, padx=5, pady=5
        )

        busca = ttk.Frame(painel)
        busca.pack(fill="x", padx=10)
        ttk.Label(busca, text="Buscar por nome").pack(side="left", padx=5)
        self.cli_busca = ttk.Entry(busca, width=25)
        self.cli_busca.pack(side="left", padx=5)
        ttk.Button(busca, text="Buscar", command=self.buscar_clientes).pack(side="left", padx=5)
        ttk.Button(busca, text="Limpar busca", command=self.listar_clientes).pack(side="left", padx=5)

        colunas = ("id", "nome", "telefone", "email", "cadastro")
        self.tree_clientes = ttk.Treeview(painel, columns=colunas, show="headings")
        for col, titulo in zip(colunas, ["ID", "Nome", "Telefone", "Email", "Cadastro"]):
            self.tree_clientes.heading(col, text=titulo)
            self.tree_clientes.column(col, width=150)
        self.tree_clientes.pack(fill="both", expand=True, padx=10, pady=10)

    def cadastrar_cliente(self):
        nome = self.cli_nome.get().strip()
        telefone = self.cli_telefone.get().strip()
        email = self.cli_email.get().strip()
        if not nome or not telefone:
            messagebox.showerror("Campos obrigatorios", "Informe nome e telefone do cliente.")
            return
        self.db.inserir_cliente(nome, telefone, email)
        self.cli_nome.delete(0, "end")
        self.cli_telefone.delete(0, "end")
        self.cli_email.delete(0, "end")
        self.listar_clientes()
        self.atualizar_combos()

    def buscar_clientes(self):
        self.listar_clientes(self.cli_busca.get().strip())

    def listar_clientes(self, filtro=""):
        for linha in self.tree_clientes.get_children():
            self.tree_clientes.delete(linha)
        for cliente in self.db.listar_clientes(filtro):
            self.tree_clientes.insert("", "end", values=cliente)

    def montar_aba_barbeiros(self):
        painel = self.aba_barbeiros
        formulario = ttk.LabelFrame(painel, text="Novo barbeiro")
        formulario.pack(fill="x", padx=10, pady=10)

        ttk.Label(formulario, text="Nome").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.barb_nome = ttk.Entry(formulario, width=30)
        self.barb_nome.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(formulario, text="Telefone").grid(row=0, column=2, padx=5, pady=5, sticky="w")
        self.barb_telefone = ttk.Entry(formulario, width=20)
        self.barb_telefone.grid(row=0, column=3, padx=5, pady=5)

        ttk.Label(formulario, text="Especialidade").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.barb_especialidade = ttk.Entry(formulario, width=30)
        self.barb_especialidade.grid(row=1, column=1, padx=5, pady=5)

        ttk.Button(formulario, text="Cadastrar", command=self.cadastrar_barbeiro).grid(
            row=1, column=3, padx=5, pady=5
        )

        colunas = ("id", "nome", "telefone", "especialidade", "contratacao")
        self.tree_barbeiros = ttk.Treeview(painel, columns=colunas, show="headings")
        for col, titulo in zip(colunas, ["ID", "Nome", "Telefone", "Especialidade", "Contratacao"]):
            self.tree_barbeiros.heading(col, text=titulo)
            self.tree_barbeiros.column(col, width=150)
        self.tree_barbeiros.pack(fill="both", expand=True, padx=10, pady=10)

    def cadastrar_barbeiro(self):
        nome = self.barb_nome.get().strip()
        telefone = self.barb_telefone.get().strip()
        especialidade = self.barb_especialidade.get().strip()
        if not nome or not telefone:
            messagebox.showerror("Campos obrigatorios", "Informe nome e telefone do barbeiro.")
            return
        self.db.inserir_barbeiro(nome, telefone, especialidade)
        self.barb_nome.delete(0, "end")
        self.barb_telefone.delete(0, "end")
        self.barb_especialidade.delete(0, "end")
        self.listar_barbeiros()
        self.atualizar_combos()

    def listar_barbeiros(self):
        for linha in self.tree_barbeiros.get_children():
            self.tree_barbeiros.delete(linha)
        for barbeiro in self.db.listar_barbeiros():
            self.tree_barbeiros.insert("", "end", values=barbeiro)

    def montar_aba_servicos(self):
        painel = self.aba_servicos
        formulario = ttk.LabelFrame(painel, text="Novo servico")
        formulario.pack(fill="x", padx=10, pady=10)

        ttk.Label(formulario, text="Nome").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.serv_nome = ttk.Entry(formulario, width=25)
        self.serv_nome.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(formulario, text="Descricao").grid(row=0, column=2, padx=5, pady=5, sticky="w")
        self.serv_descricao = ttk.Entry(formulario, width=30)
        self.serv_descricao.grid(row=0, column=3, padx=5, pady=5)

        ttk.Label(formulario, text="Preco (R$)").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.serv_preco = ttk.Entry(formulario, width=12)
        self.serv_preco.grid(row=1, column=1, padx=5, pady=5, sticky="w")

        ttk.Label(formulario, text="Duracao (min)").grid(row=1, column=2, padx=5, pady=5, sticky="w")
        self.serv_duracao = ttk.Entry(formulario, width=12)
        self.serv_duracao.grid(row=1, column=3, padx=5, pady=5, sticky="w")

        ttk.Button(formulario, text="Cadastrar", command=self.cadastrar_servico).grid(
            row=1, column=4, padx=5, pady=5
        )

        colunas = ("id", "nome", "descricao", "preco", "duracao")
        self.tree_servicos = ttk.Treeview(painel, columns=colunas, show="headings")
        for col, titulo in zip(colunas, ["ID", "Nome", "Descricao", "Preco", "Duracao (min)"]):
            self.tree_servicos.heading(col, text=titulo)
            self.tree_servicos.column(col, width=140)
        self.tree_servicos.pack(fill="both", expand=True, padx=10, pady=10)

    def cadastrar_servico(self):
        nome = self.serv_nome.get().strip()
        descricao = self.serv_descricao.get().strip()
        try:
            preco = float(self.serv_preco.get().replace(",", "."))
            duracao = int(self.serv_duracao.get())
        except ValueError:
            messagebox.showerror("Valores invalidos", "Preco e duracao precisam ser numeros.")
            return
        if not nome:
            messagebox.showerror("Campos obrigatorios", "Informe o nome do servico.")
            return
        self.db.inserir_servico(nome, descricao, preco, duracao)
        self.serv_nome.delete(0, "end")
        self.serv_descricao.delete(0, "end")
        self.serv_preco.delete(0, "end")
        self.serv_duracao.delete(0, "end")
        self.listar_servicos()
        self.atualizar_combos()

    def listar_servicos(self):
        for linha in self.tree_servicos.get_children():
            self.tree_servicos.delete(linha)
        for servico in self.db.listar_servicos():
            self.tree_servicos.insert("", "end", values=servico)

    def montar_aba_produtos(self):
        painel = self.aba_produtos
        formulario = ttk.LabelFrame(painel, text="Novo produto")
        formulario.pack(fill="x", padx=10, pady=10)

        ttk.Label(formulario, text="Nome").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.prod_nome = ttk.Entry(formulario, width=25)
        self.prod_nome.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(formulario, text="Descricao").grid(row=0, column=2, padx=5, pady=5, sticky="w")
        self.prod_descricao = ttk.Entry(formulario, width=30)
        self.prod_descricao.grid(row=0, column=3, padx=5, pady=5)

        ttk.Label(formulario, text="Preco (R$)").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.prod_preco = ttk.Entry(formulario, width=12)
        self.prod_preco.grid(row=1, column=1, padx=5, pady=5, sticky="w")

        ttk.Label(formulario, text="Estoque").grid(row=1, column=2, padx=5, pady=5, sticky="w")
        self.prod_estoque = ttk.Entry(formulario, width=12)
        self.prod_estoque.grid(row=1, column=3, padx=5, pady=5, sticky="w")

        ttk.Button(formulario, text="Cadastrar", command=self.cadastrar_produto).grid(
            row=1, column=4, padx=5, pady=5
        )

        colunas = ("id", "nome", "descricao", "preco", "estoque")
        self.tree_produtos = ttk.Treeview(painel, columns=colunas, show="headings")
        for col, titulo in zip(colunas, ["ID", "Nome", "Descricao", "Preco", "Estoque"]):
            self.tree_produtos.heading(col, text=titulo)
            self.tree_produtos.column(col, width=140)
        self.tree_produtos.pack(fill="both", expand=True, padx=10, pady=10)

    def cadastrar_produto(self):
        nome = self.prod_nome.get().strip()
        descricao = self.prod_descricao.get().strip()
        try:
            preco = float(self.prod_preco.get().replace(",", "."))
            estoque = int(self.prod_estoque.get())
        except ValueError:
            messagebox.showerror("Valores invalidos", "Preco e estoque precisam ser numeros.")
            return
        if not nome:
            messagebox.showerror("Campos obrigatorios", "Informe o nome do produto.")
            return
        self.db.inserir_produto(nome, descricao, preco, estoque)
        self.prod_nome.delete(0, "end")
        self.prod_descricao.delete(0, "end")
        self.prod_preco.delete(0, "end")
        self.prod_estoque.delete(0, "end")
        self.listar_produtos()
        self.atualizar_combos()

    def listar_produtos(self):
        for linha in self.tree_produtos.get_children():
            self.tree_produtos.delete(linha)
        for produto in self.db.listar_produtos():
            self.tree_produtos.insert("", "end", values=produto)

    def montar_aba_agendamentos(self):
        painel = self.aba_agendamentos
        formulario = ttk.LabelFrame(painel, text="Novo agendamento")
        formulario.pack(fill="x", padx=10, pady=10)

        ttk.Label(formulario, text="Cliente").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.age_cliente = ttk.Combobox(formulario, state="readonly", width=28)
        self.age_cliente.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(formulario, text="Barbeiro").grid(row=0, column=2, padx=5, pady=5, sticky="w")
        self.age_barbeiro = ttk.Combobox(formulario, state="readonly", width=28)
        self.age_barbeiro.grid(row=0, column=3, padx=5, pady=5)

        ttk.Label(formulario, text="Servico").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.age_servico = ttk.Combobox(formulario, state="readonly", width=28)
        self.age_servico.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(formulario, text="Data/hora (AAAA-MM-DD HH:MM)").grid(
            row=1, column=2, padx=5, pady=5, sticky="w"
        )
        self.age_data_hora = ttk.Entry(formulario, width=28)
        self.age_data_hora.grid(row=1, column=3, padx=5, pady=5)

        ttk.Button(formulario, text="Agendar", command=self.cadastrar_agendamento).grid(
            row=2, column=3, padx=5, pady=5, sticky="e"
        )

        colunas = ("id", "cliente", "barbeiro", "servico", "data_hora", "status")
        self.tree_agendamentos = ttk.Treeview(painel, columns=colunas, show="headings")
        for col, titulo in zip(
            colunas, ["ID", "Cliente", "Barbeiro", "Servico", "Data/Hora", "Status"]
        ):
            self.tree_agendamentos.heading(col, text=titulo)
            self.tree_agendamentos.column(col, width=130)
        self.tree_agendamentos.pack(fill="both", expand=True, padx=10, pady=10)

        acoes = ttk.Frame(painel)
        acoes.pack(fill="x", padx=10, pady=(0, 10))
        ttk.Button(
            acoes, text="Marcar como concluido",
            command=lambda: self.mudar_status_agendamento("concluido"),
        ).pack(side="left", padx=5)
        ttk.Button(
            acoes, text="Cancelar agendamento",
            command=lambda: self.mudar_status_agendamento("cancelado"),
        ).pack(side="left", padx=5)

    def cadastrar_agendamento(self):
        if not self.lista_clientes or not self.lista_barbeiros or not self.lista_servicos:
            messagebox.showerror(
                "Cadastros pendentes",
                "Cadastre ao menos um cliente, um barbeiro e um servico antes de agendar.",
            )
            return
        if self.age_cliente.current() < 0 or self.age_barbeiro.current() < 0 or self.age_servico.current() < 0:
            messagebox.showerror("Selecao obrigatoria", "Selecione cliente, barbeiro e servico.")
            return
        data_hora = self.age_data_hora.get().strip()
        if not data_hora:
            messagebox.showerror("Campo obrigatorio", "Informe a data e hora do agendamento.")
            return
        id_cliente = self.lista_clientes[self.age_cliente.current()][0]
        id_barbeiro = self.lista_barbeiros[self.age_barbeiro.current()][0]
        id_servico = self.lista_servicos[self.age_servico.current()][0]
        self.db.inserir_agendamento(id_cliente, id_barbeiro, id_servico, data_hora)
        self.age_data_hora.delete(0, "end")
        self.listar_agendamentos()

    def mudar_status_agendamento(self, status):
        selecionado = self.tree_agendamentos.selection()
        if not selecionado:
            messagebox.showerror("Nenhum item selecionado", "Selecione um agendamento na lista.")
            return
        id_agendamento = self.tree_agendamentos.item(selecionado[0])["values"][0]
        self.db.atualizar_status_agendamento(id_agendamento, status)
        self.listar_agendamentos()

    def listar_agendamentos(self):
        for linha in self.tree_agendamentos.get_children():
            self.tree_agendamentos.delete(linha)
        for agendamento in self.db.listar_agendamentos():
            self.tree_agendamentos.insert("", "end", values=agendamento)

    def montar_aba_vendas(self):
        painel = self.aba_vendas
        topo = ttk.LabelFrame(painel, text="Nova venda")
        topo.pack(fill="x", padx=10, pady=10)

        ttk.Label(topo, text="Cliente").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.venda_cliente = ttk.Combobox(topo, state="readonly", width=28)
        self.venda_cliente.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(topo, text="Barbeiro").grid(row=0, column=2, padx=5, pady=5, sticky="w")
        self.venda_barbeiro = ttk.Combobox(topo, state="readonly", width=28)
        self.venda_barbeiro.grid(row=0, column=3, padx=5, pady=5)

        ttk.Label(topo, text="Servico").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.venda_servico = ttk.Combobox(topo, state="readonly", width=28)
        self.venda_servico.grid(row=1, column=1, padx=5, pady=5)
        ttk.Button(topo, text="Adicionar servico", command=self.adicionar_servico_venda).grid(
            row=1, column=2, padx=5, pady=5
        )

        ttk.Label(topo, text="Produto").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.venda_produto = ttk.Combobox(topo, state="readonly", width=28)
        self.venda_produto.grid(row=2, column=1, padx=5, pady=5)
        ttk.Label(topo, text="Qtd").grid(row=2, column=2, padx=5, pady=5, sticky="e")
        self.venda_quantidade = ttk.Entry(topo, width=6)
        self.venda_quantidade.insert(0, "1")
        self.venda_quantidade.grid(row=2, column=3, padx=5, pady=5, sticky="w")
        ttk.Button(topo, text="Adicionar produto", command=self.adicionar_produto_venda).grid(
            row=2, column=4, padx=5, pady=5
        )

        self.lista_itens_venda = tk.Listbox(topo, height=5, width=70)
        self.lista_itens_venda.grid(row=3, column=0, columnspan=4, padx=5, pady=5, sticky="w")

        self.label_total_venda = ttk.Label(topo, text="Total: R$ 0.00", font=("Segoe UI", 10, "bold"))
        self.label_total_venda.grid(row=4, column=0, padx=5, pady=5, sticky="w")

        ttk.Button(topo, text="Finalizar venda", command=self.finalizar_venda).grid(
            row=4, column=3, padx=5, pady=5, sticky="e"
        )
        ttk.Button(topo, text="Limpar itens", command=self.limpar_itens_venda).grid(
            row=4, column=2, padx=5, pady=5, sticky="e"
        )

        colunas = ("id", "cliente", "barbeiro", "data_hora", "total")
        self.tree_vendas = ttk.Treeview(painel, columns=colunas, show="headings")
        for col, titulo in zip(colunas, ["ID", "Cliente", "Barbeiro", "Data/Hora", "Total (R$)"]):
            self.tree_vendas.heading(col, text=titulo)
            self.tree_vendas.column(col, width=150)
        self.tree_vendas.pack(fill="both", expand=True, padx=10, pady=10)

        ttk.Button(painel, text="Ver itens da venda selecionada", command=self.ver_itens_venda).pack(
            padx=10, pady=(0, 10), anchor="w"
        )

    def adicionar_servico_venda(self):
        if self.venda_servico.current() < 0:
            messagebox.showerror("Selecao obrigatoria", "Selecione um servico.")
            return
        id_servico, nome, preco = self.lista_servicos_venda[self.venda_servico.current()]
        self.itens_venda_servico_temp.append((id_servico, preco))
        self.lista_itens_venda.insert("end", f"Servico: {nome} - R$ {preco:.2f}")
        self.atualizar_total_venda()

    def adicionar_produto_venda(self):
        if self.venda_produto.current() < 0:
            messagebox.showerror("Selecao obrigatoria", "Selecione um produto.")
            return
        try:
            quantidade = int(self.venda_quantidade.get())
            if quantidade <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Quantidade invalida", "Informe uma quantidade valida.")
            return
        id_produto, nome, preco, estoque = self.lista_produtos_venda[self.venda_produto.current()]
        if quantidade > estoque:
            messagebox.showerror("Estoque insuficiente", f"Disponivel em estoque: {estoque}.")
            return
        self.itens_venda_produto_temp.append((id_produto, quantidade, preco))
        self.lista_itens_venda.insert(
            "end", f"Produto: {nome} x{quantidade} - R$ {preco * quantidade:.2f}"
        )
        self.atualizar_total_venda()

    def atualizar_total_venda(self):
        total = sum(preco for _, preco in self.itens_venda_servico_temp)
        total += sum(qtd * preco for _, qtd, preco in self.itens_venda_produto_temp)
        self.label_total_venda.config(text=f"Total: R$ {total:.2f}")

    def limpar_itens_venda(self):
        self.itens_venda_servico_temp = []
        self.itens_venda_produto_temp = []
        self.lista_itens_venda.delete(0, "end")
        self.atualizar_total_venda()

    def finalizar_venda(self):
        if self.venda_barbeiro.current() < 0:
            messagebox.showerror("Selecao obrigatoria", "Selecione o barbeiro responsavel.")
            return
        if not self.itens_venda_servico_temp and not self.itens_venda_produto_temp:
            messagebox.showerror("Venda vazia", "Adicione ao menos um servico ou produto.")
            return
        id_cliente = None
        if self.venda_cliente.current() >= 0:
            id_cliente = self.lista_clientes[self.venda_cliente.current()][0]
        id_barbeiro = self.lista_barbeiros[self.venda_barbeiro.current()][0]
        self.db.registrar_venda(
            id_cliente, id_barbeiro, self.itens_venda_servico_temp, self.itens_venda_produto_temp
        )
        self.limpar_itens_venda()
        self.listar_vendas()
        self.listar_produtos()
        self.atualizar_combos()
        messagebox.showinfo("Venda registrada", "Venda finalizada com sucesso.")

    def ver_itens_venda(self):
        selecionado = self.tree_vendas.selection()
        if not selecionado:
            messagebox.showerror("Nenhuma venda selecionada", "Selecione uma venda na lista.")
            return
        id_venda = self.tree_vendas.item(selecionado[0])["values"][0]
        servicos, produtos = self.db.itens_da_venda(id_venda)
        texto = "Servicos:\n"
        for nome, preco in servicos:
            texto += f"  - {nome}: R$ {preco:.2f}\n"
        texto += "\nProdutos:\n"
        for nome, quantidade, preco in produtos:
            texto += f"  - {nome} x{quantidade}: R$ {preco * quantidade:.2f}\n"
        messagebox.showinfo(f"Itens da venda {id_venda}", texto)

    def listar_vendas(self):
        for linha in self.tree_vendas.get_children():
            self.tree_vendas.delete(linha)
        for venda in self.db.listar_vendas():
            self.tree_vendas.insert("", "end", values=venda)

    def atualizar_combos(self):
        self.lista_clientes = self.db.listar_clientes()
        self.lista_barbeiros = self.db.listar_barbeiros()
        self.lista_servicos = self.db.listar_servicos()
        self.lista_servicos_venda = [(s[0], s[1], s[3]) for s in self.lista_servicos]
        self.lista_produtos_venda = [(p[0], p[1], p[3], p[4]) for p in self.db.listar_produtos()]

        self.age_cliente["values"] = [f"{c[0]} - {c[1]}" for c in self.lista_clientes]
        self.age_barbeiro["values"] = [f"{b[0]} - {b[1]}" for b in self.lista_barbeiros]
        self.age_servico["values"] = [f"{s[0]} - {s[1]}" for s in self.lista_servicos]

        self.venda_cliente["values"] = [f"{c[0]} - {c[1]}" for c in self.lista_clientes]
        self.venda_barbeiro["values"] = [f"{b[0]} - {b[1]}" for b in self.lista_barbeiros]
        self.venda_servico["values"] = [f"{s[0]} - {s[1]}" for s in self.lista_servicos_venda]
        self.venda_produto["values"] = [f"{p[0]} - {p[1]}" for p in self.lista_produtos_venda]

    def atualizar_tudo(self):
        self.listar_clientes()
        self.listar_barbeiros()
        self.listar_servicos()
        self.listar_produtos()
        self.listar_agendamentos()
        self.listar_vendas()
        self.atualizar_combos()


if __name__ == "__main__":
    app = App()
    app.mainloop()
