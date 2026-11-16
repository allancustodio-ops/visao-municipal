# Diário de aprendizado

Regra: registrar na hora, não no fim. Uma entrada por bloco de trabalho.
Onde está `HH:MM`, preencha com o horário real.

## Modelo de entrada

**AAAA-MM-DD HH:MM – HH:MM** · tema
- Objetivo:
- Fontes consultadas (link + ordem):
- O que tentei:
- O que funcionou / o que descartei e por quê:
- Uso de IA: o que pedi, o que veio, **como validei**
- Dúvidas em aberto:

---

## Entradas

**2026-11-14 HH:MM** · Leitura do desafio e planejamento
- Objetivo: entender os entregáveis e montar o plano de 5 dias.
- Fontes: PDF do desafio.
- Uso de IA: pedi um resumo e um passo a passo; conferi cada item contra o PDF
  e os comandos do Fabric App contra learn.microsoft.com/fabric/apps
  (overview, create-app, data-apps-template).

**2026-11-14 HH:MM** · Acesso ao ambiente
- Workspace de testes fornecido pela Venha Pra Nuvem: **VPN-DEV**.

**2026-11-14 HH:MM** · Obstáculo: item do Fabric App "não aparecia"
- O que tentei: em Novo item, pesquisei "App" esperando um item chamado "App" ou "Fabric App".
- O que aconteceu: concluí que o recurso não estava habilitado. Com ajuda de IA, levantei
  causas possíveis (configuração do tenant, região da capacidade) e cheguei a montar um
  plano B para rodar o app localmente.
- Resolução: a interface em português traduz o item como **"Aplicação"**. A descrição em
  inglês ("Build modern cloud apps… fully managed database") confirmou que era o Fabric App.
  O item "Aplicação de organização" é outra coisa (app do Power BI para distribuir conteúdo).
- Aprendizado: em recurso em preview com interface traduzida, procurar também pela
  descrição e pelo ícone, não só pelo nome da documentação em inglês.
- Uso de IA: a primeira hipótese da IA (região não suportada) estava errada; só a evidência
  da tela resolveu. Lição: tratar diagnóstico da IA como hipótese a confirmar.

**2026-11-14 HH:MM** · Criação e publicação do app
- O item foi criado em **"A minha área de trabalho"** (My workspace), não no VPN-DEV.
  Só percebi pelo comando que o portal mostra (`--workspace "My workspace"`).
- Comando: `npm create @microsoft/rayfin@latest -- "visao-municipal" --template dataapp --workspace "My workspace"`
  (o portal sugere `--template blankapp`; troquei para `dataapp`, o template feito para
  consumir modelo semântico).
- Resultado: app provisionado na região **South Central US**, URL
  `https://fit-flame-ef120c4f60-southcentralus.webapp.fabricapps.net`.

**2026-11-14 HH:MM** · Obstáculo: URL do app não abre direto
- O que aconteceu: ao abrir a URL numa aba do navegador, a tela diz que o app não pode
  ser aberto fora do Fabric.
- Por quê: o app autentica pelo portal do Fabric (SSO); numa aba avulsa não há como logar.
- Resolução: abrir pelo item **visao-municipal** dentro de "A minha área de trabalho".
- Consequência para a demo: abrir sempre pelo portal, nunca pela URL.

**2026-11-14 HH:MM** · Obstáculo: sem permissão no VPN-DEV
- O que aconteceu: o workspace VPN-DEV foi disponibilizado, mas sem permissão para criar itens.
- Decisão: pelo prazo, não esperar ajuste de permissão. Todo o projeto (Lakehouse, modelo
  semântico e app) fica em "A minha área de trabalho".
- Impacto: workspace pessoal não tem papéis de workspace; para alguém acessar, cada item
  precisa ser compartilhado individualmente. Para a apresentação, a demo é feita da minha
  conta. Em um projeto real, tudo ficaria num workspace compartilhado com Git integration.

**2026-11-14 HH:MM** · Obstáculos de ambiente local
- PowerShell bloqueou o `npm` (política de execução de scripts). Resolvido com
  `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`.
- A pasta Documentos fica no OneDrive; movi o projeto para `C:\dev\visao-municipal`
  para evitar a sincronização de `node_modules`.
- Colei vários comandos de uma vez e o terminal executou todos mesmo com o primeiro
  falhando. Passei a rodar um comando por vez.

**2026-11-14 HH:MM** · Obstáculo: página em branco no `npm run dev`
- Sintoma: `localhost:5173` abria vazio.
- Diagnóstico: console do navegador (F12) mostrava erro de variáveis de ambiente
  ausentes, pedindo `npx rayfin up`.
- Resolução: rodar `npx rayfin up` antes do primeiro `npm run dev`. Ele perguntou o tipo
  de acesso (escolhi login obrigatório, premissa 8) e se deveria usar o item já existente
  (sim, para não criar um segundo item).
- Aprendizado: a ordem do quickstart do portal (dev antes de up) não funciona no primeiro uso.

**2026-11-15 ~15:00** · Lakehouse e importação do notebook
- Criei o Lakehouse **lake_visao** em "A minha área de trabalho". Junto foi criado o
  ponto de extremidade de análise SQL (mesmo nome, ícone com grade de pontos).
- O lakehouse veio com **esquemas habilitados**: as tabelas ficam em `Tables/dbo`.
  Mantive os prefixos `bronze_`, `silver_` e `gold_` para separar as camadas.
