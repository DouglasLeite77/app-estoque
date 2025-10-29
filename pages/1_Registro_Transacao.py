# %%
import pandas as pd
import streamlit as st

# %%

from data_manager import (
    con,
    aba_transacoes, 
    get_lista_itens,
    get_lista_origens,
    get_lista_destinos,
    get_lista_medidas,
)

lista_itens = get_lista_itens(con)
lista_origens = get_lista_origens(con)
lista_destinos = get_lista_destinos(con)
lista_medida = get_lista_medidas(con)

# %%

st.set_page_config(
    page_title="Registro de transações",
    page_icon="📦"
)

st.title("Gerenciamento de estoque")

if not "dados" in st.session_state:
    st.session_state.dados = []

item_input = st.selectbox(label="Selecione o item", options=lista_itens)

col1, col2 = st.columns(2)
with col1:
    quantidade_input = st.number_input(label="Digite a quantidade", min_value=0)

with col2:
    medida_unidade = st.selectbox(label="Selecione a unidade de medida", options=lista_medida)

origem_input = st.selectbox(label="Selecione a origem", options=lista_origens)

destino_input = st.selectbox(label="Selecione o destino", options=lista_destinos)

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
        nova_linha = list(nova_transacao.values())
        aba_transacoes.append_row(nova_linha)
        st.session_state.dados.append(nova_transacao)
            
        
if st.session_state.dados:
    st.subheader("Dados Atuais")
    st.dataframe(pd.DataFrame(st.session_state.dados))
