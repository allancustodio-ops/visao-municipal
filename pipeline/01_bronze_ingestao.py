"""Camada Bronze: ingestão bruta das tabelas do SIDRA/IBGE.

Princípios:
- Bronze é cópia fiel da fonte: nada é tipado, renomeado ou filtrado.
  A linha de cabeçalho do SIDRA (linha 0) também é mantida; a Silver remove.
- Paginação por ano: uma chamada por período, para não estourar o limite
  de valores por requisição da API.
- Idempotente: cada execução reescreve a tabela inteira (overwrite).
  Rodar duas vezes produz o mesmo resultado, sem duplicar linhas.
- Auditável: JSON bruto salvo em disco + colunas de auditoria + log.

Uso:
    python pipeline/01_bronze_ingestao.py               # todas as fontes, todos os anos
    python pipeline/01_bronze_ingestao.py --fonte pib   # só uma fonte
    python pipeline/01_bronze_ingestao.py --anos 2020 2021

No Fabric (notebook PySpark), a lógica é a mesma; muda só a gravação:
    spark.createDataFrame(df).write.format("delta").mode("overwrite") \\
        .saveAsTable(f"bronze_{nome}")
"""
from __future__ import annotations

import argparse
import json
import logging
import time
from datetime import datetime, timezone

import pandas as pd
import requests

from config import (
    AGREGADOS_BASE, BRONZE_DIR, FONTES, LOG_DIR, MAX_TENTATIVAS,
    PAUSA_ENTRE_CHAMADAS_S, SIDRA_BASE, TIMEOUT_S,
)

log = logging.getLogger("bronze")


def configurar_log() -> None:
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    arquivo = LOG_DIR / f"bronze_{datetime.now():%Y%m%d_%H%M%S}.log"
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
        handlers=[logging.FileHandler(arquivo, encoding="utf-8"), logging.StreamHandler()],
    )
    log.info("Log em %s", arquivo)


def get_json(url: str) -> list | dict:
    """GET com retry e backoff exponencial."""
    for tentativa in range(1, MAX_TENTATIVAS + 1):
        try:
            resp = requests.get(url, timeout=TIMEOUT_S,
                                headers={"User-Agent": "panorama-municipal/0.1"})
            resp.raise_for_status()
            return resp.json()
        except (requests.RequestException, ValueError) as erro:
            espera = 2 ** tentativa
            log.warning("Tentativa %s/%s falhou (%s). Nova tentativa em %ss",
                        tentativa, MAX_TENTATIVAS, erro, espera)
            time.sleep(espera)
    raise RuntimeError(f"Falha definitiva ao acessar {url}")


def listar_periodos(tabela: int) -> list[str]:
    """Anos disponíveis na tabela, direto dos metadados do IBGE."""
    dados = get_json(f"{AGREGADOS_BASE}/{tabela}/periodos")
    return [p["id"] for p in dados]


def baixar_periodo(nome: str, cfg: dict, ano: str) -> pd.DataFrame:
    url = (f"{SIDRA_BASE}/t/{cfg['tabela']}/{cfg['nivel']}/all"
           f"/v/{cfg['variavel']}/p/{ano}")
    registros = get_json(url)

    # Guarda o JSON exatamente como veio (a "verdade" da Bronze)
    pasta_raw = BRONZE_DIR / "raw" / nome
    pasta_raw.mkdir(parents=True, exist_ok=True)
    (pasta_raw / f"{ano}.json").write_text(
        json.dumps(registros, ensure_ascii=False), encoding="utf-8")

    df = pd.DataFrame(registros).astype("string")
    df.insert(0, "_linha", range(len(df)))          # 0 = cabeçalho do SIDRA
    df["_fonte"] = nome
    df["_tabela_sidra"] = str(cfg["tabela"])
    df["_periodo_requisitado"] = ano
    df["_url_origem"] = url
    df["_ingerido_em"] = datetime.now(timezone.utc).isoformat()

    # Linhas de dados = total - 1 (cabeçalho)
    log.info("%s | %s | %s linhas de dados", nome, ano, len(df) - 1)
    if len(df) > 1:
        log.info("%s | variável retornada: %s", nome, df.loc[1].get("D3N", df.loc[1].get("D2N")))
    return df


def ingerir(nome: str, anos: list[str] | None) -> None:
    cfg = FONTES[nome]
    periodos = anos or listar_periodos(cfg["tabela"])
    log.info("%s | tabela %s | períodos: %s", nome, cfg["tabela"], ", ".join(periodos))

    partes, falhas = [], []
    for ano in periodos:
        try:
            partes.append(baixar_periodo(nome, cfg, ano))
        except Exception as erro:  # registra e segue; a falha entra no log
            log.error("%s | %s | FALHA: %s", nome, ano, erro)
            falhas.append(ano)
        time.sleep(PAUSA_ENTRE_CHAMADAS_S)

    if not partes:
        raise RuntimeError(f"Nenhum período ingerido para {nome}")

    df = pd.concat(partes, ignore_index=True)
    destino = BRONZE_DIR / nome
    destino.mkdir(parents=True, exist_ok=True)
    # Overwrite completo = idempotência. Parquet localmente;
    # troque por Delta (deltalake.write_deltalake) se quiser o mesmo formato do Fabric.
    df.to_parquet(destino / f"{nome}.parquet", index=False)

    log.info("%s | gravado em %s | %s linhas no total | falhas: %s",
             nome, destino, len(df), falhas or "nenhuma")


def main() -> None:
    parser = argparse.ArgumentParser(description="Ingestão Bronze do SIDRA")
    parser.add_argument("--fonte", choices=list(FONTES), help="Ingerir só esta fonte")
    parser.add_argument("--anos", nargs="+", help="Restringe a estes anos (ex.: 2020 2021)")
    args = parser.parse_args()

    configurar_log()
    for nome in ([args.fonte] if args.fonte else FONTES):
        ingerir(nome, args.anos)


if __name__ == "__main__":
    main()
