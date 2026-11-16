-- 03 · Participação de cada UF no PIB e na população do Brasil (último ano)
-- Pergunta: quais UFs concentram mais PIB do que população?
-- Técnicas: CTE, SUM() OVER () para o total nacional, RANK()

WITH uf AS (
    SELECT m.sigla_uf, m.nome_regiao,
           SUM(f.pib_reais) AS pib_reais,
           SUM(f.populacao) AS populacao
    FROM dbo.gold_fato_municipio_ano AS f
    JOIN dbo.gold_dim_municipio AS m ON m.cod_municipio = f.cod_municipio
    JOIN dbo.gold_dim_tempo     AS t ON t.ano = f.ano
    WHERE t.ultimo_ano = 1
      AND f.par_completo = 1
    GROUP BY m.sigla_uf, m.nome_regiao
),
participacao AS (
    SELECT *,
           CAST(pib_reais AS FLOAT) / SUM(pib_reais) OVER () * 100 AS part_pib_pct,
           CAST(populacao AS FLOAT) / SUM(populacao) OVER () * 100 AS part_pop_pct
    FROM uf
)
SELECT RANK() OVER (ORDER BY part_pib_pct DESC) AS posicao,
       sigla_uf, nome_regiao,
       ROUND(part_pib_pct, 2) AS part_pib_pct,
       ROUND(part_pop_pct, 2) AS part_pop_pct,
       ROUND(part_pib_pct / part_pop_pct, 2) AS indice_pib_pop   -- > 1: produz mais do que o peso da população
FROM participacao
ORDER BY posicao;
