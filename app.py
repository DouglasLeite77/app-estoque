# %%
import pandas as pd
import streamlit as st
import csv
import os


botao_csv = st.button("Criar tabela")
if botao_csv:
    if not os.path.exists("Estoque.csv"):
        with open("Estoque.csv", 'w', newline="", encoding='utf-8') as arquivo_csv:
            escritor = csv.writer(arquivo_csv)     
    dados = []   


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
    
    data = pd.to_datetime("now")
    nova_transacao = {"data": data, "item": item_input, "quantidade": quantidade_input,"Origem": origem_input, "Destino": destino_input, "obs": obs}
    st.session_state.dados.append(nova_transacao)
    print(st.session_state.dados)
    
    
    
if st.session_state.dados:
    st.subheader("Dados Atuais")
    st.dataframe(pd.DataFrame(st.session_state.dados))
