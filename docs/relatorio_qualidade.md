# Relatório de qualidade – Panorama Municipal

Execução: 2026-11-15 20:45:39 UTC  
Resumo: **24 PASS · 7 WARN · 0 FAIL**

| ID | Categoria | Tabela | Regra | Status | Ocorrências |
|---|---|---|---|---|---|
| T1 | Tipos | silver_populacao | Colunas com o tipo esperado | PASS | 0 |
| T2 | Tipos | silver_pib | Colunas com o tipo esperado | PASS | 0 |
| T3 | Tipos | silver_municipio | Colunas com o tipo esperado | PASS | 0 |
| N1_pop | Nulos | silver_populacao | Chave (cod_municipio, ano) sem nulos | PASS | 0 |
| N2_pop | Nulos | silver_populacao | Valor numérico presente quando a fonte informa número | PASS | 0 |
| N3_pop | Nulos | silver_populacao | Valores 'não disponível' na fonte (município × ano) | WARN | 83 |
| N1_pib | Nulos | silver_pib | Chave (cod_municipio, ano) sem nulos | PASS | 0 |
| N2_pib | Nulos | silver_pib | Valor numérico presente quando a fonte informa número | PASS | 0 |
| N3_pib | Nulos | silver_pib | Valores 'não disponível' na fonte (município × ano) | WARN | 74 |
| N4 | Nulos | silver_municipio | Município com nome, UF e região | PASS | 0 |
| D1_pop | Duplicidade | silver_populacao | Uma linha por (cod_municipio, ano) | PASS | 0 |
| D1_pib | Duplicidade | silver_pib | Uma linha por (cod_municipio, ano) | PASS | 0 |
| D2 | Duplicidade | silver_municipio | Uma linha por cod_municipio | PASS | 0 |
| V1_pop | Domínio | silver_populacao | Código do município com 7 dígitos | PASS | 0 |
| V2_pop | Domínio | silver_populacao | Ano entre 2001 e 2026 | PASS | 0 |
| V3_pop | Domínio | silver_populacao | Nenhum valor com formato inválido na fonte | PASS | 0 |
| V1_pib | Domínio | silver_pib | Código do município com 7 dígitos | PASS | 0 |
| V2_pib | Domínio | silver_pib | Ano entre 2001 e 2026 | PASS | 0 |
| V3_pib | Domínio | silver_pib | Nenhum valor com formato inválido na fonte | PASS | 0 |
| V4 | Domínio | silver_populacao | População maior que zero | PASS | 0 |
| V5 | Domínio | silver_pib | PIB negativo publicado pelo IBGE (aceito, premissa 15) | WARN | 1 |
| V6 | Domínio | silver_pib | Unidade do PIB sempre 'Mil Reais' | PASS | 0 |
| V7 | Domínio | silver_municipio | UF válida (27 UFs pelo código IBGE) | PASS | 0 |
| V8 | Domínio | silver_municipio | UF pelo código igual à UF escrita no nome | PASS | 0 |
| I1 | Integridade | pop × pib | Município na população sem nenhum PIB | WARN | 1 |
| I2 | Integridade | pib × pop | Município no PIB sem nenhuma população | PASS | 0 |
| I3 | Integridade | fatos × silver_municipio | Todo município dos fatos existe no cadastro | PASS | 0 |
| I4 | Integridade | pib × pop | Anos de PIB sem estimativa de população | WARN | 4 |
| I5 | Integridade | pop × pib | Anos de população sem PIB | WARN | 4 |
| I6 | Integridade | pop × pib | Nos anos em comum, população e PIB presentes juntos | WARN | 10 |
| P1 | Plausibilidade | silver_populacao | População do Brasil por ano entre 170 e 230 milhões | PASS | 0 |

Anos usados na Gold (presentes nas duas fontes): [2002, 2003, 2004, 2005, 2006, 2008, 2009, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021]

## Detalhes (até 20 exemplos por regra)

