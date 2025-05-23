modelo_relacional = {
    "empresas": {
        "pk": ["id_empresa"],
        "atributos": ["nome_fantasia", "cnpj", "data_fundacao"],
        "relacionamentos": []
    },
    "clientes": {
        "pk": ["id_cliente"],
        "atributos": ["nome", "email", "cpf"],
        "relacionamentos": []
    },
    "receitas": {
        "pk": ["id_receita"],
        "atributos": ["categoria", "valor", "data", "descricao"],
        "relacionamentos": [
            {"fk": "id_empresa", "referencia": "empresas(id_empresa)"},
            {"fk": "id_cliente", "referencia": "clientes(id_cliente)"}
        ]
    },
    "despesas": {
        "pk": ["id_despesa"],
        "atributos": ["categoria", "valor", "data", "descricao"],
        "relacionamentos": [
            {"fk": "id_empresa", "referencia": "empresas(id_empresa)"},
            {"fk": "id_cliente", "referencia": "clientes(id_cliente)"}
        ]
    },
    "orcamentos": {
        "pk": ["id_orcamento"],
        "atributos": ["ano", "mes", "tipo", "valor_estimado"],
        "relacionamentos": [
            {"fk": "id_empresa", "referencia": "empresas(id_empresa)"}
        ]
    },
    "transferencias": {
        "pk": ["id_transferencia"],
        "atributos": ["tipo", "valor", "data", "descricao"],
        "relacionamentos": [
            {"fk": "id_empresa_origem", "referencia": "empresas(id_empresa)"},
            {"fk": "id_empresa_destino", "referencia": "empresas(id_empresa)"}
        ]
    }
}

# exibir modelo relacional
for tabela, dados in modelo_relacional.items():
    print(f"\nTabela: {tabela}")
    print(f"  PK: {', '.join(dados['pk'])}")
    print(f"  Atributos: {', '.join(dados['atributos'])}")
    if dados["relacionamentos"]:
        print("  Relacionamentos:")
        for rel in dados["relacionamentos"]:
            print(f"    FK {rel['fk']} → {rel['referencia']}")


import sqlite3

# conectando/criando bd local
conexao = sqlite3.connect("financeiro.db")
cursor = conexao.cursor()

# criando  tabelas(empresas, clientes, ..., trasnferências)
cursor.execute("""
CREATE TABLE IF NOT EXISTS empresas (
    id_empresa INTEGER PRIMARY KEY,
    nome_fantasia TEXT NOT NULL,
    cnpj TEXT UNIQUE,
    data_fundacao DATE
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS clientes (
    id_cliente INTEGER PRIMARY KEY,
    nome TEXT NOT NULL,
    email TEXT,
    cpf TEXT UNIQUE
);
""")


cursor.execute("""
CREATE TABLE IF NOT EXISTS receitas (
    id_receita INTEGER PRIMARY KEY,
    id_empresa INTEGER NOT NULL,
    id_cliente INTEGER NOT NULL,
    categoria TEXT,
    valor REAL NOT NULL,
    data DATE,
    descricao TEXT,
    FOREIGN KEY (id_empresa) REFERENCES empresas(id_empresa),
    FOREIGN KEY (id_cliente) REFERENCES clientes(id_cliente)
);
""")


cursor.execute("""
CREATE TABLE IF NOT EXISTS despesas (
    id_despesa INTEGER PRIMARY KEY,
    id_empresa INTEGER NOT NULL,
    id_cliente INTEGER,
    categoria TEXT,
    valor REAL NOT NULL,
    data DATE,
    descricao TEXT,
    FOREIGN KEY (id_empresa) REFERENCES empresas(id_empresa),
    FOREIGN KEY (id_cliente) REFERENCES clientes(id_cliente)
);
""")


cursor.execute("""
CREATE TABLE IF NOT EXISTS orcamentos (
    id_orcamento INTEGER PRIMARY KEY,
    id_empresa INTEGER NOT NULL,
    ano INTEGER NOT NULL,
    mes INTEGER NOT NULL,
    tipo TEXT NOT NULL CHECK (tipo IN ('receita', 'despesa')),
    valor_estimado REAL NOT NULL,
    FOREIGN KEY (id_empresa) REFERENCES empresas(id_empresa)
);
""")


cursor.execute("""
CREATE TABLE IF NOT EXISTS transferencias (
    id_transferencia INTEGER PRIMARY KEY,
    id_empresa_origem INTEGER NOT NULL,
    id_empresa_destino INTEGER NOT NULL,
    tipo TEXT,
    valor REAL NOT NULL,
    data DATE,
    descricao TEXT,
    FOREIGN KEY (id_empresa_origem) REFERENCES empresas(id_empresa),
    FOREIGN KEY (id_empresa_destino) REFERENCES empresas(id_empresa)
);
""")




import pandas as pd

# dicionário pareado: nomes e caminhos 'path' dos arquivos
caminhos_csv = {
    "clientes": "/content/clientes.csv",
    "despesas": "/content/despesas.csv",
    "empresas": "/content/empresas.csv",
    "orcamentos": "/content/orcamentos.csv",
    "receitas": "/content/receitas.csv",
    "transferencias": "/content/transferencias.csv"
}

