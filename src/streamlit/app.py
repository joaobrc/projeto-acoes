import streamlit as st
from projeto_acoes.pegar_relatorios import RelatorioFii, CadastroFundos
from projeto_acoes.database import get_db

st.title('Gerenciamento de Fundos Imobiliários')


aba_gerenciar, aba_relatorios, aba_fundos_cadastrados = st.tabs(
    ['Gerenciar Fundos', 'Relatórios de Fundos', 'Fundos Cadastrados']
)


@st.cache_data
def get_fundos():
    db = next(get_db())
    cadastro = CadastroFundos(db)
    return [
        {'Nome': fundo.nome, 'Sigla': fundo.sigla, 'CNPJ': fundo.cnpj}
        for fundo in cadastro.get_fundos()
    ]


def colunas_fundos(coluna, dados_fundos):
    with coluna:
        st.metric(
            label=dados_fundos['Nome'],
            value=dados_fundos['Sigla'],
            delta=dados_fundos['CNPJ'],
        )


with aba_relatorios:
    st.header('Relatórios de Fundos')
    fundo = st.selectbox(
        'Selecione um fundo para visualizar o relatório',
        options=get_fundos(),
        format_func=lambda x: x['Nome'],
    )
    data_inicio = st.date_input('Data de Início', format='DD/MM/YYYY')
    data_fim = st.date_input('Data de Fim', format='DD/MM/YYYY')
    pesquisar = st.button('Pesquisar Relatório')
    if pesquisar:
        relatorio = RelatorioFii(
            db=next(get_db()),
            sigla_fundo=fundo['Sigla'],
            data_inicial=data_inicio,
            data_final=data_fim,
        )
        dados_relatorio = relatorio.dados_pagina_fundos()
        st.write(dados_relatorio)


with aba_gerenciar:
    dados_fundos = get_fundos()
    st.subheader('Fundos Cadastrados')
    if dados_fundos:
        with st.container(horizontal=True, gap='medium'):
            colunms = st.columns(len(dados_fundos[:3]), width=1000)
            for coluna, fundo in enumerate(dados_fundos[:3]):
                colunas_fundos(colunms[coluna], fundo)
            if len(dados_fundos) > 3:
                st.warning(
                    "Apenas os 3 primeiros fundos são exibidos aqui. Para ver todos os fundos cadastrados, acesse a aba 'Fundos Cadastrados'."
                )

    deletar = st.toggle('Deletar Fundo', value=False)
    if not deletar:
        st.header('Cadastro de Fundos')
        nome_fundo = st.text_input('Nome do Fundo')
        sigla_fundo = st.text_input('Sigla do Fundo')
        cnpj_fundo = st.text_input('CNPJ do Fundo')
        if st.button('Cadastrar Fundo'):
            with st.spinner('Cadastrando fundo...'):
                cadastro = CadastroFundos(db=next(get_db()))
                fundo = cadastro.cadastrar_fundos(
                    nome_fundo, sigla_fundo, cnpj_fundo
                )
                dados_fundos = get_fundos()
                st.write(dados_fundos)
                st.success(f'Fundo {fundo.nome} cadastrado com sucesso!')
            st.cache_data.clear()
            st.rerun()
    else:
        if not dados_fundos:
            st.warning('Nenhum fundo cadastrado para deletar.')
        else:
            st.header('Deletar Fundo Cadastrado')
            sigla_fundo = st.selectbox(
                'Selecione a sigla do fundo para deletar',
                options=[fundo['Sigla'] for fundo in dados_fundos],
            )
            st.warning(
                f'Tem certeza que deseja deletar o fundo com sigla {sigla_fundo}?\nEsta ação não pode ser desfeita e deletará todos os documentos relacionados a este fundo.'
            )
            deletar_fundo = st.button('Deletar Fundo')
            if deletar_fundo and sigla_fundo:
                with st.spinner('Deletando fundo...'):
                    cadastro = CadastroFundos(db=next(get_db()))
                    sucesso = cadastro.deletar_fundo(sigla_fundo)
                    if sucesso:
                        st.success(
                            f'Fundo com sigla {sigla_fundo} deletado com sucesso!'
                        )
                    else:
                        st.error(
                            f'Erro ao deletar fundo com sigla {sigla_fundo}.'
                        )
                st.cache_data.clear()
                st.rerun()


with aba_fundos_cadastrados:
    st.header('Fundos Cadastrados')
    if dados_fundos:
        for i in range(0, len(dados_fundos), 3):
            with st.container(horizontal=True, gap='medium'):
                colunms = st.columns(len(dados_fundos[i : i + 3]), width=1000)
                for coluna, fundo in enumerate(dados_fundos[i : i + 3]):
                    colunas_fundos(colunms[coluna], fundo)
    else:
        st.warning('Nenhum fundo cadastrado.')
