# Projeto Ações 📈

Sistema para gerenciamento e análise de fundos imobiliários (FIIs) e ações, com integração de dados de API, processamento com pandas e interface web com Streamlit.

## 📋 Descrição

Este projeto fornece ferramentas para:
- Cadastro e gerenciamento de fundos imobiliários (FIIs)
- Recuperação de relatórios de fundos
- Armazenamento e consulta de dados em banco de dados SQL
- Processamento e análise de dados de investimentos
- Interface web interativa com Streamlit

## 🛠️ Tecnologias

- **Python** >=3.13
- **SQLAlchemy** - ORM para banco de dados
- **Pandas** - Análise e processamento de dados
- **Streamlit** - Interface web interativa
- **HTTPX** - Cliente HTTP assíncrono
- **BeautifulSoup4** - Web scraping
- **Alembic** - Migrações de banco de dados

### Dependências de Desenvolvimento
- **Pytest** - Framework de testes
- **Pytest-cov** - Cobertura de testes
- **Ruff** - Linter e formatador
- **Taskipy** - Task runner

## 📦 Instalação

### Pré-requisitos
- Python 3.13 ou superior
- Poetry (gerenciador de dependências)

### Passos

1. Clone o repositório:
```bash
git clone <url-do-repositorio>
cd projeto-acoes
```

2. Instale as dependências:
```bash
poetry install
```

3. Ative o ambiente virtual:
```bash
poetry shell
```

4. Configure o banco de dados (se necessário):
```bash
alembic upgrade head
```

## 📂 Estrutura do Projeto

```
projeto-acoes/
├── src/projeto_acoes/
│   ├── __init__.py
│   ├── database.py          # Configuração do banco de dados
│   ├── model.py             # Modelos SQLAlchemy
│   └── pegar_relatorios.py  # Funções para recuperar relatórios
├── tests/
│   ├── test_database.py
│   └── test_pegar_relatorios.py
├── migracao/                # Migrações Alembic
│   └── versions/
├── pyproject.toml           # Configuração do projeto
└── README.md
```

## 🚀 Como Usar

### Executar Aplicação Streamlit

```bash
streamlit run src/streamlit/app.py
```

A aplicação oferece duas abas principais:

#### Aba: Gerenciar Fundos
- **Visualizar Fundos Cadastrados**: Exibe todos os fundos em cards com nome, sigla e CNPJ
- **Cadastrar Novo Fundo**: Crie novos fundos fornecendo:
  - Nome do Fundo
  - Sigla (identificador único)
  - CNPJ
- **Deletar Fundo**: Remova fundos do sistema (ativa com toggle)

#### Aba: Relatórios de Fundos
- **Selecionar Fundo**: Escolha um fundo da lista
- **Definir Período**: Especifique data inicial e final
- **Pesquisar Relatórios**: Busca documentos no período especificado via API FNET
- **Visualizar Resultados**: Exibe todos os documentos encontrados

### Executar os Testes

```bash
task test
```

Isso irá:
1. Formatar o código
2. Executar os testes com cobertura
3. Gerar relatório de cobertura em HTML

### Formatar Código

```bash
task format
```

## 📚 Principais Funcionalidades

### 1. Gerenciamento de Fundos Imobiliários
- Cadastro de novos FIIs com nome, sigla e CNPJ
- Listagem de todos os fundos cadastrados
- Exclusão de fundos e seus documentos associados

### 2. Busca de Relatórios via API
- Integração com a API B3 (FNET) para recuperação de documentos
- Filtro por período de datas customizáveis
- Suporte a diferentes tipos de documentos (Informes Mensais, Relatórios Anuais, etc.)

### 3. Gerenciamento de Documentos
- Armazenamento de documentos em banco de dados SQL
- Prevenção de duplicatas (verifica se documento já existe)
- Download de documentos em formatos múltiplos (PDF, XML, etc.)
- Rastreamento de data de entrega e tipo de documento

### 4. Interface Web Interativa
- Dashboard com abas para diferentes funcionalidades
- Exibição visual de fundos em cards
- Formulários intuitivos para cadastro e pesquisa
- Mensagens de sucesso e tratamento de erros

### 5. Banco de Dados
- Persistência de dados com SQLAlchemy ORM
- Suporte a migrações automáticas com Alembic
- Relacionamento entre Fundos, Documentos e Ações

## 🗂️ Modelos de Dados

### FundosII
Representa fundos imobiliários com os seguintes campos:
- `id` - Identificador único (autoincrement)
- `nome` - Nome descritivo do fundo
- `sigla` - Código único do fundo (usado como identificador na API)
- `cnpj` - CNPJ do fundo

### Acoes
Modelo para gerenciamento de ações (em desenvolvimento):
- `id` - Identificador único
- `nome` - Nome da ação
- `sigla` - Ticker da ação
- `cnpj` - CNPJ da empresa

### DocumentosFII
Armazena documentos baixados de fundos imobiliários:
- `id` - Identificador único
- `id_documento` - ID do documento na API FNET (único)
- `titulo` - Descrição/título do documento
- `tipo` - Tipo de documento (Informe Mensal, Relatório Anual, etc.)
- `id_sigla_fundo` - Referência foreign key para o fundo
- `data_entrega` - Data e hora da entrega do documento

