import pandas
import streamlit as st
import time

from data_manager import (
    con,
    get_lista_itens,
    get_lista_origens,
    get_lista_destinos,
    get_lista_medidas,
    transacoes_estoque,
    add_estoque,
    get_qtd,
    remove_estoque,
)

# %%


st.markdown(
    """
    <style>
    .block-container {
        max-width: 1500px !important;
    }
    div[role="radiogroup"] {
        display: flex !important;
        justify-content: center !important;
        aling-itens: center !important;
        text-aling: center !important;
    }
    .stRadio > label {
    justify-content: center !important;
    width: 100% !important;
    }
    div[data-testid="stMetric"] {
    margin-bottom: -20px !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)
st.title("Controle de estoque")
col1, col2 = st.columns([1,1], gap="medium")
with col1:
    st.subheader("Nivél de estoque")
    lista_itens = get_lista_itens(con)
    locais = get_lista_origens(con)
    local = st.selectbox(label="Selecione o local",options=locais)
    for i in lista_itens:
        nome, qtd = get_qtd(con,i,local)
        porcentagem = qtd / 1000
        if porcentagem > 1.0:
            porcentagem = 1.0
        defic = qtd - 500
        st.metric(label=nome, value=qtd, delta=defic,help="Valor aceitavel de 500")
        st.progress(porcentagem)
    
        

with col2:
    medidas = get_lista_medidas(con)
    tab_entrada, tab_saida = st.tabs(["📥 Entrada", "📤 Saída"])
    with tab_entrada:
        st.subheader("Entrada de estoque")
        item = st.selectbox(label="Selecione o item", options=lista_itens, key="item_entrada")
        qtd = st.number_input("Digite a quantidade", min_value=0, key="qtd_entrada")
        med =st.selectbox("Selecione a medida", options=medidas, index=1, key="med_entrada")
        btn = st.button("Adicionar", key="btn_entrada")
        if btn:
            add_estoque(con,item,qtd,local)
            st.success("Item adicionado ao estoque")
            time.sleep(2)
            st.rerun()
            

    with tab_saida:
        st.subheader("Saida de estoque")
        item = st.selectbox(label="Selecione o item", options=lista_itens, key="item_saida")
        qtd = st.number_input("Digite a quantidade", min_value=0, key="qtd_saida")
        med =st.selectbox("Selecione a medida", options=medidas, index=1, key="med_saida")
        btn = st.button("Adicionar", key="btn_saida")
        if btn:
            remove_estoque(con,item,qtd,local)

