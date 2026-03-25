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