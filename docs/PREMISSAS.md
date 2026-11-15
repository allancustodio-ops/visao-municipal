# Premissas e decisões

Cada decisão com o porquê. Atualize sempre que decidir algo.

| # | Data | Decisão | Por quê | Alternativa descartada |
|---|---|---|---|---|
| 1 | | Usar tabelas 6579 (pop. estimada, var. 9324) e 5938 (PIB, var. 37) | Sugeridas no desafio; cobertura municipal anual | |
| 2 | | Ingestão paginada por ano | Evita o limite de valores por requisição da API SIDRA | Uma chamada com `p/all` |
| 3 | | Bronze com overwrite completo | Idempotência simples; volume pequeno | Append incremental (mais complexo, sem ganho aqui) |
| 4 | | Bronze guarda o cabeçalho do SIDRA (`_linha = 0`) | Bronze é cópia fiel; a Silver remove | Remover já na ingestão |
| 5 | 2026-11-14 | Ambiente: **"A minha área de trabalho"** (My workspace) para Lakehouse, modelo e app | O VPN-DEV foi liberado sem permissão para criar itens e o prazo não permite esperar; o recurso Fabric App está disponível no workspace pessoal | VPN-DEV (sem permissão); tenant próprio (tempo) |
| 6 | 2026-11-14 | App chama-se **visao-municipal**; repositório chama-se panorama-municipal | Nome do item no Fabric pensado para a diretoria; repositório nomeia o produto de dados | |
| 7 | 2026-11-14 | App acessado só pelo item no workspace, não pela URL direta | Autenticação é via portal do Fabric | |
| 7b | 2026-11-14 | Limitação aceita: workspace pessoal não tem papéis; compartilhamento é item a item | Suficiente para a demo; em produção seria um workspace compartilhado | |
| 8 | 2026-11-14 | Acesso ao app restrito a quem tem permissão no item (login obrigatório) | O produto vai receber dados internos com informações pessoais (LGPD) | Acesso anônimo aos arquivos estáticos |
| 9 | 2026-11-14 | Projeto em `C:\dev\visao-municipal`, fora do OneDrive | Sincronizar `node_modules` no OneDrive deixa a máquina lenta e trava arquivos | Pasta Documentos (sincronizada) |
| 10 | | (a decidir) Tratamento dos anos sem estimativa populacional | | |
| 11 | | (a decidir) Tratamento dos códigos `...`, `-`, `X` | | |
