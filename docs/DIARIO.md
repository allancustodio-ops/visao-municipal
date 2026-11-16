# Diário de aprendizado (registro detalhado)

Registro cronológico de cada bloco de trabalho. A versão resumida, entregável, está em
`docs/diario_aprendizado.md`. Horários no fuso de Brasília; onde não há registro do
horário, a entrada traz só a data.

---

## 14/11/2026

**2026-11-14** · Leitura do desafio e planejamento
- Objetivo: entender os entregáveis e montar o plano de 5 dias.
- Fontes: PDF do desafio.
- Uso de IA: pedi um resumo e um passo a passo; conferi cada item contra o PDF e os
  comandos do Fabric App contra learn.microsoft.com/fabric/apps (overview, create-app,
  data-apps-template).

**2026-11-14** · Acesso ao ambiente e obstáculo: item do Fabric App "não aparecia"
- Workspace de testes fornecido pela Venha Pra Nuvem: **VPN-DEV**.
- O que tentei: em Novo item, pesquisei "App" esperando um item chamado "App" ou
  "Fabric App".
- O que aconteceu: concluí que o recurso não estava habilitado. Com ajuda de IA, levantei
  causas possíveis (configuração do tenant, região da capacidade) e cheguei a montar um
  plano B para rodar o app localmente.
- Resolução: a interface em português traduz o item como **"Aplicação"**. A descrição em
  inglês ("Build modern cloud apps… fully managed database") confirmou que era o Fabric
  App. O item "Aplicação de organização" é outra coisa (app do Power BI para distribuir
  conteúdo).
- Aprendizado: em recurso em preview com interface traduzida, procurar também pela
  descrição e pelo ícone, não só pelo nome da documentação em inglês.
- Uso de IA: a primeira hipótese da IA (região não suportada) estava errada; só a
  evidência da tela resolveu. Lição: tratar diagnóstico da IA como hipótese a confirmar.

**2026-11-14** · Obstáculo: sem permissão no VPN-DEV
- O workspace VPN-DEV foi disponibilizado, mas sem permissão para criar itens.
- Decisão: pelo prazo, não esperar ajuste de permissão. Todo o projeto (Lakehouse, modelo
  semântico e app) fica em "A minha área de trabalho".
- Impacto: workspace pessoal não tem papéis; para alguém acessar, cada item precisa ser
  compartilhado individualmente. Em um projeto real, tudo ficaria num workspace
  compartilhado com Git integration.

**2026-11-14 ~19:40 – 20:30** · Ambiente local, criação e publicação do app
- Instalei o Node.js (versão LTS) e criei a raiz do projeto.
- PowerShell bloqueou o `npm` (política de execução de scripts). Resolvido com
  `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`.
- A pasta Documentos fica no OneDrive; movi o projeto para `C:\dev\visao-municipal`
  para evitar a sincronização de `node_modules`.
- Colei vários comandos de uma vez e o terminal executou todos mesmo com o primeiro
  falhando. Passei a rodar um comando por vez.
- O item do app foi criado em **"A minha área de trabalho"**, não no VPN-DEV. Só percebi
  pelo comando que o portal mostra (`--workspace "My workspace"`).
- Comando (19:55): `npm create @microsoft/rayfin@latest -- "visao-municipal" --template dataapp --workspace "My workspace"`.
  O portal sugere `--template blankapp`; troquei para `dataapp`, o template feito para
  consumir modelo semântico.
- Obstáculo: `npm run dev` abria `localhost:5173` vazio. O console do navegador (F12)
  mostrava variáveis de ambiente ausentes, pedindo `npx rayfin up`. Resolução: rodar
  `npx rayfin up` antes do primeiro `npm run dev`. Ele perguntou o tipo de acesso
  (escolhi login obrigatório, premissa 8) e se deveria usar o item já existente (sim,
  para não criar um segundo item).
- Resultado: app publicado na região **South Central US**, URL
  `https://fit-flame-ef120c4f60-southcentralus.webapp.fabricapps.net`.
