import sqlite3
import os

CAMINHO_BANCO = os.path.join(os.path.dirname(os.path.abspath(__file__)), "barbearia.db")

ESQUEMA = """
CREATE TABLE IF NOT EXISTS clientes (
    id_cliente      INTEGER PRIMARY KEY AUTOINCREMENT,
    nome            TEXT NOT NULL,
    telefone        TEXT NOT NULL,
    email           TEXT,
    data_cadastro   TEXT NOT NULL DEFAULT (date('now'))
);

CREATE TABLE IF NOT EXISTS barbeiros (
    id_barbeiro         INTEGER PRIMARY KEY AUTOINCREMENT,
    nome                TEXT NOT NULL,
    telefone            TEXT NOT NULL,
    especialidade       TEXT,
    data_contratacao    TEXT NOT NULL DEFAULT (date('now'))
);

CREATE TABLE IF NOT EXISTS servicos (
    id_servico          INTEGER PRIMARY KEY AUTOINCREMENT,
    nome                TEXT NOT NULL,
    descricao           TEXT,
    preco               REAL NOT NULL CHECK (preco >= 0),
    duracao_minutos     INTEGER NOT NULL CHECK (duracao_minutos > 0)
);

CREATE TABLE IF NOT EXISTS produtos (
    id_produto          INTEGER PRIMARY KEY AUTOINCREMENT,
    nome                TEXT NOT NULL,
    descricao           TEXT,
    preco               REAL NOT NULL CHECK (preco >= 0),
    quantidade_estoque  INTEGER NOT NULL DEFAULT 0 CHECK (quantidade_estoque >= 0)
);

CREATE TABLE IF NOT EXISTS agendamentos (
    id_agendamento  INTEGER PRIMARY KEY AUTOINCREMENT,
    id_cliente      INTEGER NOT NULL,
    id_barbeiro     INTEGER NOT NULL,
    id_servico      INTEGER NOT NULL,
    data_hora       TEXT NOT NULL,
    status          TEXT NOT NULL DEFAULT 'agendado' CHECK (status IN ('agendado', 'concluido', 'cancelado')),
    FOREIGN KEY (id_cliente)  REFERENCES clientes(id_cliente),
    FOREIGN KEY (id_barbeiro) REFERENCES barbeiros(id_barbeiro),
    FOREIGN KEY (id_servico)  REFERENCES servicos(id_servico)
);

CREATE TABLE IF NOT EXISTS vendas (
    id_venda        INTEGER PRIMARY KEY AUTOINCREMENT,
    id_cliente      INTEGER,
    id_barbeiro     INTEGER NOT NULL,
    data_hora       TEXT NOT NULL DEFAULT (datetime('now')),
    valor_total     REAL NOT NULL DEFAULT 0 CHECK (valor_total >= 0),
    FOREIGN KEY (id_cliente)  REFERENCES clientes(id_cliente),
    FOREIGN KEY (id_barbeiro) REFERENCES barbeiros(id_barbeiro)
);

CREATE TABLE IF NOT EXISTS itens_venda_produto (
    id_item         INTEGER PRIMARY KEY AUTOINCREMENT,
    id_venda        INTEGER NOT NULL,
    id_produto      INTEGER NOT NULL,
    quantidade      INTEGER NOT NULL CHECK (quantidade > 0),
    preco_unitario  REAL NOT NULL CHECK (preco_unitario >= 0),
    FOREIGN KEY (id_venda)   REFERENCES vendas(id_venda),
    FOREIGN KEY (id_produto) REFERENCES produtos(id_produto)
);

CREATE TABLE IF NOT EXISTS itens_venda_servico (
    id_item         INTEGER PRIMARY KEY AUTOINCREMENT,
    id_venda        INTEGER NOT NULL,
    id_servico      INTEGER NOT NULL,
    preco_unitario  REAL NOT NULL CHECK (preco_unitario >= 0),
    FOREIGN KEY (id_venda)   REFERENCES vendas(id_venda),
    FOREIGN KEY (id_servico) REFERENCES servicos(id_servico)
);
"""


