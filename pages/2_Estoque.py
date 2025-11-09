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
    get_qtd,
)

# %%


st.title("Controle de estoque")

col1, col2, col3 = st.columns([1,0.2,1])

with col1:
    st.subheader("Nivél de estoque")
    lista_itens= get_lista_itens(con)
    for i in lista_itens:
        nome, qtd = get_qtd(con,i,"Matriz")
        porcentagem = qtd / 1000
        if porcentagem > 1.0:
            porcentagem = 1.0
        texto_progresso = f"{nome} — {qtd} unidades"
        st.progress(porcentagem, texto_progresso)
    
with col3:

    medidas = get_lista_medidas(con)
    st.subheader("Adicionar estoque")
    item = st.selectbox(label="Selecione o item", options=lista_itens)
    qtd = st.number_input("Digite a quantidade", min_value=0)
    med =st.selectbox("Selecione a medida", options=medidas)
    local = "Matriz"
    btn = st.button("Adicionar")
    if btn:
        add_estoque(con,item,qtd,local)
        pass