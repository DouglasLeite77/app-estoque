import streamlit as st
from google.oauth2.service_account import Credentials
import gspread
import sqlite3

# %%


# %%
@st.cache_resource
def conexao_bd():
    con = sqlite3.connect('estoque.db', check_same_thread=False, timeout=30)
    
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
    con.execute('''
            CREATE TABLE IF NOT EXISTS estoque(
                id_item INTEGER ,
                id_local INTEGER ,
                quantidade  REAL NOT NULL DEFAULT 0,
                PRIMARY KEY (id_item, id_local),
                FOREIGN KEY (id_item) REFERENCES itens_bd(id) ON DELETE RESTRICT,
                FOREIGN KEY (id_local) REFERENCES origens_bd(id) ON DELETE RESTRICT
                )
        ''')
    con.execute("""
        CREATE TABLE IF NOT EXISTS historico (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            data_hora TEXT,
            item TEXT,
            origem TEXT,
            destino TEXT,
            quantidade INTEGER,
            usuario TEXT
        )
    """)

    con.commit()
    return con

con = conexao_bd()

# %%
def registrar_transf(item, origem, destino, quantidade,dataHora, usuario="Admin"):
    cursor = con.cursor()
    
    cursor.execute("INSERT INTO historico (data_hora, item, origem, destino, quantidade, usuario) VALUES (?, ?, ?, ?, ?, ?)", (dataHora, item, origem, destino, quantidade, usuario))
    con.commit()
    cursor.close()

def get_qtd(conn, item, local):
    cursor = conn.cursor()
    
    cursor.execute("SELECT id_item, quantidade FROM estoque WHERE id_item = ? and id_local = ?", (item,local))
    
    lista = cursor.fetchone()
    if lista:
        nome = lista[0]
        qtd = lista[1]
        return nome, qtd
    else:
        nome = item
        return item, 0    
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
    
def transacoes_estoque(conn,item, qtd, origem, destino):
    

    if remove_estoque(conn,item, qtd, origem):
        add_estoque(conn,item, qtd, destino)
        return True
    conn.commit()

def add_estoque(conn, item, qtd, local):
    
    cursor = conn.cursor()

    cursor.execute("SELECT quantidade FROM estoque WHERE id_item = ? AND id_local = ?", (item, local))
    
    registro = cursor.fetchone()
    
    if registro:
        qtd_atual = registro[0]
        nova_qtd = qtd_atual + qtd
        cursor.execute("UPDATE estoque SET quantidade = ? WHERE id_item = ? AND id_local = ?", (nova_qtd,item,local))
    else:
        cursor.execute("INSERT INTO estoque (id_item, id_local, quantidade) VALUES (?,?,?)", (item,local,qtd))
        
    print(f"Adição de estoque concluída: Item {item} no Local {local} adicionado em {qtd} unidades.")
    
def remove_estoque(conn, item, qtd, local):
    
    cursor = conn.cursor()

    cursor.execute("SELECT quantidade FROM estoque WHERE id_item = ? AND id_local = ?", (item, local))
    
    registro = cursor.fetchone()
    if not registro:
        st.error("Produto sem registro")
        return
    
    else:
        qtd_atual = registro[0]
        if qtd_atual < qtd:
            st.error("Quantidade insuficiente")
            return
        else:
            nova_qtd = qtd_atual - qtd
            cursor.execute("UPDATE estoque SET quantidade = ? WHERE id_item = ? AND id_local = ?", (nova_qtd,item,local))   
            print(f"Remoção de estoque concluída: Item {item} no Local {local} removendo {qtd} unidades.")
            return True