class Database:
    def __init__(self, caminho=CAMINHO_BANCO):
        self.conexao = sqlite3.connect(caminho)
        self.conexao.execute("PRAGMA foreign_keys = ON")
        self.conexao.executescript(ESQUEMA)
        self.conexao.commit()

    def consultar(self, sql, parametros=()):
        cursor = self.conexao.cursor()
        cursor.execute(sql, parametros)
        return cursor.fetchall()

    def executar(self, sql, parametros=()):
        cursor = self.conexao.cursor()
        cursor.execute(sql, parametros)
        self.conexao.commit()
        return cursor.lastrowid

    def fechar(self):
        self.conexao.close()

    def listar_clientes(self, filtro=""):
        if filtro:
            return self.consultar(
                "SELECT id_cliente, nome, telefone, email, data_cadastro FROM clientes "
                "WHERE nome LIKE ? ORDER BY nome",
                (f"%{filtro}%",),
            )
        return self.consultar(
            "SELECT id_cliente, nome, telefone, email, data_cadastro FROM clientes ORDER BY nome"
        )

    def inserir_cliente(self, nome, telefone, email):
        return self.executar(
            "INSERT INTO clientes (nome, telefone, email) VALUES (?, ?, ?)",
            (nome, telefone, email or None),
        )

    def listar_barbeiros(self):
        return self.consultar(
            "SELECT id_barbeiro, nome, telefone, especialidade, data_contratacao "
            "FROM barbeiros ORDER BY nome"
        )

    def inserir_barbeiro(self, nome, telefone, especialidade):
        return self.executar(
            "INSERT INTO barbeiros (nome, telefone, especialidade) VALUES (?, ?, ?)",
            (nome, telefone, especialidade or None),
        )

    def listar_servicos(self):
        return self.consultar(
            "SELECT id_servico, nome, descricao, preco, duracao_minutos FROM servicos ORDER BY nome"
        )

    def inserir_servico(self, nome, descricao, preco, duracao_minutos):
        return self.executar(
            "INSERT INTO servicos (nome, descricao, preco, duracao_minutos) VALUES (?, ?, ?, ?)",
            (nome, descricao or None, preco, duracao_minutos),
        )

    def listar_produtos(self):
        return self.consultar(
            "SELECT id_produto, nome, descricao, preco, quantidade_estoque FROM produtos ORDER BY nome"
        )

    def inserir_produto(self, nome, descricao, preco, quantidade_estoque):
        return self.executar(
            "INSERT INTO produtos (nome, descricao, preco, quantidade_estoque) VALUES (?, ?, ?, ?)",
            (nome, descricao or None, preco, quantidade_estoque),
        )

    def ajustar_estoque(self, id_produto, delta):
        self.executar(
            "UPDATE produtos SET quantidade_estoque = quantidade_estoque + ? WHERE id_produto = ?",
            (delta, id_produto),
        )

    def listar_agendamentos(self):
        return self.consultar(
            """
            SELECT a.id_agendamento, c.nome, b.nome, s.nome, a.data_hora, a.status
            FROM agendamentos a
            JOIN clientes c  ON c.id_cliente  = a.id_cliente
            JOIN barbeiros b ON b.id_barbeiro = a.id_barbeiro
            JOIN servicos s  ON s.id_servico  = a.id_servico
            ORDER BY a.data_hora DESC
            """
        )

    def inserir_agendamento(self, id_cliente, id_barbeiro, id_servico, data_hora):
        return self.executar(
            "INSERT INTO agendamentos (id_cliente, id_barbeiro, id_servico, data_hora) "
            "VALUES (?, ?, ?, ?)",
            (id_cliente, id_barbeiro, id_servico, data_hora),
        )

    def atualizar_status_agendamento(self, id_agendamento, status):
        self.executar(
            "UPDATE agendamentos SET status = ? WHERE id_agendamento = ?",
            (status, id_agendamento),
        )

    def listar_vendas(self):
        return self.consultar(
            """
            SELECT v.id_venda, COALESCE(c.nome, 'Cliente balcao'), b.nome, v.data_hora, v.valor_total
            FROM vendas v
            LEFT JOIN clientes c ON c.id_cliente = v.id_cliente
            JOIN barbeiros b     ON b.id_barbeiro = v.id_barbeiro
            ORDER BY v.data_hora DESC
            """
        )

    def itens_da_venda(self, id_venda):
        servicos = self.consultar(
            """
            SELECT s.nome, iv.preco_unitario
            FROM itens_venda_servico iv
            JOIN servicos s ON s.id_servico = iv.id_servico
            WHERE iv.id_venda = ?
            """,
            (id_venda,),
        )
        produtos = self.consultar(
            """
            SELECT p.nome, iv.quantidade, iv.preco_unitario
            FROM itens_venda_produto iv
            JOIN produtos p ON p.id_produto = iv.id_produto
            WHERE iv.id_venda = ?
            """,
            (id_venda,),
        )
        return servicos, produtos

    def registrar_venda(self, id_cliente, id_barbeiro, itens_servico, itens_produto):
        id_venda = self.executar(
            "INSERT INTO vendas (id_cliente, id_barbeiro, valor_total) VALUES (?, ?, 0)",
            (id_cliente, id_barbeiro),
        )
        total = 0.0
        for id_servico, preco in itens_servico:
            self.executar(
                "INSERT INTO itens_venda_servico (id_venda, id_servico, preco_unitario) VALUES (?, ?, ?)",
                (id_venda, id_servico, preco),
            )
            total += preco
        for id_produto, quantidade, preco in itens_produto:
            self.executar(
                "INSERT INTO itens_venda_produto (id_venda, id_produto, quantidade, preco_unitario) "
                "VALUES (?, ?, ?, ?)",
                (id_venda, id_produto, quantidade, preco),
            )
            self.ajustar_estoque(id_produto, -quantidade)
            total += preco * quantidade
        self.executar("UPDATE vendas SET valor_total = ? WHERE id_venda = ?", (total, id_venda))
        return id_venda