### DocumentosAcoes
Modelo para documentos de ações (estrutura pronta para uso futuro):
- `id` - Identificador único
- `id_documento` - ID único do documento
- `titulo` - Título do documento
- `descricao` - Descrição detalhada
- `id_sigla_acao` - Referência para a ação relacionada

## ⚙️ Recursos Avançados

### Cache de Dados
- A aplicação Streamlit utiliza `@st.cache_data` para otimizar a performance
- Cache é automaticamente limpo após operações de cadastro/exclusão

### Validações e Tratamentos de Erro
- Prevenção de documentos duplicados no banco de dados
- Confirmação antes de deletar fundos e documentos associados
- Exibição de mensagens de alerta quando nenhum fundo está cadastrado
- Tratamento robusto de erros nas requisições HTTP

### Download de Documentos
- Suporte a múltiplos formatos (PDF, XML, etc.)
- Detecção automática do tipo de arquivo
- Armazenamento local com nomenclatura automática

## 📊 Cobertura de Testes

O projeto utiliza Pytest com cobertura de código:
```bash
task test
```

Gera relatório de cobertura em:
- Terminal: resumo de cobertura
- `htmlcov/index.html`: relatório interativo em HTML

## 🔄 Migrações de Banco de Dados

As migrações são gerenciadas com Alembic:

```bash
# Aplicar migrações
alembic upgrade head

# Criar nova migração
alembic revision --autogenerate -m "Descrição da mudança"
```

Versões disponíveis em `migracao/versions/`:
- Migração inicial: estrutura base das tabelas
- Atualização de tabela de documentos

## 📋 Dependências do Projeto

| Pacote | Versão | Propósito |
|--------|--------|----------|
| httpx | ^0.28.1 | Cliente HTTP assíncrono para requisições |
| pandas | ^2.3.2 | Análise e processamento de dados |
| streamlit | ^1.49.1 | Interface web interativa |
| sqlalchemy | ^2.0.43 | ORM para banco de dados |
| beautifulsoup4 | ^4.13.5 | Web scraping de dados |
| filetype | ^1.2.0 | Detecção de tipo de arquivo |
| pydantic | ^2.13.2 | Validação e modelagem de dados |

**Dev Dependencies:**
- pytest: Testes automatizados
- pytest-cov: Cobertura de testes
- ruff: Formatting e linting
- taskipy: Automação de tarefas
- alembic: Migrações de banco de dados

## 🚀 Comandos Disponíveis

| Comando | Descrição |
|---------|-----------|
| `task format` | Formata código com Ruff |
| `task test` | Executa testes com cobertura |
| `task run` | Inicia aplicação Streamlit |

## 📝 Configuração

### Config
O arquivo `src/config/config.py` centraliza configurações:
- URLs de API (FNET)
- URI do banco de dados
- Parâmetros de requisição

### Variáveis de Ambiente
Configure no arquivo `.env` ou variáveis do sistema:
- `DATABASE_URL` - conexão com banco de dados
- URLs de API (se necessário)

## 🔮 Próximas Melhorias

- [ ] Implementar gerenciamento de Ações
- [ ] Adicionar gráficos de análise de rentabilidade
- [ ] Suporte a exportação de dados (CSV, Excel)
- [ ] Dashboard com estatísticas agregadas
- [ ] Histórico de cotações de FIIs
- [ ] Alertas automáticos de novos relatórios
- [ ] Autenticação de usuários


## 📊 Exemplo de Uso

```python
from src.projeto_acoes.pegar_relatorios import CadastroFundos
from src.projeto_acoes.database import get_session

# Criar sessão do banco
db = get_session()

# Cadastrar fundo
cadastro = CadastroFundos(db)
fundo = cadastro.cadastrar_fundos(
    nome_fundo="Fundo XYZ",
    sigla_fundo="XYZ",
    cnpj_fundo="00.000.000/0000-00"
)

# Recuperar fundos
fundos = cadastro.get_fundos()
```

## 🧪 Testes

O projeto usa Pytest para testes unitários e de integração. Os testes cobrem:
- Operações de banco de dados
- Recuperação de relatórios
- Integração com APIs

Execute com cobertura:
```bash
task test
```

Os resultados de cobertura estão em `htmlcov/index.html`

## 🔧 Configuração de Desenvolvimento

### Linting e Formatação

O projeto usa **Ruff** para linting e formatação com as seguintes configurações:
- Comprimento de linha: 79 caracteres
- Estilo de aspas: single quotes

### Migrações de Banco de Dados

Use Alembic para criar e gerenciar migrações:

```bash
# Criar nova migração
alembic revision --autogenerate -m "descrição da migração"

# Aplicar migrações
alembic upgrade head

# Reverter última migração
alembic downgrade -1
```

## 📝 Requisitos de Sistema

- Python >= 3.13, < 4.0
- Dependências listadas em `pyproject.toml`

## 👤 Autor

João - joaobrc97@gmail.com

## 📄 Licença

Este projeto é desenvolvido como projeto de estudos.

## 🤝 Contribuindo

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## ❓ Suporte

Para dúvidas ou problemas, abra uma issue no repositório.