# lê todos os arquivos de forma iteravel e armazena em um dicionário de dataframes (dfs)
dfs = {nome: pd.read_csv(caminho) for nome, caminho in caminhos_csv.items()}

# exibir dataframe, exemplo
dfs["receitas"]



# função auxiliar para inserir os dados com tratamento de erros
def inserir_dados(tabela, df):
    """
    Insere os dados de um DataFrame em uma tabela SQLite, ignorando erros de chave primária duplicada.

    Parâmetros:
    ----------
    tabela : str
        Nome da tabela no banco de dados SQLite onde os dados serão inseridos.

    df : pandas.DataFrame
        DataFrame contendo os dados a serem inseridos. As colunas devem corresponder
        aos nomes das colunas da tabela no banco de dados.

    Comportamento:
    --------------
    Para cada linha do DataFrame, a função tenta inserir os dados na tabela.
    Caso ocorra um erro de integridade (como duplicata de chave primária), a linha é ignorada
    e o processo continua com as próximas.

    Notas:
    ------
    - A função assume que existe um cursor SQLite já definido com o nome 'cursor'.
    - O commit das transações deve ser feito fora da função, se necessário.
    """

    colunas = ", ".join(df.columns)
    valores = ", ".join(["?" for _ in df.columns])
    sql = f"INSERT INTO {tabela} ({colunas}) VALUES ({valores})"
    for _, row in df.iterrows():
        try:
            cursor.execute(sql, tuple(row))
        except sqlite3.IntegrityError:
            continue  # ignora duplicatas de chave primária


# ordem de inserção considerando dependências
ordem_insercao = ["clientes", "empresas", "despesas", "receitas", "orcamentos", "transferencias"]

# insere os dados em cada tabela
for tabela in ordem_insercao:
    inserir_dados(tabela, dfs[tabela])

# commit e fecha conexão
conexao.commit()
conexao.close()

print("Dados carregados no banco de dados: financeiro.db")


import sqlite3
import pandas as pd

# conectar ao banco
conexao = sqlite3.connect("financeiro.db")

# lista tabelas
tabelas = ["clientes", "empresas", "despesas", "receitas", "orcamentos", "transferencias"]

# dados de cada tabela
for tabela in tabelas:
    print(f"\n Tabela: {tabela}")
    df = pd.read_sql_query(f"SELECT * FROM {tabela}", conexao)
    display(df)

# fechar conexão
conexao.close()


# importar bibliotecas
import pandas as pd
import sqlite3
import re
import os

# definir esquema completo de colunas por tabela com base nas planilhas fornecidas
esquemas = {
    'clientes': {
        'id_cliente': int,
        'nome': str,
        'email': str,
        'cpf': str
    },
    'despesas': {
        'id_despesa': int,
        'id_empresa': int,
        'id_cliente': int,
        'categoria': str,
        'valor': float,
        'data': 'date',
        'descricao': str
    },
    'empresas': {
        'id_empresa': int,
        'nome_fantasia': str,
        'cnpj': str,
        'data_fundacao': 'date'
    },
    'orcamentos': {
        'id_orcamento': int,
        'id_empresa': int,
        'ano': int,
        'mes': int,
        'tipo': str,
        'valor_estimado': float
    },
    'receitas': {
        'id_receita': int,
        'id_empresa': int,
        'id_cliente': int,
        'categoria': str,
        'valor': float,
        'data': 'date',
        'descricao': str
    },
    'transferencias': {
        'id_transferencia': int,
        'id_empresa_origem': int,
        'id_empresa_destino': int,
        'tipo': str,
        'valor': float,
        'data': 'date',
        'descricao': str
    }
}

# função para listar arquivos csv automaticamente
def listar_arquivos_csv(pasta='.'):
    """
    Lista automaticamente os arquivos .csv presentes em uma pasta.

    Parâmetros:
    -----------
    pasta : str
        Caminho da pasta onde os arquivos serão listados. Por padrão, é a pasta atual ('.').

    Retorna:
    --------
    dict
        Um dicionário no formato {nome_arquivo_sem_extensao: caminho_completo_para_arquivo_csv}
    """
    return {
        os.path.splitext(f)[0]: os.path.join(pasta, f)
        for f in os.listdir(pasta)
        if f.endswith('.csv')
    }

# padronizar nomes de colunas para snake_case
def snake_case(texto: str):
    """
    Converte uma string para o formato snake_case.

    Parâmetros:
    -----------
    texto : str
        String a ser convertida.

    Retorna:
    --------
    str
        String convertida para snake_case.
    """
    texto = re.sub(r'([a-z0-9])([A-Z])', r'\1_\2', texto)
    texto = re.sub(r'[\s\-]+', '_', texto)
    return texto.lower()

