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

### Executar Aplicação Streamlit

```bash
streamlit run app.py
```

## 🗂️ Modelos Principais

### FundosII
Representa fundos imobiliários com os campos:
- `nome` - Nome do fundo
- `sigla` - Sigla do fundo
- `cnpj` - CNPJ do fundo

### Acoes
Representa ações de investimento

### DocumentosFII
Armazena documentos de fundos imobiliários

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

Especificar licença do projeto

## 🤝 Contribuindo

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## ❓ Suporte

Para dúvidas ou problemas, abra uma issue no repositório.
