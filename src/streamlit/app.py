import streamlit as st
from projeto_acoes.pegar_relatorios import RelatorioFii, CadastroFundos
from projeto_acoes.database import get_db

st.title("Doc Ações")

aba_cadastra, aba_relatorios = st.tabs(["Cadastro de Fundos", "Relatórios de Fundos"])

@st.cache_data
def get_fundos():
    db = next(get_db())
    cadastro = CadastroFundos(db)
    return [{'Nome': fundo.nome, 'Sigla': fundo.sigla, 'CNPJ': fundo.cnpj} for fundo in cadastro.get_fundos()]


with aba_relatorios:
    st.header("Relatórios de Fundos")
    fundo = st.selectbox("Selecione um fundo para visualizar o relatório",
        options=get_fundos(), format_func=lambda x: x['Nome']
    )
    data_inicio = st.date_input("Data de Início", format="DD/MM/YYYY")
    data_fim = st.date_input("Data de Fim", format="DD/MM/YYYY")
    pesquisar = st.button("Pesquisar Relatório")
    if pesquisar:
        relatorio = RelatorioFii(db=next(get_db()),
        sigla_fundo=fundo['Sigla'],
        data_inicial=data_inicio,
        data_final=data_fim)
        dados_relatorio = relatorio.dados_pagina_fundos()
        st.write(dados_relatorio)

with aba_cadastra:
    dados_fundos = get_fundos()
    st.write(dados_fundos)
    st.header("Cadastro de Fundos")
    nome_fundo = st.text_input("Nome do Fundo")
    sigla_fundo = st.text_input("Sigla do Fundo")
    cnpj_fundo = st.text_input("CNPJ do Fundo")
    if st.button("Cadastrar Fundo"):
        with st.spinner("Cadastrando fundo..."):
            cadastro = CadastroFundos(db=next(get_db()))
            fundo = cadastro.cadastrar_fundos(nome_fundo, sigla_fundo, cnpj_fundo)
            dados_fundos = get_fundos()
            st.write(dados_fundos)
            st.success(f"Fundo {fundo.nome} cadastrado com sucesso!")