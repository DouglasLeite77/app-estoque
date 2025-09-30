# %%
import pandas as pd
import streamlit as st
import csv
import os
from google.oauth2.service_account import Credentials
import gspread

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
def get_sheet(cliente):
    nome_panilha = "app-estoque"

    panilha = cliente.open(nome_panilha)

    aba_estoque = panilha.worksheet("estoque")
    return aba_estoque

cliente = get_gspread_client()
aba_estoque = get_sheet(cliente)

# %%
if not "dados" in st.session_state:
    st.session_state.dados = []
    

st.title("Gerenciamento de estoque")

itens = {"Arroz": 0, "Feijão": 0, "Açúcar": 0, "Café": 0}
origens = {"Cras1": 1, "Cras2": 2}
destinos = {"Cras1": 1, "Cras2": 2}


item_input = st.selectbox(label="Selecione o item", options=itens.keys())

quantidade_input = st.number_input(label="Digite a quantidade", min_value=0)

origem_input = st.selectbox(label="Selecione a origem", options=origens.keys())
destino_input = st.selectbox(label="Selecione o destino", options=destinos.keys())
obs = st.text_input(label="OBSERVAÇÃO")
botao_estoque = st.button(label="Adicionar")



if botao_estoque:
    if quantidade_input == 0:
        st.markdown("Quantidade inválida!")
    elif origem_input == destino_input:
        st.markdown("Origem e destino são o mesmo, verifique os dados!")
    else:
        data = pd.to_datetime("now")
        data_formatada = pd.to_datetime('now').strftime('%Y-%m-%d %H:%M:%S')
        nova_transacao = {"data": data_formatada, "item": item_input, "quantidade": quantidade_input,"Origem": origem_input, "Destino": destino_input, "obs": obs}
        st.session_state.dados.append(nova_transacao)
        print(st.session_state.dados)
        nova_lina = list(nova_transacao.values())
        aba_estoque.append_row(nova_lina)
        
if st.session_state.dados:
    st.subheader("Dados Atuais")
    st.dataframe(pd.DataFrame(st.session_state.dados))
    
    
    