**N3_pop**
- cod_municipio=1504752, de=2001, ate=2011, anos=9, nome_municipio=Mojuí dos Campos, sigla_uf=PA
- cod_municipio=2200954, de=2001, ate=2003, anos=3, nome_municipio=Aroeiras do Itaim, sigla_uf=PI
- cod_municipio=2206720, de=2001, ate=2006, anos=6, nome_municipio=Nazária, sigla_uf=PI
- cod_municipio=4212650, de=2001, ate=2011, anos=9, nome_municipio=Pescaria Brava, sigla_uf=SC
- cod_municipio=4220000, de=2001, ate=2011, anos=9, nome_municipio=Balneário Rincão, sigla_uf=SC
- cod_municipio=4314548, de=2001, ate=2011, anos=9, nome_municipio=Pinto Bandeira, sigla_uf=RS
- cod_municipio=5003900, de=2001, ate=2003, anos=3, nome_municipio=Figueirão, sigla_uf=MS
- cod_municipio=5006275, de=2001, ate=2011, anos=9, nome_municipio=Paraíso das Águas, sigla_uf=MS
- cod_municipio=5101837, de=2001, ate=2024, anos=20, nome_municipio=Boa Esperança do Norte, sigla_uf=MT
- cod_municipio=5104526, de=2001, ate=2003, anos=3, nome_municipio=Ipiranga do Norte, sigla_uf=MT
- cod_municipio=5104542, de=2001, ate=2003, anos=3, nome_municipio=Itanhangá, sigla_uf=MT

**N3_pib**
- cod_municipio=1504752, de=2002, ate=2012, anos=11, nome_municipio=Mojuí dos Campos, sigla_uf=PA
- cod_municipio=2200954, de=2002, ate=2004, anos=3, nome_municipio=Aroeiras do Itaim, sigla_uf=PI
- cod_municipio=2206720, de=2002, ate=2008, anos=7, nome_municipio=Nazária, sigla_uf=PI
- cod_municipio=4212650, de=2002, ate=2012, anos=11, nome_municipio=Pescaria Brava, sigla_uf=SC
- cod_municipio=4220000, de=2002, ate=2012, anos=11, nome_municipio=Balneário Rincão, sigla_uf=SC
- cod_municipio=4314548, de=2002, ate=2012, anos=11, nome_municipio=Pinto Bandeira, sigla_uf=RS
- cod_municipio=5003900, de=2002, ate=2004, anos=3, nome_municipio=Figueirão, sigla_uf=MS
- cod_municipio=5006275, de=2002, ate=2012, anos=11, nome_municipio=Paraíso das Águas, sigla_uf=MS
- cod_municipio=5104526, de=2002, ate=2004, anos=3, nome_municipio=Ipiranga do Norte, sigla_uf=MT
- cod_municipio=5104542, de=2002, ate=2004, anos=3, nome_municipio=Itanhangá, sigla_uf=MT

**V5**
- cod_municipio=2404507, nome_municipio=Guamaré, sigla_uf=RN, ano=2012, pib_mil_reais=-19046.000

**I1**
- cod_municipio=5101837, nome_municipio=Boa Esperança do Norte, sigla_uf=MT

**I4**
- [2007, 2010, 2022, 2023]

**I5**
- [2001, 2024, 2025, 2026]

**I6**
- cod_municipio=1504752, ano=2012, populacao=15018, pib_mil_reais=None, nome_municipio=Mojuí dos Campos, sigla_uf=PA
- cod_municipio=2200954, ano=2004, populacao=2561, pib_mil_reais=None, nome_municipio=Aroeiras do Itaim, sigla_uf=PI
- cod_municipio=2206720, ano=2008, populacao=7817, pib_mil_reais=None, nome_municipio=Nazária, sigla_uf=PI
- cod_municipio=4212650, ano=2012, populacao=9416, pib_mil_reais=None, nome_municipio=Pescaria Brava, sigla_uf=SC
- cod_municipio=4220000, ano=2012, populacao=11136, pib_mil_reais=None, nome_municipio=Balneário Rincão, sigla_uf=SC
- cod_municipio=4314548, ano=2012, populacao=2578, pib_mil_reais=None, nome_municipio=Pinto Bandeira, sigla_uf=RS
- cod_municipio=5003900, ano=2004, populacao=2908, pib_mil_reais=None, nome_municipio=Figueirão, sigla_uf=MS
- cod_municipio=5006275, ano=2012, populacao=4723, pib_mil_reais=None, nome_municipio=Paraíso das Águas, sigla_uf=MS
- cod_municipio=5104526, ano=2004, populacao=2445, pib_mil_reais=None, nome_municipio=Ipiranga do Norte, sigla_uf=MT
- cod_municipio=5104542, ano=2004, populacao=4054, pib_mil_reais=None, nome_municipio=Itanhangá, sigla_uf=MT
