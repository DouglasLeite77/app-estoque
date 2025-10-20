import streamlit as st
from google.oauth2.service_account import Credentials
import gspread
import sqlite3

# %%

@st.cache_resource()
def get_gspread_client():
    SCOPE = [
        'https://www.googleapis.com/auth/spreadsheets',
        'https://www.googleapis.com/auth/drive'
    ]

    creds = Credentials.from_service_account_file("./keys/credenciais.json", scopes=SCOPE)

    cliente_gs = gspread.authorize(creds)
    return cliente_gs
    
@st.cache_resource()
def get_sheet(_c, esc):
    nome_panilha = "app-estoque"

    panilha = _c.open(nome_panilha)

    aba = panilha.worksheet(esc)
    return aba

cliente = get_gspread_client()
aba_saidas = get_sheet(cliente, "Saídas")
aba_entradas = get_sheet(cliente, "Entradas")

# %%
@st.cache_resource
def conexao_bd():
    con = sqlite3.connect('estoque.bd', check_same_thread=False, isolation_level=None)
    
    con.execute('''
                CREATE TABLE IF NOT EXISTS itens_bd(
                    id INTEGER PRIMARY KEY,
                    nome_item TEXT UNIQUE NOT NULL
                    )
            ''')
    con.execute('''
                CREATE TABLE IF NOT EXISTS origens_bd(
                    id INTEGER PRIMARY KEY,
                    nome_origem TEXT UNIQUE NOT NULL
                    )
            ''')
    con.execute('''
                CREATE TABLE IF NOT EXISTS destinos_bd(
                    id INTEGER PRIMARY KEY,
                    nome_destino TEXT UNIQUE NOT NULL
                    )
            ''')
    con.execute('''
                CREATE TABLE IF NOT EXISTS medidas_bd(
                    id INTEGER PRIMARY KEY,
                    nome_medida TEXT UNIQUE NOT NULL
                    )
            ''')

    con.commit()
    return con

con = conexao_bd()


# %%

def get_lista_itens(conn):
    cursor = conn.cursor()
    
    cursor.execute("SELECT nome_item FROM itens_bd ORDER BY nome_item")
    lista = [row[0] for row in cursor.fetchall()]
    return lista
def get_lista_origens(conn):
    cursor = conn.cursor()
    
    cursor.execute("SELECT nome_origem FROM origens_bd ORDER BY nome_origem")
    lista = [row[0] for row in cursor.fetchall()]
    return lista
def get_lista_destinos(conn):
    cursor = conn.cursor()
    
    cursor.execute("SELECT nome_destino FROM destinos_bd ORDER BY nome_destino")
    lista = [row[0] for row in cursor.fetchall()]
    return lista
def get_lista_medidas(conn):
    cursor = conn.cursor()
    
    cursor.execute("SELECT nome_medida FROM medidas_bd ORDER BY nome_medida")
    lista = [row[0] for row in cursor.fetchall()]
    return lista

def retirar_item(conn, nome):
    cursor = conn.cursor()
    
    conn.commit()
    cursor.execute("DELETE from itens_bd WHERE nome_item = (?)", (nome,))
    
def retirar_origem(conn, nome):
    cursor = conn.cursor()
    
    conn.commit()
    cursor.execute("DELETE from origens_bd WHERE nome_origem = (?)", (nome,))
    
def retirar_destino(conn, nome):
    cursor = conn.cursor()
    
    conn.commit()
    cursor.execute("DELETE from destinos_bd WHERE nome_destino = (?)", (nome,))
    
def retirar_medida(conn, nome):
    cursor = conn.cursor()
    
    conn.commit()
    cursor.execute("DELETE from medidas_bd WHERE nome_medida = (?)", (nome,))

def inserir_novo_item(conn, nome):
    
    cursor = conn.cursor()
    cursor.execute("INSERT INTO itens_bd(nome_item) VALUES (?)", (nome,))
    conn.commit()

def inserir_nova_origem(conn, nome):
    
    cursor = conn.cursor()
    conn.commit()
    cursor.execute("INSERT INTO origens_bd(nome_origem) VALUES (?)", (nome,))

def inserir_novo_destino(conn, nome):
    
    cursor = conn.cursor()
    conn.commit()
    cursor.execute("INSERT INTO destinos_bd(nome_destino) VALUES (?)", (nome,))
    
def inserir_nova_medida(conn, nome):
    
    cursor = conn.cursor()
    conn.commit()
    cursor.execute("INSERT INTO medidas_bd(nome_medida) VALUES (?)", (nome,))

