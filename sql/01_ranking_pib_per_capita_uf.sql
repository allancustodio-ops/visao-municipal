-- 01 · Ranking de PIB per capita dentro de cada UF (último ano disponível)
-- Pergunta: quais são os 3 municípios mais ricos por habitante em cada UF?
-- Técnicas: CTE encadeada, RANK() com PARTITION BY, COUNT() OVER
-- Executar no ponto de extremidade de análise SQL do lake_visao (T-SQL)

WITH base AS (
    SELECT f.ano, m.sigla_uf, m.municipio_uf, f.populacao, f.pib_reais
    FROM dbo.gold_fato_municipio_ano AS f
    JOIN dbo.gold_dim_municipio AS m ON m.cod_municipio = f.cod_municipio
    JOIN dbo.gold_dim_tempo     AS t ON t.ano = f.ano
    WHERE t.ultimo_ano = 1
      AND f.par_completo = 1          -- só linhas com população e PIB
),
per_capita AS (
    SELECT *, CAST(pib_reais AS FLOAT) / populacao AS pib_per_capita
    FROM base
),
ranking AS (
    SELECT *,
           RANK()   OVER (PARTITION BY sigla_uf ORDER BY pib_per_capita DESC) AS posicao_na_uf,
           COUNT(*) OVER (PARTITION BY sigla_uf)                              AS municipios_na_uf
    FROM per_capita
)
SELECT ano, sigla_uf, posicao_na_uf, municipios_na_uf, municipio_uf, populacao,
       ROUND(pib_per_capita, 2) AS pib_per_capita
FROM ranking
WHERE posicao_na_uf <= 3
ORDER BY sigla_uf, posicao_na_uf;
