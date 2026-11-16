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
| 10 | 2026-11-15 | Gold usa só os anos presentes nas duas fontes (18 anos: 2002–2006, 2008–2009, 2011–2021) | Série de população consistente (só estimativas); evita saltos artificiais na variação anual | Completar 2010 e 2022 com os Censos (mistura metodologias; fica como evolução futura) |
| 11 | 2026-11-15 | Códigos especiais do SIDRA: `-` vira 0; `..`, `...` e `X` viram nulo; significado em `status_valor` | Preserva a informação da fonte sem inventar valor | Descartar as linhas na Silver |
| 12 | 2026-11-15 | Colunas do SIDRA mapeadas pelo cabeçalho (linha 0): D1 = município, D2 = variável, D3 = ano | Não depender da ordem das dimensões, que muda entre tabelas | Posição fixa das colunas |
| 13 | 2026-11-15 | Lista de anos obtida pela API SIDRA (nível Brasil), não pela API de metadados | `servicodados.ibge.gov.br` não respondeu a partir do Fabric | Lista fixa de anos no código |
| 14 | 2026-11-15 | Portão de qualidade: com qualquer FAIL, a Gold não é gerada; WARN exige decisão documentada | Evita publicar dado inválido para a diretoria | Só registrar e seguir |
| 15 | 2026-11-15 | PIB negativo mantido como publicado pelo IBGE; regra V5 vira WARN | É dado oficial (2404507-RN, 2012: −19.046 mil reais); alterar ou excluir seria inventar dado. Medidas de variação e per capita tratam base ≤ 0 | Excluir o registro; forçar zero |
| 16 | 2026-11-15 | Modelo semântico em modo **Import** (Power BI Desktop, arquivo `.pbix`) | O Fabric não aceita "A minha área de trabalho" como destino de modelo Direct Lake e o tenant bloqueia a criação de workspaces | Direct Lake em workspace dedicado (bloqueado pelo tenant) |
| 17 | 2026-11-15 | Visões entregues como relatório do Power BI Desktop, com o modelo lendo cópias em Excel das tabelas Gold | A conta corporativa passou a exigir MFA (Microsoft Authenticator) sem acesso ao aplicativo no momento; sem login não é possível publicar o modelo nem ligar o Fabric App a ele | Esperar a recuperação do MFA (prazo de entrega) |