- Obstáculo: a URL não abre numa aba avulsa, porque o app autentica pelo portal do
  Fabric. Resolução: abrir pelo item **visao-municipal** dentro do workspace. Na demo,
  abrir sempre pelo portal.
- Aprendizado: a ordem do quickstart do portal (dev antes de up) não funciona no
  primeiro uso.

---

## 15/11/2026

**2026-11-15 ~15:00** · Lakehouse e importação do notebook
- Criei o Lakehouse **lake_visao** em "A minha área de trabalho". Junto foi criado o
  ponto de extremidade de análise SQL (mesmo nome, ícone com grade de pontos).
- O lakehouse veio com **esquemas habilitados**: as tabelas ficam em `Tables/dbo`.
  Mantive os prefixos `bronze_`, `silver_` e `gold_` para separar as camadas.
- Importei o notebook `01_bronze_ingestao.ipynb` (Importar → Bloco de notas).
- Obstáculo: a opção "Adicionar → Lakehouse existente" citada pela IA não existe mais.
  Na versão atual, o caminho é **Explorador → Itens de dados → Adicionar itens de
  dados**. Para escolher entre os dois `lake_visao`, usei o ícone: casa com ondas =
  Lakehouse.

**2026-11-15 15:16 – 15:18** · Obstáculo: parâmetro de anos passado como texto
- Sintoma: a ingestão falhou com `400 Bad Request` em todas as chamadas e terminou com
  "Nenhum período ingerido".
- Diagnóstico pelo log: `períodos: 2, 0, 2, 1`. Eu tinha escrito `ANOS = "2021"` em vez
  de `ANOS = ["2021"]`; o Python percorreu o texto letra por letra.
- Resolução: corrigi o parâmetro manualmente.
- Uso de IA: a IA sugeriu deixar o código tolerante a esse erro e parar de repetir
  requisições com erro 4xx. **Decidi não aplicar**: o erro era meu, não do código, e
  preferi manter o notebook simples e igual ao que eu consigo explicar.

**2026-11-15 15:28 – 15:29** · Teste da Bronze com 2021
- Também levei alguns minutos achando que o notebook estava rodando quando não estava:
  aprendi a conferir pelo indicador embaixo da célula e pelo botão Executar/Parar.
- Resultado: `bronze_populacao` com 5.571 municípios e `bronze_pib` com 5.570, sem falhas.
- Achado: o log mostrava "variável retornada: 2021". O código gerado pela IA supunha que
  a variável estava na coluna `D3N`. Consultei a linha 0 (cabeçalho do SIDRA) e
  confirmei: **D1 = Município, D2 = Variável, D3 = Ano** nas duas tabelas; PIB em
  **mil reais**.
- Lição: a Silver vai mapear as colunas pelo cabeçalho, não pela posição.
- Validação: conferi um registro real (Alta Floresta D'Oeste - RO, PIB 2021 = 734.467
  mil reais).

**2026-11-15 15:37 – 15:46** · Obstáculo: API de metadados do IBGE fora do ar para o Fabric
- Sintoma: na carga completa (`ANOS = None`), 4 tentativas de 2 minutos cada deram
  timeout de conexão em `servicodados.ibge.gov.br`, usada para listar os anos.
- Por que o teste anterior funcionou: com anos fixos, essa API nunca era chamada; os
  dados vêm de outro endereço (`apisidra.ibge.gov.br`), que respondia normalmente.
- Causa: não confirmada (instabilidade ou bloqueio a acessos de fora do Brasil; o Fabric
  roda nos EUA).
- Resolução: passei a obter a lista de anos pela própria API SIDRA (nível Brasil, todos
  os períodos), lendo a coluna do ano pelo cabeçalho. Reduzi a dependência a um único
  serviço.

