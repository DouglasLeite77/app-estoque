import pandas as pd
import streamlit as st

# %% 

from data_manager import (
    con,
    inserir_novo_item,
    inserir_nova_origem,
    inserir_novo_destino,
    inserir_nova_medida,
    retirar_item,
    retirar_origem,
    retirar_destino,
    retirar_medida,
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
    page_title="Gerenciamento de campos",
    page_icon="📦"
)

st.title("Gerenciamento de campos")

gerenciamento = st.radio(
    label="Tipo de Transação",
    options=["Cadastras", "Retirar"],
    index=0,
    horizontal=True
)

col1, col2, col3, col4 = st.columns([1,1.2,1.2,1.2])

def set_menu(nome_menu):
        st.session_state.menu = nome_menu


if 'menu' not in st.session_state:
    st.session_state.menu = None
    
if 'feedback' not in st.session_state:
    st.session_state.feedback = None

with col1:
    btn_item = st.button("Item", on_click=set_menu, args=['item'])
with col2:
    btn_origem = st.button("Origem", on_click=set_menu,args=['origem'])
with col3:
    btn_destino = st.button("Destino", on_click=set_menu, args=['destino'])
with col4:
    btn_medida = st.button("Medida", on_click=set_menu, args=['medida'])

if st.session_state.feedback:
    st.success(st.session_state.feedback)
    st.session_state.feedback = None
if gerenciamento == "Cadastras":
    
    if st.session_state.menu == 'item':
        st.subheader("Cadastro de item")
        nome_item = st.text_input("Digite o nome do item que deseja cadastrar")
        btn_registrar = st.button("Cadastrar")

        if btn_registrar:
            if nome_item in lista_itens:
                st.error(f"Item '{nome_item} já esta cadastrado") 
            else:
                if nome_item != "":
                        inserir_novo_item(con, nome_item)    
                        st.session_state.feedback = f"Item '{nome_item}' cadastrado com sucesso"
                        st.session_state.menu = None
                        st.rerun()
                else:
                    st.error("Digite o nome do item")
    elif st.session_state.menu == 'origem':
        st.subheader("Cadastro de local origem")
        nome = st.text_input("Digite o nome do local de origem que deseja cadastrar")
        btn_registrar_or = st.button("Cadastrar")

        if btn_registrar_or:
            if nome in lista_origens:
                st.error(f"Item '{nome} já esta cadastrado") 
            else:
                if nome != "":
                        inserir_nova_origem(con, nome)    
                        st.session_state.feedback = f"Local '{nome}' cadastrado com sucesso"
                        st.session_state.menu = None
                        st.rerun()
                else:
                    st.error("Digite o nome do local origem")
    elif st.session_state.menu == 'destino':
        st.subheader("Cadastro de local destino")
        nome = st.text_input("Digite o nome do local de destino que deseja cadastrar")
        btn_registrar_or = st.button("Cadastrar")

        if btn_registrar_or:
            if nome in lista_destinos:
                st.error(f"Item '{nome} já esta cadastrado") 
            else:
                if nome != "":
                        inserir_novo_destino(con, nome)    
                        st.session_state.feedback = f"Local '{nome}' cadastrado com sucesso"
                        st.session_state.menu = None
                        st.rerun()
                else:
                    st.error("Digite o nome do local destino")
    elif st.session_state.menu == 'medida':
        st.subheader("Cadastro de medida")
        nome = st.text_input("Digite o nome da medida que deseja cadastrar")
        btn_registrar_or = st.button("Cadastrar")

        if btn_registrar_or:
            if nome in lista_medida:
                st.error(f"Item '{nome} já esta cadastrado") 
            else:
                if nome != "":
                        inserir_nova_medida(con, nome)    
                        st.session_state.feedback = f"Medida '{nome}' cadastrado com sucesso"
                        st.session_state.menu = None
                        st.rerun()
                else:
                    st.error("Digite o nome da medida")
elif gerenciamento == "Retirar":
    
    if st.session_state.menu == "item":
        st.subheader("Retirar item")
        item = st.selectbox("Itens", options=lista_itens)
        btn_retirar = st.button("Retirar", key="item")
        if btn_retirar:
            if item != "":
                retirar_item(con, item)
                st.session_state.feedback = f"Item '{item}' retirado com sucesso"
                st.session_state.menu = None
                st.rerun()
            else:
                st.error("Selecione o nome do item")
                
    if st.session_state.menu == "origem":
        st.subheader("Retirar origem")
        origem = st.selectbox("Origens", options=lista_origens)
        btn_retirar = st.button("Retirar",key="origem")
        if btn_retirar:
            if origem != "":
                retirar_origem(con,origem)
                st.session_state.feedback = f"Item '{origem}' retirado com sucesso"
                st.session_state.menu = None
                st.rerun()
            else:
                st.error("Selecione o nome da origem")
            
    if st.session_state.menu == "destino":
        st.subheader("Retirar destino")
        destino = st.selectbox("destino", options=lista_destinos)
        btn_retirar = st.button("Retirar",key="destino")
        if btn_retirar:
            if destino != "":
                retirar_destino(con,destino)
                st.session_state.feedback = f"Item '{destino}' retirado com sucesso"
                st.session_state.menu = None
                st.rerun()
            else:
                st.error("Selecione o nome do destino")

    if st.session_state.menu == "medida":
        st.subheader("Retirar medida")
        medida = st.selectbox("medida", options=lista_medida)
        btn_retirar = st.button("Retirar",key="medida")
        if btn_retirar:
            if medida != "":
                retirar_medida(con,medida)
                st.session_state.feedback = f"Item '{medida}' retirado com sucesso"
                st.session_state.menu = None
                st.rerun()
            else:
                st.error("Selecione o nome do medida")