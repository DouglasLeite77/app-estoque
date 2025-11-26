import streamlit as st

st.set_page_config(
    page_title="Gestão de Estoque",
    layout="wide"
)

st.title("Sistema de Gerenciamento de Estoque")
st.markdown("### Um projeto em Python para controle logístico")

st.divider()
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("Sobre o Projeto")
    st.write("""
    Este aplicativo foi desenvolvido para simular um sistema real de controle de inventário.
    O objetivo é permitir o gerenciamento eficiente de entradas, saídas e transferências de itens
    entre diferentes locais de armazenamento.
    
    **Principais Funcionalidades:**
    * ✅ **Dashboard em Tempo Real:** Visualização de KPIs e níveis de estoque.
    * ✅ **CRUD Completo:** Adição e remoção de itens e locais.
    * ✅ **Rastreabilidade:** Histórico detalhado de todas as movimentações (Logs).
    * ✅ **Persistência de Dados:** Banco de dados SQL integrado.
    """)

with col2:
    st.subheader("Tecnologias")
    st.write("**Linguagem:** Python 3.10+")
    st.write("**Framework Web:** Streamlit")
    st.write("**Manipulação de Dados:** Pandas")
    st.write("**Banco de Dados:** SQLite3")
    st.info("Solução Cloud: Implementação de lógica para escrita em *readonly filesystem* usando `/tmp`.")

st.divider()


st.subheader("Guia de Navegação")

col_a, col_b, col_c= st.columns(3)

with col_a:
    st.markdown("#### 1. Relatório")
    st.markdown("Visão geral do estoque, histórico de transferencias e métricas de ocupação.")

with col_b:
    st.markdown("#### 2. Estoque")
    st.markdown("Gerenciamente especifico de cada local e registro de entrada ou saída para destinos externos")

with col_c:
    st.markdown("#### 3. Manejamento")
    st.markdown("Realize transferências entre locais e registre entradas/saídas.")



st.divider()
st.markdown("### Desenvolvido por Douglas Leite")

col_social1, col_social2, col_social3 = st.columns([1,1,10])

with col_social1:
    st.link_button("LinkedIn", "https://www.linkedin.com/in/douglas-renan-0983b4240/")

with col_social2:
    st.link_button("GitHub", "https://github.com/DouglasLeite77")