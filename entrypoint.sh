#!/bin/sh
set -e

echo "Inicializando banco de dados..."
python -c "
from projeto_acoes.model import registro_tabelas
from projeto_acoes.database import engine
registro_tabelas.metadata.create_all(engine)
print('Tabelas criadas com sucesso!')
"

echo "Iniciando Streamlit..."
exec python -m streamlit run src/streamlit/app.py --server.port=8501 --server.address=0.0.0.0
