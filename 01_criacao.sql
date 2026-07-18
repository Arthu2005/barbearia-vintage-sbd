PRAGMA foreign_keys = ON;

DROP TABLE IF EXISTS itens_venda_servico;
DROP TABLE IF EXISTS itens_venda_produto;
DROP TABLE IF EXISTS vendas;
DROP TABLE IF EXISTS agendamentos;
DROP TABLE IF EXISTS produtos;
DROP TABLE IF EXISTS servicos;
DROP TABLE IF EXISTS barbeiros;
DROP TABLE IF EXISTS clientes;

CREATE TABLE clientes (
    id_cliente      INTEGER PRIMARY KEY AUTOINCREMENT,
    nome            TEXT NOT NULL,
    telefone        TEXT NOT NULL,
    email           TEXT,
    data_cadastro   TEXT NOT NULL DEFAULT (date('now'))
);

CREATE TABLE barbeiros (
    id_barbeiro         INTEGER PRIMARY KEY AUTOINCREMENT,
    nome                TEXT NOT NULL,
    telefone            TEXT NOT NULL,
    especialidade       TEXT,
    data_contratacao    TEXT NOT NULL DEFAULT (date('now'))
);

CREATE TABLE servicos (
    id_servico          INTEGER PRIMARY KEY AUTOINCREMENT,
    nome                TEXT NOT NULL,
    descricao           TEXT,
    preco               REAL NOT NULL CHECK (preco >= 0),
    duracao_minutos     INTEGER NOT NULL CHECK (duracao_minutos > 0)
);

CREATE TABLE produtos (
    id_produto          INTEGER PRIMARY KEY AUTOINCREMENT,
    nome                TEXT NOT NULL,
    descricao           TEXT,
    preco               REAL NOT NULL CHECK (preco >= 0),
    quantidade_estoque  INTEGER NOT NULL DEFAULT 0 CHECK (quantidade_estoque >= 0)
);

CREATE TABLE agendamentos (
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

CREATE TABLE vendas (
    id_venda        INTEGER PRIMARY KEY AUTOINCREMENT,
    id_cliente      INTEGER,
    id_barbeiro     INTEGER NOT NULL,
    data_hora       TEXT NOT NULL DEFAULT (datetime('now')),
    valor_total     REAL NOT NULL DEFAULT 0 CHECK (valor_total >= 0),
    FOREIGN KEY (id_cliente)  REFERENCES clientes(id_cliente),
    FOREIGN KEY (id_barbeiro) REFERENCES barbeiros(id_barbeiro)
);

CREATE TABLE itens_venda_produto (
    id_item         INTEGER PRIMARY KEY AUTOINCREMENT,
    id_venda        INTEGER NOT NULL,
    id_produto      INTEGER NOT NULL,
    quantidade      INTEGER NOT NULL CHECK (quantidade > 0),
    preco_unitario  REAL NOT NULL CHECK (preco_unitario >= 0),
    FOREIGN KEY (id_venda)   REFERENCES vendas(id_venda),
    FOREIGN KEY (id_produto) REFERENCES produtos(id_produto)
);

CREATE TABLE itens_venda_servico (
    id_item         INTEGER PRIMARY KEY AUTOINCREMENT,
    id_venda        INTEGER NOT NULL,
    id_servico      INTEGER NOT NULL,
    preco_unitario  REAL NOT NULL CHECK (preco_unitario >= 0),
    FOREIGN KEY (id_venda)   REFERENCES vendas(id_venda),
    FOREIGN KEY (id_servico) REFERENCES servicos(id_servico)
);

CREATE INDEX idx_agendamentos_data ON agendamentos(data_hora);
CREATE INDEX idx_vendas_data ON vendas(data_hora);
