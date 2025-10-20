# Home.py

import streamlit as st

st.set_page_config(
    page_title="App de Estoque Principal",
    page_icon="📦"
)

st.title("📦 Bem-vindo ao Gerenciamento de Estoque")
st.markdown("""
Este aplicativo permite o controle de entrada e saída de itens de estoque,
além do gerenciamento dos campos de cadastro.

Use o menu lateral esquerdo para navegar entre as seguintes seções:

* **Registro de Transação:** Para adicionar entradas e saídas.
* **Gerenciamento de Campos:** Para cadastrar/remover Itens, Origens, Destinos e Medidas.
""")