"""Configuração central do pipeline Panorama Municipal.

Tudo que é premissa (tabelas, variáveis, caminhos) fica aqui, para ser
citado no PREMISSAS.md e trocado em um único lugar.
"""
from pathlib import Path

# Raiz do repositório (este arquivo está em <raiz>/pipeline/config.py)
ROOT = Path(__file__).resolve().parents[1]

# Camadas do medalhão (versão local). No Fabric, viram tabelas do Lakehouse.
DATA_DIR = ROOT / "data"
BRONZE_DIR = DATA_DIR / "bronze"
SILVER_DIR = DATA_DIR / "silver"
GOLD_DIR = DATA_DIR / "gold"
LOG_DIR = ROOT / "logs"

# APIs do IBGE
SIDRA_BASE = "https://apisidra.ibge.gov.br/values"
AGREGADOS_BASE = "https://servicodados.ibge.gov.br/api/v3/agregados"

# Fontes. Confira os códigos de variável nos metadados antes de rodar
# (o script também imprime o nome da variável retornado pela API).
FONTES = {
    "populacao": {
        "tabela": 6579,   # População residente estimada
        "variavel": 9324, # População residente estimada (pessoas)
        "nivel": "n6",    # n6 = município
    },
    "pib": {
        "tabela": 5938,   # PIB dos Municípios
        "variavel": 37,   # PIB a preços correntes (mil reais)
        "nivel": "n6",
    },
}

# Rede
TIMEOUT_S = 120
MAX_TENTATIVAS = 4
PAUSA_ENTRE_CHAMADAS_S = 1.0  # gentileza com a API pública
