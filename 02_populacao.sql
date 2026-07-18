INSERT INTO clientes (nome, telefone, email, data_cadastro) VALUES
('Marcos Vinicius Andrade', '31 99123-4501', 'marcos.andrade@gmail.com', '2026-01-10'),
('Rafael Oliveira Costa', '31 99123-4502', 'rafael.costa@gmail.com', '2026-01-12'),
('Bruno Henrique Silva', '31 99123-4503', 'bruno.silva@gmail.com', '2026-01-15'),
('Thiago Ferreira Lima', '31 99123-4504', 'thiago.lima@gmail.com', '2026-01-20'),
('Gustavo Pereira Souza', '31 99123-4505', 'gustavo.souza@gmail.com', '2026-02-02'),
('Eduardo Ramos Nunes', '31 99123-4506', NULL, '2026-02-05'),
('Felipe Augusto Reis', '31 99123-4507', 'felipe.reis@gmail.com', '2026-02-10'),
('Leonardo Martins Dias', '31 99123-4508', 'leo.dias@gmail.com', '2026-03-01'),
('Vitor Hugo Barbosa', '31 99123-4509', NULL, '2026-03-08'),
('Diego Almeida Rocha', '31 99123-4510', 'diego.rocha@gmail.com', '2026-03-14');

INSERT INTO barbeiros (nome, telefone, especialidade, data_contratacao) VALUES
('Carlos Eduardo Mendes', '31 98811-2201', 'Corte degradê e barba', '2024-02-01'),
('Anderson Luiz Freitas', '31 98811-2202', 'Cortes clássicos', '2024-06-15'),
('Paulo Roberto Cardoso', '31 98811-2203', 'Barba e navalha', '2025-01-10');

INSERT INTO servicos (nome, descricao, preco, duracao_minutos) VALUES
('Corte masculino', 'Corte tradicional na tesoura e máquina', 45.00, 40),
('Corte degradê', 'Degradê navalhado com acabamento na régua', 55.00, 50),
('Barba completa', 'Toalha quente, navalha e finalização', 35.00, 30),
('Corte + barba', 'Combo de corte degradê e barba completa', 80.00, 70),
('Sobrancelha', 'Design de sobrancelha na navalha', 15.00, 15),
('Pigmentação de barba', 'Aplicação de pigmento para uniformizar a barba', 60.00, 45);

INSERT INTO produtos (nome, descricao, preco, quantidade_estoque) VALUES
('Pomada modeladora', 'Pomada efeito matte 120g', 38.90, 25),
('Óleo para barba', 'Óleo hidratante com aroma amadeirado 30ml', 42.50, 18),
('Shampoo anticaspa', 'Shampoo específico para couro cabeludo 200ml', 29.90, 20),
('Balm pós-barba', 'Balm calmante pós-barbear 100ml', 33.00, 15),
('Cera capilar', 'Cera fixação forte 60g', 27.00, 22),
('Kit navalha descartável', 'Pacote com 5 lâminas', 12.00, 40);

INSERT INTO agendamentos (id_cliente, id_barbeiro, id_servico, data_hora, status) VALUES
(1, 1, 2, '2026-07-14 09:00', 'concluido'),
(2, 2, 1, '2026-07-14 10:00', 'concluido'),
(3, 1, 4, '2026-07-14 14:30', 'concluido'),
(4, 3, 3, '2026-07-15 09:30', 'concluido'),
(5, 2, 2, '2026-07-15 11:00', 'concluido'),
(6, 1, 1, '2026-07-16 15:00', 'cancelado'),
(7, 3, 4, '2026-07-17 10:00', 'agendado'),
(8, 2, 6, '2026-07-18 09:00', 'agendado'),
(9, 1, 2, '2026-07-18 11:30', 'agendado'),
(10, 3, 5, '2026-07-20 16:00', 'agendado');

INSERT INTO vendas (id_cliente, id_barbeiro, data_hora, valor_total) VALUES
(1, 1, '2026-07-14 09:45', 93.90),
(2, 2, '2026-07-14 10:40', 45.00),
(3, 1, '2026-07-14 15:20', 134.50),
(NULL, 3, '2026-07-15 12:00', 38.90),
(5, 2, '2026-07-15 11:45', 55.00);

INSERT INTO itens_venda_servico (id_venda, id_servico, preco_unitario) VALUES
(1, 2, 55.00),
(2, 1, 45.00),
(3, 4, 80.00),
(5, 2, 55.00);

INSERT INTO itens_venda_produto (id_venda, id_produto, quantidade, preco_unitario) VALUES
(1, 1, 1, 38.90),
(3, 2, 1, 42.50),
(3, 6, 1, 12.00),
(4, 1, 1, 38.90);
