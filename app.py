# %%
import pandas as pd
import streamlit as st
import csv
import os
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
# ------------------------------------------------- BANCO DE DADOS ----------------------------------------------------------------- 
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


# ------------------------------------------------------------------------------------------------------------------

# %%

origens = {"Cras1": 1, "Cras2": 2}
destinos = {"Cras1": 1, "Cras2": 2}
medidas = ["kg", "L", "g"]


def get_lista_itens(conn):
    cursor = conn.cursor()
    
    cursor.execute("SELECT nome_item FROM itens_bd ORDER BY nome_item")
    lista = [row[0] for row in cursor.fetchall()]
    return lista

def inserir_novo_item(conn, nome):
    
    cursor = conn.cursor()
    conn.commit()
    cursor.execute("INSERT INTO itens_bd(nome_item) VALUES (?)", (nome,))

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

lista_itens = get_lista_itens(con)

# %%
if not "dados" in st.session_state:
    st.session_state.dados = []
    


pag_selecionada = st.sidebar.radio("Navegação", ["Registro de Transação", "Gerenciamento de campos"])

if pag_selecionada == "Registro de Transação":

    st.title("Gerenciamento de estoque")
    tipo_transacao = st.radio(
        label="Tipo de Transação",
        options=["Entrada", "Saída"],
        index=0,
        horizontal=True
    )


    item_input = st.selectbox(label="Selecione o item", options=lista_itens)

    col1, col2 = st.columns(2)
    with col1:
        quantidade_input = st.number_input(label="Digite a quantidade", min_value=0)

    with col2:
        medida_unidade = st.selectbox(label="Selecione a unidade de medida", options=medidas)
    origem_input = st.selectbox(label="Selecione a origem", options=origens.keys())

    destino_input = st.selectbox(label="Selecione o destino", options=destinos.keys())

    obs = st.text_input(label="OBSERVAÇÃO")

    botao_estoque = st.button(label="Adicionar")


    if botao_estoque:
        if quantidade_input == 0:
            st.error("Quantidade inválida!")
        elif origem_input == destino_input:
            st.error("Origem e destino são os mesmos, verifique os dados!")
        else:
            data = pd.to_datetime("now")
            data_formatada = pd.to_datetime('now').strftime('%Y-%m-%d %H:%M:%S')
            nova_transacao = {"data": data_formatada, "item": item_input, "quantidade": quantidade_input,"Medida": medida_unidade, "Origem": origem_input, "Destino": destino_input, "obs": obs}
            st.success("Item registrado!")
            print(st.session_state.dados)
            nova_lina = list(nova_transacao.values())
            if tipo_transacao == "Entrada":
                aba_entradas.append_row(nova_lina)
                nova_transacao['Tipo de transação'] = "Entrada"
            elif tipo_transacao == "Saída":
                aba_saidas.append_row(nova_lina)   
                nova_transacao['Tipo de transação'] = "Saída"
            else:
                st.error("Error no tipo de transação") 
            st.session_state.dados.append(nova_transacao)
                
            
    if st.session_state.dados:
        st.subheader("Dados Atuais")
        st.dataframe(pd.DataFrame(st.session_state.dados))
    
    
elif pag_selecionada == "Gerenciamento de campos":
    

    
    
    st.title("Gerenciamento de campos")
    
    col1, col2, col3, col4 = st.columns([1,1.2,1.2,1.2])
    
    if 'menu' not in st.session_state:
        st.session_state.menu = None
        
        
    def set_menu(nome_menu):
            st.session_state.menu = nome_menu

        
    
    with col1:
        btn_item = st.button("Item", on_click=set_menu, args=['item'])
    
    with col2:
        btn_origem = st.button("Origem", on_click=set_menu,args=['origem'])
    
    with col3:
        btn_destino = st.button("Destino", on_click=set_menu, args=['destino'])
    with col4:
        btn_medida = st.button("Medida", on_click=set_menu, args=['medida'])
    

    
    if st.session_state.menu == 'item':
        st.subheader("Cadastro de item")
        nome_item = st.text_input("Digite o nome do item que deseja cadastrar")
        btn_registrar = st.button("Cadastrar")

        if btn_registrar:
            if nome_item != "":
                inserir_novo_item(con, nome_item)
            else:
                st.error("Digite um nome")
    elif st.session_state.menu == 'origem':
        st.subheader("Cadastro de local Origem")
        nome_item = st.text_input("Digite o nome do local que deseja cadastrar")
        btn_registrar_or = st.button("Cadastrar")

        if btn_registrar_or:
            inserir_novo_item(con, nome_item)
            
    