**2026-11-15 16:15 – 16:17** · Carga completa da Bronze
- Duração: cerca de 2 minutos para as duas tabelas.
- População (6579): 22 anos × 5.571 municípios = 122.584 linhas (com cabeçalho).
  Anos: 2001–2006, 2008–2009, 2011–2021, 2024–2026.
- PIB (5938): 22 anos × 5.570 municípios = 122.562 linhas. Anos: 2002–2023.
- Validação: os totais batem com anos × (municípios + 1 linha de cabeçalho).
- Achados para a fase de qualidade: 18 anos em comum; PIB sem população em 2007, 2010,
  2022 e 2023 (anos de Contagem e Censo, sem estimativa); população sem PIB em 2001 e
  2024–2026; o ano mais recente com as duas informações é **2021**; um município a mais
  na população do que no PIB.
- Salvei no repositório a versão do notebook baixada do Fabric (a que realmente rodou).

**2026-11-15** · Silver
- Notebook `02_silver`: colunas mapeadas pelo cabeçalho, códigos especiais do SIDRA
  tratados (`status_valor`), UF e região derivadas do código IBGE, PIB em mil reais e em
  reais.
- Reconciliação: `silver_populacao` com 122.562 linhas e `silver_pib` com 122.540, ou
  seja, a Bronze menos as 22 linhas de cabeçalho de cada tabela.
- Achados: só apareceu o código "..." (não disponível): 83 casos na população e 74 no
  PIB. Regiões somam 5.571 municípios, sem região vazia. O município a mais é
  **Boa Esperança do Norte (MT)**, recente, ainda sem PIB publicado.
- Decisão (premissa 10): a Gold usa só os 18 anos presentes nas duas fontes. Completar
  2010 e 2022 com os Censos misturaria metodologias e criaria saltos falsos na variação
  anual; fica como evolução.

**2026-11-15 17:38** · Qualidade: o portão bloqueou a Gold
- Notebook `03_qualidade` com 31 regras (tipos, nulos, duplicidade, domínio,
  integridade e plausibilidade).
- Primeira execução: 24 PASS, 6 WARN e **1 FAIL**: a regra "PIB maior ou igual a zero"
  encontrou um valor negativo.
- Investigação: o valor original da fonte também é negativo: **Guamaré (RN), 2012,
  −19.046 mil reais**. É dado oficial do IBGE (economia dependente de uma atividade
  industrial; o valor adicionado ficou negativo no ano).
- Decisão (premissa 15): manter o dado como publicado e reclassificar a regra como WARN
  documentado. A regra era uma suposição minha; o portão serviu para testá-la.
- Execução final: **24 PASS, 7 WARN, 0 FAIL**. Relatório em `docs/relatorio_qualidade.md`.

**2026-11-15** · Obstáculo: Git dentro do Git
- Ao versionar o relatório de qualidade, descobri que a raiz do projeto não era um
  repositório: o primeiro commit tinha ido para o repositório que o Rayfin cria dentro
  de `app/visao-municipal`.
- Resolução: removi o `.git` interno do app, criei um único repositório na raiz e refiz
  o commit, conferindo no `git status` que `node_modules` e arquivos `.env` ficaram de fora.

**2026-11-15** · Gold
- Notebook `04_gold`: modelo estrela com `gold_fato_municipio_ano` (grão município ×
  ano), `gold_dim_municipio` e `gold_dim_tempo`. Só roda se a última validação não teve
  FAIL.
- Validação: nenhuma chave duplicada nem órfã; população e PIB somados iguais aos da
  Silver nos anos usados; 100.197 linhas com par completo e 10 sem (as mesmas da regra I6).
- PIB per capita do Brasil em 2021: **R$ 42.247,52**.
- Decisão: o PIB per capita não é gravado na fato; é razão de somas, calculada na medida.

**2026-11-15** · Consultas SQL
- Quatro consultas com CTE e window functions no ponto de extremidade SQL: ranking per
  capita por UF, variação anual, participação da UF e concentração acumulada.
- Cuidado na variação anual: sem 2007 e 2010, o `LAG` compararia 2008 com 2006; a
  variação só é calculada quando o ano anterior é exatamente o ano − 1.
