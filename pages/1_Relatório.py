
import streamlit as st
import pandas as pd

from data_manager import(
    con,
    get_lista_itens,
    get_lista_origens,
    get_lista_destinos,
    get_lista_medidas,
    get_qtd,
    get_transf
)

st.markdown(
    """
    <style>
    .block-container {
        max-width: 1200px !important;
        padding-top: 2rem !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.subheader("Visão geral sobre o estoque")

col1, col2, col3 = st.columns([0.8,0.2,1])
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
            
with col3:
    st.subheader("Historico recente de transferencias")
    lista_transf = get_transf(con)
    st.dataframe(pd.DataFrame(lista_transf), hide_index=True)