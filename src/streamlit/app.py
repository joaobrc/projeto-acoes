import streamlit as st
from src.projeto_acoes.pegar_relatorios import RelatorioFii

st.title("Doc Ações")

with st.sidebar:
    st.sidebar.header("Menu Lateral")
    st.sidebar.write("Formulário de Ações")
    acao = st.sidebar.text_input("Digite o nome da ação")
    data_pesquisa = st.sidebar.date_input("Data de Pesquisa Inicial", format="DD/MM/YYYY")
    data_pesquisa_final = st.sidebar.date_input("Data de Pesquisa Final", format="DD/MM/YYYY")
    pesquisa = st.sidebar.button("Pesquisar")

if pesquisa:
    pesquisa_fii = RelatorioFii()