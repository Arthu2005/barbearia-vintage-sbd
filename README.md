# Barbearia Vintage — Sistema de Gestao para Barbearia

Projeto pratico de banco de dados (CSI440/CSI602) — sistema desktop para gerenciar clientes,
barbeiros, servicos, produtos, agendamentos e vendas de uma barbearia.

## Tecnologias

- Python 3 (nenhuma biblioteca externa e necessaria)
- Tkinter para a interface grafica desktop
- SQLite como SGBD relacional, acessado via `sqlite3` com SQL puro (sem ORM)

## Estrutura dos arquivos

- `app_database.py` — conexao com o banco e todas as consultas/comandos SQL
- `app_main.py` — interface grafica (Tkinter)
- `01_criacao.sql` — script de criacao das tabelas
- `02_populacao.sql` — script de povoamento com dados de exemplo
- `diagrama_er.svg` — diagrama entidade-relacionamento
- `Especificacao_Projeto_Pratico.html` — documento de especificacao completo (abrir no navegador
  e usar Ctrl+P > Salvar como PDF para gerar o `.pdf` de entrega)

## Como rodar

1. Coloque `app_main.py` e `app_database.py` na mesma pasta.
2. Rode `python app_main.py`.
3. Na primeira execucao o arquivo `barbearia.db` e criado automaticamente com as tabelas vazias.
   Se quiser comecar com os dados de exemplo, rode antes:
   `sqlite3 barbearia.db < 01_criacao.sql` e depois `sqlite3 barbearia.db < 02_populacao.sql`
   (ou abra os dois scripts em qualquer cliente SQLite e execute).

## Antes de entregar

1. Numero de matricula ja preenchido em `Especificacao_Projeto_Pratico.html` (Arthur Silva
   Santos — 24.2.8076).
2. Criar o repositorio no GitHub (passo a passo abaixo) e subir `app_main.py`,
   `app_database.py`, `01_criacao.sql` e `02_populacao.sql`.
3. Colar o link do repositorio no lugar do texto marcado em vermelho, no final do documento.
4. Abrir o HTML no navegador e exportar como PDF (Ctrl+P > Salvar como PDF).
5. Gravar o video de apresentacao (ate 15 min) — use o roteiro em
   `Roteiro_Video_Apresentacao.md` como guia.

### Como subir o codigo no GitHub (sem usar linha de comando)

1. Entre em github.com, faca login (ou crie uma conta gratuita).
2. Clique em "New repository". De um nome, por exemplo `barbearia-vintage-sbd`, marque como
   publico e clique em "Create repository".
3. Na pagina do repositorio recem-criado, clique em "Add file" > "Upload files".
4. Arraste os quatro arquivos (`app_main.py`, `app_database.py`, `01_criacao.sql`,
   `02_populacao.sql`) e clique em "Commit changes".
5. Copie a URL do repositorio (a que aparece no navegador, tipo
   `https://github.com/seu-usuario/barbearia-vintage-sbd`) e cole no documento de
   especificacao, no lugar do texto em vermelho.
