import pandas
import streamlit as st

from data_manager import (
    con,
    aba_transacoes, 
    get_lista_itens,
    get_lista_origens,
    get_lista_destinos,
    get_lista_medidas,
    transacoes_estoque,
    add_estoque,
)

# %%


st.title("Adição de estoque")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Nivél de estoque")
    