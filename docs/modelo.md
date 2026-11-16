# Modelo dimensional – Panorama Municipal (Gold)

## Diagrama

```
gold_dim_tempo (ano)                 gold_dim_municipio (cod_municipio)
        1                                        1
        │                                        │
        └──────────── N ──────┬────── N ─────────┘
                              │
                gold_fato_municipio_ano
                (cod_municipio, ano)
```

## Tabelas

| Tabela | Grão | Chave | Colunas principais |
|---|---|---|---|
| `gold_fato_municipio_ano` | 1 linha por município × ano | (`cod_municipio`, `ano`) | `populacao`, `pib_reais`, `pib_mil_reais`, `par_completo`, `pib_negativo` |
| `gold_dim_municipio` | 1 linha por município | `cod_municipio` | `nome_municipio`, `municipio_uf`, `sigla_uf`, `nome_uf`, `nome_regiao` |
| `gold_dim_tempo` | 1 linha por ano | `ano` | `decada`, `ultimo_ano` |

Hierarquia geográfica para drill-down: **região → UF → município** (`nome_regiao` → `sigla_uf` → `municipio_uf`).

## Decisões

- **Chave natural do município**: o código IBGE de 7 dígitos é estável e único; não há
  ganho em criar chave substituta (surrogate key) neste escopo.
- **Escopo de anos**: só os anos presentes nas duas fontes (premissa 10): 2002–2006,
  2008–2009 e 2011–2021, 18 anos.
- **PIB per capita não é gravado na fato**: é uma razão, então precisa ser calculado na
  medida como soma do PIB ÷ soma da população no contexto do filtro. Gravar o valor por
  município e depois tirar média distorce o resultado para UF e região (um município de
  800 habitantes pesaria igual a São Paulo).
- **`par_completo`**: verdadeiro quando a linha tem população e PIB. O PIB per capita usa
  só essas linhas, para numerador e denominador cobrirem os mesmos municípios.
- **`pib_negativo`**: marca o PIB negativo publicado pelo IBGE (Guamaré-RN, 2012;
  premissa 15). As medidas de variação devolvem vazio quando o ano anterior tem PIB ≤ 0.
- **Duas unidades de PIB**: `pib_reais` para cálculos e `pib_mil_reais` como vem da fonte.
- **Portão de qualidade**: a Gold só é gerada se a última execução do 03_qualidade não
  teve FAIL.

## No modelo do Power BI

- `gold_dim_municipio` ganhou `latitude`, `longitude` e `capital`, vindas de
  `semantic-model/dados/municipios_coordenadas.xlsx` (premissa 18) por mesclagem no
  Power Query, sem tabela nova nem relacionamento extra.
- Um parâmetro numérico de porte mínimo (população) alimenta a medida
  `Atende porte mínimo`, usada na tabela de candidatos à expansão.