- Resultado da concentração: em 2021, **87 municípios (1,56%) somam metade do PIB** e
  reúnem 36,66% da população. Último incluído: Cotia (SP).

**2026-11-15** · Obstáculo: modelo Direct Lake sem workspace de destino
- Sintoma: em "Novo modelo semântico" no lake_visao, o botão Confirmar ficava
  desabilitado e o campo de área de trabalho pedia para criar uma primeiro.
- Tentativa: criar um workspace próprio. O tenant bloqueia ("A criação da área de
  trabalho da aplicação está desativada").
- Decisão (premissa 16): modelo em modo Import pelo Power BI Desktop, conectado ao ponto
  de extremidade SQL do lake_visao. Salvo como `.pbix`; o formato PBIP (texto, melhor
  para versionar) fica como melhoria.
- Medidas validadas pela consulta DAX: PIB per capita 2021 = 42.247,52 (igual à Gold);
  variação vazia em 2002, 2008 e 2011.
- Impacto: o modelo guarda uma cópia dos dados e precisa de atualização quando a Gold
  muda. Em um ambiente real, seria Direct Lake num workspace compartilhado.

**2026-11-15** · Bloqueio: autenticação multifator (MFA) na conta corporativa
- Sintoma: ao entrar com a conta da empresa, foi exigido um código do Microsoft
  Authenticator, ao qual eu não tinha acesso no momento.
- Impacto: sem login, não consigo publicar o modelo semântico, rodar `npx rayfin` nem
  acessar o Lakehouse.
- Decisão (premissa 17): exportei as tabelas Gold para Excel
  (`semantic-model/dados/`) e conectei o Power BI Desktop a esses arquivos, mantendo o
  mesmo modelo (relacionamentos, hierarquia e medidas). As visões pedidas para o app
  foram montadas como relatório do Power BI.
- Validação: depois da troca de fonte, a consulta DAX continuou dando PIB per capita 2021
  = 42.247,52.
- O que fica pendente: publicar o modelo e ligar o Fabric App via conector
  (`npx rayfin connector add`), assim que o MFA for regularizado.
- Lição: em ambiente corporativo, confirmar no primeiro dia que o MFA está configurado
  em um dispositivo disponível durante todo o prazo.

---

## 16/11/2026

**2026-11-16** · Documentação e apresentação
- Nota LGPD (`docs/lgpd.md`), diário resumido (`docs/diario_aprendizado.md`), README com
  o estado da entrega e apresentação.

**2026-11-16** · Repensando o painel: de mostrar números a responder perguntas
- Percebi que quem respondia as perguntas de negócio eram as consultas SQL; o painel só
  exibia números do PIB.
- Decisão: levar a lógica das consultas 04 e 01 para medidas DAX (municípios que somam
  50% do PIB, participação do núcleo nos municípios e na população, posição per capita
  na UF) e um parâmetro de porte mínimo ajustável pela diretoria.
- Validação: com 2021 e sem filtros, as medidas deram 87, 1,56% e 36,66%, iguais à SQL 04.
- Obstáculos: duas medidas coladas juntas no editor; a coluna `par_completo` não era
  reconhecida; o nome da medida criada pelo parâmetro era diferente do esperado. Resolvi
  conferindo os nomes no painel de dados.
- Mapa: Azure Maps (os mapas antigos estão sendo descontinuados), com coordenadas por
  código IBGE para não errar municípios homônimos (premissa 18).
- Relatório final com duas páginas: **Executiva** (indicadores, drill-down, mapa e
  tabela) e **Insights** (concentração do PIB, recomendação, significado e ressalva).

**2026-11-16** · Publicação no GitHub
- Os commits ficavam só no computador: faltava o `git push`. Criei o repositório vazio
  `allancustodio-ops/visao-municipal` (público, sem README inicial, para não gerar
  conflito), liguei o remoto e enviei a branch `main`.
