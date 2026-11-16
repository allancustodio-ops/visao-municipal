-- 02 · Variação anual do PIB por UF
-- Pergunta: quanto o PIB de cada UF cresceu em relação ao ano anterior?
-- Técnicas: CTE, LAG() com PARTITION BY
-- Cuidado: a série não tem 2007 e 2010 (premissa 10). LAG pegaria 2006 como
-- "ano anterior" de 2008, então a variação só é calculada quando o ano anterior
-- é exatamente ano - 1. Também não há variação quando a base é <= 0 (premissa 15).

WITH pib_uf AS (
    SELECT m.sigla_uf, f.ano, SUM(f.pib_reais) AS pib_reais
    FROM dbo.gold_fato_municipio_ano AS f
    JOIN dbo.gold_dim_municipio AS m ON m.cod_municipio = f.cod_municipio
    GROUP BY m.sigla_uf, f.ano
),
com_anterior AS (
    SELECT *,
           LAG(ano)       OVER (PARTITION BY sigla_uf ORDER BY ano) AS ano_anterior,
           LAG(pib_reais) OVER (PARTITION BY sigla_uf ORDER BY ano) AS pib_anterior
    FROM pib_uf
)
SELECT sigla_uf, ano,
       ROUND(CAST(pib_reais AS FLOAT) / 1e9, 2) AS pib_bilhoes,
       CASE WHEN ano_anterior = ano - 1 AND pib_anterior > 0
            THEN ROUND((CAST(pib_reais AS FLOAT) / pib_anterior - 1) * 100, 2)
       END AS variacao_pct
FROM com_anterior
ORDER BY sigla_uf, ano;
