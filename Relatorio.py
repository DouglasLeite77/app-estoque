# Home.py

import streamlit as st

from data_manager import(
    con,
    get_lista_itens,
    get_lista_origens,
    get_lista_destinos,
    get_lista_medidas,
    get_qtd
)


st.title("Bem-vindo ao Gerenciamento de Estoque")
st.subheader("Visão geral sobre o estoque")

col1, col2 = st.columns([1,1])
lista_itens = get_lista_itens(con)
lista_locais = get_lista_origens(con)
with col1:
    for i in lista_itens:
        st.subheader(i)
        for x in lista_locais:
            nome, qtd = get_qtd(con,i,x)
            porcentagem = qtd / 1000
            if porcentagem > 1.0:
                porcentagem = 1.0
            texto_progresso = f"{x} — {qtd} unidades"
            st.progress(porcentagem, texto_progresso)