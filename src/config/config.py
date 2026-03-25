"""
Módulo para leitura e gerenciamento de configurações de links TOML
"""

import tomllib
from pathlib import Path
from typing import Any, Dict


class LinkConfig:
    """Gerenciador de configurações de links do projeto"""

    def __init__(self, config_path: str | None = None):
        """
        Inicializa o gerenciador de configurações

        Args:
            config_path: Caminho para o arquivo link.toml.
                        Se None, usa o arquivo padrão na pasta do projeto
        """
        if config_path is None:
            # Usa o arquivo padrão
            config_file = Path(__file__).parent / 'link.toml'
        else:
            config_file = Path(config_path)

        if not config_file.exists():
            raise FileNotFoundError(
                f'Arquivo de configuração não encontrado: {config_file}'
            )

        self.config_path = config_file
        self._config = self._load_config()

    def _load_config(self) -> Dict[str, Any]:
        """
        Carrega o arquivo TOML

        Returns:
            Dicionário com as configurações
        """
        with open(self.config_path, 'rb') as f:
            return tomllib.load(f)

    def get(self, key: str, default: Any = None) -> Any:
        """
        Obtém um valor da configuração usando notação de ponto

        Args:
            key: Chave em formato de ponto (ex: 'fnet.consulta.pesquisar_documentos')
            default: Valor padrão se a chave não existir

        Returns:
            Valor da configuração ou None
        """
        keys = key.split('.')
        value = self._config

        try:
            for k in keys:
                value = value[k]
            return value
        except (KeyError, TypeError):
            return default

    def get_fnet_consulta_url(self) -> str:
        """Retorna a URL de consulta de documentos FNET"""
        return self.get('fnet.consulta.pesquisar_documentos')
    
    def get_uri_db(self) -> str:
        """Retorna a URI de conexão com o banco de dados"""
        return self.get('db.uri')

    def get_fnet_download_url(self) -> str:
        """Retorna a URL de download de documentos FNET"""
        return self.get('fnet.download.documento')

    def get_fnet_params(self) -> Dict[str, str]:
        """Retorna os parâmetros padrão para consultas FNET"""
        params = self.get('fnet.parametros_consulta', {})
        return {
            'd': '1',
            's': '0',
            'l': str(params.get('paginacao', 15)),
            'o[0][dataEntrega]': params.get('ordenacao_direcao', 'desc'),
            'idCategoriaDocumento': str(
                params.get('categoria_documento', '0')
            ),
            'idTipoDocumento': str(params.get('tipo_documento', '0')),
            'idEspecieDocumento': str(params.get('especie_documento', '0')),
            'isSession': 'true',
        }

    def get_bovespa_url(self, tipo: str = 'fundos_imobiliarios') -> str:
        """
        Retorna a URL de consulta B3 para um tipo específico

        Args:
            tipo: Tipo de consulta ('fundos_imobiliarios' ou 'acoes')

        Returns:
            URL de consulta
        """
        return self.get(f'bovespa.{tipo}.url_consulta')

    def get_all(self) -> Dict[str, Any]:
        """Retorna todas as configurações"""
        return self._config

    def get_section(self, section: str) -> Dict[str, Any]:
        """
        Obtém uma seção inteira da configuração

        Args:
            section: Nome da seção (ex: 'fnet', 'bovespa')

        Returns:
            Dicionário com os dados da seção
        """
        return self.get(section, {})

    def __repr__(self) -> str:
        return f'LinkConfig(path={self.config_path})'


def get_links_config(config_path: str | None = None) -> LinkConfig:
    """
    Factory function para criar uma instância de LinkConfig

    Args:
        config_path: Caminho para o arquivo link.toml

    Returns:
        Instância de LinkConfig
    """
    return LinkConfig(config_path)


# Função auxiliar para uso direto
def load_links(config_path: str | None = None) -> Dict[str, Any]:
    """
    Carrega as configurações de links

    Args:
        config_path: Caminho para o arquivo link.toml

    Returns:
        Dicionário com todas as configurações
    """
    config = get_links_config(config_path)
    return config.get_all()


if __name__ == '__main__':
    # Exemplo de uso
    try:
        config = LinkConfig()

        print('=' * 60)
        print('CONFIGURAÇÕES DE LINKS - PROJETO AÇÕES')
        print('=' * 60)

        print('\n📍 URL de Consulta FNET:')
        print(f'  {config.get_fnet_consulta_url()}')

        print('\n📍 URL de Download FNET:')
        print(f'  {config.get_fnet_download_url()}')

        print('\n📍 Parâmetros Padrão FNET:')
        params = config.get_fnet_params()
        for key, value in params.items():
            print(f'  {key}: {value}')

        print('\n📍 URL B3 Fundos Imobiliários:')
        print(f'  {config.get_bovespa_url("fundos_imobiliarios")}')

        print('\n📍 URL B3 Ações:')
        print(f'  {config.get_bovespa_url("acoes")}')

        print('\n📍 Seção FNET Completa:')
        fnet_section = config.get_section('fnet')
        import json

        print(json.dumps(fnet_section, indent=2, ensure_ascii=False))

    except Exception as e:
        print(f'Erro ao carregar configurações: {e}')
