-- 04 · Concentração do PIB entre os municípios (último ano)
-- Pergunta: quantos municípios somam metade do PIB do Brasil?
-- Técnicas: CTE, ROW_NUMBER(), SUM() OVER com janela acumulada (ROWS UNBOUNDED PRECEDING)

WITH municipios AS (
    SELECT m.municipio_uf, f.pib_reais, f.populacao
    FROM dbo.gold_fato_municipio_ano AS f
    JOIN dbo.gold_dim_municipio AS m ON m.cod_municipio = f.cod_municipio
    JOIN dbo.gold_dim_tempo     AS t ON t.ano = f.ano
    WHERE t.ultimo_ano = 1
      AND f.par_completo = 1
),
acumulado AS (
    SELECT municipio_uf, pib_reais, populacao,
           ROW_NUMBER() OVER (ORDER BY pib_reais DESC) AS posicao,
           COUNT(*)     OVER ()                         AS total_municipios,
           CAST(SUM(pib_reais) OVER (ORDER BY pib_reais DESC ROWS UNBOUNDED PRECEDING) AS FLOAT)
               / SUM(pib_reais) OVER () * 100           AS pib_acumulado_pct,
           CAST(SUM(populacao) OVER (ORDER BY pib_reais DESC ROWS UNBOUNDED PRECEDING) AS FLOAT)
               / SUM(populacao) OVER () * 100           AS pop_acumulada_pct
    FROM municipios
)
-- Primeiro município em que o PIB acumulado passa de 50%
SELECT posicao AS municipios_para_50pct_do_pib,
       total_municipios,
       ROUND(CAST(posicao AS FLOAT) / total_municipios * 100, 2) AS pct_dos_municipios,
       ROUND(pop_acumulada_pct, 2) AS pct_da_populacao,
       municipio_uf AS ultimo_municipio_incluido
FROM acumulado
WHERE posicao = (SELECT MIN(posicao) FROM acumulado WHERE pib_acumulado_pct >= 50);