- Importei o notebook `01_bronze_ingestao.ipynb` (Importar → Bloco de notas).
- Obstáculo: a opção "Adicionar → Lakehouse existente" citada pela IA não existe mais.
  Na versão atual, o caminho é **Explorador → Itens de dados → Adicionar itens de dados**.
  Para escolher entre os dois `lake_visao`, usei o ícone: casa com ondas = Lakehouse.

**2026-11-15 15:16 – 15:18** · Obstáculo: parâmetro de anos passado como texto
- Sintoma: a ingestão falhou com `400 Bad Request` em todas as chamadas e terminou com
  "Nenhum período ingerido".
- Diagnóstico pelo log: `períodos: 2, 0, 2, 1`. Eu tinha escrito `ANOS = "2021"` em vez de
  `ANOS = ["2021"]`; o Python percorreu o texto letra por letra.
- Resolução: corrigi o parâmetro manualmente.
- Uso de IA: a IA sugeriu deixar o código tolerante a esse erro e parar de repetir
  requisições com erro 4xx. **Decidi não aplicar**: o erro era meu, não do código, e
  preferi manter o notebook simples e igual ao que eu consigo explicar.

**2026-11-15 15:28 – 15:29** · Teste da Bronze com 2021
- Também levei alguns minutos achando que o notebook estava rodando quando não estava:
  aprendi a conferir pelo indicador embaixo da célula e pelo botão Executar/Parar.
- Resultado: `bronze_populacao` com 5.571 municípios e `bronze_pib` com 5.570, sem falhas.
- Achado: o log mostrava "variável retornada: 2021". O código gerado pela IA supunha que a
  variável estava na coluna `D3N`. Consultei a linha 0 (cabeçalho do SIDRA) e confirmei:
  **D1 = Município, D2 = Variável, D3 = Ano** nas duas tabelas; PIB em **mil reais**.
- Lição: a Silver vai mapear as colunas pelo cabeçalho, não pela posição.
- Validação: conferi um registro real (Alta Floresta D'Oeste - RO, PIB 2021 = 734.467 mil reais).

**2026-11-15 15:37 – 15:46** · Obstáculo: API de metadados do IBGE fora do ar para o Fabric
- Sintoma: na carga completa (`ANOS = None`), 4 tentativas de 2 minutos cada deram timeout
  de conexão em `servicodados.ibge.gov.br`, usada para listar os anos disponíveis.
- Por que o teste anterior funcionou: com anos fixos, essa API nunca era chamada; os dados
  vêm de outro endereço (`apisidra.ibge.gov.br`), que respondia normalmente.
- Causa: não confirmada (instabilidade ou bloqueio a acessos de fora do Brasil; o Fabric
  roda nos EUA).
- Resolução: passei a obter a lista de anos pela própria API SIDRA (nível Brasil, todos os
  períodos), lendo a coluna do ano pelo cabeçalho. Reduzi a dependência a um único serviço.

**2026-11-15 16:15 – 16:17** · Carga completa da Bronze
- Duração: cerca de 2 minutos para as duas tabelas.
- População (6579): 22 anos × 5.571 municípios = 122.584 linhas (com cabeçalho).
  Anos: 2001–2006, 2008–2009, 2011–2021, 2024–2026.
- PIB (5938): 22 anos × 5.570 municípios = 122.562 linhas. Anos: 2002–2023.
- Validação: os totais batem com anos × (municípios + 1 linha de cabeçalho).
- Achados para a fase de qualidade:
  - 18 anos em comum. PIB sem população em 2007, 2010, 2022 e 2023 (anos de Contagem e
    Censo, sem estimativa). População sem PIB em 2001 e 2024–2026.
  - O ano mais recente com as duas informações é **2021**.
  - Um município a mais na população do que no PIB.
- Salvei no repositório a versão do notebook baixada do Fabric (a que realmente rodou).

**2026-11-15 HH:MM** · Obstáculo: modelo Direct Lake sem workspace de destino
- Sintoma: em "Novo modelo semântico" no lake_visao, o botão Confirmar ficava desabilitado
  e o campo de área de trabalho pedia para criar uma primeiro.
- Tentativa: criar um workspace próprio. O tenant bloqueia ("A criação da área de trabalho
  da aplicação está desativada").
- Decisão: modelo em modo Import pelo Power BI Desktop, conectado ao ponto de extremidade
  SQL do lake_visao (premissa 16). Salvo como `.pbix`; o formato PBIP (texto, melhor para
  versionar) fica como melhoria.
- Impacto: o modelo guarda uma cópia dos dados e precisa de atualização quando a Gold muda.
  Em um ambiente real, seria Direct Lake num workspace compartilhado, sem cópia.

**2026-11-15 HH:MM** · Bloqueio: autenticação multifator (MFA) na conta corporativa
- Sintoma: ao entrar com a conta da empresa, foi exigido um código do Microsoft
  Authenticator, ao qual eu não tinha acesso no momento.
- Impacto: sem login, não consigo publicar o modelo semântico, rodar `npx rayfin` nem
  acessar o Lakehouse.
- Decisão (prazo de entrega): exportei as tabelas Gold para Excel e conectei o Power BI
  Desktop a esses arquivos, mantendo o mesmo modelo (relacionamentos, hierarquia e
  medidas). As visões pedidas para o app foram montadas como relatório do Power BI.
- Validação: depois da troca de fonte, a consulta DAX de validação precisa continuar
  dando PIB per capita 2021 = 42.247,52.
- O que fica pendente: publicar o modelo e ligar o Fabric App via conector
  (`npx rayfin connector add`), assim que o MFA for regularizado. O app já está criado e
  publicado no Fabric (item visao-municipal).
- Lição: em ambiente corporativo, confirmar no primeiro dia que o MFA está configurado
  em um dispositivo disponível durante todo o prazo.