# formatar colunas monetárias para exibição
def formatar_valores(dados: pd.DataFrame):
    """
    Formata colunas com a palavra 'valor' para o padrão monetário brasileiro (BRL).

    Parâmetros:
    -----------
    dados : pd.DataFrame
        DataFrame com colunas a serem formatadas.

    Retorna:
    --------
    pd.DataFrame
        DataFrame com os valores monetários formatados.
    """
    for coluna in dados.columns:
        if 'valor' in coluna:
            dados[coluna] = dados[coluna].apply(
                lambda x: f'R$ {x:,.2f}'.replace('.', '#').replace(',', '.').replace('#', ',')
                if pd.notnull(x) else x
            )
    return dados

# tratar, limpar e validar dados
def tratar_csv(caminho: str, nome_tabela: str):
    """
    Realiza o tratamento e validação de dados de um arquivo CSV conforme esquema definido.

    Parâmetros:
    -----------
    caminho : str
        Caminho para o arquivo CSV a ser tratado.

    nome_tabela : str
        Nome da tabela que será usada como referência de esquema.

    Retorna:
    --------
    pd.DataFrame
        DataFrame tratado e validado.
    """
    tabela = pd.read_csv(caminho)
    tabela.columns = [snake_case(col) for col in tabela.columns]

    for coluna in tabela.columns:
        if 'data' in coluna or 'dt' in coluna:
            tabela[coluna] = pd.to_datetime(tabela[coluna], errors='coerce').dt.date

    tabela = tabela.drop_duplicates()
    tabela = tabela.dropna(how='all')

    for coluna in tabela.columns:
        if tabela[coluna].dtype in ['float64', 'int64']:
            tabela[coluna] = tabela[coluna].fillna(0)
        elif tabela[coluna].dtype == 'object':
            tabela[coluna] = tabela[coluna].fillna('desconhecido')
        elif 'data' in coluna or 'dt' in coluna:
            tabela[coluna] = tabela[coluna].fillna(pd.NaT)

    if nome_tabela in esquemas:
        esquema = esquemas[nome_tabela]
        colunas_esperadas = set(esquema.keys())
        colunas_encontradas = set(tabela.columns)
        faltantes = colunas_esperadas - colunas_encontradas

        if faltantes:
            print(f'Aviso: Tabela "{nome_tabela}" está com colunas faltantes: {faltantes}')

        for coluna, tipo_esperado in esquema.items():
            if coluna in tabela.columns:
                if tipo_esperado == int:
                    tabela[coluna] = pd.to_numeric(tabela[coluna], errors='coerce').fillna(0).astype(int)
                elif tipo_esperado == float:
                    tabela[coluna] = pd.to_numeric(tabela[coluna], errors='coerce').fillna(0.0)
                elif tipo_esperado == 'date':
                    tabela[coluna] = pd.to_datetime(tabela[coluna], errors='coerce').dt.date
                elif tipo_esperado == str:
                    tabela[coluna] = tabela[coluna].astype(str).fillna('desconhecido')

    return tabela

# criar schema em SQL
script_schema = '''
    create table if not exists clientes (
        id_cliente integer primary key,
        nome text,
        email text,
        cpf text
    );

    create table if not exists despesas (
        id_despesa integer primary key,
        id_empresa integer,
        id_cliente integer,
        categoria text,
        valor real,
        data date,
        descricao text
    );

    create table if not exists empresas (
        id_empresa integer primary key,
        nome_fantasia text,
        cnpj text,
        data_fundacao date
    );

    create table if not exists orcamentos (
        id_orcamento integer primary key,
        id_empresa integer,
        ano integer,
        mes integer,
        tipo text,
        valor_estimado real
    );

    create table if not exists receitas (
        id_receita integer primary key,
        id_empresa integer,
        id_cliente integer,
        categoria text,
        valor real,
        data date,
        descricao text
    );

    create table if not exists transferencias (
        id_transferencia integer primary key,
        id_empresa_origem integer,
        id_empresa_destino integer,
        tipo text,
        valor real,
        data date,
        descricao text
    );
'''

# função para carregar dados no SQLite
def carregar_para_sqlite(banco_dados='dados.db', pasta_csv='.'):
    """
    Carrega dados CSV tratados em um banco SQLite com base no schema definido.

    Parâmetros:
    -----------
    banco_dados : str
        Caminho para o arquivo .db do SQLite (será criado se não existir).

    pasta_csv : str
        Caminho da pasta contendo os arquivos .csv.
    """
    arquivos_csv = listar_arquivos_csv(pasta_csv)
    conexao = sqlite3.connect(banco_dados)
    cursor = conexao.cursor()

    cursor.executescript(script_schema)

    for nome_tabela, caminho_arquivo in arquivos_csv.items():
        print(f'carregando {nome_tabela} ...')
        dados = tratar_csv(caminho_arquivo, nome_tabela)

        colunas = ', '.join(dados.columns)
        placeholders = ', '.join(['?' for _ in dados.columns])
        query = f'insert into {nome_tabela} ({colunas}) values ({placeholders})'

        cursor.executemany(query, dados.values.tolist())
        conexao.commit()

    print('dados carregados com sucesso.')
    conexao.close()

# executar carga
if __name__ == '__main__':
    carregar_para_sqlite()
    print('pipeline concluído.')


